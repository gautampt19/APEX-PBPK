import torch
from transformers import AutoModel, AutoTokenizer
from PIL import Image

from unlimited_ocr_pdf_parser import load_unlimited_ocr_model

model, tokenizer = load_unlimited_ocr_model("baidu/Unlimited-OCR")

img_path = "./ocr_output/s12249-023-02680-y/temp_pages/page_0002.png"

prompts = [
    "<image>document parsing.",
    "<image>\nformat text: ",
    "<image>\nFree OCR. ",
    "<image>\n<|grounding|>Given the layout of the image. ",
    "<image>\nExtract the text in the image. "
]

for p in prompts:
    print(f"=== Testing prompt: {repr(p)} ===")
    try:
        res = model.infer(
            tokenizer=tokenizer,
            prompt=p,
            image_file=img_path,
            output_path="./test_out",
            base_size=1024,
            crop_mode=False,
            max_length=4096,
            save_results=False,
            eval_mode=True
        )
        # clean BPE spaces if needed
        clean_res = res.replace('Ġ', ' ').replace('Ċ', '\n') if res else res
        print("Result (first 300 chars):")
        print(clean_res[:300] if clean_res else "None/Empty")
    except Exception as e:
        print("Error:", e)
    print("\n" + "="*40 + "\n")
