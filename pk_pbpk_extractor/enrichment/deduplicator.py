import pandas as pd
import json

def deduplicate_extracted_parameters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Deduplicate rows based on semantic identity (ontology ID, compound, species, organ_or_tissue).
    When duplicates are found, keeps the one with the highest match_score.
    """
    if df.empty or "parameter_name" not in df.columns:
        return df

    original_columns = list(df.columns)

    def extract_pbpko_id(row):
        try:
            raw = row.get('ontology_mapping', '{}')
            if pd.isna(raw):
                raw = '{}'
            mapping = json.loads(raw)
            if isinstance(mapping, dict):
                return mapping.get('pbpko_id', '')
        except:
            pass
        return ''

    def extract_match_score(row):
        try:
            raw = row.get('ontology_mapping', '{}')
            if pd.isna(raw):
                raw = '{}'
            mapping = json.loads(raw)
            if isinstance(mapping, dict):
                return float(mapping.get('match_score', 0.0))
        except:
            pass
        return 0.0

    df = df.copy()

    # Only use ontology_mapping if it already exists
    has_ontology = 'ontology_mapping' in df.columns

    if has_ontology:
        df['_pbpko_id'] = df.apply(extract_pbpko_id, axis=1)
        df['_match_score'] = df.apply(extract_match_score, axis=1)
    else:
        df['_pbpko_id'] = ''
        df['_match_score'] = 0.0

    df['_norm_param'] = df['parameter_name'].fillna('').str.lower().str.strip()
    
    compound_col = df['compound'].fillna('') if 'compound' in df.columns else ''
    species_col = df['species'].fillna('') if 'species' in df.columns else ''
    organ_col = df['organ_or_tissue'].fillna('') if 'organ_or_tissue' in df.columns else ''

    df['_dedup_key'] = df.apply(
        lambda r: f"{r['_pbpko_id'] or r['_norm_param']}_{compound_col[r.name] if isinstance(compound_col, pd.Series) else ''}_{species_col[r.name] if isinstance(species_col, pd.Series) else ''}_{organ_col[r.name] if isinstance(organ_col, pd.Series) else ''}", 
        axis=1
    )

    df = df.sort_values(by=['_dedup_key', '_match_score'], ascending=[True, False])
    df_dedup = df.drop_duplicates(subset=['_dedup_key'], keep='first').copy()

    # Return ONLY the original columns
    df_dedup = df_dedup[original_columns]
    return df_dedup
