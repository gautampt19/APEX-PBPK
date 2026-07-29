import re
import logging
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Standard parameter key map for organs
ORGAN_PARAM_MAP = {
    'liver': {'vol': 'VL', 'flow': 'QL', 'part': 'PL', 'code': 'liver', 'short': 'L'},
    'kidney': {'vol': 'VK', 'flow': 'QK', 'part': 'PK', 'code': 'kidney', 'short': 'K'},
    'brain': {'vol': 'VB', 'flow': 'QB', 'part': 'PB', 'code': 'brain', 'short': 'B'},
    'heart': {'vol': 'VH', 'flow': 'QH', 'part': 'PH', 'code': 'heart', 'short': 'H'},
    'fat': {'vol': 'VF', 'flow': 'QF', 'part': 'PF', 'code': 'fat', 'short': 'F'},
    'lung': {'vol': 'VLu', 'flow': 'QLu', 'part': 'PLu', 'code': 'lung', 'short': 'Lu'},
    'slow': {'vol': 'VS', 'flow': 'QS', 'part': 'PS', 'code': 'slow', 'short': 'S'},
    'rapid': {'vol': 'VR', 'flow': 'QR', 'part': 'PR', 'code': 'rapid', 'short': 'R'},
    'rest': {'vol': 'VR', 'flow': 'QR', 'part': 'PR', 'code': 'rest', 'short': 'R'},
}

def generate_r_script(schema: Dict[str, Any], params: Dict[str, float]) -> str:
    """
    Generates a full R script with deSolve ODEs programmatically based on model schema and parameters.
    """
    raw_compartments = schema.get('compartments', ['liver', 'kidney', 'brain', 'fat', 'rest'])
    compartments = []
    seen = set()
    for c in raw_compartments:
        c_clean = re.sub(r'[^a-zA-Z0-9_]', '', re.sub(r'[\s\-]+', '_', str(c).lower().strip()))
        if c_clean and c_clean not in seen and c_clean not in ['blood', 'gut', 'urine', 'feces', 'bile']:
            seen.add(c_clean)
            compartments.append(c_clean)
    if not compartments:
        compartments = ['liver', 'kidney', 'brain', 'fat', 'rest']
        
    route = schema.get('route', 'oral').lower()
    has_lung = schema.get('has_lung_compartment', 'lung' in compartments)
    has_ehr = schema.get('has_ehr', False)
    
    # Ensure parameter dictionary has defaults if missing
    default_params = {
        'BW': 0.25,
        'Dose': 10.0,
        'Qc': 15.0,
        'Kabs': 0.69,
        'Fu': 0.04,
        'Vmax': 250000.0,
        'Km': 140.0,
        'Clurine': 0.3771,
        'Kfeces': 0.013,
        'Kehr': 0.05,
        'VP': 0.074
    }
    
    # Fill in standard organ params if not in params
    for org, mapping in ORGAN_PARAM_MAP.items():
        if mapping['vol'] not in params:
            params[mapping['vol']] = 0.01
        if mapping['flow'] not in params:
            params[mapping['flow']] = 0.05
        if mapping['part'] not in params:
            params[mapping['part']] = 1.0
            
    for k, v in default_params.items():
        if k not in params:
            params[k] = v

    # Build R script string
    r_lines = [
        "library(deSolve)",
        "",
        "# APEX-PBPK Dynamically Generated Model",
        "params <- c("
    ]
    
    param_strs = []
    for k, v in params.items():
        param_strs.append(f"  {k} = {v}")
    r_lines.append(",\n".join(param_strs))
    r_lines.append(")")
    r_lines.append("")
    
    # Initial states
    r_lines.append("# Initial state amounts (mg)")
    r_lines.append("Dose_mg <- as.numeric(params[\"Dose\"] * params[\"BW\"])")
    r_lines.append("init_states <- c(")
    
    states = []
    if route == 'oral':
        states.append("  A_gut = Dose_mg")
    else:
        states.append("  A_gut = 0")
        
    for comp in compartments:
        states.append(f"  A_{comp} = 0")
        
    states.append("  A_blood = 0")
    if route == 'iv':
        # Add initial dose to blood pool
        states[states.index("  A_blood = 0")] = "  A_blood = Dose_mg"
        
    states.append("  A_urine = 0")
    states.append("  A_feces = 0")
    if has_ehr:
        states.append("  A_bile = 0")
        
    r_lines.append(",\n".join(states))
    r_lines.append(")")
    r_lines.append("")
    
    # ODE function definition
    r_lines.append("pbpk_ode <- function(time, state, parameters) {")
    r_lines.append("  with(as.list(c(state, parameters)), {")
    
    # Volume calculation
    r_lines.append("    # 1. Compartment Volumes (L)")
    r_lines.append("    Vol_Blood <- VP * BW")
    for comp in compartments:
        vol_key = ORGAN_PARAM_MAP.get(comp, {}).get('vol', f"V_{comp}")
        r_lines.append(f"    Vol_{comp} <- get0('{vol_key}', ifnotfound = 0.01) * BW")
        
    r_lines.append("")
    
    # Flow calculation
    r_lines.append("    # 2. Blood Flows (L/h)")
    r_lines.append("    Flow_c <- Qc")
    for comp in compartments:
        flow_key = ORGAN_PARAM_MAP.get(comp, {}).get('flow', f"Q_{comp}")
        r_lines.append(f"    Flow_{comp} <- get0('{flow_key}', ifnotfound = 0.05) * Flow_c")
        
    r_lines.append("")
    
    # Concentrations
    r_lines.append("    # 3. Concentrations (mg/L)")
    r_lines.append("    C_gut <- A_gut / Vol_Blood")
    r_lines.append("    C_blood <- A_blood / Vol_Blood")
    for comp in compartments:
        r_lines.append(f"    C_{comp} <- A_{comp} / Vol_{comp}")
        
    r_lines.append("")
    
    # Metabolism & Clearance
    r_lines.append("    # 4. Metabolic & Clearance terms")
    if 'liver' in compartments:
        r_lines.append("    C_liver_uM <- (C_liver / 234.2) * 1000")
        r_lines.append("    Vmet_uM_h <- (Vmax * C_liver_uM * get0('Fu', ifnotfound = 1.0)) / (Km + C_liver_uM * get0('Fu', ifnotfound = 1.0))")
        r_lines.append("    Vmet <- Vmet_uM_h * (BW^0.75) * 1e-6 * 234.2")
    else:
        r_lines.append("    Vmet <- 0")
        
    r_lines.append("")
    
    # Differential Equations
    r_lines.append("    # 5. Differential Equations (dA/dt)")
    if route == 'oral':
        if has_ehr:
            r_lines.append("    dA_gut_dt <- -Kabs * A_gut + get0('Kehr', ifnotfound = 0.0) * A_bile")
        else:
            r_lines.append("    dA_gut_dt <- -Kabs * A_gut - Kfeces * A_gut")
    else:
        r_lines.append("    dA_gut_dt <- 0")
        
    # Organ ODEs
    blood_inflow_terms = []
    for comp in compartments:
        part_key = ORGAN_PARAM_MAP.get(comp, {}).get('part', f"P_{comp}")
        outflow_conc = f"C_{comp} / get0('{part_key}', ifnotfound = 1.0)"
        
        if comp == 'liver':
            r_lines.append(f"    dA_liver_dt <- Flow_liver * (C_blood - {outflow_conc}) + (if ('A_gut' %in% names(state)) Kabs * A_gut else 0) - Vmet")
        elif comp == 'kidney':
            r_lines.append(f"    dA_kidney_dt <- Flow_kidney * (C_blood - {outflow_conc}) - Clurine * ({outflow_conc}) * get0('Fu', ifnotfound = 1.0)")
        else:
            r_lines.append(f"    dA_{comp}_dt <- Flow_{comp} * (C_blood - {outflow_conc})")
            
        blood_inflow_terms.append(f"Flow_{comp} * ({outflow_conc})")
        
    # Blood pool ODE
    inflow_str = " + ".join(blood_inflow_terms) if blood_inflow_terms else "0"
    r_lines.append(f"    dA_blood_dt <- ({inflow_str}) - Flow_c * C_blood")
    
    # Excretions
    if 'kidney' in compartments:
        r_lines.append("    dA_urine_dt <- Clurine * (C_kidney / get0('PK', ifnotfound = 1.0)) * get0('Fu', ifnotfound = 1.0)")
    else:
        r_lines.append("    dA_urine_dt <- 0")
        
    r_lines.append("    dA_feces_dt <- Kfeces * A_gut")
    
    if has_ehr:
        r_lines.append("    dA_bile_dt <- Kfeces * get0('A_liver', ifnotfound = 0) * 0.9 - get0('Kehr', ifnotfound = 0) * A_bile")
        
    # Return statement
    derivs = ["dA_gut_dt"] + [f"dA_{comp}_dt" for comp in compartments] + ["dA_blood_dt", "dA_urine_dt", "dA_feces_dt"]
    if has_ehr:
        derivs.append("dA_bile_dt")
        
    r_lines.append("")
    r_lines.append(f"    return(list(c({', '.join(derivs)})))")
    r_lines.append("  })")
    r_lines.append("}")
    r_lines.append("")
    
    # Simulation solver call
    r_lines.append("# Execute simulation")
    r_lines.append("times <- seq(0, 24, by = 0.1)")
    r_lines.append("sol <- ode(y = init_states, times = times, func = pbpk_ode, parms = params)")
    r_lines.append("write.csv(sol, \"pbpk_output.csv\", row.names = FALSE)")
    r_lines.append("")
    
    return "\n".join(r_lines)
