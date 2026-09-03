"""
entity_linker.py
~~~~~~~~~~~~~~~~
Maps raw extracted PK/PBPK parameter names to formal PBPKO ontology terms.

PBPKO: Physiologically Based Pharmacokinetic Ontology
       https://github.com/InSilicoVida-Research-Lab/pbpko
       https://doi.org/10.1016/j.comtox.2026.100445
"""

from __future__ import annotations
import json, os, re
from difflib import get_close_matches, SequenceMatcher
from functools import lru_cache

_TERMS_PATH = os.path.join(os.path.dirname(__file__), "pbpko_terms.json")
_CLEAN_RE   = re.compile(r"[_\-/]")
_SPACE_RE   = re.compile(r"\s+")


@lru_cache(maxsize=1)
def _load_terms() -> dict:
    with open(_TERMS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _norm(text: str) -> str:
    text = text.lower().strip()
    text = _CLEAN_RE.sub(" ", text)
    text = _SPACE_RE.sub(" ", text)
    return text


# Common PK abbreviations → PBPKO preferred label
_ABBREV: dict[str, str] = {
    # Clearance — use exact PBPKO labels
    "cl":          "clearance rate",
    "clint":       "intrinsic clearance rate",
    "cl int":      "intrinsic clearance rate",
    "cl h":        "hepatic clearance rate",
    "cl r":        "urinary clearance rate",
    "cl ren":      "urinary clearance rate",
    "cl urine":    "urinary clearance rate",
    "cl bile":     "biliary clearance rate",
    "cl sweat":    "sweat clearance rate",
    "clrenal":     "urinary clearance rate",
    "clhepatic":   "hepatic clearance rate",
    # Volume of distribution
    "vd":          "volume of distribution",
    "vdss":        "volume of distribution",
    "vc":          "volume of compartment",
    "vp":          "volume of plasma",
    "vb":          "volume of blood",
    # Partition coefficients
    "kp":          "tissue plasma partition coefficient",
    "kpuu":        "tissue plasma partition coefficient",
    "pb":          "blood plasma partition coefficient",
    "rbp":         "blood plasma partition coefficient",
    "bp":          "blood plasma partition coefficient",
    # Michaelis-Menten / metabolism
    "vmax":        "maximum metabolic rate",
    "km":          "michaelis constant liver",
    "ka":          "absorption rate constant",
    "fa":          "fraction absorbed",
    "fg":          "intestinal extraction",
    "fh":          "hepatic extraction",
    "f":           "bioavailability",
    "fabs":        "fraction absorbed",
    # Binding
    "fu":          "unbound fraction",
    "fup":         "fraction unbound plasma",
    "fuinc":       "unbound fraction in incubation",
    # Rate constants
    "kel":         "elimination rate constant",
    "k12":         "intercompartmental transfer rate constant",
    "k21":         "intercompartmental transfer rate constant",
    "k10":         "elimination rate constant",
    "kabs":        "absorption rate constant",
    "kmet":        "metabolism rate constant in liver",
    "kbile":       "biliary excretion rate constant",
    "kren":        "renal elimination rate constant",
    # PK metrics — PBPKO labels
    "auc":         "area under curve",
    "aucinf":      "area under curve 0 to infinity",
    "auc0inf":     "area under curve 0 to infinity",
    "cmax":        "maximum concentration",
    "tmax":        "time of maximum concentration",
    "t1 2":        "half-life",
    "t12":         "half-life",
    "thalf":       "half-life",
    "mrt":         "mean residence time",
    "mat":         "mean absorption time",
    # Blood flows
    "qh":          "hepatic blood flow rate",
    "qk":          "renal blood flow rate",
    "ql":          "lung blood flow rate",
    "qi":          "intestinal blood flow rate",
    "qco":         "cardiac output",
    "co":          "cardiac output",
    # Organ volumes
    "vl":          "volume of liver",
    "vk":          "volume of kidney",
    "vlu":         "volume of lung",
    "vbr":         "volume of brain",
    "vmuscle":     "volume of muscle",
    "vfat":        "volume of fat",
    # Permeability & physicochemical
    "papp":        "specific intestinal permeability",
    "mw":          "molecular weight",
    "logp":        "log p",
    "pka":         "pka value",
    "sol":         "water solubility",
}


def link_pk_entity(raw_name: str) -> dict:
    """
    Map a raw parameter name to the best-matching PBPKO term.
    Returns dict: canonical_name, pbpko_id, pbpko_iri, match_type, match_score.
    """
    terms  = _load_terms()
    normed = _norm(raw_name)

    # 1. Abbreviation map
    if normed in _ABBREV:
        target = _norm(_ABBREV[normed])
        for label, data in terms.items():
            if _norm(label) == target:
                return {"canonical_name": label, "pbpko_id": data["id"],
                        "pbpko_iri": data["iri"], "match_type": "abbreviation",
                        "match_score": 1.0}
        return {"canonical_name": _ABBREV[normed], "pbpko_id": "",
                "pbpko_iri": "", "match_type": "abbreviation_unresolved",
                "match_score": 0.9}

    # 2. Exact label match
    norm_to_label = {_norm(l): l for l in terms}
    if normed in norm_to_label:
        orig = norm_to_label[normed]
        return {"canonical_name": orig, "pbpko_id": terms[orig]["id"],
                "pbpko_iri": terms[orig]["iri"], "match_type": "exact",
                "match_score": 1.0}

    # 3. Synonym match
    for label, data in terms.items():
        for syn in data.get("exact_synonyms", []) + data.get("related_synonyms", []):
            if _norm(syn) == normed:
                return {"canonical_name": label, "pbpko_id": data["id"],
                        "pbpko_iri": data["iri"], "match_type": "synonym_exact",
                        "match_score": 0.95}

    # 4. Fuzzy match
    candidates = list(norm_to_label.keys())
    matches = get_close_matches(normed, candidates, n=1, cutoff=0.6)
    if matches:
        orig  = norm_to_label[matches[0]]
        score = SequenceMatcher(None, normed, matches[0]).ratio()
        return {"canonical_name": orig, "pbpko_id": terms[orig]["id"],
                "pbpko_iri": terms[orig]["iri"], "match_type": "fuzzy",
                "match_score": round(score, 3)}

    # 5. No match
    return {"canonical_name": raw_name, "pbpko_id": "", "pbpko_iri": "",
            "match_type": "unmatched", "match_score": 0.0}


def link_pk_entity_simple(raw_name: str) -> str:
    """Backward-compatible: returns just canonical_name string."""
    return link_pk_entity(raw_name)["canonical_name"]


if __name__ == "__main__":
    tests = ["CL", "Vd", "fu", "KP_liver", "Vmax", "Km", "AUC", "Cmax",
             "t1/2", "ka", "clint", "QH", "V_liver", "hepatic clearance",
             "volume of distribution", "fraction unbound in plasma", "xyz_unknown"]
    print(f"{'Raw':<35} {'Canonical':<45} {'ID':<18} {'Type':<25} Score")
    print("-"*135)
    for n in tests:
        r = link_pk_entity(n)
        print(f"{n:<35} {r['canonical_name']:<45} {r['pbpko_id']:<18} {r['match_type']:<25} {r['match_score']:.2f}")
