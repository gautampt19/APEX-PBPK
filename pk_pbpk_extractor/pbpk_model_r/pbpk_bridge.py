import os
import json
import subprocess
from pk_pbpk_extractor.storage.db_handler import _get_supabase

def fetch_compound_params(paper_id: str, compound: str = "BPA") -> dict:
    """Queries Supabase pk_parameters and aggregates canonical values."""
    sb = _get_supabase()
    res = sb.table("pk_parameters")\
            .select("*")\
            .eq("paper_id", paper_id)\
            .execute()
    
    rows = res.data or []
    extracted = {}
    for r in rows:
        canon = (r.get("parameter_normalized") or r.get("parameter_raw") or "").strip()
        val = r.get("value")
        if canon and val is not None:
            try:
                extracted[canon] = float(val)
            except (ValueError, TypeError):
                continue
    return extracted

def classify_model_and_prepare_input(extracted: dict, compound: str = "BPA", dose: float = 50.0, route: str = "oral") -> dict:
    """
    Automated decision tree based on Final_Pharmacokinetic_ODEs.docx:
      - Model 3: If P_eff and R_gut are present
      - Model 2: If absolute physiological values are present
      - Model 4: If Qliver is % of QCC
      - Model 1: Default fractional scaling (% BW and % QCC)
    """
    # Defaults / Fallbacks for BPA (Rat/Human physiological reference)
    defaults = {
        "BW": 70.0,       # kg
        "QCC": 15.0,      # L/h/kg
        "Qliver": 25.0,   # %
        "Vliver": 2.6,    # % BW
        "V_plasma": 4.3,  # % BW
        "Kp_liver": 1.2,
        "CL_hep": 45.0,   # L/h
        "k_a": 1.5,       # 1/h
        "P_eff": None,
        "R_gut": None
    }
    
    params = {**defaults, **extracted}
    
    # ── Decision Tree ──
    if params.get("P_eff") is not None and params.get("R_gut") is not None:
        model_type = 3
        desc = "Mechanistic Absorption (Peff & Rgut)"
    elif "V_liver" in extracted and "QLiver" in extracted and extracted.get("V_liver", 0) > 0.5:
        model_type = 2
        desc = "Absolute Physiological Values"
    elif extracted.get("is_qcc_flow_only", False):
        model_type = 4
        desc = "Hybrid Fractional (Flow % QCC)"
    else:
        model_type = 1
        desc = "Fractional Scaling (%BW and %QCC)"
        
    return {
        "compound": compound,
        "model_type": model_type,
        "model_description": desc,
        "dose": dose,
        "route": route,
        "t_end": 24.0,
        "parameters": params
    }

def run_pbpk_pipeline(paper_id: str, compound: str = "BPA", dose: float = 50.0, route: str = "oral"):
    print(f"\n[Bridge] 1. Fetching parameters from Supabase for paper: {paper_id}...")
    extracted = fetch_compound_params(paper_id, compound)
    print(f"  Found {len(extracted)} extracted parameters.")
    
    payload = classify_model_and_prepare_input(extracted, compound, dose, route)
    print(f"[Bridge] 2. Selected Model: {payload['model_type']} ({payload['model_description']})")
    
    json_path = f"/tmp/{compound}_pbpk_input.json"
    with open(json_path, "w") as f:
        json.dump(payload, f, indent=2)
        
    print(f"[Bridge] 3. Invoking Rscript pbpk_solver.R...")
    r_script = os.path.join(os.path.dirname(__file__), "pbpk_solver.R")
    output_prefix = f"./output_{compound}"
    
    subprocess.run(["Rscript", r_script, json_path, output_prefix], check=True)
    
    # Print metrics
    with open(f"{output_prefix}_metrics.json") as f:
        metrics = json.load(f)
    print("\n" + "="*50)
    print(f"  PBPK Simulation Results for {compound}:")
    print(f"  Cmax: {metrics['Cmax']} mg/L at Tmax: {metrics['Tmax']} h")
    print(f"  AUC(0-24h): {metrics['AUC_0_t']} mg*h/L")
    print(f"  Plot: {output_prefix}_plot.png")
    print("="*50 + "\n")

if __name__ == "__main__":
    import sys
    paper = sys.argv[1] if len(sys.argv) > 1 else "10.1038/jes.2013.81"
    run_pbpk_pipeline(paper, compound="BPA", dose=50.0, route="oral")
