import re

with open("run_pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update argparse
code = code.replace(
    'parser.add_argument("--dump-prompts-only", action="store_true",\n                        help="Run OCR and text cleaning, save the LLM prompt payloads to disk, and exit without running the LLMs.")\n    args = parser.parse_args()',
    'parser.add_argument("--dump-prompts-only", action="store_true",\n                        help="Run OCR and text cleaning, save the LLM prompt payloads to disk, and exit without running the LLMs.")\n    parser.add_argument("--run-step", choices=["all", "extract", "generate"], default="all",\n                        help="Control the execution flow. \'extract\' stops after parameter extraction. \'generate\' starts at R code generation. \'all\' runs everything.")\n    parser.add_argument("--non-interactive", action="store_true",\n                        help="Bypass the interactive terminal editor for parameters.")\n    args = parser.parse_args()'
)

# 2. Extract Phase Skipping
lines = code.split('\n')
out_lines = []
in_extract_phase = False
for i, line in enumerate(lines):
    if line.startswith("    # ── ColPali Visual Retrieval Path ────────────────────────────────────"):
        out_lines.append(line)
        out_lines.append("    if args.run_step in ['all', 'extract']:")
        in_extract_phase = True
        continue
    
    if in_extract_phase and line.startswith("    # ── Step 3b: Interactive Parameter Editor ────────────────────────────"):
        in_extract_phase = False
        out_lines.append("        if args.run_step == 'extract':")
        out_lines.append("            print('✅ Pipeline extraction complete. Exiting (--run-step extract).')")
        out_lines.append("            sys.exit(0)")
        out_lines.append("    else:")
        out_lines.append("        extract_script = 'extract_pbpk_params.py'")
        out_lines.append("        cleaned_md = os.path.join(args.output_dir, f'{paper_name}_cleaned.md')")
        out_lines.append("        params_json = os.path.join(args.output_dir, f'{paper_name}_params.json')")
        out_lines.append("        r_script_llm = os.path.join(args.output_dir, f'{paper_name}_pbpk_model.R')")
        out_lines.append("        ocr_images_dir = os.path.join('ocr_output', paper_name)")
        out_lines.append("")

    if in_extract_phase:
        if line == "":
            out_lines.append("")
        else:
            out_lines.append("    " + line)
    else:
        # Check for interactive bypass
        if line == '            try:':
            # See if it's the choice = input part
            if i+1 < len(lines) and 'choice = input("▶ Choice: ").strip().lower()' in lines[i+1]:
                out_lines.append("            if getattr(args, 'non_interactive', False):")
                out_lines.append("                choice = 'enter'")
                out_lines.append("            else:")
                out_lines.append("                try:")
                continue
        if line == '                choice = input("▶ Choice: ").strip().lower()':
            out_lines.append("                    choice = input('▶ Choice: ').strip().lower()")
            continue
        if line == '            except EOFError:':
            if i > 0 and 'choice = input("▶ Choice: ").strip().lower()' in lines[i-1]:
                out_lines.append("                except EOFError:")
                continue
        if line == '                choice = ""  # Non-interactive: auto-continue':
            if i > 1 and 'choice = input("▶ Choice: ").strip().lower()' in lines[i-2]:
                out_lines.append("                    choice = ''  # Non-interactive: auto-continue")
                continue
            
        out_lines.append(line)

with open("run_pipeline.py", "w", encoding="utf-8") as f:
    f.write('\n'.join(out_lines))
