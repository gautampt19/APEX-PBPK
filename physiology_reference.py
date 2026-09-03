"""
physiology_reference.py — Standard PBPK physiological reference data & organ inference.

Rather than hardcoding organ defaults, this module:
  1. Provides a comprehensive reference table of standard physiological
     parameters for rat and human (from Brown et al. 1997; ICRP 2002).
  2. Infers which organ compartments are relevant for a given paper
     by scanning the extracted biochemical_parameters keys and equations
     for organ-related keywords.
  3. Returns only the relevant subset of organs + their standard values.
"""

from typing import Dict, Tuple, Any

# ─────────────────────────────────────────────────────────────────────────────
# Standard physiological reference values
# Blood flow fractions: fraction of cardiac output going to each organ
# Volume fractions: organ volume as fraction of body weight
# Sources: Brown et al. 1997 (Toxicol Ind Health), ICRP 89, PK-Sim defaults
# ─────────────────────────────────────────────────────────────────────────────

REFERENCE_BLOOD_FLOWS = {
    # organ_name -> {"rat": frac, "human": frac}
    "lung":       {"rat": 1.0,    "human": 1.0},
    "liver":      {"rat": 0.183,  "human": 0.227},
    "kidney":     {"rat": 0.141,  "human": 0.175},
    "brain":      {"rat": 0.020,  "human": 0.114},
    "heart":      {"rat": 0.051,  "human": 0.040},
    "fat":        {"rat": 0.070,  "human": 0.052},
    "muscle":     {"rat": 0.278,  "human": 0.170},
    "skin":       {"rat": 0.058,  "human": 0.050},
    "gut":        {"rat": 0.141,  "human": 0.150},
    "spleen":     {"rat": 0.020,  "human": 0.030},
    "bone":       {"rat": 0.122,  "human": 0.050},
    "pancreas":   {"rat": 0.013,  "human": 0.010},
    "thymus":     {"rat": 0.003,  "human": 0.001},
    "adrenal":    {"rat": 0.003,  "human": 0.003},
}

REFERENCE_VOLUMES = {
    # organ_name -> {"rat": frac_of_BW, "human": frac_of_BW}
    "lung":       {"rat": 0.005,  "human": 0.008},
    "liver":      {"rat": 0.034,  "human": 0.026},
    "kidney":     {"rat": 0.007,  "human": 0.004},
    "brain":      {"rat": 0.006,  "human": 0.020},
    "heart":      {"rat": 0.003,  "human": 0.005},
    "fat":        {"rat": 0.070,  "human": 0.214},
    "muscle":     {"rat": 0.404,  "human": 0.400},
    "skin":       {"rat": 0.190,  "human": 0.037},
    "gut":        {"rat": 0.027,  "human": 0.017},
    "spleen":     {"rat": 0.002,  "human": 0.003},
    "bone":       {"rat": 0.060,  "human": 0.143},
    "plasma":     {"rat": 0.041,  "human": 0.044},
    "pancreas":   {"rat": 0.004,  "human": 0.001},
    "thymus":     {"rat": 0.001,  "human": 0.0003},
    "adrenal":    {"rat": 0.0003, "human": 0.0002},
}

# ─────────────────────────────────────────────────────────────────────────────
# Keyword → Organ mapping
# Maps biochemical parameter keywords / equation tokens to relevant organs.
# ─────────────────────────────────────────────────────────────────────────────

KEYWORD_ORGAN_MAP = {
    # Liver indicators
    "cyp":        "liver",
    "hepat":      "liver",
    "liver":      "liver",
    "biliary":    "liver",
    "bile":       "liver",
    "intrinsic_clearance": "liver",
    "vmax":       "liver",
    "metabolism": "liver",
    "first_pass": "liver",
    "portal":     "liver",

    # Kidney indicators
    "gfr":        "kidney",
    "renal":      "kidney",
    "kidney":     "kidney",
    "tubular":    "kidney",
    "nephro":     "kidney",
    "creatinine": "kidney",
    "glomerul":   "kidney",
    "filtration":  "kidney",

    # Gut / GI indicators
    "intestin":   "gut",
    "absorb":     "gut",
    "absorption": "gut",
    "kabs":       "gut",
    "peff":       "gut",
    "permeabil":  "gut",
    "transit_time": "gut",
    "gastric":    "gut",
    "gi_tract":   "gut",
    "weibull":    "gut",
    "dissolution": "gut",
    "solubility": "gut",

    # Lung indicators
    "lung":       "lung",
    "pulmon":     "lung",
    "inhalat":    "lung",
    "aerosol":    "lung",
    "alveol":     "lung",

    # Brain indicators
    "brain":      "brain",
    "bbb":        "brain",
    "cns":        "brain",
    "cerebr":     "brain",
    "neurolog":   "brain",

    # Heart indicators
    "heart":      "heart",
    "cardiac":    "heart",
    "myocard":    "heart",

    # Fat indicators
    "fat":        "fat",
    "adipos":     "fat",
    "lipophil":   "fat",
    "logp":       "fat",

    # Muscle indicators
    "muscle":     "muscle",
    "skeletal":   "muscle",

    # Skin indicators
    "skin":       "skin",
    "dermal":     "skin",
    "cutaneous":  "skin",
    "topical":    "skin",

    # Spleen indicators
    "spleen":     "spleen",

    # Bone indicators
    "bone":       "bone",
    "marrow":     "bone",
}

# Minimum organ set for a valid PBPK model
# (lung for arterial/venous mixing, liver for metabolism)
MINIMUM_ORGANS = {"lung", "liver"}


def infer_organs_from_params(biochem: Dict[str, Any], equations: Dict[str, str] = None) -> set:
    """
    Scan biochemical parameter keys and equation strings for organ-related
    keywords. Returns a set of organ names that should be in the PBPK model.
    """
    organs = set()

    # Collect all searchable text from biochem keys (recursively)
    search_tokens = set()

    def _collect_keys(d, prefix=""):
        for k, v in d.items():
            full_key = f"{prefix}_{k}" if prefix else k
            search_tokens.add(full_key.lower())
            search_tokens.add(k.lower())
            if isinstance(v, dict):
                _collect_keys(v, full_key)

    _collect_keys(biochem)

    # Also scan equation keys and values
    if equations:
        for k, v in equations.items():
            search_tokens.add(k.lower())
            search_tokens.add(v.lower())

    # Match keywords to organs
    joined_text = " ".join(search_tokens)
    for keyword, organ in KEYWORD_ORGAN_MAP.items():
        if keyword in joined_text:
            organs.add(organ)

    # Ensure minimum viable PBPK structure
    organs.update(MINIMUM_ORGANS)

    return organs


def get_organ_physiology(organs: set, species: str = "human") -> Tuple[Dict[str, float], Dict[str, float]]:
    """
    Given a set of organ names and a species, return dictionaries of
    blood flow fractions and volume fractions from the reference tables.

    Args:
        organs: Set of organ names to include
        species: "rat" or "human"

    Returns:
        (blood_flows, volumes) — dicts mapping organ name → fraction
    """
    species_key = species.lower()
    if species_key not in ("rat", "human"):
        species_key = "human"

    flows = {}
    vols = {}

    for organ in organs:
        organ_lower = organ.lower()
        if organ_lower in REFERENCE_BLOOD_FLOWS:
            flows[organ_lower] = REFERENCE_BLOOD_FLOWS[organ_lower][species_key]
        if organ_lower in REFERENCE_VOLUMES:
            vols[organ_lower] = REFERENCE_VOLUMES[organ_lower][species_key]

    # Always include plasma volume for the model
    if "plasma" not in vols and "plasma" in REFERENCE_VOLUMES:
        vols["plasma"] = REFERENCE_VOLUMES["plasma"][species_key]

    return flows, vols


def infer_and_get_physiology(
    biochem: Dict[str, Any],
    equations: Dict[str, str] = None,
    species: str = "human"
) -> Tuple[Dict[str, float], Dict[str, float], set]:
    """
    Convenience function: infer organs, then return their physiology.

    Returns:
        (blood_flows, volumes, inferred_organs)
    """
    organs = infer_organs_from_params(biochem, equations)
    flows, vols = get_organ_physiology(organs, species)
    return flows, vols, organs
