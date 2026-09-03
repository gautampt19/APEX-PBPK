"""
pk_pbpk_extractor/enrichment/__init__.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
PBPK-specific compound parameter enrichment using Scientific Agent Skills
(PubChem, ChEMBL, DrugBank, UniProt).
"""
from .pbpk_compound_enricher import enrich_pbpk_properties, resolve_compound_name
