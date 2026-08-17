import os
import sys
import torch
import fitz  # PyMuPDF
from pathlib import Path
from PIL import Image
from transformers import AutoTokenizer, AutoModel, AutoConfig

def patch_unlimited_ocr_hf_code():
    """
    Scans HuggingFace modules cache for 'baidu/Unlimited-OCR' and patches
    modeling_unlimitedocr.py and modeling_deepseekv2.py for CPU/CUDA compatibility.
    """
    hf_modules_dir = Path.home() / ".cache" / "huggingface" / "modules" / "transformers_modules"
    if not hf_modules_dir.exists():
        return False

    patched_any = False
    for file_path in hf_modules_dir.rglob("modeling_unlimitedocr.py"):
        try:
            content = file_path.read_text(encoding="utf-8")
            modified = False

            if "past_key_values.get_seq_length(" in content and "position_ids[:," not in content:
                old_str = "position_ids = torch.arange(past_key_values.get_seq_length(self.layer_id), past_key_values.get_seq_length(self.layer_id) + seq_length, dtype=torch.long, device=device)"
                new_str = (
                    "seq_len_kv = past_key_values.get_seq_length(self.layer_id)\n"
                    "            if position_ids.dim() == 2 and position_ids.shape[1] > seq_length:\n"
                    "                position_ids = position_ids[:, seq_len_kv : seq_len_kv + seq_length]\n"
                    "            else:\n"
                    "                position_ids = torch.arange(seq_len_kv, seq_len_kv + seq_length, dtype=torch.long, device=device)"
                )
                if old_str in content:
                    content = content.replace(old_str, new_str)
                    modified = True

            if "logits = self.lm_head(hidden_states)" in content and "logits = logits.float()" not in content:
                content = content.replace(
                    "logits = self.lm_head(hidden_states)",
                    "logits = self.lm_head(hidden_states)\n        logits = logits.float()"
                )
                modified = True

            if modified:
                file_path.write_text(content, encoding="utf-8")
                print(f"[Auto-Patch] Successfully updated '{file_path.name}' for CPU/CUDA/Generation compatibility.")
                patched_any = True

        except Exception as e:
            print(f"[Auto-Patch Warning] Could not patch {file_path}: {e}")

    for file_path in hf_modules_dir.rglob("modeling_deepseekv2.py"):
        try:
            content = file_path.read_text(encoding="utf-8")
            if "_prepare_4d_causal_attention_mask" in content:
                content = content.replace(
                    "from transformers.modeling_attn_mask_utils import _prepare_4d_causal_attention_mask",
                    "def _prepare_4d_causal_attention_mask(*args, **kwargs):\n    from transformers.modeling_attn_mask_utils import _prepare_4d_causal_attention_mask as _p4d\n    return _p4d(*args, **kwargs)"
                )
                file_path.write_text(content, encoding="utf-8")
                print(f"[Auto-Patch] Successfully fixed attention mask API bug in '{file_path.name}'.")
                patched_any = True

            if "is_torch_fx_available" in content:
                content = content.replace("is_torch_fx_available", "is_torch_available")
                content = content.replace("from flash_attn.bert_padding import ", "pass # from flash_attn.bert_padding import ")
                file_path.write_text(content, encoding="utf-8")
                print(f"[Auto-Patch] Successfully fixed attention mask API bug in '{file_path.name}'.")
                patched_any = True
        except Exception as e:
            print(f"[Auto-Patch Warning] Could not patch {file_path}: {e}")

    return patched_any

def load_unlimited_ocr_model(model_name: str = "opendatalab/MinerU2.5-Pro-2604-1.2B"):
    """
    Loads either MinerU 2.5 Pro (default) or Baidu Unlimited-OCR model.
    """
    if "mineru" in model_name.lower() or "opendatalab" in model_name.lower():
        from transformers import AutoProcessor, Qwen2VLForConditionalGeneration
        from mineru_vl_utils import MinerUClient

        print(f"Loading MinerU 2.5 Pro model: '{model_name}'...")
        processor = AutoProcessor.from_pretrained(model_name, trust_remote_code=True)
        device_dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
        model = Qwen2VLForConditionalGeneration.from_pretrained(
            model_name,
            dtype=device_dtype,
            device_map="auto" if torch.cuda.is_available() else None,
            trust_remote_code=True
        )

        if not hasattr(model, "lm_head") or getattr(model, "lm_head", None) is None or model.lm_head.weight is None:
            model.lm_head.weight = model.model.embed_tokens.weight

        client = MinerUClient(
            backend="transformers",
            model=model,
            processor=processor,
            image_analysis=False
        )

        print("MinerU 2.5 Pro successfully loaded.")
        return ("mineru", client), processor

    else:
        # Baidu Unlimited-OCR fallback
        import transformers.utils.import_utils as iu
        iu.is_torch_fx_available = lambda: True

        patch_unlimited_ocr_hf_code()

        print(f"Loading config from '{model_name}'...")
        config = AutoConfig.from_pretrained(model_name, trust_remote_code=True)

        force_overrides = {
            '_attn_implementation': 'eager',
            'rope_parameters': {'rope_type': 'default', 'rope_theta': 10000.0, 'factor': 1.0},
        }
        fill_if_missing = {
            'pad_token_id': getattr(config, 'eos_token_id', getattr(config, 'bos_token_id', 0)),
            'attention_bias': False, 'attention_dropout': 0.0, 'hidden_dropout': 0.0,
            'rope_theta': 10000.0, 'rope_scaling': None, 'aux_loss_alpha': 0.001,
            'ep_size': 1, 'moe_layer_freq': 1, 'norm_topk_prob': False,
            'routed_scaling_factor': 1.0, 'scoring_func': 'softmax', 'seq_aux': True,
            'hidden_act': 'silu', 'rms_norm_eps': 1e-6, 'initializer_range': 0.02,
            'pretraining_tp': 1, 'use_cache': True, 'cache_implementation': None,
            'tie_word_embeddings': False, 'use_return_dict': True, 'output_attentions': False,
            'output_hidden_states': False, 'num_labels': 1, 'problem_type': None,
            '_ring_window': None,
        }
        for attr, val in force_overrides.items():
            setattr(config, attr, val)
        for attr, val in fill_if_missing.items():
            if not hasattr(config, attr):
                setattr(config, attr, val)

        print(f"Loading tokenizer from '{model_name}'...")
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True, use_fast=False)

        print(f"Loading model '{model_name}'...")
        device_dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
        model = AutoModel.from_pretrained(
            model_name,
            config=config,
            trust_remote_code=True,
            use_safetensors=True,
            torch_dtype=device_dtype
        )

        if torch.cuda.is_available():
            model = model.eval().cuda()
            print("Model successfully loaded on CUDA GPU.")
        else:
            model = model.eval().to("cpu")

        return ("baidu", model), tokenizer

def pdf_to_images(pdf_path: str, output_folder: str, dpi: int = 200) -> list:
    """
    Converts PDF pages into PNG images using PyMuPDF (fitz).
    """
    import io
    os.makedirs(output_folder, exist_ok=True)
    doc = fitz.open(pdf_path)
    image_paths = []

    MAX_SIZE = 1024

    for page_idx in range(len(doc)):
        page = doc[page_idx]
        pix = page.get_pixmap(dpi=dpi)
        
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        
        if img.width > MAX_SIZE or img.height > MAX_SIZE:
            img.thumbnail((MAX_SIZE, MAX_SIZE), Image.LANCZOS)
            
        img_path = os.path.join(output_folder, f"page_{page_idx + 1:04d}.png")
        img.save(img_path, format="PNG")
        image_paths.append(img_path)

    doc.close()
    return image_paths

def parse_pdf(model_info, tokenizer_or_processor, pdf_path: str, output_dir: str = "./ocr_output", mode: str = "multi", force_mineru: bool = False):
    """
    Parses a single PDF document using PyMuPDF fast-path or MinerU 2.5 Pro / Baidu Unlimited-OCR VLM fallback.
    """
    pdf_path_obj = Path(pdf_path)
    if not pdf_path_obj.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
    pdf_name = pdf_path_obj.stem
    pdf_output_dir = os.path.join(output_dir, pdf_name)
    temp_img_dir = os.path.join(pdf_output_dir, "temp_pages")
    
    print(f"\n==========================================")
    print(f"Processing PDF: {pdf_path}")
    print(f"==========================================")
    
    # 0. Try direct PyMuPDF text extraction (for digital/searchable PDFs)
    doc_check = fitz.open(pdf_path)
    total_text = ""
    page_texts = []
    for p in doc_check:
        txt = p.get_text()
        page_texts.append(txt)
        total_text += txt
    doc_check.close()
    
    if not force_mineru and len(total_text.strip()) > 300 * len(page_texts):
        print(f"[PyMuPDF] Successfully extracted {len(total_text)} characters of text directly from digital PDF.")
        os.makedirs(pdf_output_dir, exist_ok=True)
        final_md_content = "\n\n<PAGE>\n\n".join(page_texts)
        with open(os.path.join(pdf_output_dir, "result.md"), "w", encoding="utf-8") as f:
            f.write(final_md_content)
        print(f"Completed! Output saved to: {os.path.join(pdf_output_dir, 'result.md')}")
        return
        
    # 1. Convert PDF pages to PNGs
    img_paths = pdf_to_images(pdf_path, temp_img_dir)
    print(f"Converted {len(img_paths)} pages to images in '{temp_img_dir}'.")
    
    model_type, model_obj = model_info

    # 2. Run MinerU 2.5 Pro VLM inference
    if model_type == "mineru":
        print("Running MinerU 2.5 Pro 2-step extraction...")
        combined_markdown = []
        for idx, img_path in enumerate(img_paths):
            print(f"Parsing page {idx + 1}/{len(img_paths)} with MinerU 2.5 Pro...")
            image = Image.open(img_path).convert("RGB")
            extracted_blocks = model_obj.two_step_extract(image)
            
            page_blocks = []
            for block in extracted_blocks:
                if isinstance(block, dict):
                    cnt = (block.get('content') or '').strip()
                    if cnt:
                        page_blocks.append(cnt)
            combined_markdown.append("\n\n".join(page_blocks))
            
        os.makedirs(pdf_output_dir, exist_ok=True)
        final_md_content = "\n\n<PAGE>\n\n".join(combined_markdown)
        with open(os.path.join(pdf_output_dir, "result.md"), "w", encoding="utf-8") as f:
            f.write(final_md_content)
        print(f"Completed! MinerU 2.5 Pro output saved to: {os.path.join(pdf_output_dir, 'result.md')}")

    else:
        # Baidu Unlimited-OCR fallback
        tokenizer = tokenizer_or_processor
        model = model_obj
        if mode == "multi":
            img_size = 640 if len(img_paths) > 5 else 1024
            print(f"Running Multi-Page Inference (infer_multi) with image_size={img_size}...")
            model.infer_multi(
                tokenizer=tokenizer,
                prompt='<image>Multi page parsing.',
                image_files=img_paths,
                output_path=pdf_output_dir,
                image_size=img_size,
                max_length=32768,
                no_repeat_ngram_size=35,
                ngram_window=1024,
                save_results=True
            )
        else:
            combined_markdown = []
            for idx, img_path in enumerate(img_paths):
                print(f"Parsing page {idx + 1}/{len(img_paths)}...")
                page_out = os.path.join(pdf_output_dir, f"page_{idx + 1}")
                model.infer(
                    tokenizer=tokenizer,
                    prompt='<image>document parsing.',
                    image_file=img_path,
                    output_path=page_out,
                    base_size=1024,
                    crop_mode=True,
                    max_length=32768,
                    no_repeat_ngram_size=0,
                    ngram_window=0,
                    save_results=True
                )
                page_md_file = os.path.join(page_out, "result.md")
                if os.path.exists(page_md_file):
                    with open(page_md_file, "r", encoding="utf-8") as pf:
                        cleaned_txt = pf.read().replace('Ġ', ' ').replace('Ċ', '\n').strip()
                        combined_markdown.append(cleaned_txt)
                else:
                    combined_markdown.append("")
                    
            final_md_content = "\n\n<PAGE>\n\n".join(combined_markdown)
            with open(os.path.join(pdf_output_dir, "result.md"), "w", encoding="utf-8") as f:
                f.write(final_md_content)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="PDF to Markdown Converter using MinerU 2.5 Pro / Baidu Unlimited-OCR")
    parser.add_argument("--pdf", required=True, help="Path to PDF file or directory of PDFs")
    parser.add_argument("--output-dir", default="./ocr_output", help="Directory to save output files")
    parser.add_argument("--model", default="opendatalab/MinerU2.5-Pro-2604-1.2B", help="Model name (default: opendatalab/MinerU2.5-Pro-2604-1.2B)")
    parser.add_argument("--mode", default="multi", choices=["multi", "single"], help="Inference mode for Baidu model")
    parser.add_argument("--force-mineru", action="store_true", help="Force MinerU OCR even for digital PDFs (to extract images)")
    
    args = parser.parse_args()
    
    model_info, tokenizer_or_processor = load_unlimited_ocr_model(args.model)
    
    pdf_input = Path(args.pdf)
    if pdf_input.is_file():
        parse_pdf(model_info, tokenizer_or_processor, str(pdf_input), args.output_dir, mode=args.mode, force_mineru=args.force_mineru)
    elif pdf_input.is_dir():
        pdf_files = list(pdf_input.glob("*.pdf"))
        print(f"Found {len(pdf_files)} PDF files in '{pdf_input}'.")
        for pdf_file in pdf_files:
            parse_pdf(model_info, tokenizer_or_processor, str(pdf_file), args.output_dir, mode=args.mode, force_mineru=args.force_mineru)
    else:
        print(f"Error: Invalid input path '{args.pdf}'")
        sys.exit(1)

if __name__ == "__main__":
    main()
