"""
pk_pbpk_extractor/tests/evaluate_pipeline.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Evaluation helper: loads ground truth from the *_extracted_from_ant.csv files
and compares them against parameters stored in the database for a given paper.

This version uses an LLM to map Antimony mathematical variables to the 
standardized extracted parameters.
"""
import os
import json
import argparse
import sqlite3
import pandas as pd
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from pk_pbpk_extractor.inference.vllm_worker import OllamaWorker
except ImportError:
    OllamaWorker = None

DB_PATH = os.path.join(PROJECT_ROOT, "pk_parameters.db")
GT_DIR  = os.path.join(PROJECT_ROOT, "test_data", "paper_parameters")


def load_ground_truth(model_name: str) -> pd.DataFrame | None:
    csv_path = os.path.join(GT_DIR, f"{model_name}_extracted_from_ant.csv")
    if not os.path.exists(csv_path):
        return None
    df = pd.read_csv(csv_path)
    
    # Only keep constants
    df = df[df["Type"] == "Constant / Initial Value"].copy()
    
    # Filter out initial state variables that are exactly 0
    if "Value_or_Formula" in df.columns:
        df["numeric_value"] = pd.to_numeric(df["Value_or_Formula"], errors="coerce")
        df = df[df["numeric_value"] != 0.0].copy()
    elif "Value" in df.columns:
        df["numeric_value"] = pd.to_numeric(df["Value"], errors="coerce")
        df = df[df["numeric_value"] != 0.0].copy()
        
    return df.reset_index(drop=True)



def fetch_extracted_parameters(paper_id: str, db_path: str = DB_PATH) -> pd.DataFrame | None:
    from pk_pbpk_extractor.storage.db_handler import fetch_parameters, DB_BACKEND
    
    if DB_BACKEND == "supabase":
        data = fetch_parameters(paper_id)
        if not data:
            return None
        import pandas as pd
        return pd.DataFrame(data)
        
    db = db_path if os.path.isabs(db_path) else db_path
    if not os.path.exists(db):
        return None
    import sqlite3
    import pandas as pd
    conn = sqlite3.connect(db)
    df = pd.read_sql_query(
        "SELECT * FROM pk_parameters WHERE paper_id LIKE ?",
        conn,
        params=("%" + paper_id + "%",),
    )
    conn.close()
    return df


def _llm_map_parameters(ground_truth_names: list[str], extracted_names: list[str]) -> dict:
    """Uses the LLM to map ground truth Antimony variables to extracted parameters."""
    if OllamaWorker is None:
        print("[Warning] OllamaWorker could not be imported. Returning empty map.")
        return {}

    worker = OllamaWorker()
    
    prompt = f"""You are a pharmacokinetic (PBPK) ontology expert. 
Your task is to map abstract Antimony mathematical variables to their standardized extracted parameter names.

Ground Truth (Antimony) Parameters:
{json.dumps(ground_truth_names, indent=2)}

Extracted Parameters from pipeline:
{json.dumps(extracted_names, indent=2)}

Rules:
1. Output a STRICT JSON dictionary. No markdown formatting, no explanation.
2. The keys must be EXACTLY the items from the Ground Truth Parameters list.
3. The values must be EXACTLY the matching string from the Extracted Parameters list.
4. If a Ground Truth parameter does not conceptually match any extracted parameter (or is missing), map it to null.
5. Examples: "VmaxLMet1c" maps to "maximum metabolic rate", "PL" maps to "partition coefficient", "VLc" maps to "V_liver", "bw" maps to "body weight", "kabsC" maps to "ka" or "absorption".

JSON Output:"""
    
    try:
        response = worker.chat(prompt)
        # Parse out any markdown blocks
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            response = response.split("```")[1].split("```")[0].strip()
            
        mapping = json.loads(response)
        return mapping
    except Exception as e:
        print(f"[ERROR] LLM Mapping failed: {e}")
        return {}


def evaluate(model_name: str, db_path: str = DB_PATH, verbose: bool = True) -> dict:
    result = {
        "model": model_name,
        "total_expected": 0,
        "matched": 0,
        "missed": [],
        "recall": 0.0,
        "has_extracted": False,
    }

    gt = load_ground_truth(model_name)
    if gt is None or len(gt) == 0:
        if verbose: print(f"  [{model_name}] No ground truth CSV found — skipping.")
        return result

    result["total_expected"] = len(gt)

    extr = fetch_extracted_parameters(model_name, db_path)
    if extr is None or len(extr) == 0:
        if verbose: print(f"  [{model_name}] No extracted parameters in DB (run pipeline first).")
        return result

    result["has_extracted"] = True
    
    out_csv = os.path.join(GT_DIR, f"{model_name}_extracted_from_db.csv")
    extr.to_csv(out_csv, index=False)
    if verbose: print(f"  [{model_name}] Saved extracted parameters to {out_csv}")

    # Unique names for the LLM
    gt_names = list(set(gt["Parameter"].astype(str).tolist()))
    extr_names = list(set(extr["parameter_name"].fillna("").astype(str).tolist() + 
                          extr["canonical_name"].fillna("").astype(str).tolist()))
    
    # Clean up empty strings
    extr_names = [n for n in extr_names if n.strip()]

    # Call LLM
    if verbose: print(f"  [{model_name}] Asking LLM to map {len(gt_names)} parameters...")
    mapping = _llm_map_parameters(gt_names, extr_names)

    matched = 0
    missed = []
    
    for _, row in gt.iterrows():
        ant_param = str(row["Parameter"])
        mapped_val = mapping.get(ant_param)
        
        if mapped_val is not None:
            matched += 1
        else:
            missed.append(ant_param)

    result["matched"] = matched
    result["missed"] = missed
    result["recall"] = matched / len(gt) if len(gt) > 0 else 0.0

    if verbose:
        print(f"  [{model_name}]")
        print(f"    Expected : {len(gt)}")
        print(f"    Matched  : {matched}")
        print(f"    Recall   : {result['recall']:.1%}")
        if missed:
            print(f"    Missed   : {missed}")

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate pipeline output for one model.")
    parser.add_argument("--model", required=True, help="Model name")
    parser.add_argument("--db", default=DB_PATH, help="Path to pk_parameters.db")
    args = parser.parse_args()
    evaluate(args.model, db_path=args.db)
