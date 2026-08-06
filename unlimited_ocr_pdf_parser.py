import os
import sys
import argparse
import importlib
from pathlib import Path
import fitz  # PyMuPDF
import torch
from transformers import AutoModel, AutoTokenizer

# Disable Flash SDPA to avoid CUDA device-side asserts on certain PyTorch versions
if hasattr(torch.backends.cuda, "enable_flash_sdp"):
    torch.backends.cuda.enable_flash_sdp(False)
    torch.backends.cuda.enable_mem_efficient_sdp(False)

def patch_unlimited_ocr_hf_code():
    """
    Patches Baidu's custom model file (modeling_unlimitedocr.py) in the Hugging Face cache
    to replace hardcoded `.cuda()` and `autocast('cuda')` calls with dynamic CPU/CUDA fallback.
    """
    hf_cache_dir = Path.home() / ".cache" / "huggingface" / "modules" / "transformers_modules"
    if not hf_cache_dir.exists():
        return False
    
    ocr_files = list(hf_cache_dir.glob("**/modeling_unlimitedocr.py"))
    patched_any = False
    
    for file_path in ocr_files:
        try:
            content = file_path.read_text(encoding="utf-8")
            modified = False
            
            # Replace hardcoded .cuda() calls
            if ".cuda()" in content:
                content = content.replace(".cuda()", ".to('cuda' if torch.cuda.is_available() else 'cpu')")
                modified = True
                
            # Replace hardcoded autocast("cuda"
            if 'torch.autocast("cuda"' in content:
                content = content.replace(
                    'torch.autocast("cuda"', 
                    'torch.autocast("cuda" if torch.cuda.is_available() else "cpu"'
                )
                modified = True
            elif "torch.autocast('cuda'" in content:
                content = content.replace(
                    "torch.autocast('cuda'", 
                    "torch.autocast('cuda' if torch.cuda.is_available() else 'cpu'"
                )
                modified = True
                
            # Fix position_ids shape mismatch during generation decoding
            buggy_pos_code = 'position_ids = kwargs.get("position_ids", None)'
            fixed_pos_code = '''position_ids = kwargs.get("position_ids", None)
        if past_key_values is not None and position_ids is not None:
            if position_ids.shape[-1] > input_ids.shape[1]:
                position_ids = position_ids[:, -input_ids.shape[1]:]'''
            if buggy_pos_code in content and fixed_pos_code not in content:
                content = content.replace(buggy_pos_code, fixed_pos_code)
                modified = True
                
            if modified:
                file_path.write_text(content, encoding="utf-8")
                print(f"[Auto-Patch] Successfully updated '{file_path.name}' for CPU/CUDA/Generation compatibility.")
                patched_any = True
        except Exception as e:
            print(f"[Auto-Patch Warning] Could not patch {file_path}: {e}")

    # -- Patch modeling_unlimitedocr.py to remove flash_attn requirement --
    modeling_files = list(hf_cache_dir.glob("**/modeling_unlimitedocr.py"))
    for file_path in modeling_files:
        try:
            content = file_path.read_text(encoding="utf-8")
            
            # Disable Flash Attention 2 (causes CUDA asserts)
            if "if is_flash_attn_2_available():" in content:
                content = content.replace("if is_flash_attn_2_available():", "if False:")
                # Also comment out the imports so transformers AST checker doesn't enforce it
                content = content.replace("from flash_attn import ", "pass # from flash_attn import ")
                content = content.replace("from flash_attn.bert_padding import ", "pass # from flash_attn.bert_padding import ")
                file_path.write_text(content, encoding="utf-8")
                print(f"[Auto-Patch] Successfully updated '{file_path.name}' for CPU/CUDA compatibility.")
                patched_any = True
        except Exception as e:
            print(f"[Auto-Patch Warning] Could not patch {file_path}: {e}")
            
    # -- Patch deepencoder.py to fix position_ids corruption bug --
    deepencoder_files = list(hf_cache_dir.glob("**/deepencoder.py"))
    for file_path in deepencoder_files:
        try:
            content = file_path.read_text(encoding="utf-8")
            
            buggy_line = "embeddings = embeddings + get_abs_pos(self.position_embedding(self.position_ids), embeddings.size(1))"
            fixed_line = (
                "actual_pos_ids = torch.arange(self.position_embedding.weight.size(0), device=embeddings.device).unsqueeze(0)\n"
                "        embeddings = embeddings + get_abs_pos(self.position_embedding(actual_pos_ids), embeddings.size(1))"
            )
            
            if buggy_line in content:
                content = content.replace(buggy_line, fixed_line)
                file_path.write_text(content, encoding="utf-8")
                print(f"[Auto-Patch] Successfully fixed position_ids bug in '{file_path.name}'.")
                patched_any = True
        except Exception as e:
            print(f"[Auto-Patch Warning] Could not patch {file_path}: {e}")

    # -- Patch modeling_deepseekv2.py to fix transformers >= 4.43 mask API bug and import errors --
    deepseek_files = list(hf_cache_dir.glob("**/modeling_deepseekv2.py"))
    for file_path in deepseek_files:
        try:
            content = file_path.read_text(encoding="utf-8")
            if "is_torch_fx_available" in content:
                content = content.replace("is_torch_fx_available", "is_torch_available")
                modified = True
            
            buggy_mask_block = """            attention_mask = _prepare_4d_causal_attention_mask(
                attention_mask,
                (batch_size, seq_length),
                inputs_embeds,
                past_key_values_length,
            )"""
            
            fixed_mask_block = """            try:
                attention_mask = _prepare_4d_causal_attention_mask(
                    attention_mask,
                    (batch_size, seq_length),
                    inputs_embeds,
                    past_key_values_length,
                )
            except RuntimeError:
                # Fallback for transformers >= 4.43 where the old API is broken during generation
                target_length = past_key_values_length + seq_length
                if attention_mask is not None and attention_mask.dim() == 2:
                    if attention_mask.size(1) < target_length:
                        padding = torch.ones((attention_mask.size(0), target_length - attention_mask.size(1)), device=attention_mask.device, dtype=attention_mask.dtype)
                        attention_mask = torch.cat([attention_mask, padding], dim=1)
                    elif attention_mask.size(1) > target_length:
                        attention_mask = attention_mask[:, :target_length]
                    expanded_mask = attention_mask[:, None, None, :].expand(batch_size, 1, seq_length, target_length).to(inputs_embeds.dtype)
                    attention_mask = expanded_mask.masked_fill(expanded_mask == 0, torch.finfo(inputs_embeds.dtype).min)
                    attention_mask = attention_mask.masked_fill(expanded_mask == 1, 0.0)
                else:
                    attention_mask = None"""
            
            if buggy_mask_block in content:
                content = content.replace(buggy_mask_block, fixed_mask_block)
                
            # Disable flash_attn import AST check
            if "from flash_attn import " in content:
                content = content.replace("from flash_attn import ", "pass # from flash_attn import ")
                content = content.replace("from flash_attn.bert_padding import ", "pass # from flash_attn.bert_padding import ")
                
            file_path.write_text(content, encoding="utf-8")
            print(f"[Auto-Patch] Successfully fixed attention mask API bug in '{file_path.name}'.")
            patched_any = True
        except Exception as e:
            print(f"[Auto-Patch Warning] Could not patch {file_path}: {e}")

    return patched_any

def load_unlimited_ocr_model(model_name: str = "baidu/Unlimited-OCR"):
    """
    Loads the Baidu Unlimited-OCR tokenizer and model with trust_remote_code=True.
    Applies automatic CPU fallback patching if CUDA GPU is not present.
    """
    import transformers.utils.import_utils as iu
    iu.is_torch_fx_available = lambda: True
    from transformers import AutoConfig

    # 1. Patch pre-downloaded cache files if present
    patch_unlimited_ocr_hf_code()

    print(f"Loading config from '{model_name}'...")
    config = AutoConfig.from_pretrained(model_name, trust_remote_code=True)

    # ── Patch all missing / None attributes ─────────────────────────────────
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
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        trust_remote_code=True,
        use_fast=False
    )

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
        print("NOTE: Running on CPU mode with automatic device compatibility patch applied.")

    return model, tokenizer

def pdf_to_images(pdf_path: str, output_folder: str, dpi: int = 200) -> list:
    """
    Converts PDF pages into PNG images using PyMuPDF (fitz).
    Caps image dimensions to 1024x1024 to avoid CUDA out-of-bounds errors in the CLIP encoder.
    """
    from PIL import Image
    import io
    os.makedirs(output_folder, exist_ok=True)
    doc = fitz.open(pdf_path)
    image_paths = []

    MAX_SIZE = 1024

    for page_idx in range(len(doc)):
        page = doc[page_idx]
        pix = page.get_pixmap(dpi=dpi)
        
        # Convert to PIL Image for resizing
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        
        if img.width > MAX_SIZE or img.height > MAX_SIZE:
            img.thumbnail((MAX_SIZE, MAX_SIZE), Image.LANCZOS)
            
        img_path = os.path.join(output_folder, f"page_{page_idx + 1:04d}.png")
        img.save(img_path, format="PNG")
        image_paths.append(img_path)

    doc.close()
    return image_paths

def parse_pdf(model, tokenizer, pdf_path: str, output_dir: str = "./ocr_output", mode: str = "multi"):
    """
    Parses a single PDF document using Baidu Unlimited-OCR.
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
    doc = fitz.open(pdf_path)
    extracted_pages = []
    for i, page in enumerate(doc):
        t = page.get_text()
        if t.strip():
            extracted_pages.append(t.strip())
    doc.close()
    
    # If we extracted significant text from most pages, use this clean text
    if len(extracted_pages) == len(pdf_path_obj.name) and sum(len(p) for p in extracted_pages) > 200 * len(extracted_pages):
        pass # fallback check
    
    # Check if fitz got good text
    doc_check = fitz.open(pdf_path)
    total_text = ""
    page_texts = []
    for p in doc_check:
        txt = p.get_text()
        page_texts.append(txt)
        total_text += txt
    doc_check.close()
    
    if len(total_text.strip()) > 300 * len(page_texts):
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
    
    # 2. Run Baidu Unlimited-OCR inference
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
        print("Running Single-Page High-Precision Inference (Gundam mode)...")
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
            
    print(f"Completed! Output files saved to: {pdf_output_dir}")

def main():
    parser = argparse.ArgumentParser(description="Parse PDF documents using Baidu Unlimited-OCR")
    parser.add_argument("--pdf", type=str, help="Path to a single PDF file to parse")
    parser.add_argument("--dir", type=str, help="Directory containing PDF files to parse batch-wise")
    parser.add_argument("--output", type=str, default="./ocr_output", help="Directory to save OCR outputs")
    parser.add_argument("--mode", type=str, choices=["multi", "single"], default="single", help="Inference mode ('multi' for multi-page document, 'single' for page-by-page)")
    
    args = parser.parse_args()
    
    model, tokenizer = load_unlimited_ocr_model()
    
    if args.pdf:
        parse_pdf(model, tokenizer, args.pdf, args.output, args.mode)
    elif args.dir:
        pdf_files = [os.path.join(args.dir, f) for f in os.listdir(args.dir) if f.lower().endswith(".pdf")]
        print(f"Found {len(pdf_files)} PDF files in directory '{args.dir}'.")
        for pdf_file in pdf_files:
            parse_pdf(model, tokenizer, pdf_file, args.output, args.mode)
    else:
        current_dir_pdfs = [f for f in os.listdir(".") if f.lower().endswith(".pdf")]
        if current_dir_pdfs:
            print(f"Found {len(current_dir_pdfs)} PDF files in current directory.")
            for pdf_file in current_dir_pdfs:
                parse_pdf(model, tokenizer, pdf_file, args.output, args.mode)
        else:
            print("No PDF files specified or found in current directory. Use --pdf <file.pdf> or --dir <directory>.")

if __name__ == "__main__":
    main()
