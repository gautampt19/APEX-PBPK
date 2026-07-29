import os
import sys
import argparse
import logging
import re
import matplotlib.pyplot as plt

# Import project modules
from .config import (
    DEFAULT_PDF_PATH, 
    R_SCRIPT_PATH, 
    WORKSPACE_DIR,
    BASE_DIR,
    VERIFIED_RILUZOLE_PARAMS,
    VERIFIED_RETARDANT_PARAMS
)
from .pdf_extractor import extract_relevant_pages
from .llm_manager import extract_model_schema_and_params
from .r_builder import generate_r_script
from .r_executor import execute_r_simulation
from .validator import verify_simulation

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_extracted_parameters(params: dict, base_params: dict) -> dict:
    """
    Applies physiological filters to extracted parameters to reject unphysical values.
    Ensures flows and volumes are within bounds, and their sums do not exceed 1.0.
    """
    cleaned = {}
    for k, v in params.items():
        val = None
        if isinstance(v, (int, float)):
            val = float(v)
        elif isinstance(v, str):
            match = re.search(r'[-+]?\d*\.?\d+(e[-+]?\d+)?', v)
            if match:
                val = float(match.group(0))
                
        if val is not None:
            cleaned[k] = val
            
    # 1. Flow checks (fractions must sum to <= 1.0 and be individually reasonable)
    flow_keys = ['QL', 'QK', 'QH', 'QB', 'QF', 'QS', 'QR']
    extracted_flows = {k: cleaned[k] for k in flow_keys if k in cleaned}
    if extracted_flows:
        temp_flows = {k: base_params.get(k, 0.0) for k in flow_keys}
        temp_flows.update(extracted_flows)
        total_flow = sum(temp_flows.values())
        if total_flow > 1.0 or any(val > 1.0 or val < 0.0 for val in extracted_flows.values()):
            logging.warning(f"Rejected extracted flows due to unphysiological total sum ({total_flow:.4f}) or values: {extracted_flows}")
            for k in flow_keys:
                cleaned.pop(k, None)

    # 2. Volume checks (fractions must sum to <= 1.0 and be individually reasonable)
    vol_keys = ['VL', 'VLu', 'VK', 'VH', 'VB', 'VF', 'VP', 'VS', 'VR']
    extracted_vols = {k: cleaned[k] for k in vol_keys if k in cleaned}
    if extracted_vols:
        temp_vols = {k: base_params.get(k, 0.0) for k in vol_keys}
        temp_vols.update(extracted_vols)
        total_vol = sum(temp_vols.values())
        if total_vol > 1.0 or any(val > 1.0 or val < 0.0 for val in extracted_vols.values()):
            logging.warning(f"Rejected extracted volumes due to unphysiological total sum ({total_vol:.4f}) or values: {extracted_vols}")
            for k in vol_keys:
                cleaned.pop(k, None)
                
    return cleaned

def run_pipeline(pdf_path: str, user_overrides: dict = None, plot: bool = True):
    """
    Runs the fully generic PBPK model generator pipeline:
    1. Extracts text from paper PDF.
    2. Uses LLM to discover model architecture (schema) & parameters.
    3. Programmatically generates an R script with deSolve ODEs.
    4. Saves the R script named after the paper.
    5. Executes the R script and verifies output.
    """
    print("\n" + "="*80)
    print("      APEX-PBPK: Automated Parameter Extraction & Execution Pipeline")
    print("="*80)
    
    # Derive output R script path based on input PDF name
    pdf_stem = os.path.splitext(os.path.basename(pdf_path))[0]
    r_script_filename = f"{pdf_stem}_pbpk.R"
    target_r_path = os.path.join(WORKSPACE_DIR, r_script_filename)
    
    logging.info(f"Target R script will be saved as: {r_script_filename}")

    # 1. Extract PDF Text
    try:
        relevant_text = extract_relevant_pages(pdf_path)
    except Exception as e:
        logging.error(f"Failed to parse PDF: {e}")
        sys.exit(1)
        
    # 2. LLM Model Architecture & Parameter Extraction
    extracted_data = {}
    try:
        extracted_data = extract_model_schema_and_params(relevant_text)
    except Exception as e:
        logging.warning(f"LLM extraction failed: {e}. Falling back to standard schema.")
        
    schema = extracted_data.get("schema", {})
    extracted_params = extracted_data.get("parameters", {})
    
    # Fallback defaults if schema is empty
    if not schema.get("compartments"):
        logging.info("Using default 5-compartment model schema (liver, kidney, brain, fat, rest)")
        schema = {
            "species": "rat",
            "route": "oral",
            "compartments": ["liver", "kidney", "brain", "fat", "rest"],
            "has_ehr": False
        }
        
    base_params = VERIFIED_RILUZOLE_PARAMS.copy()
    cleaned_params = validate_extracted_parameters(extracted_params, base_params)
    
    # Merge base -> extracted -> user_overrides
    final_params = base_params.copy()
    final_params.update(cleaned_params)
    if user_overrides:
        final_params.update(user_overrides)
        
    print(f"\nDiscovered Model Schema for '{pdf_stem}':")
    print(f"  - Compartments: {', '.join(schema.get('compartments', []))}")
    print(f"  - Administration Route: {schema.get('route', 'oral')}")
    print(f"  - Enterohepatic Recirculation: {schema.get('has_ehr', False)}")
    
    # 3. Generate dynamic R Script using r_builder
    logging.info("Building custom deSolve R script dynamically...")
    r_code = generate_r_script(schema, final_params)
    
    # Save to paper-specific R script path (and default location)
    with open(target_r_path, 'w', encoding='utf-8') as f:
        f.write(r_code)
    with open(R_SCRIPT_PATH, 'w', encoding='utf-8') as f:
        f.write(r_code)
        
    print(f"\n[+] Dynamic R script generated and saved to: {target_r_path}")
    
    # 4. Execute R script
    try:
        df = execute_r_simulation(target_r_path)
    except Exception as e:
        logging.error(f"Failed to execute R simulation: {e}")
        sys.exit(1)
        
    # 5. Verification & Plotting
    success, validation_details = verify_simulation(df)
    
    print("\n" + "="*50)
    print("                 VERIFICATION RESULTS")
    print("="*50)
    if success:
        print("[PASS] Validation Status: PASSED (Physiologically Consistent)")
    else:
        print("[FAIL] Validation Status: FAILED (Numerical or unphysical issues)")
        for col, val in validation_details["negative_warnings"]:
            print(f"  - Compartment '{col}' has unphysical negative value: {val}")
            
    # Print PK metrics
    for comp, metrics in validation_details["pk_metrics"].items():
        print(f"\nPharmacokinetics for {comp} (Column: {metrics['column']}):")
        print(f"  - Cmax: {metrics['Cmax']:.4f}")
        print(f"  - Tmax: {metrics['Tmax']:.2f} hours")
        print(f"  - AUC (0-24h): {metrics['AUC']:.4f}")
    print("="*50 + "\n")
    
    if plot:
        plt.figure(figsize=(10, 6))
        cols_to_plot = [col for col in df.columns if col.startswith('A_') and col not in ['A_urine', 'A_feces', 'A_bile']]
        for col in cols_to_plot:
            plt.plot(df['time'], df[col], label=col, linewidth=2)
            
        plt.title(f'PBPK Model Simulation ({pdf_stem}): Concentration vs Time', fontsize=14)
        plt.xlabel('Time (hours)', fontsize=12)
        plt.ylabel('Amount (mg)', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plot_path = os.path.join(WORKSPACE_DIR, f"{pdf_stem}_plot.png")
        plt.savefig(plot_path)
        print(f"[+] Concentration plot saved to: {plot_path}")
        plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="APEX-PBPK: Automated Parameter Extraction & Execution for PBPK CLI")
    parser.add_argument('--pdf', type=str, default=DEFAULT_PDF_PATH, help="Path to PBPK paper PDF file")
    parser.add_argument('--dose', type=float, help="Override dose parameter")
    parser.add_argument('--bw', type=float, help="Override body weight parameter")
    parser.add_argument('--no-plot', action='store_true', help="Disable result plotting")
    
    args = parser.parse_args()
    
    overrides = {}
    if args.dose is not None:
        overrides['Dose'] = args.dose
    if args.bw is not None:
        overrides['BW'] = args.bw
        
    run_pipeline(args.pdf, overrides if overrides else None, not args.no_plot)

