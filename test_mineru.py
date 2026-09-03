import os
import sys
import argparse
import torch
import fitz  # PyMuPDF
from PIL import Image
from pathlib import Path
from transformers import AutoProcessor, Qwen2VLForConditionalGeneration
from mineru_vl_utils import MinerUClient

def pdf_to_images(pdf_path: str, output_folder: str, dpi: int = 200) -> list:
    """Converts PDF pages to PNG images using PyMuPDF (fitz)."""
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

def main():
    parser = argparse.ArgumentParser(description="Run MinerU 2.5 Pro OCR on a scientific paper PDF.")
    parser.add_argument("--pdf", default="papers/CPT Pharmacom   Syst Pharma - 2016 - Kuepfer - Applied Concepts in PBPK Modeling  How to Build a PBPK PD Model.pdf", help="Path to input PDF paper")
    parser.add_argument("--output-dir", default="ocr_output", help="Output directory")
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"Error: PDF file '{pdf_path}' not found.")
        sys.exit(1)

    paper_name = pdf_path.stem
    pdf_output_dir = os.path.join(args.output_dir, paper_name)
    temp_img_dir = os.path.join(pdf_output_dir, "mineru_temp_pages")

    print(f"==========================================")
    print(f"Running MinerU 2.5 Pro OCR on: {pdf_path}")
    print(f"==========================================")

    # 1. Convert PDF to images
    img_paths = pdf_to_images(str(pdf_path), temp_img_dir)
    print(f"Converted {len(img_paths)} pages to images in '{temp_img_dir}'.")

    # 2. Load MinerU 2.5 Pro model and processor
    model_id = "opendatalab/MinerU2.5-Pro-2604-1.2B"
    print(f"Loading processor and model from '{model_id}'...")

    processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
    device_dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
    model = Qwen2VLForConditionalGeneration.from_pretrained(
        model_id,
        torch_dtype=device_dtype,
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

    # 3. Perform 2-step layout detection & text recognition on each page
    combined_markdown = []
    for idx, img_path in enumerate(img_paths):
        print(f"\n--- Parsing Page {idx + 1}/{len(img_paths)} with MinerU 2.5 Pro ---")
        image = Image.open(img_path).convert("RGB")
        extracted_blocks = client.two_step_extract(image)
        
        page_blocks = []
        for block in extracted_blocks:
            if isinstance(block, dict):
                content = (block.get('content') or '').strip()
                if content:
                    page_blocks.append(content)
        
        page_text = "\n\n".join(page_blocks)
        combined_markdown.append(page_text)
        print(f"Page {idx + 1} extracted {len(page_blocks)} content blocks.")

    # 4. Save aggregated markdown result
    os.makedirs(pdf_output_dir, exist_ok=True)
    out_md_path = os.path.join(pdf_output_dir, "mineru_result.md")
    final_content = "\n\n<PAGE>\n\n".join(combined_markdown)
    
    with open(out_md_path, "w", encoding="utf-8") as f:
        f.write(final_content)

    print(f"\n==========================================")
    print(f"🎉 MinerU 2.5 Pro OCR complete!")
    print(f"Output saved to: {out_md_path}")
    print(f"Total extracted characters: {len(final_content)}")
    print(f"==========================================")

if __name__ == "__main__":
    main()
