import re

with open("run_pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update argparse
argparse_target = """    parser.add_argument("--dump-prompts-only", action="store_true",
                        help="Run OCR and text cleaning, save the LLM prompt payloads to disk, and exit without running the LLMs.")
    args = parser.parse_args()"""
argparse_replacement = """    parser.add_argument("--dump-prompts-only", action="store_true",
                        help="Run OCR and text cleaning, save the LLM prompt payloads to disk, and exit without running the LLMs.")
    parser.add_argument("--run-step", choices=["all", "extract", "generate"], default="all",
                        help="Control the execution flow. 'extract' stops after parameter extraction. 'generate' starts at R code generation. 'all' runs everything.")
    parser.add_argument("--non-interactive", action="store_true",
                        help="Bypass the interactive terminal editor for parameters.")
    args = parser.parse_args()"""
code = code.replace(argparse_target, argparse_replacement)

# 2. Add skipping logic around ColPali and Extraction
# In python we can just insert early returns or skips, but `run_pipeline.py` is procedural.
# Let's find the step 1/2/3a logic and wrap it. Or even simpler, if args.run_step == "generate": we just skip down to Step 3b.
# But it's procedural in `main()`.

skip_start_marker = "    # ── ColPali Visual Retrieval Path ────────────────────────────────────"
skip_end_marker = "    # ── Step 3b: Interactive Parameter Editor ────────────────────────────"

lines = code.split('\n')
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if line.startswith(skip_start_marker):
        start_idx = i
    if line.startswith(skip_end_marker):
        end_idx = i

if start_idx != -1 and end_idx != -1:
    # We want to indent everything between start_idx and end_idx, and wrap it in `if args.run_step in ["all", "extract"]:`
    new_lines = lines[:start_idx]
    new_lines.append("    if args.run_step in ['all', 'extract']:")
    for j in range(start_idx, end_idx):
        if lines[j].strip() == "":
            new_lines.append("")
        else:
            new_lines.append("    " + lines[j])
    
    # Also add an early exit if run_step == 'extract'
    new_lines.append("        if args.run_step == 'extract':")
    new_lines.append("            print('✅ Pipeline extraction complete. Exiting (--run-step extract).')")
    new_lines.append("            sys.exit(0)")
    new_lines.append("    else:")
    new_lines.append("        # If generate step, initialize required variables that would have been set in extract step")
    new_lines.append("        extract_script = 'extract_pbpk_params.py'")
    new_lines.append("        cleaned_md = os.path.join(args.output_dir, f'{paper_name}_cleaned.md')")
    new_lines.append("        params_json = os.path.join(args.output_dir, f'{paper_name}_params.json')")
    new_lines.append("        r_script_llm = os.path.join(args.output_dir, f'{paper_name}_pbpk_model.R')")
    new_lines.append("        ocr_images_dir = os.path.join('ocr_output', paper_name)")
    new_lines.append("")
    
    new_lines.extend(lines[end_idx:])
    code = '\n'.join(new_lines)


# 3. Add non-interactive bypass to Step 3b
interactive_target = """    # ── Step 3b: Interactive Parameter Editor ────────────────────────────
    if os.path.exists(params_json):
        with open(params_json, "r", encoding="utf-8") as f:"""
        
interactive_replacement = """    # ── Step 3b: Interactive Parameter Editor ────────────────────────────
    if os.path.exists(params_json):
        if getattr(args, 'non_interactive', False):
            print(f"\\n  ✅ --non-interactive is set. Skipping parameter review.")
        else:
            with open(params_json, "r", encoding="utf-8") as f:"""

if interactive_target in code:
    code = code.replace(interactive_target, interactive_replacement)
    
    # We must also indent the rest of step 3b. 
    # Let's do it by finding the start and end of step 3b block
    # It ends at `# ── Step 3c: LLM R Code Generation ───────────────────────────────────`
    lines = code.split('\n')
    step3b_start = -1
    step3c_start = -1
    for i, line in enumerate(lines):
        if line.startswith("            with open(params_json, \"r\", encoding=\"utf-8\") as f:"): # Start of the `else:` block we just made
            step3b_start = i
        if line.startswith("    # ── Step 3c: LLM R Code Generation ───────────────────────────────────"):
            step3c_start = i
            
    if step3b_start != -1 and step3c_start != -1:
        # Indent lines from step3b_start to step3c_start-1
        # Wait, the `if getattr(args, 'non_interactive', False):` block already handles `else:`.
        # So we just indent everything inside `else:` EXCEPT `    else:` on line 437 which is for `if os.path.exists(params_json):`
        # Let's find the matching `else:` for `if os.path.exists`
        # It looks like:
        #     else:
        #         print(f"⚠️  No params JSON found at {params_json}. Skipping validation.")
        pass

# Since regex/indentation hacking is complex in string replacement, let me write a simpler approach:
# Just override the entire `_display_params()` loop if non_interactive is true.
