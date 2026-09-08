"""
ingestion/pdf_mineru.py — PDF text and table extraction.

Strategy:
  1. Try PyMuPDF (fitz) or pypdf for raw text extraction.
  2. Use pdfplumber for structured table extraction (AutoPK methodology).
"""

import os
import json

def run_mineru(pdf_path: str, output_dir: str):
    """
    Extract text and structured tables from a PDF.
    """
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    md_cache = os.path.join(output_dir, f"{base_name}.md")
    tables_cache = os.path.join(output_dir, f"{base_name}_tables.json")

    # Load text
    md_content = ""
    if os.path.exists(md_cache):
        with open(md_cache, "r", encoding="utf-8") as f:
            md_content = f.read()
    else:
        md_content = _extract_with_pymupdf(pdf_path)
        if not md_content:
            md_content = _extract_with_pypdf(pdf_path)
        with open(md_cache, "w", encoding="utf-8") as f:
            f.write(md_content)

    # Extract tables via pdfplumber
    tables = []
    if os.path.exists(tables_cache):
        with open(tables_cache, "r", encoding="utf-8") as f:
            tables = json.load(f)
    else:
        tables = _extract_tables_with_pdfplumber(pdf_path)
        with open(tables_cache, "w", encoding="utf-8") as f:
            json.dump(tables, f)

    layout_data = {"structured_tables": tables}
    return md_content, layout_data

def _extract_tables_with_pdfplumber(pdf_path: str):
    tables_data = []
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                page_tables = page.extract_tables(table_settings={"vertical_strategy": "text", "horizontal_strategy": "text"})
                for t_idx, table in enumerate(page_tables):
                    if table and len(table) > 1:
                        tables_data.append({
                            "page": page_num + 1,
                            "table_index": t_idx + 1,
                            "data": table
                        })
        print(f"  [MinerU/pdfplumber] Extracted {len(tables_data)} structured tables.")
    except Exception as e:
        print(f"  [MinerU/pdfplumber] Failed to extract tables: {e}")
    return tables_data

def _extract_with_pymupdf(pdf_path: str) -> str:
    try:
        import fitz
        doc = fitz.open(pdf_path)
        pages_text = []
        for page_num, page in enumerate(doc):
            text = page.get_text("text").strip()
            if text:
                pages_text.append(f"\n\n<!-- Page {page_num + 1} -->\n\n{text}")
        return "\n".join(pages_text)
    except:
        return ""

def _extract_with_pypdf(pdf_path: str) -> str:
    try:
        import pypdf
        with open(pdf_path, "rb") as f:
            reader = pypdf.PdfReader(f)
            pages_text = []
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                if text.strip():
                    pages_text.append(f"\n\n<!-- Page {page_num + 1} -->\n\n{text.strip()}")
            return "\n".join(pages_text)
    except:
        return ""
