import argparse
import subprocess
import os
import sys

def run_command(cmd_list, description, **kwargs):
    print(f"\n{'='*60}")
    print(f"STEP: {description}")
    print(f"CMD:  {' '.join(cmd_list)}")
    print(f"{'='*60}")
    
    result = subprocess.run(cmd_list, **kwargs)
    if result.returncode != 0:
        print(f"\n❌ Error during {description}. Pipeline aborted.")
        sys.exit(1)
    print(f"✅ {description} completed successfully.")

def main():
    parser = argparse.ArgumentParser(
        description="End-to-End PBPK Pipeline: PDF → OCR → Clean → LLM Extract → R Model"
    )
    parser.add_argument("--pdf", required=True, help="Path to the input PDF paper.")
    parser.add_argument("--output-dir", default="pipeline_output",
                        help="Directory to store intermediate and final results.")
    parser.add_argument("--model", default="google/gemma-4-31b-it",
                        help="Model for extraction (HF ID for vllm, Ollama tag for ollama).")
    parser.add_argument("--backend", choices=["vllm", "ollama"], default="vllm",
                        help="Inference backend (default: vllm).")
    parser.add_argument("--tensor-parallel-size", type=str, default="1",
                        help="Number of GPUs to shard the model across (vLLM only).")
    
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    paper_name = os.path.splitext(os.path.basename(args.pdf))[0]
    
    # ── Step 1: PDF → OCR Markdown ───────────────────────────────────────
    ocr_script = "unlimited_ocr_pdf_parser.py"
    ocr_output_md = os.path.join("ocr_output", paper_name, "result.md")
    
    ocr_python = os.path.join(os.path.dirname(__file__) or ".", ".venv-ocr", "bin", "python")
    
    # Strip parent virtualenv environment variables to prevent module leakage
    env = os.environ.copy()
    env.pop("VIRTUAL_ENV", None)
    env.pop("PYTHONPATH", None)
    
    run_command([
        ocr_python, ocr_script,
        "--pdf", args.pdf
    ], "PDF OCR Conversion (baidu/Unlimited-OCR)", env=env)
    
    if not os.path.exists(ocr_output_md):
        print(f"❌ Expected OCR output not found at {ocr_output_md}")
        sys.exit(1)
        
    # ── Step 2: Clean Markdown (header/footer suppression + chunking) ────
    clean_script = "clean_markdown.py"
    cleaned_md = os.path.join(args.output_dir, f"{paper_name}_cleaned.md")
    
    run_command([
        sys.executable, clean_script,
        "--input", ocr_output_md,
        "--output", cleaned_md
    ], "Markdown Cleaning (header/footer suppression & chunking)")
    
    # ── Step 3: LLM Parameter Extraction ─────────────────────────────────
    extract_script = "extract_pbpk_params.py"
    params_json = os.path.join(args.output_dir, f"{paper_name}_params.json")
    
    run_command([
        sys.executable, extract_script,
        "--input", cleaned_md,
        "--output", params_json,
        "--model", args.model,
        "--backend", args.backend,
        "--tensor-parallel-size", args.tensor_parallel_size
    ], f"LLM PBPK Parameter Extraction ({args.backend.upper()})")
    
    # ── Step 4: Dynamic R Model Generation ───────────────────────────────
    generate_script = "generate_r_model.py"
    r_script = os.path.join(args.output_dir, f"{paper_name}_pbpk_model.R")
    
    run_command([
        sys.executable, generate_script,
        "--input", params_json,
        "--output", r_script
    ], "Dynamic R Model Generation")
    
    # ── Step 5: Execute R Model ──────────────────────────────────────────
    run_command([
        "Rscript", r_script
    ], "R Model Simulation (deSolve)")
    
    print(f"\n🎉 PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"   Output directory: {args.output_dir}/")
    print(f"   Cleaned markdown: {paper_name}_cleaned.md")
    print(f"   Parameters JSON:  {paper_name}_params.json")
    print(f"   R Model Script:   {paper_name}_pbpk_model.R")

if __name__ == "__main__":
    main()

