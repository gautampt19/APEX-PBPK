import re
import numpy as np
import pandas as pd
import logging
from typing import Dict, Any, Tuple

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_pk_metrics(time: np.ndarray, conc: np.ndarray) -> Dict[str, float]:
    """
    Performs basic Non-Compartmental Analysis (NCA) to calculate Cmax, Tmax, and AUC.
    """
    if len(time) == 0 or len(conc) == 0:
        return {"Cmax": 0.0, "Tmax": 0.0, "AUC": 0.0}
        
    cmax = float(np.max(conc))
    tmax = float(time[np.argmax(conc)])
    
    # Trapezoidal rule for AUC
    auc = 0.0
    for i in range(len(time) - 1):
        dt = time[i+1] - time[i]
        mean_c = (conc[i+1] + conc[i]) / 2.0
        auc += mean_c * dt
        
    return {
        "Cmax": cmax,
        "Tmax": tmax,
        "AUC": auc
    }

def verify_simulation(df: pd.DataFrame) -> Tuple[bool, Dict[str, Any]]:
    """
    Performs checks on the output CSV data:
    1. Check for negative concentrations.
    2. Auto-detect Plasma and Brain columns.
    3. Calculate PK metrics for detected columns.
    """
    logging.info("Starting simulation verification...")
    
    results = {
        "non_negative": True,
        "negative_warnings": [],
        "pk_metrics": {}
    }
    
    # 1. Non-negativity check
    for col in df.columns:
        if col == 'time':
            continue
        min_val = df[col].min()
        if min_val < -1e-5:  # tolerance for small numerical errors
            results["non_negative"] = False
            results["negative_warnings"].append((col, min_val))
            logging.warning(f"Negative value detected in compartment '{col}': {min_val}")
            
    # 2. Extract time
    time = df['time'].values
    
    # 3. Identify plasma and brain columns using regex
    plasma_col = None
    brain_col = None
    for col in df.columns:
        if re.search(r'(?i)plasma|blood|C_p|Cplasma', col):
            plasma_col = col
        if re.search(r'(?i)brain|C_b|Cbrain', col):
            brain_col = col
            
    # Calculate PK metrics for identified columns
    if plasma_col:
        results["pk_metrics"]["Plasma"] = {
            "column": plasma_col,
            **calculate_pk_metrics(time, df[plasma_col].values)
        }
        logging.info(f"Plasma PK metrics calculated for column '{plasma_col}'")
        
    if brain_col:
        results["pk_metrics"]["Brain"] = {
            "column": brain_col,
            **calculate_pk_metrics(time, df[brain_col].values)
        }
        logging.info(f"Brain PK metrics calculated for column '{brain_col}'")
        
    verification_passed = results["non_negative"]
    return verification_passed, results
