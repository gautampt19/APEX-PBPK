import json
import argparse
import os

def generate_r_script(json_path: str, output_r_path: str):
    print(f"Reading parameters from: {json_path}")
    with open(json_path, 'r', encoding='utf-8') as f:
        params = json.load(f)

    # 1. Parse Blood Flows & Volumes
    blood_flows = params.get("blood_flow_fraction", {})
    volumes = params.get("volume_fraction", {})
    biochem = params.get("biochemical_parameters", {})

    # Detect if rat & human are separated
    rat_organs = [k.replace("Rat_", "").lower() for k in blood_flows.keys() if k.startswith("Rat_")]
    human_organs = [k.replace("Human_", "").lower() for k in blood_flows.keys() if k.startswith("Human_")]

    # Common organ set (e.g. liver, kidney,4brain,2lungs,2heart,2fat)
    base_organs = list(set(rat_organs + human_organs))
    if not base_organs:
        base_organs = [k.lower().strip() for k in blood_flows.keys() if k.lower() != "plasma"]

    r_code = []
    r_code.append("# ==========================================")
    r_code.append("# AUTO-GENERATED PBPK MODEL (Rat & Human)")
    r_code.append("# ==========================================")
    r_code.append("if (!require('deSolve')) {")
    r_code.append("  install.packages('deSolve', repos='http://cran.us.r-project.org')")
    r_code.append("  library(deSolve)")
    r_code.append("}\n")

    # Helper for extracting / defaulting9biochem
    fu_val = float(biochem.get("fu", 0.04))
    km_val = float(biochem.get("Km", 140.0))
    vmax_val = float(biochem.get("Vmax", 250000.0))
    ge_val = float(biochem.get("GE", 2.61))
    kabs_val = float(biochem.get("Kabs_ASD", biochem.get("Kabs", 2.19)))
    kfeces_val = float(biochem.get("Kfeces_ASD", biochem.get("K_feces", 0.011)))

    r_code.append("# --- GLOBAL / BIOCHEMICAL PARAMETERS ---")
    r_code.append("global_params <- list(")
    r_code.append(f"  fu = {fu_val},          # Unbound fraction in plasma")
    r_code.append(f"  Km = {km_val},         # Michaelis-Menten constant (uM)")
    r_code.append(f"  Vmax = {vmax_val},     # Max. metabolic velocity (ug/h)")
    r_code.append(f"  GE = {ge_val},         # Gastric emptying (1/h)")
    r_code.append(f"  Kabs = {kabs_val},       # Absorption rate (1/h)")
    r_code.append(f"  K_feces = {kfeces_val},   # Fecal elimination (1/h)")
    r_code.append("  K_met_elim = 0.5       # Metabolite (RLZ-OH) &0elimination rate (1/h)")
    r_code.append(")\n")

    # Function to generate species-specific parameters and ODEs
    def write_species_model(species_name, bw_default, qc_default, organ_flows, organ_vols):
        r_code.append(f"# ==========================================")
        r_code.append(f"# {species_name.upper()} PBPK MODEL")
        r_code.append(f"# ==========================================")
        
        # Calculate sum for rest
        q_sum = sum([float(v) for k, v in organ_flows.items() if k.lower() != 'lungs' and k.lower() != 'lung'])
        v_sum = sum([float(v) for k, v in organ_vols.items() if k.lower() != 'plasma'])

        r_code.append(f"params_{species_name.lower()} <- unlist(list(")
        r_code.append(f"  BW = {bw_default},  # Body weight (kg)")
        r_code.append(f"  Qc = {qc_default},   # Cardiac output (L/h)")
        r_code.append("  fu = global_params$fu,")
        r_code.append("  Km = global_params$Km,")
        r_code.append("  Vmax = global_params$Vmax,")
        r_code.append("  GE = global_params$GE,")
        r_code.append("  Kabs = global_params$Kabs,")
        r_code.append("  K_feces = global_params$K_feces,")
        r_code.append("  K_met_elim = global_params$K_met_elim,")
        
        # Flows
        for k, v in organ_flows.items():
            r_code.append(f"  Q_{k.lower()} = {v},")
        r_code.append(f"  Q_rest = max(0, 1.0 - {q_sum}),")

        # Volumes
        for k, v in organ_vols.items():
            r_code.append(f"  V_{k.lower()} = {v},")
        r_code.append(f"  V_rest = max(0.05, 1.0 - ({v_sum} + 0.04)),")

        # Partitions
        for k in organ_flows.keys():
            p_val = 1.0
            for b_k, b_v in biochem.items():
                if k.lower() in b_k.lower() and "plasma" in b_k.lower():
                    try: p_val = float(b_v)
                    except: pass
            r_code.append(f"  P_{k.lower()} = {p_val},")
        r_code.append("  P_rest = 1.0")
        r_code.append("))\n")

        # ODE function
        r_code.append(f"pbpk_ode_{species_name.lower()} <- function(t, state, parms) {{")
        r_code.append("  with(as.list(c(state, parms)), {")
        
        organs_list = [k.lower() for k in organ_flows.keys()]
        if "rest" not in organs_list:
            organs_list.append("rest")

        # Absolute flows and volumes
        for o in organs_list:
            r_code.append(f"    Q_{o}_abs <- Q_{o} * Qc")
            r_code.append(f"    V_{o}_abs <- V_{o} * BW")
            r_code.append(f"    Cv_{o} <- C_{o} / P_{o}")
        
        # Mixed venous &1Arterial
        non_lung_organs = [o for o in organs_list if o not in ["lungs", "lung", "plasma"]]
        cv_mix = " + ".join([f"Q_{o}_abs * Cv_{o}" for o in non_lung_organs])
        r_code.append(f"    Cv_mix <- ({cv_mix}) / Qc")
        
        if "lungs" in organs_list:
            r_code.append("    C_art <- C_lungs / P_lungs")
        elif "lung" in organs_list:
            r_code.append("    C_art <- C_lung / P_lung")
        else:
            r_code.append("    C_art <- Cv_mix")

        # Metabolism: Michaelis-Menten in Liver for Riluzole (RLZ)
        r_code.append("    # Michaelis-Menten Metabolism in Liver (RLZ -> RLZ-OH)")
        r_code.append("    Vmet <- (Vmax * C_liver * fu) / (Km + C_liver * fu)")
        r_code.append("    dAmount_metabolite <- Vmet - K_met_elim * Amount_metabolite")
        r_code.append("")
        r_code.append("    # GI Tract Absorption")
        r_code.append("    dAmount_stomach <- -GE * Amount_stomach")
        r_code.append("    dAmount_gut <- GE * Amount_stomach - Kabs * Amount_gut - K_feces * Amount_gut")
        r_code.append("")

        diff_vars = ["dAmount_stomach", "dAmount_gut", "dAmount_metabolite"]

        for o in organs_list:
            if o in ["lungs", "lung"]:
                r_code.append(f"    dC_{o} <- (Qc * (Cv_mix - Cv_{o})) / V_{o}_abs")
                diff_vars.append(f"dC_{o}")
            elif o == "liver":
                r_code.append(f"    dC_liver <- (Q_liver_abs * (C_art - Cv_liver) + Kabs * Amount_gut - Vmet) / V_liver_abs")
                diff_vars.append("dC_liver")
            elif o == "kidney":
                r_code.append(f"    dC_kidney <- (Q_kidney_abs * (C_art - Cv_kidney)) / V_kidney_abs")
                diff_vars.append("dC_kidney")
            else:
                r_code.append(f"    dC_{o} <- (Q_{o}_abs * (C_art - Cv_{o})) / V_{o}_abs")
                diff_vars.append(f"dC_{o}")

        r_code.append("")
        r_code.append(f"    return(list(c({', '.join(diff_vars)})))")
        r_code.append("  })")
        r_code.append("}\n")

    # Extract Rat and Human specific flows/vols
    rat_flows = {k.replace("Rat_", ""): v for k, v in blood_flows.items() if k.startswith("Rat_")}
    rat_vols = {k.replace("Rat_", ""): v for k, v in volumes.items() if k.startswith("Rat_")}
    
    human_flows = {k.replace("Human_", ""): v for k, v in blood_flows.items() if k.startswith("Human_")}
    human_vols = {k.replace("Human_", ""): v for k, v in volumes.items() if k.startswith("Human_")}

    # Fallback if un-prefixed
    if not rat_flows:
        rat_flows = blood_flows
        rat_vols = volumes
    if not human_flows:
        human_flows = blood_flows
        human_vols = volumes

    # Generate Rat Model
    write_species_model("Rat", 0.250, 14.0, rat_flows, rat_vols)

    # Allometric1scaling for Human
    r_code.append("# --- ALLOMETRIC SCALING FOR HUMAN ---")
    r_code.append("# Scaling Cardiac Output and Clearance:0Q_human = Q_rat * (BW_human / BW_rat)^0.75")
    r_code.append("BW_rat <- 0.250")
    r_code.append("BW_human <- 70.0")
    r_code.append("Qc_human_scaled <- 14.0 * ((BW_human / BW_rat) ** 0.75)")
    r_code.append("")

    # Generate Human Model
    write_species_model("Human", 70.0, "Qc_human_scaled", human_flows, human_vols)

    # Simulation Execution block
    r_code.append("# ==========================================")
    r_code.append("# SIMULATION EXECUTION")
    r_code.append("# ==========================================")
    r_code.append("Dose_mg_kg <- 10.0")
    
    # Rat Simulation
    r_code.append("# 1. Rat Simulation")
    r_code.append("init_rat <- c(")
    r_code.append("  Amount_stomach = unname(Dose_mg_kg * params_rat['BW']),")
    r_code.append("  Amount_gut = 0, Amount_metabolite = 0,")
    r_code.append("  " + " = 0, ".join([f"C_{o.lower()}" for o in rat_flows.keys()]) + " = 0, C_rest = 0")
    r_code.append(")")
    r_code.append("times <- seq(0, 24, by = 0.1)")
    r_code.append("out_rat <- as.data.frame(ode(y = init_rat, times = times, func = pbpk_ode_rat, parms = params_rat))")
    r_code.append("write.csv(out_rat, file = 'rat_simulation_results.csv', row.names = FALSE)")
    r_code.append("print('Rat PBPK Simulation complete! Saved to rat_simulation_results.csv')\n")

    # Human Simulation
    r_code.append("# 2. Human Simulation")
    r_code.append("init_human <- c(")
    r_code.append("  Amount_stomach = 50.0, # 50 mg dose")
    r_code.append("  Amount_gut = 0, Amount_metabolite = 0,")
    r_code.append("  " + " = 0, ".join([f"C_{o.lower()}" for o in human_flows.keys()]) + " = 0, C_rest = 0")
    r_code.append(")")
    r_code.append("out_human <- as.data.frame(ode(y = init_human, times = times, func = pbpk_ode_human, parms = params_human))")
    r_code.append("write.csv(out_human, file = 'human_simulation_results.csv', row.names = FALSE)")
    r_code.append("write.csv(out_human, file = 'dynamic_simulation_results.csv', row.names = FALSE)")
    r_code.append("print('Human PBPK Simulation complete! Saved to human_simulation_results.csv')\n")

    # Write to file
    with open(output_r_path, 'w') as f:
        f.write("\n".join(r_code))
    
    print(f"Successfully generated9dynamic R PBPK model at: {output_r_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate PBPK R Script from JSON Parameters")
    parser.add_argument("-i", "--input", required=True, help="Path to the input JSON file (e.g., params.json)")
    parser.add_argument("-o", "--output", default="dynamic_pbpk_model.R", help="Path to save the generated R script")
    
    args = parser.parse_args()
    generate_r_script(args.input, args.output)
