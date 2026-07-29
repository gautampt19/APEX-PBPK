import os
import re
import pypdf
import logging
try:
    from .config import (
        HIGH_PRIORITY_KEYWORDS,
        MEDIUM_PRIORITY_KEYWORDS,
        LOW_PRIORITY_KEYWORDS,
        PK_UNITS_PATTERNS,
        MAX_EXTRACTED_PAGES,
        ENABLE_OCR_FALLBACK,
        FORCE_OCR,
        OCR_MODEL_NAME
    )
except ImportError:
    from config import (
        HIGH_PRIORITY_KEYWORDS,
        MEDIUM_PRIORITY_KEYWORDS,
        LOW_PRIORITY_KEYWORDS,
        PK_UNITS_PATTERNS,
        MAX_EXTRACTED_PAGES,
        ENABLE_OCR_FALLBACK,
        FORCE_OCR,
        OCR_MODEL_NAME
    )


# Global lazy-loaded OCR model & tokenizer
_OCR_TOKENIZER = None
_OCR_MODEL = None

def _patch_unlimited_ocr_config(config):
    """
    Patch missing attributes in UnlimitedOCRConfig that the underlying DeepSeekV2 /
    UnlimitedOCR architecture code accesses directly on the config object during __init__.
    Sourced by grepping all `config.<attr>` usages in modeling_deepseekv2.py and
    modeling_unlimitedocr.py against the keys present in config.json.
    """
    defaults = {
        # Token IDs
        'pad_token_id': getattr(config, 'eos_token_id', getattr(config, 'bos_token_id', 0)),
        # Attention implementation — needed by DeepseekV2DecoderLayer to pick
        # between 'mha_eager' (use_mla=False) and 'mla_eager' (use_mla=True)
        '_attn_implementation': 'eager',
        # Attention
        'attention_bias': False,
        'attention_dropout': 0.0,
        'hidden_dropout': 0.0,
        # Rope — keep None: the code guards with `if config.rope_scaling is not None`
        'rope_theta': 10000.0,
        'rope_scaling': None,
        # MoE / routing
        'aux_loss_alpha': 0.001,
        'ep_size': 1,
        'moe_layer_freq': 1,
        'norm_topk_prob': False,
        'routed_scaling_factor': 1.0,
        'scoring_func': 'softmax',
        'seq_aux': True,
        # Hidden act
        'hidden_act': 'silu',
        # Norm
        'rms_norm_eps': 1e-6,
        # Init
        'initializer_range': 0.02,
        'pretraining_tp': 1,
        # Cache / generation
        'use_cache': True,
        'cache_implementation': None,
        'tie_word_embeddings': False,
        # Misc model flags
        'use_return_dict': True,
        'output_attentions': False,
        'output_hidden_states': False,
        'num_labels': 1,
        'problem_type': None,
        # Sliding window (UnlimitedOCR specific)
        '_ring_window': None,
    }
    for attr, val in defaults.items():
        if not hasattr(config, attr):
            setattr(config, attr, val)

    # _attn_implementation is pre-set by transformers to None — force override
    if getattr(config, '_attn_implementation', None) is None:
        config._attn_implementation = 'eager'

    return config




def load_unlimited_ocr_model(model_name: str = OCR_MODEL_NAME):

    """
    Lazy loader for Baidu Unlimited-OCR model using HuggingFace AutoModelForCausalLM.
    """
    global _OCR_TOKENIZER, _OCR_MODEL
    if _OCR_MODEL is None:
        logging.info(f"Loading Baidu Unlimited-OCR model '{model_name}'...")
        try:
            import transformers.utils.import_utils as import_utils
            if not hasattr(import_utils, 'is_torch_fx_available'):
                import_utils.is_torch_fx_available = lambda: True

            from transformers import AutoConfig, AutoModel, AutoTokenizer
            import torch

            device = "cuda" if torch.cuda.is_available() else "cpu"
            config = AutoConfig.from_pretrained(model_name, trust_remote_code=True)
            _patch_unlimited_ocr_config(config)

            _OCR_TOKENIZER = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
            _OCR_MODEL = AutoModel.from_pretrained(
                model_name,
                config=config,
                trust_remote_code=True,
                torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32
            ).to(device).eval()
            logging.info(f"Baidu Unlimited-OCR model successfully loaded on {device}.")



        except Exception as e:
            logging.warning(f"Could not load '{model_name}': {e}. OCR fallback will use basic text extraction.")
            return None, None
    return _OCR_TOKENIZER, _OCR_MODEL

def ocr_extract_page(pdf_path: str, page_num: int) -> str:
    """
    Converts a PDF page to an image and parses it into text using Baidu Unlimited-OCR.
    Uses the model's built-in .infer(tokenizer, prompt, image_file) API.
    """
    import tempfile, os
    try:
        from pdf2image import convert_from_path
        images = convert_from_path(pdf_path, first_page=page_num, last_page=page_num, dpi=150)
        if not images:
            return ""
        page_img = images[0]

        tokenizer, model = load_unlimited_ocr_model()
        if tokenizer is None or model is None:
            return ""

        # Save to a temp file — model.infer() takes a file path, not a PIL image
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name
            page_img.save(tmp_path, format="PNG")

        try:
            # Official API from modeling_unlimitedocr.py:
            # model.infer(tokenizer, prompt='<image>\nFree OCR.', image_file='path')
            ocr_text = model.infer(
                tokenizer,
                prompt='<image>\nFree OCR.',
                image_file=tmp_path,
                output_path=tempfile.gettempdir(),
                max_length=4096,
                temperature=0.0,
            )
            logging.info(f"Page {page_num} successfully parsed via Baidu Unlimited-OCR.")
            return ocr_text if isinstance(ocr_text, str) else str(ocr_text)
        finally:
            os.unlink(tmp_path)

    except Exception as e:
        logging.warning(f"OCR processing failed for page {page_num}: {e}")
    return ""






logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_page_score(text: str, page_num: int, total_pages: int) -> float:
    """
    Calculates a weighted score for a page based on:
    1. High, Medium, Low priority keywords (e.g. Table I, Vmax, Km vs generic 'compartment').
    2. PK unit patterns (e.g. mg/kg, L/h, umol/L).
    3. Numerical density (counts of numeric/tabular values).
    4. First-page/Abstract penalty if lacking tables or numerical data.
    """
    if not text:
        return 0.0

    score = 0.0

    # 1. High priority keywords (+5.0 each)
    for kw in HIGH_PRIORITY_KEYWORDS:
        if re.search(r'(?i)\b' + re.escape(kw) + r'\b', text):
            score += 5.0

    # 2. Medium priority keywords (+2.0 each)
    for kw in MEDIUM_PRIORITY_KEYWORDS:
        if re.search(r'(?i)\b' + re.escape(kw) + r'\b', text):
            score += 2.0

    # 3. Low priority keywords (+0.5 each)
    for kw in LOW_PRIORITY_KEYWORDS:
        if re.search(r'(?i)\b' + re.escape(kw) + r'\b', text):
            score += 0.5

    # 4. PK Unit patterns (+3.0 each)
    for pattern in PK_UNITS_PATTERNS:
        matches = len(re.findall(r'(?i)' + pattern, text))
        score += matches * 3.0

    # 5. Numerical density check (numbers, decimal values)
    numbers = re.findall(r'\b\d+\.?\d*\b', text)
    num_count = len(numbers)
    if num_count > 15:
        score += 5.0
    if num_count > 30:
        score += 5.0

    # 6. Penalize Page 1 / Abstract if it lacks parameter tables or PK units
    if page_num == 1:
        has_table = any(re.search(r'(?i)table\s+[0-9i]+', text) for _ in [0])
        has_units = any(re.search(r'(?i)' + pattern, text) for pattern in PK_UNITS_PATTERNS)
        if not (has_table or has_units):
            score -= 10.0  # Apply penalty to prevent abstract page false positives

    return max(0.0, score)

def extract_relevant_pages(pdf_path: str, force_ocr: bool = False) -> str:
    """
    Reads a PBPK PDF paper, scores pages using weighted keyword and numerical density analysis,
    and returns concatenated text of the highest-scoring pages.
    Supports force_ocr mode to run Baidu Unlimited-OCR on all pages.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF paper not found at: {pdf_path}")
        
    logging.info(f"Opening PDF file: {pdf_path}")
    reader = pypdf.PdfReader(pdf_path)
    num_pages = len(reader.pages)
    logging.info(f"Total pages in document: {num_pages}")
    
    # If the document is small (<= MAX_EXTRACTED_PAGES) and not forcing OCR, extract all pages directly
    if num_pages <= MAX_EXTRACTED_PAGES and not (force_ocr or FORCE_OCR):
        logging.info(f"Document has {num_pages} pages (<= {MAX_EXTRACTED_PAGES}). Extracting all pages.")
        extracted = []
        for idx in range(num_pages):
            txt = reader.pages[idx].extract_text() or ""
            extracted.append(f"--- START PAGE {idx + 1} ---\n{txt}\n--- END PAGE {idx + 1} ---")
        return "\n\n".join(extracted)

    page_scores = []
    for page_idx in range(num_pages):
        page_num = page_idx + 1
        page = reader.pages[page_idx]
        text = page.extract_text() or ""
        
        # Trigger OCR if force_ocr is set, or if text layer is empty (<50 chars) and fallback is enabled
        if force_ocr or FORCE_OCR or (len(text.strip()) < 50 and ENABLE_OCR_FALLBACK):
            reason = "Force OCR requested" if (force_ocr or FORCE_OCR) else f"Minimal text layer ({len(text.strip())} chars)"
            logging.info(f"Page {page_num}: {reason}. Running Baidu Unlimited-OCR extraction...")
            ocr_text = ocr_extract_page(pdf_path, page_num)
            if ocr_text:
                text = ocr_text

        if not text.strip():
            continue

            
        score = calculate_page_score(text, page_num, num_pages)
        page_scores.append((page_num, score, text))

        
    # Sort pages by score in descending order
    page_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Select top MAX_EXTRACTED_PAGES
    top_pages = page_scores[:MAX_EXTRACTED_PAGES]
    
    # Sort back by page number order
    top_pages.sort(key=lambda x: x[0])
    
    extracted_content = []
    for pnum, score, txt in top_pages:
        logging.info(f"Selected Page {pnum} (weighted score: {score:.1f})")
        extracted_content.append(f"--- START PAGE {pnum} ---\n{txt}\n--- END PAGE {pnum} ---")
            
    return "\n\n".join(extracted_content)

