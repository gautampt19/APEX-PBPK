#!/usr/bin/env python3
"""
pk_pbpk_extractor/tests/run_all_evaluations.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Batch runner: sequentially extracts parameters from every PDF in
test_data/paper_parameters/ and then evaluates the results against
the *_extracted_from_ant.csv ground truth files.

Usage:
    # Run from the project root with the venv active
    source .venv/bin/activate
    python3 pk_pbpk_extractor/tests/run_all_evaluations.py

    # Skip extraction (if you already have results in the DB):
    python3 pk_pbpk_extractor/tests/run_all_evaluations.py --eval-only

    # Only extract, skip evaluation:
    python3 pk_pbpk_extractor/tests/run_all_evaluations.py --extract-only

    # Run a single model for quick testing:
    python3 pk_pbpk_extractor/tests/run_all_evaluations.py --model Bisphenols_Deepika_2022
"""
import os
import sys
import glob
import argparse
import time

# Ensure the project root is on the path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from pk_pbpk_extractor.tests.evaluate_pipeline import evaluate, DB_PATH, GT_DIR


# ── Helpers ────────────────────────────────────────────────────────────────────

def discover_models(gt_dir: str = GT_DIR) -> list[str]:
    """Return a sorted list of model names from the ground truth CSV files."""
    pattern = os.path.join(gt_dir, "*_extracted_from_ant.csv")
    paths = glob.glob(pattern)
    models = []
    for p in sorted(paths):
        basename = os.path.basename(p)
        model_name = basename.replace("_extracted_from_ant.csv", "")
        models.append(model_name)
    return models


def discover_pdf(model_name: str, gt_dir: str = GT_DIR) -> str | None:
    """Find the PDF that corresponds to a given model name."""
    pdf_path = os.path.join(gt_dir, f"{model_name}.pdf")
    if os.path.exists(pdf_path):
        return pdf_path
    return None


def run_extraction(model_name: str, pdf_path: str) -> bool:
    """Run the extraction pipeline for a single PDF. Returns True on success."""
    try:
        from pk_pbpk_extractor.main import setup_database, process_pdf
        from pk_pbpk_extractor.inference.vllm_worker import OllamaWorker

        print(f"\n  Extracting: {model_name}")
        print(f"  PDF: {pdf_path}")

        setup_database()
        worker = OllamaWorker()
        process_pdf(pdf_path, worker, paper_id=model_name)
        return True
    except Exception as e:
        print(f"  [ERROR] Extraction failed for {model_name}: {e}")
        return False


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Batch PBPK extraction + evaluation runner")
    parser.add_argument("--model",        type=str,  default=None,  help="Run a single model only")
    parser.add_argument("--extract-only", action="store_true",      help="Only run extraction, skip evaluation")
    parser.add_argument("--eval-only",    action="store_true",      help="Skip extraction, run evaluation only")
    parser.add_argument("--db",           type=str,  default=DB_PATH, help="Path to pk_parameters.db")
    args = parser.parse_args()

    models = discover_models()
    if args.model:
        models = [m for m in models if args.model in m]
        if not models:
            print(f"No model matching '{args.model}' found in {GT_DIR}")
            sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  APEX-PBPK Batch Evaluation — {len(models)} model(s)")
    print(f"{'='*60}")

    total_start = time.time()
    extraction_results: dict[str, bool] = {}

    # ── Phase 1: Extraction ────────────────────────────────────────────────────
    if not args.eval_only:
        print(f"\n[Phase 1 / 2]  Extraction  ({len(models)} PDFs, sequential)")
        print("-" * 60)
        for model_name in models:
            pdf = discover_pdf(model_name)
            if pdf is None:
                print(f"  [SKIP] No PDF found for {model_name}")
                extraction_results[model_name] = False
                continue
            t0 = time.time()
            ok = run_extraction(model_name, pdf)
            elapsed = time.time() - t0
            extraction_results[model_name] = ok
            status = "✓" if ok else "✗"
            print(f"  {status}  {model_name:50s}  ({elapsed:.0f}s)")
    else:
        print("\n[Phase 1 / 2]  Extraction  — SKIPPED (--eval-only)")

    # ── Phase 2: Evaluation ────────────────────────────────────────────────────
    if not args.extract_only:
        print(f"\n[Phase 2 / 2]  Evaluation  ({len(models)} models)")
        print("-" * 60)
        all_results = []
        for model_name in models:
            r = evaluate(model_name, db_path=args.db, verbose=True)
            all_results.append(r)

        # ── Summary ─────────────────────────────────────────────────────────────
        print(f"\n{'='*60}")
        print("  SUMMARY")
        print(f"  {'Model':<50s} {'Expected':>10} {'Matched':>8} {'Recall':>8}")
        print(f"  {'-'*50} {'-'*10} {'-'*8} {'-'*8}")
        total_expected = 0
        total_matched  = 0
        for r in all_results:
            status_col = "" if r["has_extracted"] else "  (no data)"
            print(f"  {r['model']:<50s} {r['total_expected']:>10} {r['matched']:>8} {r['recall']:>7.1%}{status_col}")
            total_expected += r["total_expected"]
            total_matched  += r["matched"]
        overall_recall = total_matched / total_expected if total_expected > 0 else 0.0
        print(f"  {'-'*50} {'-'*10} {'-'*8} {'-'*8}")
        print(f"  {'TOTAL':<50s} {total_expected:>10} {total_matched:>8} {overall_recall:>7.1%}")
        print(f"{'='*60}")
    else:
        print("\n[Phase 2 / 2]  Evaluation  — SKIPPED (--extract-only)")

    elapsed_total = time.time() - total_start
    print(f"\nDone in {elapsed_total:.0f}s.")


if __name__ == "__main__":
    main()
