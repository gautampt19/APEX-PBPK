"""
generate_r_model.py — Dynamically generate deSolve-based PBPK R scripts
from LLM-extracted parameter JSON files.

Handles:
  • Any combination of organs (inferred or explicitly extracted)
  • Multiple administration routes (oral, IV, inhaled)
  • Multiple metabolism types (Michaelis-Menten, linear clearance, both)
  • Nested or flat biochemical parameter structures
  • Single or multi-species models
  • Renal & biliary elimination
"""

import json
import argparse
import os
from physiology_reference import infer_and_get_physiology

# ─── Parameter Alias Tables ──────────────────────────────────────────────────
# Maps canonical parameter names to possible key substrings (case-insensitive).
# Order matters: more specific aliases first to avoid false matches.

PARAM_ALIASES = {
    "fu":         ["fraction_unbound", "fu_human", "fu_rat", "fup", "f_u", "fu"],
    "Vmax":       ["vmax", "max_velocity", "maximum_rate"],
    "Km":         ["michaelis", "km"],
    "CLint":      ["intrinsic_clearance", "clint", "cl_int"],
    "CL":         ["total_clearance", "systemic_clearance"],
    "GE":         ["gastric_emptying", "ge_rate"],
    "Kabs":       ["absorption_rate", "absorption_constant", "kabs", "ka"],
    "K_feces":    ["fecal_elimination", "kfeces", "k_feces", "fecal"],
    "GFR":        ["glomerular_filtration", "gfr_specific", "gfr"],
    "CL_renal":   ["renal_clearance", "cl_renal"],
    "CL_biliary": ["biliary_secretion", "biliary_clearance", "cl_biliary"],
    "Peff":       ["intestinal_permeability", "peff", "permeability"],
    "logP":       ["logp", "log_p"],
    "MW":         ["molecular_weight", "mw"],
}


# ─── Utility Functions ────────────────────────────────────────────────────────

def _flatten_dict(d, parent_key='', sep='__'):
    """Recursively flatten a nested dict, preserving the full key path."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(_flatten_dict(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def _find_param(flat_params, aliases, default=None):
    """
    Search flat_params for the first key matching any alias
    (case-insensitive substring match). Returns (value, matched_key).
    """
    for alias in aliases:
        for key, value in flat_params.items():
            if alias.lower() in key.lower():
                try:
                    return float(value), key
                except (ValueError, TypeError):
                    continue
    return default, None


# ─── Model Characteristic Detection ───────────────────────────────────────────

def _detect_admin_route(flat_params):
    """Detect administration route from parameter key names."""
    keys_lower = " ".join(k.lower() for k in flat_params.keys())

    score = {
        "oral":    sum(1 for kw in ["kabs", "absorption", "gastric", "intestin",
                                     "permeabil", "transit_time", "dissolution",
                                     "solubility", "weibull", "oral"] if kw in keys_lower),
        "iv":      sum(1 for kw in ["infusion", "bolus", "intravenous", "iv_dose"] if kw in keys_lower),
        "inhaled": sum(1 for kw in ["inhalation", "aerosol", "deposition",
                                     "particle_size", "pulmonary_dose"] if kw in keys_lower),
        "topical": sum(1 for kw in ["dermal", "skin_flux", "topical",
                                     "transdermal"] if kw in keys_lower),
    }
    best = max(score, key=score.get)
    return best if score[best] > 0 else "oral"  # default oral


def _detect_metabolism(flat_params, equations):
    """Return dict describing the metabolism type, organ, and parameter values."""
    vmax, _ = _find_param(flat_params, PARAM_ALIASES["Vmax"])
    km, _   = _find_param(flat_params, PARAM_ALIASES["Km"])
    clint, _ = _find_param(flat_params, PARAM_ALIASES["CLint"])
    cl, _    = _find_param(flat_params, PARAM_ALIASES["CL"])

    has_mm     = vmax is not None and km is not None
    has_linear = clint is not None or cl is not None

    # Check equations for MM hints even if Vmax/Km not in flat params
    eq_text = " ".join(equations.values()).lower() if equations else ""
    if "vmax" in eq_text and "km" in eq_text:
        has_mm = True

    if has_mm and has_linear:
        met_type = "both"
    elif has_mm:
        met_type = "mm"
    elif has_linear:
        met_type = "linear"
    else:
        met_type = "linear"  # safe default — CLint=0 means no metabolism

    # Detect metabolising organ (default: liver)
    met_organ = "liver"
    keys_lower = " ".join(k.lower() for k in flat_params.keys())
    if "kidney" in keys_lower and "liver" not in keys_lower and "cyp" not in keys_lower:
        met_organ = "kidney"

    return {
        "type":  met_type,
        "organ": met_organ,
        "Vmax":  vmax,
        "Km":    km,
        "CLint": clint if clint is not None else cl,
    }


def _detect_elimination(flat_params):
    """Return dict of elimination routes found in the data."""
    elim = {}
    gfr, _        = _find_param(flat_params, PARAM_ALIASES["GFR"])
    cl_renal, _   = _find_param(flat_params, PARAM_ALIASES["CL_renal"])
    cl_biliary, _ = _find_param(flat_params, PARAM_ALIASES["CL_biliary"])
    k_feces, _    = _find_param(flat_params, PARAM_ALIASES["K_feces"])

    if gfr is not None or cl_renal is not None:
        elim["renal"] = gfr if gfr is not None else cl_renal
    if cl_biliary is not None:
        elim["biliary"] = cl_biliary
    if k_feces is not None:
        elim["fecal"] = k_feces
    return elim


def _detect_species(params):
    """Detect species from parameter key prefixes and nested keys."""
    blood_flows = params.get("blood_flow_fraction", {})
    volumes     = params.get("volume_fraction", {})
    biochem_str = json.dumps(params.get("biochemical_parameters", {})).lower()

    species = set()
    for k in list(blood_flows.keys()) + list(volumes.keys()):
        for sp in ("Rat", "Human", "Mouse", "Dog", "Monkey"):
            if k.startswith(f"{sp}_"):
                species.add(sp.lower())

    for tag in ("_human", "_rat", "_mouse", "_dog"):
        if tag in biochem_str:
            species.add(tag.strip("_"))

    return sorted(species) if species else ["human"]


# ─── Species Default Physiology ───────────────────────────────────────────────

SPECIES_DEFAULTS = {
    "rat":    {"BW": 0.250, "Qc": 14.0},
    "human":  {"BW": 70.0,  "Qc": 372.0},
    "mouse":  {"BW": 0.025, "Qc": 1.68},
    "dog":    {"BW": 10.0,  "Qc": 120.0},
    "monkey": {"BW": 5.0,   "Qc": 66.0},
}


# ─── Main R Code Generator ───────────────────────────────────────────────────

def generate_r_script(json_path: str, output_r_path: str):
    print(f"Reading parameters from: {json_path}")
    with open(json_path, 'r', encoding='utf-8') as f:
        params = json.load(f)

    blood_flows = params.get("blood_flow_fraction", {})
    volumes     = params.get("volume_fraction", {})
    biochem     = params.get("biochemical_parameters", {})
    equations   = params.get("equations", {})

    # Flatten for parameter discovery
    flat_biochem = _flatten_dict(biochem)

    # Detect model characteristics
    admin_route  = _detect_admin_route(flat_biochem)
    metabolism   = _detect_metabolism(flat_biochem, equations)
    elimination  = _detect_elimination(flat_biochem)
    species_list = _detect_species(params)

    print(f"  [Detected] Route: {admin_route} | "
          f"Metabolism: {metabolism['type']} in {metabolism['organ']} | "
          f"Species: {species_list}")
    if elimination:
        print(f"  [Detected] Elimination: {list(elimination.keys())}")

    # Resolve global biochem parameters
    fu_val,   _ = _find_param(flat_biochem, PARAM_ALIASES["fu"],      default=0.5)
    ge_val,   _ = _find_param(flat_biochem, PARAM_ALIASES["GE"],      default=2.5)
    kabs_val, _ = _find_param(flat_biochem, PARAM_ALIASES["Kabs"],    default=1.0)
    kfec_val, _ = _find_param(flat_biochem, PARAM_ALIASES["K_feces"], default=0.01)

    # ── Start building R code ─────────────────────────────────────────────────
    r = []  # accumulator list — joined with \n at end

    r.append("# ==========================================")
    r.append("# AUTO-GENERATED PBPK MODEL")
    r.append(f"# Route: {admin_route} | Metabolism: {metabolism['type']}")
    r.append(f"# Species: {', '.join(species_list)}")
    r.append("# ==========================================")
    r.append("if (!require('deSolve')) {")
    r.append("  install.packages('deSolve', repos='http://cran.us.r-project.org')")
    r.append("  library(deSolve)")
    r.append("}\n")

    # ── Global parameter list ─────────────────────────────────────────────────
    gp_lines = []
    gp_lines.append(f"  fu = {fu_val}")

    if metabolism["type"] in ("mm", "both"):
        gp_lines.append(f"  Vmax = {metabolism['Vmax'] or 250000.0}")
        gp_lines.append(f"  Km = {metabolism['Km'] or 140.0}")
    if metabolism["type"] in ("linear", "both"):
        gp_lines.append(f"  CLint = {metabolism['CLint'] or 1.0}")
    if admin_route == "oral":
        gp_lines.append(f"  GE = {ge_val}")
        gp_lines.append(f"  Kabs = {kabs_val}")
        gp_lines.append(f"  K_feces = {kfec_val}")
    if "renal" in elimination:
        gp_lines.append(f"  GFR = {elimination['renal']}")
    if "biliary" in elimination:
        gp_lines.append(f"  CL_biliary = {elimination['biliary']}")

    r.append("# --- GLOBAL / BIOCHEMICAL PARAMETERS ---")
    r.append("global_params <- list(")
    r.append(",\n".join(gp_lines))
    r.append(")\n")

    # ── Per-species model blocks ──────────────────────────────────────────────
    for species in species_list:
        sp = species.lower()
        SP = species.capitalize()

        _generate_species_block(
            r, sp, SP, params, blood_flows, volumes,
            biochem, equations, flat_biochem,
            admin_route, metabolism, elimination,
        )

    # Convenience copy of last species output
    r.append(f"write.csv(out_{species_list[-1]}, "
             f"file = 'dynamic_simulation_results.csv', row.names = FALSE)")

    # ── Write ─────────────────────────────────────────────────────────────────
    with open(output_r_path, 'w') as f:
        f.write("\n".join(r))

    print(f"Successfully generated dynamic R PBPK model at: {output_r_path}")


# ─── Per-species helper ──────────────────────────────────────────────────────

def _generate_species_block(
    r, sp, SP, params, blood_flows, volumes,
    biochem, equations, flat_biochem,
    admin_route, metabolism, elimination,
):
    """Append R code for one species to the accumulator list *r*."""

    # ── Resolve organ flows / volumes for this species ────────────────────────
    prefix = f"{SP}_"
    sp_flows = {k.replace(prefix, ""): v
                for k, v in blood_flows.items() if k.startswith(prefix)}
    sp_vols  = {k.replace(prefix, ""): v
                for k, v in volumes.items()     if k.startswith(prefix)}

    # Fall back to un-prefixed keys
    if not sp_flows:
        sp_flows = {k: v for k, v in blood_flows.items()
                    if not any(k.startswith(p)
                               for p in ("Rat_","Human_","Mouse_","Dog_","Monkey_"))}
        sp_vols  = {k: v for k, v in volumes.items()
                    if not any(k.startswith(p)
                               for p in ("Rat_","Human_","Mouse_","Dog_","Monkey_"))}

    # Fall back to inference from biochem context
    if not sp_flows:
        sp_flows, sp_vols, inferred = infer_and_get_physiology(
            biochem, equations, species=sp)
        print(f"  [Inferred] {SP} organs from biochem context: {sorted(inferred)}")

    # Ensure metabolism organ is present
    met_organ = metabolism["organ"]
    if met_organ not in (k.lower() for k in sp_flows):
        from physiology_reference import REFERENCE_BLOOD_FLOWS, REFERENCE_VOLUMES
        ref_sp = sp if sp in ("rat", "human") else "human"
        if met_organ in REFERENCE_BLOOD_FLOWS:
            sp_flows[met_organ] = REFERENCE_BLOOD_FLOWS[met_organ][ref_sp]
        if met_organ in REFERENCE_VOLUMES:
            sp_vols[met_organ]  = REFERENCE_VOLUMES[met_organ][ref_sp]

    bw = SPECIES_DEFAULTS.get(sp, SPECIES_DEFAULTS["human"])["BW"]
    qc = SPECIES_DEFAULTS.get(sp, SPECIES_DEFAULTS["human"])["Qc"]

    organs = [k.lower() for k in sp_flows.keys()]
    if "rest" not in organs:
        organs.append("rest")

    q_sum = sum(float(v) for k, v in sp_flows.items()
                if k.lower() not in ("lungs", "lung"))
    v_sum = sum(float(v) for k, v in sp_vols.items()
                if k.lower() != "plasma")

    # ── Params vector ─────────────────────────────────────────────────────────
    r.append(f"# ==========================================")
    r.append(f"# {SP.upper()} PBPK MODEL")
    r.append(f"# ==========================================")
    pv = []
    pv.append(f"  BW = {bw}")
    pv.append(f"  Qc = {qc}")
    pv.append("  fu = global_params$fu")

    if metabolism["type"] in ("mm", "both"):
        pv.append("  Vmax = global_params$Vmax")
        pv.append("  Km = global_params$Km")
    if metabolism["type"] in ("linear", "both"):
        pv.append("  CLint = global_params$CLint")
    if admin_route == "oral":
        pv.append("  GE = global_params$GE")
        pv.append("  Kabs = global_params$Kabs")
        pv.append("  K_feces = global_params$K_feces")
    if "renal" in elimination:
        pv.append("  GFR = global_params$GFR")
    if "biliary" in elimination:
        pv.append("  CL_biliary = global_params$CL_biliary")

    for k, v in sp_flows.items():
        pv.append(f"  Q_{k.lower()} = {v}")
    pv.append(f"  Q_rest = max(0, 1.0 - {q_sum})")

    for k, v in sp_vols.items():
        pv.append(f"  V_{k.lower()} = {v}")
    pv.append(f"  V_rest = max(0.05, 1.0 - ({v_sum} + 0.04))")

    # Partition coefficients (try to extract from biochem, default 1.0)
    for k in sp_flows.keys():
        p_val = 1.0
        for b_k, b_v in flat_biochem.items():
            if k.lower() in b_k.lower() and "plasma" in b_k.lower():
                try:
                    p_val = float(b_v)
                except (ValueError, TypeError):
                    pass
        pv.append(f"  P_{k.lower()} = {p_val}")
    pv.append("  P_rest = 1.0")

    r.append(f"params_{sp} <- unlist(list(")
    r.append(",\n".join(pv))
    r.append("))\n")

    # ── ODE function ──────────────────────────────────────────────────────────
    r.append(f"pbpk_ode_{sp} <- function(t, state, parms) {{")
    r.append("  with(as.list(c(state, parms)), {")

    # Absolute flows, volumes, venous concentrations
    for o in organs:
        r.append(f"    Q_{o}_abs <- Q_{o} * Qc")
        r.append(f"    V_{o}_abs <- V_{o} * BW")
        r.append(f"    Cv_{o} <- C_{o} / P_{o}")

    # Mixed venous
    non_lung = [o for o in organs if o not in ("lungs", "lung", "plasma")]
    cv_parts = " + ".join(f"Q_{o}_abs * Cv_{o}" for o in non_lung)
    r.append(f"    Cv_mix <- ({cv_parts}) / Qc")

    # Arterial
    if "lungs" in organs:
        r.append("    C_art <- C_lungs / P_lungs")
    elif "lung" in organs:
        r.append("    C_art <- C_lung / P_lung")
    else:
        r.append("    C_art <- Cv_mix")

    # ── Metabolism ────────────────────────────────────────────────────────────
    r.append("")
    r.append(f"    # --- Metabolism in {met_organ.capitalize()} ---")
    if metabolism["type"] == "mm":
        r.append(f"    Vmet <- (Vmax * C_{met_organ} * fu) / "
                 f"(Km + C_{met_organ} * fu)")
    elif metabolism["type"] == "linear":
        r.append(f"    Vmet <- CLint * C_{met_organ} * fu / P_{met_organ}")
    elif metabolism["type"] == "both":
        r.append(f"    Vmet_mm  <- (Vmax * C_{met_organ} * fu) / "
                 f"(Km + C_{met_organ} * fu)")
        r.append(f"    Vmet_lin <- CLint * C_{met_organ} * fu / P_{met_organ}")
        r.append("    Vmet <- Vmet_mm + Vmet_lin")
    else:
        r.append("    Vmet <- 0")

    # ── Renal elimination ─────────────────────────────────────────────────────
    has_renal = "renal" in elimination and "kidney" in organs
    if has_renal:
        r.append("")
        r.append("    # --- Renal Elimination ---")
        r.append("    CL_renal_abs <- GFR * fu")

    # ── Biliary elimination ───────────────────────────────────────────────────
    has_biliary = "biliary" in elimination
    if has_biliary:
        r.append("")
        r.append("    # --- Biliary Elimination ---")
        r.append(f"    CL_bil_abs <- CL_biliary * C_{met_organ} * fu / P_{met_organ}")

    # ── Route-dependent absorption ────────────────────────────────────────────
    diff_vars = []
    if admin_route == "oral":
        r.append("")
        r.append("    # --- GI Tract Absorption (oral) ---")
        r.append("    dAmount_stomach <- -GE * Amount_stomach")
        r.append("    dAmount_gut <- GE * Amount_stomach - "
                 "Kabs * Amount_gut - K_feces * Amount_gut")
        diff_vars += ["dAmount_stomach", "dAmount_gut"]

    # ── Organ concentration ODEs ──────────────────────────────────────────────
    r.append("")
    r.append("    # --- Organ Concentration ODEs ---")
    for o in organs:
        if o in ("lungs", "lung"):
            r.append(f"    dC_{o} <- (Qc * (Cv_mix - Cv_{o})) / V_{o}_abs")

        elif o == met_organ:
            # The metabolism organ receives arterial blood,
            # portal-vein drug input (oral), and handles metabolism
            parts = [f"Q_{o}_abs * (C_art - Cv_{o})"]
            if admin_route == "oral":
                parts.append("Kabs * Amount_gut")
            parts.append("- Vmet")
            if has_biliary:
                parts.append("- CL_bil_abs")
            r.append(f"    dC_{o} <- ({' + '.join(parts)}) / V_{o}_abs")

        elif o == "kidney" and has_renal:
            r.append(f"    dC_{o} <- (Q_{o}_abs * (C_art - Cv_{o}) "
                     f"- CL_renal_abs * Cv_{o}) / V_{o}_abs")

        else:
            r.append(f"    dC_{o} <- (Q_{o}_abs * (C_art - Cv_{o})) / V_{o}_abs")

        diff_vars.append(f"dC_{o}")

    r.append("")
    r.append(f"    return(list(c({', '.join(diff_vars)})))")
    r.append("  })")
    r.append("}\n")

    # ── Initial conditions ────────────────────────────────────────────────────
    r.append(f"# --- {SP} Simulation ---")

    if admin_route == "oral":
        if sp in ("human",):
            dose_expr = "50.0"  # flat 50 mg dose
        else:
            dose_expr = f"unname(10.0 * params_{sp}['BW'])"  # 10 mg/kg

        ic_parts = [f"Amount_stomach = {dose_expr}", "Amount_gut = 0"]
        for o in organs:
            ic_parts.append(f"C_{o} = 0")
    elif admin_route == "iv":
        # IV bolus: deposit dose in lung compartment (≈ venous blood)
        lung_key = "lungs" if "lungs" in organs else ("lung" if "lung" in organs else None)
        ic_parts = []
        for o in organs:
            if o == lung_key:
                if sp in ("human",):
                    ic_parts.append(
                        f"C_{o} = unname(50.0 / "
                        f"(params_{sp}['V_{o}'] * params_{sp}['BW']))")
                else:
                    ic_parts.append(
                        f"C_{o} = unname(10.0 * params_{sp}['BW'] / "
                        f"(params_{sp}['V_{o}'] * params_{sp}['BW']))")
            else:
                ic_parts.append(f"C_{o} = 0")
    else:
        # Generic — all zero (user should set manually)
        ic_parts = [f"C_{o} = 0" for o in organs]

    r.append(f"init_{sp} <- c(")
    r.append(f"  {', '.join(ic_parts)}")
    r.append(")")
    r.append("times <- seq(0, 24, by = 0.1)")
    r.append(f"out_{sp} <- as.data.frame(ode("
             f"y = init_{sp}, times = times, "
             f"func = pbpk_ode_{sp}, parms = params_{sp}))")
    r.append(f"write.csv(out_{sp}, file = '{sp}_simulation_results.csv', "
             f"row.names = FALSE)")
    r.append(f"print('{SP} PBPK Simulation complete! "
             f"Saved to {sp}_simulation_results.csv')\n")


# ─── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate PBPK R Script from JSON Parameters")
    parser.add_argument("-i", "--input",  required=True,
                        help="Path to the input JSON file (e.g., params.json)")
    parser.add_argument("-o", "--output", default="dynamic_pbpk_model.R",
                        help="Path to save the generated R script")

    args = parser.parse_args()
    generate_r_script(args.input, args.output)
