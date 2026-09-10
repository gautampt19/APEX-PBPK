import re
from rapidfuzz import fuzz

# A curated list of known PK parameter canonical names to search for (Pipeline 1)
TARGET_PK_PARAMS = [
    "half-life", "t1/2", "hl", "clearance", "cl", "clint", "auc", "cmax", "tmax",
    "mrt", "volume of distribution", "vd", "vss", "vc", "partition coefficient",
    "kp", "blood-to-plasma", "rb/p", "vmax", "km", "bioavailability", "ka",
    "kabs", "kel", "k10", "k12", "k21", "logp", "pka", "hematocrit", "hct",
    "fraction unbound", "fup", "fu"
]

def _tokenize(s: str) -> set:
    if not isinstance(s, str): return set()
    s = s.lower().strip()
    return set(re.split(r'[\s_\-\(\)\[\]]+', s))

def compute_hybrid_similarity(cell_text: str, target_variants: list[str]) -> float:
    """
    Computes a hybrid similarity score (Levenshtein + Token Overlap) 
    between the cell_text and any target variant, returning the max score.
    """
    if not cell_text or not isinstance(cell_text, str):
        return 0.0
        
    cell_text = str(cell_text).lower().strip()
    cell_tokens = _tokenize(cell_text)
    
    max_score = 0.0
    for variant in target_variants:
        variant_tokens = _tokenize(variant)
        
        # Exact match fast path
        if cell_text == variant or variant in cell_tokens:
            return 1.0
            
        # 1. Levenshtein ratio (rapidfuzz returns 0-100)
        lev_score = fuzz.ratio(cell_text, variant) / 100.0
        
        # 2. Token overlap (Dice coefficient)
        intersection = len(cell_tokens.intersection(variant_tokens))
        if len(cell_tokens) + len(variant_tokens) > 0:
            tok_score = (2.0 * intersection) / (len(cell_tokens) + len(variant_tokens))
        else:
            tok_score = 0.0
            
        # Hybrid score (we weight Levenshtein higher for short abbreviations like CL, T1/2)
        score = (0.6 * lev_score) + (0.4 * tok_score)
        
        if score > max_score:
            max_score = score
            
    return max_score

def autopk_filter_and_flatten(table: list[list[str]], sim_threshold: float = 0.65) -> str:
    """
    Implements AutoPK Pipeline 2: Table Simplification and KV Flattening.
    Takes a parsed table (list of lists of strings), filters irrelevant rows,
    and returns a Key-Value formatted string.
    """
    if not table or len(table) < 2:
        return ""
        
    # Assume first non-empty row is header
    header = []
    start_idx = 0
    for idx, row in enumerate(table):
        if row and any(c for c in row if c and str(c).strip()):
            header = [str(c).strip().replace("\n", " ") if c else f"Col_{i}" for i, c in enumerate(row)]
            start_idx = idx + 1
            break
            
    if not header:
        return ""
        
    # Ensure all rows pad to header length
    kv_strings = []
    
    for row in table[start_idx:]:
        if not row or all(c is None or str(c).strip() == "" for c in row):
            continue
            
        row = [str(c).strip().replace("\n", " ") if c else "" for c in row]
        # Pad row if smaller than header
        if len(row) < len(header):
            row.extend([""] * (len(header) - len(row)))
            
        # Pipeline 1: Check if this row contains any PK parameter variants
        row_max_score = 0.0
        for cell in row:
            if cell:
                score = compute_hybrid_similarity(cell, TARGET_PK_PARAMS)
                if score > row_max_score:
                    row_max_score = score
                    
        # If it doesn't meet threshold, skip this row (AutoPK Filtering)
        if row_max_score < sim_threshold:
            continue
            
        # Pipeline 2: Flatten to Key-Value pairs
        kv_pairs = []
        for i, val in enumerate(row):
            if val and val not in ["", "-", "NA", "N/A"]:
                col_name = header[i] if i < len(header) else f"Col_{i}"
                kv_pairs.append(f"<{val}@{col_name}>")
                
        if kv_pairs:
            kv_strings.append(" ".join(kv_pairs))
            
    return "\n".join(kv_strings)
