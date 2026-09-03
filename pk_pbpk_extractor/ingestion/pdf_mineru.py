"""
ingestion/pdf_mineru.py — PDF text extraction without MinerU dependency.

Strategy:
  1. Try PyMuPDF (fitz) — fast, accurate for digital PDFs, also renders page images.
  2. Fallback to pypdf — pure-python text extraction.
  
Returns (md_content: str, layout_data: dict)
  md_content  — extracted text as a markdown-ish string
  layout_data — empty dict (maintained for API compatibility with ColPali pipeline)
"""

import os
import json


def run_mineru(pdf_path: str, output_dir: str):
    """
    Extract text from a PDF using PyMuPDF or pypdf.
    No MinerU / magic-pdf CLI dependency required.
    """
    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    md_cache = os.path.join(output_dir, f"{base_name}.md")

    # Return cached result if it exists
    if os.path.exists(md_cache):
        print(f"  [MinerU] Using cached text: {md_cache}")
        with open(md_cache, "r", encoding="utf-8") as f:
            return f.read(), {}

    md_content = _extract_with_pymupdf(pdf_path)
    if not md_content:
        print("  [MinerU] PyMuPDF produced no text. Trying pypdf fallback...")
        md_content = _extract_with_pypdf(pdf_path)

    if not md_content:
        raise RuntimeError(f"Could not extract any text from PDF: {pdf_path}")

    # Cache the result
    with open(md_cache, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"  [MinerU] Text cached to: {md_cache}")

    return md_content, {}


def _extract_with_pymupdf(pdf_path: str) -> str:
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf_path)
        pages_text = []
        for page_num, page in enumerate(doc):
            text = page.get_text("text").strip()
            if text:
                pages_text.append(f"\n\n<!-- Page {page_num + 1} -->\n\n{text}")
        result = "\n".join(pages_text)
        print(f"  [MinerU] PyMuPDF extracted {len(doc)} pages ({len(result)} chars).")
        return result
    except Exception as e:
        print(f"  [MinerU] PyMuPDF failed: {e}")
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
            result = "\n".join(pages_text)
            print(f"  [MinerU] pypdf extracted {len(reader.pages)} pages ({len(result)} chars).")
            return result
    except Exception as e:
        print(f"  [MinerU] pypdf failed: {e}")
        return ""
