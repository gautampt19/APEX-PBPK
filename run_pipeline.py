import argparse
import json
import re
import subprocess
import os
import sys
import time

step_timings = []

def format_time(elapsed_seconds):
    if elapsed_seconds >= 60:
        mins = int(elapsed_seconds // 60)
        secs = elapsed_seconds % 60
        return f"{mins}m {secs:.1f}s"
    return f"{elapsed_seconds:.1f}s"


def run_command(cmd_list, description, **kwargs):
    print(f"\n{'='*60}")
    print(f"STEP: {description}")
    print(f"CMD:  {' '.join(cmd_list)}")
    print(f"{'='*60}")
    
    start_time = time.time()
    result = subprocess.run(cmd_list, **kwargs)
    elapsed = time.time() - start_time
    
    if result.returncode != 0:
        print(f"\n❌ Error during {description}. Pipeline aborted.")
        sys.exit(1)
        
    time_str = format_time(elapsed)
    step_timings.append((description, time_str))
    print(f"✅ {description} completed successfully in {time_str}.")


def validate_r_syntax(r_script_path):
    """Check R script syntax. Returns (is_valid, stderr_message)."""
    # Use --vanilla to avoid .Rprofile interference; quote path inside R string
    escaped = r_script_path.replace("'", "\\'")
    result = subprocess.run(
        ["Rscript", "--vanilla", "-e", f"parse(file='{escaped}')"],
        capture_output=True, text=True,
    )
    return result.returncode == 0, result.stderr.strip()


def auto_repair_r(r_script_path):
    """
    Apply a sequence of deterministic regex repairs for common LLM
    hallucinations in generated R code. Returns True if any repairs were made.
    """
    with open(r_script_path, "r", encoding="utf-8") as f:
        original = f.read()

    code = original

    # ── 1. Double closing braces: }}) → })  (with() block hallucination) ──
    code = re.sub(r'\}\}\)', '})', code)

    # ── 2. Double closing braces on their own line: }}\n} → }\n} ──
    code = re.sub(r'\}\}\s*\n(\s*\})', r'}\n\1', code)

    # ── 3. Stray << operator (common OCR artifact) ──
    code = code.replace("<<-", "<-")

    # ── 4. Unicode minus sign → ASCII hyphen ──
    code = code.replace("\u2212", "-")

    # ── 5. Backtick-quoted names left from markdown: `name` → name ──
    # Only strip backticks around valid R identifiers (letters/digits/._)
    code = re.sub(r'`([A-Za-z][A-Za-z0-9_.]*)`', r'\1', code)

    if code != original:
        with open(r_script_path, "w", encoding="utf-8") as f:
            f.write(code)
        return True
    return False


def main():
    parser = argparse.ArgumentParser(
        description=(
            "End-to-End PBPK Pipeline: "
            "PDF → OCR → Clean → LLM Extract + Generate R → Simulate"
        )
    )
    parser.add_argument("--pdf", required=True, help="Path to the input PDF paper.")
    parser.add_argument("--output-dir", default="pipeline_output",
                        help="Directory to store intermediate and final results.")
    parser.add_argument("--model-extract", default="google/gemma-4-31b-it",
                        help="Model for extraction (HF ID for vllm, Ollama tag for ollama).")
    parser.add_argument("--model-generate", default="google/gemma-4-31b-it",
                        help="Model for R code generation (HF ID for vllm, Ollama tag for ollama).")
    parser.add_argument("--backend", choices=["vllm", "ollama"], default="vllm",
                        help="Inference backend (default: vllm).")
    parser.add_argument("--tensor-parallel-size", type=str, default="1",
                        help="Number of GPUs to shard the model across (vLLM only).")
    parser.add_argument("--use-colpali", action="store_true", default=False,
                        help="Use ColPali visual retrieval to find relevant pages, then pass page images directly to Vision-LLM (bypasses OCR).")
    parser.add_argument("--colpali-top-k", type=int, default=5,
                        help="Number of pages to retrieve via ColPali (default: 5).")
    parser.add_argument("--force-ocr", action="store_true",
                        help="Force Baidu/MinerU to OCR every page (slow but gets tables/formulas). Default is quick PyMuPDF text extraction.")
    parser.add_argument("--dump-prompts-only", action="store_true",
                        help="Run OCR and text cleaning, save the LLM prompt payloads to disk, and exit without running the LLMs.")
    parser.add_argument("--run-step", choices=["all", "extract", "generate"], default="all",
                        help="Control the execution flow. 'extract' stops after parameter extraction. 'generate' starts at R code generation. 'all' runs everything.")
    parser.add_argument("--non-interactive", action="store_true",
                        help="Bypass the interactive terminal editor for parameters.")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    paper_name = os.path.splitext(os.path.basename(args.pdf))[0]

    # ── ColPali Visual Retrieval Path ────────────────────────────────────
    if args.run_step in ['all', 'extract']:
        colpali_image_paths = []
        if args.use_colpali:
            from colpali_retriever import retrieve_relevant_pages
            import time as _time
            _cp_start = _time.time()
            print(f"\n{'='*60}")
            print(f"STEP: ColPali Visual Page Retrieval")
            print(f"{'='*60}")

            colpali_output_dir = os.path.join(args.output_dir, "colpali_pages")
            _page_images, _page_nums, colpali_image_paths = retrieve_relevant_pages(
                pdf_path=args.pdf,
                top_k=args.colpali_top_k,
                output_dir=colpali_output_dir,
            )

            _cp_elapsed = _time.time() - _cp_start
            _cp_time_str = format_time(_cp_elapsed)
            step_timings.append(("ColPali Visual Retrieval", _cp_time_str))
            print(f"✅ ColPali retrieved {len(_page_nums)} pages: {_page_nums} in {_cp_time_str}")

        # ── Step 1: PDF → OCR Markdown ───────────────────────────────────────
        ocr_script    = "unlimited_ocr_pdf_parser.py"
        ocr_output_md = os.path.join("ocr_output", paper_name, "result.md")
        ocr_python    = os.path.join(os.path.dirname(__file__) or ".", ".venv-ocr", "bin", "python")

        env = os.environ.copy()
        env.pop("VIRTUAL_ENV", None)
        env.pop("PYTHONPATH",  None)

        ocr_cmd = [ocr_python, ocr_script, "--pdf", args.pdf]
        if args.force_ocr:
            ocr_cmd.append("--force-mineru")

        if args.use_colpali:
            # Skip full OCR — create minimal placeholder markdown from PyMuPDF text
            import fitz
            _doc = fitz.open(args.pdf)
            _text_pages = [_doc[i].get_text() for i in range(len(_doc))]
            _doc.close()
            os.makedirs(os.path.dirname(ocr_output_md) or ".", exist_ok=True)
            with open(ocr_output_md, "w", encoding="utf-8") as _f:
                _f.write("\n\n".join(_text_pages))
            _cp_msg = "Skipped full OCR (ColPali mode — using direct PyMuPDF text as fallback context)"
            step_timings.append((_cp_msg, "0.0s"))
            print(f"✅ {_cp_msg}")
        else:
            run_command(ocr_cmd, "PDF OCR Conversion (baidu/Unlimited-OCR)", env=env)

        if not os.path.exists(ocr_output_md):
            print(f"❌ Expected OCR output not found at {ocr_output_md}")
            sys.exit(1)

        # ── Step 2: Clean Markdown ───────────────────────────────────────────
        clean_script = "clean_markdown.py"
        cleaned_md   = os.path.join(args.output_dir, f"{paper_name}_cleaned.md")

        run_command([sys.executable, clean_script, "--input", ocr_output_md, "--output", cleaned_md],
                    "Markdown Cleaning (header/footer suppression & chunking)")

        # ── Step 3a: LLM Parameter Extraction ────────────────────────────────
        extract_script = "extract_pbpk_params.py"
        params_json    = os.path.join(args.output_dir, f"{paper_name}_params.json")
        r_script_llm   = os.path.join(args.output_dir, f"{paper_name}_pbpk_model.R")
        ocr_images_dir = os.path.join("ocr_output", paper_name)

        extract_cmd = [sys.executable, extract_script,
             "--input",               cleaned_md,
             "--output",              params_json,
             "--output-r",            r_script_llm,
             "--model-extract",       args.model_extract,
             "--model-generate",      args.model_generate,
             "--backend",             args.backend,
             "--tensor-parallel-size", args.tensor_parallel_size,
             "--image-dir",           ocr_images_dir,
             "--step",                "extract"]

        if args.dump_prompts_only:
            prompts_dir = os.path.join(args.output_dir, "llm_inputs")
            extract_cmd.extend(["--dump-prompts-dir", prompts_dir])
            run_command(extract_cmd, f"Dumping LLM Extraction Prompt")
            print(f"✅ Prompts dumped to {prompts_dir}. Exiting as requested by --dump-prompts-only.")
            sys.exit(0)

        if colpali_image_paths:
            extract_cmd.extend(["--page-images", ",".join(colpali_image_paths)])

        run_command(extract_cmd, f"LLM Parameter Extraction ({args.backend.upper()})")

        if args.run_step == 'extract':
            print('✅ Pipeline extraction complete. Exiting (--run-step extract).')
            sys.exit(0)
    else:
        extract_script = 'extract_pbpk_params.py'
        cleaned_md = os.path.join(args.output_dir, f'{paper_name}_cleaned.md')
        params_json = os.path.join(args.output_dir, f'{paper_name}_params.json')
        r_script_llm = os.path.join(args.output_dir, f'{paper_name}_pbpk_model.R')
        ocr_images_dir = os.path.join('ocr_output', paper_name)

    # ── Step 3b: Interactive Parameter Editor ────────────────────────────
    if os.path.exists(params_json):
        with open(params_json, "r", encoding="utf-8") as f:
            params = json.load(f)

        def _save_params():
            with open(params_json, "w", encoding="utf-8") as f:
                json.dump(params, f, indent=4)

        def _display_params():
            print(f"\n{'='*60}")
            print(f"  EXTRACTED PARAMETERS — REVIEW & EDIT")
            print(f"{'='*60}")

            bf = params.get("blood_flow_fraction", {})
            vf = params.get("volume_fraction", {})
            compartments = sorted(set(list(bf.keys()) + list(vf.keys())))
            print(f"\n📦 Compartments detected ({len(compartments)}):")
            print(f"   {', '.join(compartments)}")

            if bf:
                print(f"\n🩸 Blood Flow Fractions (fraction of cardiac output):")
                for organ, val in sorted(bf.items()):
                    print(f"   {organ:<20s} {val}")

            if vf:
                print(f"\n📐 Volume Fractions (fraction of body weight):")
                for organ, val in sorted(vf.items()):
                    print(f"   {organ:<20s} {val}")

            biochem = params.get("biochemical_parameters", {})
            if biochem:
                print(f"\n⚗️  Biochemical Parameters ({len(biochem)}):")
                kps = {k: v for k, v in biochem.items() if "plasma" in k.lower() or "partition" in k.lower() or k.startswith("Kp")}
                other = {k: v for k, v in biochem.items() if k not in kps}
                if kps:
                    print(f"   ── Partition Coefficients ──")
                    for k, v in sorted(kps.items()):
                        print(f"   {k:<30s} {v}")
                if other:
                    print(f"   ── Other ──")
                    for k, v in sorted(other.items()):
                        print(f"   {k:<30s} {v}")

            equations = params.get("equations", {})
            if equations:
                print(f"\n📝 Equations ({len(equations)}):")
                for name, eq in equations.items():
                    eq_display = eq if len(eq) < 80 else eq[:77] + "..."
                    print(f"   {name:<30s} {eq_display}")

        def _try_numeric(val_str):
            """Convert string to float/int if possible, else return string."""
            try:
                f = float(val_str)
                return int(f) if f == int(f) else f
            except ValueError:
                return val_str

        def _pick_section():
            sections = [
                ("blood_flow_fraction",    "Blood Flow Fractions"),
                ("volume_fraction",        "Volume Fractions"),
                ("biochemical_parameters", "Biochemical Parameters"),
                ("equations",              "Equations"),
            ]
            print("\n   Which section?")
            for i, (_, label) in enumerate(sections, 1):
                print(f"   {i}) {label}")
            try:
                choice = input("   Section number: ").strip()
                idx = int(choice) - 1
                if 0 <= idx < len(sections):
                    return sections[idx][0]
            except (ValueError, EOFError):
                pass
            print("   ⚠️  Invalid section.")
            return None

        def _edit_param():
            section_key = _pick_section()
            if not section_key:
                return
            section = params.get(section_key, {})
            if not section:
                print(f"   Section is empty. Use 'add' to add parameters first.")
                return
            print(f"\n   Current keys: {', '.join(section.keys())}")
            try:
                key = input("   Parameter name to edit: ").strip()
            except EOFError:
                return
            if key not in section:
                print(f"   ⚠️  '{key}' not found in this section.")
                return
            print(f"   Current value: {section[key]}")
            try:
                new_val = input(f"   New value: ").strip()
            except EOFError:
                return
            if not new_val:
                print("   ⚠️  Empty input — value unchanged.")
                return
            section[key] = _try_numeric(new_val)
            params[section_key] = section
            _save_params()
            print(f"   ✅ {key} → {section[key]}")

        def _add_param():
            section_key = _pick_section()
            if not section_key:
                return
            if section_key not in params:
                params[section_key] = {}
            try:
                key = input("   New parameter name: ").strip()
            except EOFError:
                return
            if not key:
                print("   ⚠️  Empty name — cancelled.")
                return
            if key in params[section_key]:
                print(f"   ⚠️  '{key}' already exists (value: {params[section_key][key]}). Use 'edit' to change it.")
                return
            try:
                val = input(f"   Value for '{key}': ").strip()
            except EOFError:
                return
            if not val:
                print("   ⚠️  Empty value — cancelled.")
                return
            params[section_key][key] = _try_numeric(val)
            _save_params()
            print(f"   ✅ Added {key} = {params[section_key][key]}")

        def _delete_param():
            section_key = _pick_section()
            if not section_key:
                return
            section = params.get(section_key, {})
            if not section:
                print(f"   Section is empty.")
                return
            print(f"\n   Current keys: {', '.join(section.keys())}")
            try:
                key = input("   Parameter name to delete: ").strip()
            except EOFError:
                return
            if key not in section:
                print(f"   ⚠️  '{key}' not found.")
                return
            del section[key]
            params[section_key] = section
            _save_params()
            print(f"   🗑️  Deleted '{key}'")

        def _add_compartment():
            try:
                name = input("   New compartment name (e.g., Spleen): ").strip()
            except EOFError:
                return
            if not name:
                print("   ⚠️  Empty name — cancelled.")
                return
            # Add to blood_flow_fraction
            try:
                bf_val = input(f"   Blood flow fraction for {name} (or press Enter to skip): ").strip()
            except EOFError:
                bf_val = ""
            if bf_val:
                if "blood_flow_fraction" not in params:
                    params["blood_flow_fraction"] = {}
                params["blood_flow_fraction"][name] = _try_numeric(bf_val)
            # Add to volume_fraction
            try:
                vf_val = input(f"   Volume fraction for {name} (or press Enter to skip): ").strip()
            except EOFError:
                vf_val = ""
            if vf_val:
                if "volume_fraction" not in params:
                    params["volume_fraction"] = {}
                params["volume_fraction"][name] = _try_numeric(vf_val)
            # Add partition coefficient
            try:
                kp_val = input(f"   {name}:plasma partition coefficient (or press Enter to skip): ").strip()
            except EOFError:
                kp_val = ""
            if kp_val:
                if "biochemical_parameters" not in params:
                    params["biochemical_parameters"] = {}
                params["biochemical_parameters"][f"{name}:plasma"] = _try_numeric(kp_val)
            _save_params()
            print(f"   ✅ Compartment '{name}' added.")

        # ── Interactive loop ──
        _display_params()

        MENU = """
┌────────────────────────────────────────┐
│  [v] View parameters                   │
│  [e] Edit a parameter value            │
│  [a] Add a parameter                   │
│  [d] Delete a parameter                │
│  [c] Add a new compartment             │
│  [ENTER] ✅ Continue to R generation   │
│  [q] ❌ Abort pipeline                 │
└────────────────────────────────────────┘"""

        while True:
            print(MENU)
            if getattr(args, 'non_interactive', False):
                choice = 'enter'
            else:
                try:
                    choice = input('▶ Choice: ').strip().lower()
                except EOFError:
                    choice = ''  # Non-interactive: auto-continue

            if choice == "" or choice == "enter":
                print("\n  ✅ Parameters approved. Continuing to R model generation...")
                break
            elif choice == "q":
                print("❌ Pipeline aborted by user.")
                sys.exit(0)
            elif choice == "v":
                _display_params()
            elif choice == "e":
                _edit_param()
            elif choice == "a":
                _add_param()
            elif choice == "d":
                _delete_param()
            elif choice == "c":
                _add_compartment()
            else:
                print(f"   ⚠️  Unknown option '{choice}'")

    else:
        print(f"⚠️  No params JSON found at {params_json}. Skipping validation.")

    # ── Step 3c: LLM R Code Generation ───────────────────────────────────
    generate_cmd = [sys.executable, extract_script,
         "--input",               cleaned_md,
         "--output",              params_json,
         "--output-r",            r_script_llm,
         "--model-extract",       args.model_extract,
         "--model-generate",      args.model_generate,
         "--backend",             args.backend,
         "--tensor-parallel-size", args.tensor_parallel_size,
         "--image-dir",           ocr_images_dir,
         "--step",                "generate",
         "--input-json",          params_json]

    run_command(generate_cmd, f"LLM R Code Generation ({args.backend.upper()})")

    # ── Step 4: Validate → Auto-Repair → LLM Retry × 2 → Fallback ─────
    r_script_to_run = r_script_llm
    use_fallback    = False
    MAX_LLM_RETRIES = 2

    if not os.path.exists(r_script_llm):
        print("⚠️  LLM did not produce an R script. Will attempt LLM retry …")
        valid = False
        err   = "LLM did not produce an R script file."
    else:
        valid, err = validate_r_syntax(r_script_llm)
        if valid:
            print("✅ LLM-generated R script passed syntax validation.")
        else:
            print(f"⚠️  LLM R script has syntax errors:\n{err}")
            print("   Attempting automatic regex repair …")
            repaired = auto_repair_r(r_script_llm)
            if repaired:
                valid, err = validate_r_syntax(r_script_llm)
                if valid:
                    print("✅ Auto-repair succeeded — LLM R script is now valid.")
                else:
                    print(f"⚠️  Auto-repair did not fix all errors:\n{err}")

    # ── LLM Self-Correction Retry Loop ────────────────────────────────────
    if not valid:
        broken_script = r_script_llm  # track which file is broken for next retry
        for retry_num in range(1, MAX_LLM_RETRIES + 1):
            print(f"\n🔄  LLM Retry {retry_num}/{MAX_LLM_RETRIES}: sending broken code + error back to LLM …")
            retry_r_script = os.path.join(args.output_dir, f"{paper_name}_pbpk_model_retry{retry_num}.R")
            retry_cmd = [sys.executable, extract_script,
                "--input",               cleaned_md,
                "--output",              params_json,
                "--output-r",            retry_r_script,
                "--model-extract",       args.model_extract,
                "--model-generate",      args.model_generate,
                "--backend",             args.backend,
                "--tensor-parallel-size", args.tensor_parallel_size,
                "--image-dir",           ocr_images_dir,
                "--step",                "generate",
                "--input-json",          params_json,
                "--previous-r",          broken_script if os.path.exists(broken_script) else r_script_llm,
                "--error-msg",           err,
            ]
            run_command(retry_cmd, f"LLM Self-Correction Attempt {retry_num}/{MAX_LLM_RETRIES}")
            if os.path.exists(retry_r_script):
                valid, err = validate_r_syntax(retry_r_script)
                if valid:
                    print(f"✅ LLM retry {retry_num} succeeded — R script is now valid!")
                    r_script_llm    = retry_r_script
                    r_script_to_run = retry_r_script
                    break
                else:
                    print(f"⚠️  LLM retry {retry_num} still has errors:\n{err}")
                    broken_script = retry_r_script  # feed this into the next retry
            else:
                print(f"⚠️  LLM retry {retry_num} did not produce an R script.")
        else:
            print(f"\n⚠️  All {MAX_LLM_RETRIES} LLM retries exhausted. Falling back to template generator …")
            use_fallback = True

    if use_fallback:
        r_script_fallback = os.path.join(args.output_dir, f"{paper_name}_pbpk_model_fallback.R")
        run_command(
            [sys.executable, "generate_r_model.py",
             "--input",  params_json,
             "--output", r_script_fallback],
            "Fallback Template R Model Generation"
        )
        r_script_to_run = r_script_fallback

    # ── Step 4b: LLM Semantic Review
    print("\n⚙️  Running LLM semantic review of the generated R code …")
    try:
        from extract_pbpk_params import verify_r_code
        r_code_for_review = open(r_script_to_run, encoding="utf-8").read() if os.path.exists(r_script_to_run) else ""
        params_str        = open(params_json,     encoding="utf-8").read() if os.path.exists(params_json)     else "{}"
        md_str            = open(cleaned_md,      encoding="utf-8").read() if os.path.exists(cleaned_md)      else ""
        review_result = verify_r_code(r_code_for_review, params_str, md_str, model=args.model_generate, backend=args.backend, tensor_parallel_size=args.tensor_parallel_size)
        review_json_path = os.path.join(args.output_dir, f"{paper_name}_review.json")
        with open(review_json_path, "w", encoding="utf-8") as rf:
            json.dump(review_result, rf, indent=2)
        print(f"✅ LLM review saved to {review_json_path}: {review_result.get('overall_status','?')} - {review_result.get('summary','')}")
    except Exception as rev_err:
        print(f"⚠️  Semantic review failed (non-critical): {rev_err}")

    # ── Step 5: Execute R Model ──────────────────────────────────────────
    run_command(["Rscript", "--vanilla", r_script_to_run],
                "R Model Simulation (deSolve)")

    print(f"\n🎉 PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"   Output directory : {args.output_dir}/")
    print(f"   Cleaned markdown : {paper_name}_cleaned.md")
    print(f"   Parameters JSON  : {paper_name}_params.json")
    print(f"   R Model Script   : {os.path.basename(r_script_to_run)}")
    if use_fallback:
        print("   ⚠️  Used FALLBACK template generator (LLM R code had unfixable syntax errors)")
    else:
        print("   ✅ Used LLM-generated faithful model")
        
    print(f"\n⏱️  EXECUTION TIME SUMMARY:")
    for step_desc, step_time in step_timings:
        print(f"   - {step_desc:<60} {step_time}")



if __name__ == "__main__":
    main()
