import os
import re
import pypdf
import logging
from .config import RELEVANT_KEYWORDS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_relevant_pages(pdf_path: str) -> str:
    """
    Reads a PBPK PDF paper, scores pages based on relevant keywords, 
    and returns a concatenated text of the top 2 highest-scoring pages.
    This keeps the prompt size small and the execution fast.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF paper not found at: {pdf_path}")
        
    logging.info(f"Opening PDF file: {pdf_path}")
    reader = pypdf.PdfReader(pdf_path)
    num_pages = len(reader.pages)
    logging.info(f"Total pages in document: {num_pages}")
    
    page_scores = []
    
    for page_idx in range(num_pages):
        page = reader.pages[page_idx]
        text = page.extract_text()
        if not text:
            continue
            
        # Score the page based on keyword matches
        score = sum(1 for keyword in RELEVANT_KEYWORDS if re.search(r'(?i)\b' + re.escape(keyword) + r'\b', text))
        page_scores.append((page_idx + 1, score, text))
        
    # Sort pages by score in descending order
    page_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Take the top 2 pages
    top_pages = page_scores[:2]
    # Sort them back by page number
    top_pages.sort(key=lambda x: x[0])
    
    extracted_content = []
    for pnum, score, txt in top_pages:
        logging.info(f"Selected Page {pnum} (match score: {score})")
        extracted_content.append(f"--- START PAGE {pnum} ---\n{txt}\n--- END PAGE {pnum} ---")
            
    return "\n\n".join(extracted_content)
