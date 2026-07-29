#!/usr/bin/env python3
"""
Standalone test for baidu/Unlimited-OCR following the approach from the model's own code.
Usage:
    .venv/bin/python test_ocr.py papers/s12249-023-02680-y.pdf 7
"""
import sys
import traceback
import tempfile
import os
import logging

logging.basicConfig(level=logging.WARNING)  # suppress INFO noise

MODEL_NAME = "baidu/Unlimited-OCR"


def load_model():
    """Load model and tokenizer with all required config patches."""
    import transformers.utils.import_utils as iu
    iu.is_torch_fx_available = lambda: True

    from transformers import AutoConfig, AutoModel, AutoTokenizer
    import torch

    print(f"[1/3] Loading config from '{MODEL_NAME}' ...")
    config = AutoConfig.from_pretrained(MODEL_NAME, trust_remote_code=True)

    # ── Patch all missing / None attributes ─────────────────────────────────
    # _attn_implementation is set by transformers to None by default.
    # We must override None values (not just missing attributes) for key ones.
    force_overrides = {
        '_attn_implementation': 'eager',          # needed by mha/mla dispatch
    }
    fill_if_missing = {
        'pad_token_id':        getattr(config, 'eos_token_id', getattr(config, 'bos_token_id', 0)),
        'attention_bias':      False,
        'attention_dropout':   0.0,
        'hidden_dropout':      0.0,
        'rope_theta':          10000.0,
        'rope_scaling':        None,               # guarded by `if config.rope_scaling is not None`
        'aux_loss_alpha':      0.001,
        'ep_size':             1,
        'moe_layer_freq':      1,
        'norm_topk_prob':      False,
        'routed_scaling_factor': 1.0,
        'scoring_func':        'softmax',
        'seq_aux':             True,
        'hidden_act':          'silu',
        'rms_norm_eps':        1e-6,
        'initializer_range':   0.02,
        'pretraining_tp':      1,
        'use_cache':           True,
        'cache_implementation': None,
        'tie_word_embeddings': False,
        'use_return_dict':     True,
        'output_attentions':   False,
        'output_hidden_states': False,
        'num_labels':          1,
        'problem_type':        None,
        '_ring_window':        None,
    }

    for attr, val in force_overrides.items():
        old = getattr(config, attr, '<missing>')
        setattr(config, attr, val)
        print(f"    config.{attr}: {old!r} -> {val!r}")

    for attr, val in fill_if_missing.items():
        if not hasattr(config, attr):
            setattr(config, attr, val)
            print(f"    config.{attr} = {val!r}  (was missing)")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[2/3] Loading tokenizer on {device} ...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    print("      Tokenizer OK:", type(tokenizer).__name__)

    print(f"[3/3] Loading model ...")
    model = AutoModel.from_pretrained(
        MODEL_NAME,
        config=config,
        trust_remote_code=True,
        torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
    ).to(device).eval()
    print("      Model OK:", type(model).__name__, f"  device={device}")
    return tokenizer, model


def ocr_page(pdf_path: str, page_num: int, tokenizer, model) -> str:
    """Run OCR on a single PDF page using model.infer() -- the official API."""
    from pdf2image import convert_from_path

    print(f"\n[OCR] Rendering page {page_num} of '{pdf_path}' at 150 dpi ...")
    images = convert_from_path(pdf_path, first_page=page_num, last_page=page_num, dpi=150)
    if not images:
        print("      ERROR: no images rendered")
        return ""

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = tmp.name
        images[0].save(tmp_path, format="PNG")
    print(f"      Saved to {tmp_path}")

    try:
        print("[OCR] Running model.infer() ...")
        # Official API from modeling_unlimitedocr.py:
        #   model.infer(tokenizer, prompt, image_file, output_path, ...)
        result = model.infer(
            tokenizer,
            prompt='<image>\nFree OCR.',
            image_file=tmp_path,
            output_path=tempfile.gettempdir(),
            max_length=4096,
            temperature=0.0,
        )
        print("[OCR] Done!\n")
        return result if isinstance(result, str) else str(result)
    finally:
        os.unlink(tmp_path)


if __name__ == "__main__":
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else "papers/s12249-023-02680-y.pdf"
    page_num = int(sys.argv[2]) if len(sys.argv) > 2 else 7

    print("=" * 60)
    print(f" baidu/Unlimited-OCR standalone test")
    print(f" PDF:  {pdf_path}")
    print(f" Page: {page_num}")
    print("=" * 60)

    try:
        tokenizer, model = load_model()
        text = ocr_page(pdf_path, page_num, tokenizer, model)
        print("-" * 60)
        print("EXTRACTED TEXT:")
        print("-" * 60)
        print(text)
        print("-" * 60)
        # Save result
        out_path = f"test_ocr_page{page_num}.txt"
        with open(out_path, "w") as f:
            f.write(text)
        print(f"\n[+] Text saved to: {out_path}")
    except Exception:
        print("\n[!] FAILED with traceback:")
        traceback.print_exc()
        sys.exit(1)
