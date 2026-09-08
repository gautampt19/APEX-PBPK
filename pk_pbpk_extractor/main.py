"""
main.py — CLI orchestrator for the 100% local PK/PBPK extractor.

Routing chain (auto-detected from PDF when only --pdf is given):
  1. PMC Open Access XML  (DOI + Title parallel search) → lossless JATS XML
  2. Unpaywall free PDF   (DOI lookup)                  → OCR via PyMuPDF + ColPali
  3. Semantic Scholar PDF (DOI / Title)                 → OCR via PyMuPDF + ColPali
  4. Local PDF (provided via --pdf)                     → OCR via PyMuPDF + ColPali
"""

import argparse
import os
import json
import math
import ollama

from .ingestion.xml_parser import parse_xml_tables
from .ingestion.pdf_mineru import run_mineru
from .ingestion.colpali_retriever import retrieve_top_k_pages
from .ingestion.pmc_fetcher import (
    resolve_paper,
    extract_doi_from_pdf,
    extract_title_from_pdf,
    fetch_supplementary_pdfs
)
import sys, importlib.util as _ilu, os as _os
_cm_path = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.dirname(__file__))), "clean_markdown.py")
if _os.path.exists(_cm_path):
    _spec = _ilu.spec_from_file_location("clean_markdown", _cm_path)
    _cm_mod = _ilu.module_from_spec(_spec); _spec.loader.exec_module(_cm_mod)
    clean_markdown_fn = _cm_mod.clean_markdown
    chunk_text_fn     = _cm_mod.chunk_text
else:
    clean_markdown_fn = lambda x, **kw: x
    chunk_text_fn     = lambda x, chunk_size=8000, **kw: [x]
from .inference.vllm_worker import OllamaWorker
from .storage.db_handler import setup_database, upsert_document, insert_pk_parameters, delete_paper_data
from .normalization.unit_normalizer import normalize_unit
from .normalization.entity_linker import link_pk_entity
from .normalization.harmonizer import harmonize
from .enrichment.pbpk_compound_enricher import enrich_pbpk_properties, resolve_compound_name
from .enrichment.deduplicator import deduplicate_extracted_parameters
from .templates.template_loader import build_prompt
from .schemas.pbpk_schema import ExtractedTablePayload


# ─────────────────────────────────────────────────────────────
# XML fast-path extraction
# ─────────────────────────────────────────────────────────────

def _extract_xml_table_text_only(client, model, json_schema, table: dict, paper_id: str) -> dict:
    rows_as_text = "\n".join([" | ".join(cell for cell in row) for row in table["rows"]])
    caption = table.get("caption", "")
    footer  = table.get("footer", "")

    table_text = (
        f"Caption: {caption}\n"
        f"Table Footer: {footer}\n\n"
        f"{rows_as_text}"
    )
    prompt = build_prompt(
        "pharmacometrics_table",
        paper_id=paper_id,
        table_id=table["table_id"],
        table_text=table_text,
    )

    print(f"  [XML Fast-Path] Extracting {table['table_id']} via {model}...")
    response = client.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        format=json_schema,
        options={"temperature": 0.0, "num_predict": 16384, "num_ctx": 32768},
    )

    result_text = response["message"]["content"]
    try:
        validated = ExtractedTablePayload.model_validate_json(result_text)
        payload = validated.model_dump()
        payload["table_id"] = table["table_id"]
        return payload
    except Exception as e:
        print(f"  [XML Fast-Path] Validation warning: {e}")
        raw = json.loads(result_text)
        raw["table_id"] = table["table_id"]
        return raw


def process_xml(xml_path: str, worker: OllamaWorker, paper_id: str = None):
    print(f"\n[XML Fast-Path] Parsing {xml_path}...")
    tables = parse_xml_tables(xml_path)
    if not paper_id:
        paper_id = os.path.splitext(os.path.basename(xml_path))[0]

    delete_paper_data(paper_id)
    upsert_document(paper_id, f"Parsed from {paper_id}", {"source": "xml"})
    print(f"  Found {len(tables)} tables in the XML.")

    for table in tables:
        payload = _extract_xml_table_text_only(
            worker.client, worker.model, worker.json_schema, table, paper_id
        )
        _save_payload(payload, paper_id, source_pass="xml_table")


# ─────────────────────────────────────────────────────────────
# PDF OCR path
# ─────────────────────────────────────────────────────────────


def process_md_text_pass(md_raw: str, worker: OllamaWorker, paper_id: str, output_dir: str):
    """
    Text-only extraction pass: clean the full markdown with clean_markdown.py,
    chunk it into 8k-char segments, and run Qwen on each chunk to extract PK
    parameters from the text representation (no image needed).
    """
    print(f"\n[MD Text Pass] Cleaning and chunking markdown ({len(md_raw):,} chars)...")

    # Save cleaned .md alongside other pipeline outputs
    cleaned = clean_markdown_fn(md_raw)
    cleaned_path = os.path.join(output_dir, f"{os.path.basename(output_dir)}_{paper_id.replace('/', '_')}_cleaned.md")
    try:
        with open(cleaned_path, "w", encoding="utf-8") as f:
            f.write(cleaned)
        print(f"  Cleaned .md saved: {cleaned_path}")
    except Exception:
        pass

    # Split into chunks (8k chars each with overlap)
    chunks = chunk_text_fn(cleaned, chunk_size=8000, overlap_words=15)
    print(f"  Processing {len(chunks)} text chunk(s) via Qwen...")

    for idx, chunk in enumerate(chunks):
        prompt = (
            "You are a Senior Pharmacometrics Data Extractor.\n"
            "The following is a section of a scientific paper on pharmacokinetics (PK) "
            "and physiologically based pharmacokinetic (PBPK) modelling.\n"
            "Extract ALL numerical PK/PBPK parameters mentioned (values, units, species, etc.).\n"
            "Include organ volumes, blood flow fractions, partition coefficients, clearance, "
            "absorption rates, Cmax, AUC, t1/2, Vd — everything numerical.\n"
            "Return ONLY valid JSON matching the schema.\n\n"
            f"=== PAPER TEXT (chunk {idx + 1}/{len(chunks)}) ===\n"
            f"{chunk}"
        )

        print(f"  [MD Chunk {idx + 1}/{len(chunks)}] Sending to {worker.model} (text-only)...")
        try:
            response = worker.client.chat(
                model=worker.model,
                messages=[{"role": "user", "content": prompt}],
                format=worker.json_schema,
                options={"temperature": 0.0, "num_predict": 16384, "num_ctx": 32768},
            )
            result_text = response["message"]["content"]
            try:
                validated = ExtractedTablePayload.model_validate_json(result_text)
                payload = validated.model_dump()
            except Exception:
                import json as _json
                payload = _json.loads(result_text)

            payload["table_id"] = f"MD_Chunk_{idx + 1}"
            _save_payload(payload, paper_id, source_pass="xml_table")
        except Exception as e:
            print(f"  [MD Chunk {idx + 1}] Error: {e}")


def _split_md_by_page(md_content: str) -> dict:
    """
    Splits the PyMuPDF-extracted markdown into per-page sections.
    Pages are delimited by <!-- Page N --> markers inserted by pdf_mineru.py.
    Returns dict {page_number (0-indexed): text_content}.
    """
    import re
    pages = {}
    parts = re.split(r"<!--\s*Page\s+(\d+)\s*-->", md_content)
    # parts = [pre_text, page_num, content, page_num, content, ...]
    for j in range(1, len(parts) - 1, 2):
        page_num = int(parts[j]) - 1   # convert 1-indexed marker to 0-indexed
        pages[page_num] = parts[j + 1].strip()
    return pages


def process_pdf(pdf_path: str, worker: OllamaWorker, paper_id: str = None):
    print(f"\n[PDF OCR Path] Processing {pdf_path}...")
    output_dir = "/tmp/mineru_output"
    os.makedirs(output_dir, exist_ok=True)

    md_content, layout_data = run_mineru(pdf_path, output_dir)

    if not paper_id:
        paper_id = os.path.splitext(os.path.basename(pdf_path))[0]

    delete_paper_data(paper_id)
    upsert_document(paper_id, f"Parsed from {paper_id}", {"source": "pdf"})

    # ── Pass 1: Text-only extraction from full cleaned markdown ──────────
    process_md_text_pass(md_content, worker, paper_id, output_dir)

    # ── Pass 1.5: AutoPK Structured Table Pass ─────────────────────────────
    structured_tables = layout_data.get("structured_tables", [])
    if structured_tables:
        try:
            from pk_pbpk_extractor.inference.autopk_filter import autopk_filter_and_flatten
            from pk_pbpk_extractor.schemas.pbpk_schema import ExtractedTablePayload
            import json
            
            print(f"\n[AutoPK Table Pass] Processing {len(structured_tables)} extracted tables...")
            for table_data in structured_tables:
                table_idx = table_data.get("table_index", 1)
                raw_table = table_data.get("data", [])
                
                kv_flattened_text = autopk_filter_and_flatten(raw_table, sim_threshold=0.60)
                if not kv_flattened_text:
                    continue
                    
                print(f"  [AutoPK] Filtered Table {table_idx} to key-value format (len={len(kv_flattened_text)})")
                
                prompt = (
                    "You are a Senior Pharmacometrics Data Extractor.\n"
                    "The following are highly condensed Key-Value formatted rows extracted from a PK table.\n"
                    "Extract ALL parameters and map them precisely. The format is <Value@ColumnHeader>.\n"
                    "Return ONLY valid JSON matching the schema.\n\n"
                    f"Paper: {paper_id} | Table: {table_idx}\n"
                    "=== CONDENSED TABLE ===\n"
                    f"{kv_flattened_text}\n"
                    "=======================\n"
                )
                
                response = worker.client.chat(
                    model=worker.model,
                    messages=[{"role": "user", "content": prompt}],
                    format=worker.json_schema,
                    options={"temperature": 0.0}
                )
                
                try:
                    res_dict = ExtractedTablePayload.model_validate_json(response["message"]["content"]).model_dump()
                    _save_payload(res_dict, paper_id, source_pass="autopk_table")
                except Exception as e:
                    print(f"  [AutoPK] Extraction warning: {e}")
        except Exception as e:
            print(f"  [AutoPK] Error during AutoPK pass: {e}")


    # ── Pass 2: Multimodal image extraction via ColPali ───────────────────
    # Split the full markdown into per-page sections for targeted context
    md_pages = _split_md_by_page(md_content)
    print(f"  Parsed {len(md_pages)} page text sections from markdown.")

    queries = [
        "Table of physiological parameters organ volumes blood flow fractions",
        "Pharmacokinetic parameters clearance partition coefficients Kp Vmax Km",
    ]

    print("  Retrieving top-K pages via ColPali...")
    top_k_images, indices = retrieve_top_k_pages(pdf_path, queries, top_k=5)
    print(f"  Selected pages: {indices}")

    for i, img in enumerate(top_k_images):
        page_idx = indices[i]

        # Use the page-specific markdown section (± 1 neighbouring page for context)
        page_text_parts = []
        for offset in [-1, 0, 1]:
            pt = md_pages.get(page_idx + offset, "")
            if pt:
                page_text_parts.append(pt)
        page_context = "\n\n".join(page_text_parts)[:4000]  # cap at 4k chars

        if page_context.strip():
            print(f"  [Page {page_idx}] Using {len(page_context)} chars of page-specific markdown.")
        else:
            # Fallback: first 3000 chars of the full document
            page_context = md_content[:3000]
            print(f"  [Page {page_idx}] No page-specific text found, using document header.")

        print(f"\n  [Page {page_idx}] Running multimodal extraction...")
        payload = worker.extract_table_data(
            img, page_context, {},
            paper_id=paper_id,
            table_id=f"Page_{page_idx}"
        )
        _save_payload(payload, paper_id, source_pass="colpali_page")

    # ── Pass 3: Prose text scan ──────────────────────────────────────────
    print("\n  [Pass 3] Scanning prose paragraphs for inline PK values...")
    _prose_scan_pass(md_content, worker, paper_id)

    # ── Pass 4: PBPK Compound Skill Enrichment (PubChem, ChEMBL, DrugBank) ──
    _compound_enrichment_pass(paper_id, paper_title=paper_id, text_context=md_content)


# ─────────────────────────────────────────────────────────────
# Pass 3: Prose text scan (inline parameter extraction)
# ─────────────────────────────────────────────────────────────

def _prose_scan_pass(md_content: str, worker, paper_id: str):
    """
    Scans the full markdown text in chunks for PK parameters mentioned
    inline in prose paragraphs (e.g. 'clearance was 12 L/h').
    Only chunks that mention numeric values near PK keywords are processed.
    """
    import re as _re
    # Simple heuristic: only scan chunks that likely contain a PK value
    _PK_HINT = _re.compile(
        r"\b(CL|Vd|Vmax|Km|fu|fup|ka|Kp|AUC|Cmax|t1/2|half.life|"
        r"clearance|volume|bioavailability|partition|unbound|hematocrit|"
        r"absorption|elimination|distribution)\b",
        _re.IGNORECASE
    )
    _NUM_HINT = _re.compile(r"\d+\.?\d*\s*(L|mL|h|min|mg|kg|nmol|uM|nM|ng|%)")

    chunk_size = 1500
    overlap = 200
    text = md_content
    chunks = []
    i = 0
    while i < len(text):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
        i += chunk_size - overlap

    schema = worker.json_schema
    client = worker.client
    model = worker.model

    total_saved = 0
    for idx, chunk in enumerate(chunks):
        # Skip chunks that don't look like they contain PK parameter prose
        if not _PK_HINT.search(chunk):
            continue
        if not _NUM_HINT.search(chunk):
            continue

        chunk_id = f"prose_chunk_{idx}"
        prompt = build_prompt(
            "pharmacometrics_text",
            paper_id=paper_id,
            chunk_id=chunk_id,
            text_chunk=chunk,
        )
        print(f"    [Prose] Scanning {chunk_id} ({len(chunk)} chars)...")

        try:
            response = client.chat(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                format=schema,
                options={"temperature": 0.0, "num_predict": 4096, "num_ctx": 8192},
            )
            result_text = response["message"]["content"]

            from .schemas.pbpk_schema import ExtractedTablePayload
            import json
            try:
                validated = ExtractedTablePayload.model_validate_json(result_text)
                payload = validated.model_dump()
            except Exception:
                payload = json.loads(result_text)

            payload["table_id"] = chunk_id
            n_params = len(payload.get("biochemical_parameters", []))
            if n_params > 0:
                _save_payload(payload, paper_id, source_pass="prose_pass")
                total_saved += n_params
                print(f"    [Prose] ✓ Found {n_params} parameters in {chunk_id}")

        except Exception as e:
            print(f"    [Prose] ⚠ Skipped {chunk_id}: {e}")
            continue

    print(f"\n  [Pass 3] Prose scan complete. {total_saved} parameters saved.")


# ─────────────────────────────────────────────────────────────
# Pass 4: PBPK Compound Skill Enrichment (PubChem, ChEMBL, DrugBank)
# ─────────────────────────────────────────────────────────────

def _compound_enrichment_pass(paper_id: str, paper_title: str = "", text_context: str = "", explicit_compound: str = None):
    """
    Enriches PBPK modeling parameters (MW, LogP, TPSA, HBD, HBA, fup) using
    scientific agent skills (PubChem, ChEMBL, DrugBank).
    """
    compound = explicit_compound or resolve_compound_name(paper_title, text_context)
    if not compound:
        print("  [Pass 4] No target compound identified for skill enrichment.")
        return

    records, meta = enrich_pbpk_properties(compound, paper_id=paper_id)
    if records:
        insert_pk_parameters(records)
        print(f"  [Pass 4] Enriched & saved {len(records)} fundamental PBPK properties for '{compound}'.")
    if meta.get("pubchem_cid") or meta.get("chembl_id"):
        upsert_document(paper_id, f"Parsed from {paper_id}", {
            "source": "pdf",
            "compound_enrichment": meta
        })

# ─────────────────────────────────────────────────────────────
# DB save helper
# ─────────────────────────────────────────────────────────────

def _save_payload(payload: dict, paper_id: str, source_pass: str = "xml_table"):
    params_to_insert = []
    
    # Extract global context if available
    ctx = payload.get("table_context", {})
    global_compound = ctx.get("compound")
    global_species = ctx.get("species")
    global_route = ctx.get("route")
    global_dose_val = ctx.get("dose_value")
    global_dose_unit = ctx.get("dose_unit")
    global_formulation = ctx.get("formulation")
    
    records = payload.get("records", [])
    if not records:
        print("  [DB] No records found in payload to save.")
        return
        
    for rec in records:
        # Fallback to global table context if specific record lacks it
        compound = rec.get("compound") or global_compound
        species = rec.get("species") or global_species
        route = rec.get("route") or global_route
        dose = rec.get("dose_value")
        if dose is None:
            dose = global_dose_val
        dose_unit = rec.get("dose_unit") or global_dose_unit
        formulation = rec.get("formulation") or global_formulation
        
        # Prepare row for DB
        row = {
            "paper_id": paper_id,
            "table_id": payload.get("table_id", "Unknown"),
            "record_id": rec.get("record_id"),
            "source_row_index": rec.get("source_row_index"),
            "source_column_index": rec.get("source_column_index"),
            "source_row_label": rec.get("source_row_label"),
            "source_column_header": rec.get("source_column_header"),
            
            "parameter_raw": rec.get("parameter_raw"),
            "parameter_normalized": rec.get("parameter_normalized"),
            "parameter_category": rec.get("parameter_category"),
            "is_target_parameter": rec.get("is_target_parameter", False),
            "organ_or_tissue": rec.get("organ_or_tissue"),
            
            "compound": compound,
            "species": species,
            "sex": rec.get("sex"),
            "route": route,
            "dose_value": dose,
            "dose_unit": dose_unit,
            "dose_raw": rec.get("dose_raw") or ctx.get("dose_raw"),
            "formulation": formulation,
            
            "cohort_or_condition": rec.get("cohort_or_condition"),
            "replicate_or_subject": rec.get("replicate_or_subject"),
            "value_index": rec.get("value_index", 1),
            
            "value": rec.get("value"),
            "unit": rec.get("unit"),
            "qualifier": rec.get("qualifier"),
            
            "deviation_value": rec.get("deviation_value"),
            "deviation_unit": rec.get("deviation_unit"),
            "deviation_type": rec.get("deviation_type"),
            
            "interval_lower": rec.get("interval_lower"),
            "interval_upper": rec.get("interval_upper"),
            "interval_unit": rec.get("interval_unit"),
            "interval_type": rec.get("interval_type"),
            
            "raw_value": rec.get("raw_value"),
            "notes": rec.get("notes"),
            "source_pass": source_pass
        }
        params_to_insert.append(row)

    if params_to_insert:
        # Scrub None/NaN safety
        import math
        def _scrub_nan(obj):
            if isinstance(obj, float) and math.isnan(obj):
                return None
            if isinstance(obj, dict):
                return {k: _scrub_nan(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [_scrub_nan(v) for v in obj]
            return obj
            
        params_to_insert = [_scrub_nan(r) for r in params_to_insert]
        insert_pk_parameters(params_to_insert)
        print(f"  Saved {len(params_to_insert)} parameter records to the database.")

    print("\n  ── Extracted Parameters ──────────────────────────")
    for row in params_to_insert:
        # Display logic for terminal
        val_str = f"{row['value']:.4f}" if row.get('value') is not None else f"[{row.get('interval_lower')} - {row.get('interval_upper')}]"
        name = row.get('parameter_raw') or "Unknown Parameter"
        unit = row.get('unit') or ""
        print(f"    {name:30s} = {val_str} {unit}")


def main():
    parser = argparse.ArgumentParser(
        description="Auto-Routing PK/PBPK Extractor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Let the system find the paper automatically from the PDF
  python3 -m pk_pbpk_extractor.main --pdf papers/mypaper.pdf

  # Force a specific DOI search
  python3 -m pk_pbpk_extractor.main --doi 10.1208/s12249-023-02680-y --pdf papers/mypaper.pdf

  # Use a pre-downloaded local XML directly
  python3 -m pk_pbpk_extractor.main --pmc-xml papers/PMC1234567.xml
        """
    )
    parser.add_argument("--doi",     type=str, help="DOI of the paper")
    parser.add_argument("--pmcid",   type=str, help="PMCID of the paper")
    parser.add_argument("--title",   type=str, help="Paper title to search for")
    parser.add_argument("--pdf",     type=str, help="Path to a local PDF file")
    parser.add_argument("--pmc-xml", type=str, help="Path to a local PMC-OA XML file (skips all API calls)")
    parser.add_argument("--compound", type=str, help="Target compound name for PBPK skill enrichment (PubChem/ChEMBL)")
    args = parser.parse_args()

    print("Setting up database...")
    setup_database()
    worker = OllamaWorker()

    # ── 0. Explicit local XML ───────────────────────────────────
    if args.pmc_xml:
        process_xml(args.pmc_xml, worker)
        return

    # ── 1. Auto-detect DOI + Title from PDF ────────────────────
    auto_doi   = None
    auto_title = None

    if args.pdf and not args.doi and not args.pmcid and not args.title:
        print(f"\n[Auto-Routing] Scanning PDF for DOI and Title...")
        auto_doi   = extract_doi_from_pdf(args.pdf)
        auto_title = extract_title_from_pdf(args.pdf)

        if auto_doi:
            print(f"  Found DOI   : {auto_doi}")
        else:
            print(f"  No DOI found in PDF text.")

        if auto_title:
            print(f"  Found Title : {auto_title[:80]}")
        else:
            print(f"  No Title found in PDF metadata.")

    active_doi   = args.doi   or auto_doi
    active_pmcid = args.pmcid
    active_title = args.title or auto_title
    paper_id     = active_doi or active_pmcid or active_title or (
        os.path.splitext(os.path.basename(args.pdf))[0] if args.pdf else "unknown"
    )

    # ── 2. Try all free API sources ─────────────────────────────
    if active_doi or active_pmcid or active_title:
        print(f"\n[Auto-Routing] Querying free sources for: {paper_id[:60]}...")
        resolved = resolve_paper(doi=active_doi, title=active_title, pmcid=active_pmcid)

        if resolved["xml_path"]:
            print(f"\n[Auto-Routing] ✓ Got XML via {resolved['source']}. Using fast-path.")
            process_xml(resolved["xml_path"], worker, paper_id=paper_id)
            
            # Extract pmcid and fetch supplementary files
            pmcid = resolved["xml_path"].split("/")[-1].split(".")[0]
            print(f"\n[PMC Scraper] Searching for supplementary files for {pmcid}...")
            supp_pdfs = fetch_supplementary_pdfs(pmcid)
            for supp_pdf in supp_pdfs:
                print(f"\n[Auto-Routing] Processing supplementary file: {supp_pdf}")
                process_pdf(supp_pdf, worker, paper_id=paper_id)
            return

        if resolved["pdf_path"]:
            print(f"\n[Auto-Routing] ✓ Got PDF via {resolved['source']}. Using OCR path.")
            process_pdf(resolved["pdf_path"], worker, paper_id=paper_id)
            return

    # ── 3. Fallback: local PDF ──────────────────────────────────
    if args.pdf:
        print(f"\n[Fallback] No free source found. Using local PDF OCR for {args.pdf}")
        process_pdf(args.pdf, worker, paper_id=paper_id)
    else:
        print("\n[Error] No input provided and no API source found. Use --pdf or --doi.")
        parser.print_help()


if __name__ == "__main__":
    main()
