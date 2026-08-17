import logging
"""
extract_pbpk_params.py — Extract PBPK parameters AND generate a faithful
deSolve R model from a scientific paper in a single LLM session.

Two inference calls share one loaded model to avoid reload overhead:
  Call 1: Paper text + images → structured JSON (parameters)
  Call 2: Paper text + images + params JSON → complete R/deSolve script

Supports two inference backends:
  • vllm  (default) — GPU-accelerated
  • ollama           — fallback for smaller setups
"""

import os
import json
import argparse
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


# ── Pydantic Schema for Parameter Extraction ─────────────────────────────────

class PBPKParameters(BaseModel):
    blood_flow_fraction: Dict[str, float] = Field(
        description="Dictionary mapping organ names (e.g., 'Liver', 'Brain', 'Kidney') to their blood flow as a fraction of cardiac output."
    )
    volume_fraction: Dict[str, float] = Field(
        description="Dictionary mapping organ names to their volume as a fraction of body weight."
    )
    biochemical_parameters: Dict[str, Any] = Field(
        description="Dictionary containing all other biochemical parameters like Gastric Emptying (GE), Absorption rate (Kabs), Partition Coefficients (e.g., 'Liver:plasma'), Vmax, Km, Clearance (Cl), Fraction unbound (fu), etc."
    )
    equations: Dict[str, str] = Field(
        description="Any important mathematical equations identified for the PBPK model, such as metabolism or allometric scaling."
    )


EXPECTED_SCHEMA = json.dumps(PBPKParameters.model_json_schema(), indent=2)

PARAM_EXTRACTION_SYSTEM_PROMPT = (
    "You are an expert pharmacometrician. Your task is to extract PBPK "
    "(Physiologically Based Pharmacokinetic) parameters from the OCR text of "
    "a scientific paper. Extract organ blood flow fractions, organ volume "
    "fractions, tissue:plasma partition coefficients, and any biochemical "
    "parameters (clearance, Vmax, Km, absorption rates, etc.).\n\n"
    "CRITICAL: You must aggressively hunt for and extract:\n"
    "- Hematocrit (HCT) or Blood:Plasma ratios.\n"
    "- Free fraction (fu) and whether the paper uses it explicitly in tissue distribution gradients.\n"
    "- Any parameters for METABOLITES (e.g., fu_M1, CL_M1, Kp_M1) if a metabolite is modeled.\n"
    "Also extract any relevant kinetic equations mentioned.\n\n"
    "You MUST respond with ONLY valid JSON matching this EXACT schema "
    "(no wrapper keys, no extra nesting):\n"
    f"{EXPECTED_SCHEMA}"
)

R_GENERATION_SYSTEM_PROMPT = """\
You are an expert pharmacometrician and R programmer. Your task is to generate
a COMPLETE, RUNNABLE R script that faithfully implements the PBPK (and PD if
applicable) model described in a scientific paper.

## CRITICAL RULES — you MUST follow ALL of these to exactly replicate the paper:

1. **FAITHFUL REPRODUCTION**: Implement the EXACT model structure from the
   paper. Do NOT simplify, substitute, or omit any model components.
   - If the paper explicitly lists a compartment (e.g., "Muscle"), you MUST create a distinct ODE for it. Do NOT lump it into "Rest of Body" unless the paper explicitly does so.
   - If the paper models a Metabolite (e.g., M1), you MUST include a full parallel set of ODEs for the metabolite's distribution and elimination.
   - If the paper includes a PD model (e.g., bacterial killing, tumor growth), include it with all ODEs and parameters.

2. **DISTRIBUTION MECHANICS & FREE FRACTION**:
   - Pay strict attention to how the paper drives tissue distribution. If the paper equations multiply the concentration gradient by the free fraction (e.g., `Q * (C_plasma * fu - C_tissue * fu / Kp)`), you MUST implement that exact math. Do not default to total concentration gradients unless the paper does.

3. **BLOOD VS PLASMA FLOW**:
   - Differentiate between blood flow and plasma flow. If the paper uses total cardiac output as blood flow, and calculates organ flows based on plasma (using Hematocrit: `QCplasma = QCblood * (1 - HCT)`), you MUST implement this conversion.

4. **UNIT CONSISTENCY**: Convert ALL parameters to a single consistent unit
   system before plugging them into the ODEs. State your chosen unit system
   in a comment at the top. Show each conversion step in comments.

5. **PORTAL CIRCULATION**: Route intestinal/splanchnic blood flow through the
   portal vein into the liver. Do NOT mix gut venous return directly into systemic blood.

6. **COMPLETE ELIMINATION**: Include ALL elimination routes (hepatic, renal via kurine, biliary, fecal). Use the exact clearance forms specified (e.g., `k_urine * C_plasma`).

7. **R CODE REQUIREMENTS**:
   - Use `library(deSolve)` and the `ode()` solver.
   - Define all parameters in a named vector or list.
   - Define the ODE function with signature: function(t, state, parms)
   - Define initial conditions as a named vector.
   - Run the simulation with `ode()` and save results to 'dynamic_simulation_results.csv'.

8. **OUTPUT**: Respond with ONLY the R code. No explanatory text. Do NOT wrap in markdown code fences.

## EXTRACTED PARAMETERS (for reference — use these numerical values):
{params_json}
"""


def _build_extraction_prompt(md_content: str) -> str:
    return (
        f"Read the following OCR text from a scientific paper and extract "
        f"the PBPK parameters.\n\nPaper text:\n\n{md_content}"
    )


def _build_r_generation_prompt(md_content: str, params_json: str) -> str:
    # For very long papers, truncate to key sections to leave room for output
    # Max ~10000 words for the R generation call
    words = md_content.split()
    if len(words) > 10000:
        md_content = " ".join(words[:10000]) + "\n\n[... truncated for length ...]"

    return (
        f"Read the following scientific paper and generate a complete R/deSolve "
        f"script that faithfully implements the PBPK/PD model described in it. "
        f"Use the extracted parameter values provided in the system prompt.\n\n"
        f"Paper text:\n\n{md_content}"
    )


# ── JSON Schema Normalisation ────────────────────────────────────────────────

REQUIRED_KEYS = {"blood_flow_fraction", "volume_fraction", "biochemical_parameters", "equations"}

def _flatten_to_schema(data: dict) -> dict:
    """Unwrap nested JSON structures into the expected flat schema."""
    if REQUIRED_KEYS.issubset(data.keys()):
        return data

    for key, value in data.items():
        if isinstance(value, dict) and REQUIRED_KEYS.issubset(value.keys()):
            return value

    for key, value in data.items():
        if isinstance(value, dict):
            for k2, v2 in value.items():
                if isinstance(v2, dict) and REQUIRED_KEYS.issubset(v2.keys()):
                    return v2

    return data


def _extract_r_code(response_text: str) -> str:
    """Extract R code from LLM response, handling markdown fences."""
    text = response_text.strip()
    extracted = text
    if "```r" in text.lower():
        # Find ```r or ```R block
        for marker in ("```r\n", "```R\n", "```r\r\n", "```R\r\n"):
            if marker in text:
                extracted = text.split(marker, 1)[1]
                if "```" in extracted:
                    extracted = extracted.rsplit("```", 1)[0]
                break
        else:
            import re
            match = re.search(r'```[rR]\s*\n(.*?)```', text, re.DOTALL)
            if match:
                extracted = match.group(1)
    elif "```" in text:
        parts = text.split("```")
        if len(parts) >= 3:
            extracted = parts[1]

    extracted = extracted.strip()
    extracted = extracted.replace("  }})\n}", "  })\n}")
    extracted = extracted.replace("}})\n}", "})\n}")
    extracted = extracted.replace("  }})", "  })")
    extracted = extracted.replace("}})", "})")

    return extracted



# ── vLLM backend ─────────────────────────────────────────────────────────────

def _load_vllm(model_name: str, tensor_parallel_size: int = 1):
    """Load the vLLM model once and return (llm, SamplingParams_class)."""
    import sys
    venv_bin = os.path.join(os.path.dirname(sys.executable))
    if venv_bin not in os.environ.get("PATH", ""):
        os.environ["PATH"] = venv_bin + os.pathsep + os.environ.get("PATH", "")

    from vllm import LLM, SamplingParams
    import torch

    num_gpus = torch.cuda.device_count()
    if tensor_parallel_size > num_gpus:
        print(f"  [Notice] Requested TP={tensor_parallel_size}, "
              f"but only {num_gpus} GPU(s). Using {max(1, num_gpus)}.")
        tensor_parallel_size = max(1, num_gpus)

    print(f"  Loading model '{model_name}' with vLLM "
          f"(Tensor Parallelism: {tensor_parallel_size}) …")
    llm = LLM(
        model=model_name,
        trust_remote_code=True,
        max_model_len=32768,
        gpu_memory_utilization=0.85,
        tensor_parallel_size=tensor_parallel_size,
    )
    return llm, SamplingParams


def _build_multimodal_content(text: str, image_paths: list = None):
    """Build user content with optional images for multimodal models."""
    if not image_paths:
        return text

    from PIL import Image
    pil_images = []
    for p in image_paths:
        if os.path.exists(p):
            try:
                pil_images.append(Image.open(p).convert("RGB"))
            except Exception as e:
                print(f"  [Notice] Could not load image {p}: {e}")

    if not pil_images:
        return text

    print(f"  [Multimodal] Attaching {len(pil_images[:5])} figure/page images …")
    content = [{"type": "text", "text": text}]
    for img in pil_images[:5]:
        content.append({"type": "image_pil", "image_pil": img})
    return content


def _vllm_chat(llm, SamplingParams, system_prompt: str, user_content,
               max_tokens: int = 4096, temperature: float = 0.0) -> str:
    """Run a single chat completion on the already-loaded vLLM model."""
    sampling = SamplingParams(temperature=temperature, max_tokens=max_tokens)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": user_content},
    ]
    outputs = llm.chat(messages=[messages], sampling_params=sampling, use_tqdm=True)
    return outputs[0].outputs[0].text.strip()


def extract_and_generate_vllm(
    md_content: str,
    model_extract: str,
    model_generate: str,
    tensor_parallel_size: int = 1,
    image_paths: list = None,
    step: str = "all",
    input_json_str: str = None,
    dump_prompts_dir: str = None,
) -> tuple:
    """
    Single vLLM session: extract parameters (JSON) + generate R code.
    Returns (params_dict, r_code_string).
    """
    if model_extract != model_generate and step == "all" and not dump_prompts_dir:
        raise NotImplementedError("vLLM backend does not support different models for extraction and generation in a single session without reloading. Please use Ollama for multi-model workflows, or provide the same model.")

    if not dump_prompts_dir:
        model_to_load = model_extract if step in ["extract", "all"] else model_generate
        llm, SamplingParams = _load_vllm(model_to_load, tensor_parallel_size)
    else:
        os.makedirs(dump_prompts_dir, exist_ok=True)

    params_dict = None
    r_code = None
    params_json_str = input_json_str

    if step in ["extract", "all"]:
        # ── Call 1: Parameter Extraction ──────────────────────────────────────
        print("\n  ── Call 1/2: Extracting PBPK parameters (JSON) ──")
        user_content_1 = _build_multimodal_content(
            _build_extraction_prompt(md_content), image_paths)

        if dump_prompts_dir:
            dump_path = os.path.join(dump_prompts_dir, "vllm_call1_prompt.json")
            # Convert PIL images to placeholders for JSON dumping
            safe_content = []
            if isinstance(user_content_1, list):
                for item in user_content_1:
                    if isinstance(item, dict) and item.get("type") == "image_pil":
                        safe_content.append({"type": "image_pil", "image_pil": "<PIL.Image object>"})
                    else:
                        safe_content.append(item)
            else:
                safe_content = user_content_1
            with open(dump_path, "w") as f:
                json.dump({"system": PARAM_EXTRACTION_SYSTEM_PROMPT, "user": safe_content}, f, indent=2)
            print(f"  ✅ Prompt dumped to {dump_path}")
            return None, None

        response_1 = _vllm_chat(
            llm, SamplingParams,
            system_prompt=PARAM_EXTRACTION_SYSTEM_PROMPT,
            user_content=user_content_1,
            max_tokens=4096,
        )

        # Parse JSON
        json_text = response_1
        if "```json" in json_text:
            json_text = json_text.split("```json")[1].split("```")[0].strip()
        elif "```" in json_text:
            json_text = json_text.split("```")[1].split("```")[0].strip()

        parsed = json.loads(json_text)
        params_dict = _flatten_to_schema(parsed)

        # Validate
        validated = PBPKParameters(**params_dict)
        params_dict = validated.model_dump()
        params_json_str = json.dumps(params_dict, indent=2)
        print("  ✅ Parameter extraction complete.")

    # ── Call 2: R Code Generation ─────────────────────────────────────────
    if step in ["generate", "all"]:
        if not params_json_str and not dump_prompts_dir:
            raise ValueError("Missing parameters JSON for R code generation.")
        print("\n  ── Call 2/2: Generating faithful R/deSolve model ──")
        # If dumping prompts and we don't have json, use a placeholder
        safe_params_json = params_json_str if params_json_str else '{"placeholder": "Run step 1 to generate JSON"}'
        r_system = R_GENERATION_SYSTEM_PROMPT.format(params_json=safe_params_json)
        user_content_2 = _build_multimodal_content(
            _build_r_generation_prompt(md_content, safe_params_json), image_paths)

        if dump_prompts_dir:
            dump_path = os.path.join(dump_prompts_dir, "vllm_call2_prompt.json")
            safe_content = []
            if isinstance(user_content_2, list):
                for item in user_content_2:
                    if isinstance(item, dict) and item.get("type") == "image_pil":
                        safe_content.append({"type": "image_pil", "image_pil": "<PIL.Image object>"})
                    else:
                        safe_content.append(item)
            else:
                safe_content = user_content_2
            with open(dump_path, "w") as f:
                json.dump({"system": r_system, "user": safe_content}, f, indent=2)
            print(f"  ✅ Prompt dumped to {dump_path}")
            return None, None
    
        response_2 = _vllm_chat(
            llm, SamplingParams,
            system_prompt=r_system,
            user_content=user_content_2,
            max_tokens=8192,   # R scripts can be long
            temperature=0.0,
        )
    
        r_code = _extract_r_code(response_2)
        print("  ✅ R code generation complete.")

    return params_dict, r_code


# ── Ollama backend (fallback) ────────────────────────────────────────────────

def extract_and_generate_ollama(
    md_content: str, 
    model_extract: str, 
    model_generate: str, 
    image_paths: list = None,
    step: str = "all",
    input_json_str: str = None,
    dump_prompts_dir: str = None,
) -> tuple:
    """Ollama backend: two sequential calls with multimodal support."""
    import ollama
    import base64

    if dump_prompts_dir:
        os.makedirs(dump_prompts_dir, exist_ok=True)

    # Helper to load images for Ollama
    images_b64 = []
    if image_paths:
        for p in image_paths[:5]:
            if os.path.exists(p):
                try:
                    with open(p, "rb") as f:
                        images_b64.append(base64.b64encode(f.read()).decode("utf-8"))
                except Exception as e:
                    print(f"  [Notice] Could not load image {p}: {e}")
        if images_b64:
            print(f"  [Multimodal] Attaching {len(images_b64)} figure/page images …")

    params_dict = None
    r_code = None
    params_json_str = input_json_str

    if step in ["extract", "all"]:
        # Call 1: Parameter extraction
        print("\n  ── Call 1/2: Extracting PBPK parameters (JSON) ──")
        user_msg_1 = {"role": "user", "content": _build_extraction_prompt(md_content)}
        if images_b64:
            user_msg_1["images"] = images_b64
    
        if dump_prompts_dir:
            dump_path = os.path.join(dump_prompts_dir, "ollama_call1_prompt.json")
            # Save a truncated version of base64 images so JSON is readable
            safe_msg = dict(user_msg_1)
            if "images" in safe_msg:
                safe_msg["images"] = [img[:50] + "...<truncated>" for img in safe_msg["images"]]
            with open(dump_path, "w") as f:
                json.dump({"system": PARAM_EXTRACTION_SYSTEM_PROMPT, "user": safe_msg, "model": model_extract}, f, indent=2)
            print(f"  ✅ Prompt dumped to {dump_path}")
            if step == "extract":
                return None, None
        else:
            try:
                response_1 = ollama.chat(
                    model=model_extract,
                    messages=[
                        {"role": "system", "content": PARAM_EXTRACTION_SYSTEM_PROMPT},
                        user_msg_1,
                    ],
                    format=PBPKParameters.model_json_schema(),
                    options={"temperature": 0.0},
                )
            except Exception as e:
                err_str = str(e).lower()
                if "multimodal" in err_str and images_b64:
                    print(f"  ⚠️  Model does not support images — retrying text-only …")
                    user_msg_1.pop("images", None)
                    images_b64 = []  # Disable for Call 2 as well
                    response_1 = ollama.chat(
                        model=model_extract,
                        messages=[
                            {"role": "system", "content": PARAM_EXTRACTION_SYSTEM_PROMPT},
                            user_msg_1,
                        ],
                        format=PBPKParameters.model_json_schema(),
                        options={"temperature": 0.0},
                    )
                else:
                    raise
        
            parsed = json.loads(response_1["message"]["content"])
            params_dict = _flatten_to_schema(parsed)
            validated = PBPKParameters(**params_dict)
            params_dict = validated.model_dump()
            params_json_str = json.dumps(params_dict, indent=2)
            print("  ✅ Parameter extraction complete.")

    # Call 2: R code generation
    if step in ["generate", "all"]:
        if not params_json_str and not dump_prompts_dir:
            raise ValueError("Missing parameters JSON for R code generation.")
        print("\n  ── Call 2/2: Generating faithful R/deSolve model ──")
        safe_params_json = params_json_str if params_json_str else '{"placeholder": "Run step 1 to generate JSON"}'
        r_system = R_GENERATION_SYSTEM_PROMPT.format(params_json=safe_params_json)
        user_msg_2 = {"role": "user", "content": _build_r_generation_prompt(md_content, safe_params_json)}
        if images_b64:
            user_msg_2["images"] = images_b64

        if dump_prompts_dir:
            dump_path = os.path.join(dump_prompts_dir, "ollama_call2_prompt.json")
            safe_msg = dict(user_msg_2)
            if "images" in safe_msg:
                safe_msg["images"] = [img[:50] + "...<truncated>" for img in safe_msg["images"]]
            with open(dump_path, "w") as f:
                json.dump({"system": r_system, "user": safe_msg, "model": model_generate}, f, indent=2)
            print(f"  ✅ Prompt dumped to {dump_path}")
            return None, None
        else:
            try:
                response_2 = ollama.chat(
                    model=model_generate,
                    messages=[
                        {"role": "system", "content": r_system},
                        user_msg_2,
                    ],
                    options={"temperature": 0.0, "num_predict": 8192},
                )
            except Exception as e:
                err_str = str(e).lower()
                if "multimodal" in err_str and images_b64:
                    print(f"  ⚠️  Model does not support images — retrying text-only …")
                    user_msg_2.pop("images", None)
                    response_2 = ollama.chat(
                        model=model_generate,
                        messages=[
                            {"role": "system", "content": r_system},
                            user_msg_2,
                        ],
                        options={"temperature": 0.0, "num_predict": 8192},
                    )
                else:
                    raise
            r_code = _extract_r_code(response_2["message"]["content"])
            print("  ✅ R code generation complete.")

    return params_dict, r_code



# ── Main entry point ─────────────────────────────────────────────────────────

def extract_pbpk_parameters(
    md_content: str = None, # Left for backward compatibility if ever called directly
    md_file_path: str = None,
    output_json_path: str = "pbpk_parameters.json",
    output_r_path: Optional[str] = None,
    model_extract: str = "google/gemma-4-31b-it",
    model_generate: str = "google/gemma-4-31b-it",
    backend: str = "vllm",
    tensor_parallel_size: int = 1,
    image_dir: str = None,
    step: str = "all",
    input_json_path: str = None,
    dump_prompts_dir: str = None,
    page_image_paths: list = None,
):
    if md_file_path:
        print(f"Reading markdown from: {md_file_path}")
        if not os.path.exists(md_file_path):
            print(f"Error: File '{md_file_path}' not found.")
            return

        with open(md_file_path, "r", encoding="utf-8") as f:
            md_content = f.read()

    # Strip chunk-break markers
    md_content = md_content.replace("\n\n---CHUNK_BREAK---\n\n", "\n\n")

    # Read input json if provided
    input_json_str = None
    if step in ["generate"] and input_json_path and os.path.exists(input_json_path):
        with open(input_json_path, "r", encoding="utf-8") as f:
            input_json_str = f.read()

    # Auto-discover images — prefer ColPali page images if provided
    image_paths = []
    if page_image_paths:
        image_paths = [p for p in page_image_paths if os.path.exists(p)]
        logging.info(f"Using {len(image_paths)} ColPali-retrieved page images as primary input.")
    elif image_dir and os.path.exists(image_dir):
        from pathlib import Path
        for ext in ("*.jpg", "*.jpeg", "*.png"):
            image_paths.extend([str(p) for p in Path(image_dir).rglob(ext)])
        image_paths = sorted(image_paths)

    print(f"Running extraction + R generation using {backend.upper()} "
          f"(Extract: {model_extract} | Generate: {model_generate} | Step: {step}) …")

    try:
        if backend == "vllm":
            params_dict, r_code = extract_and_generate_vllm(
                md_content, model_extract, model_generate, tensor_parallel_size, image_paths, step, input_json_str, dump_prompts_dir)
        elif backend == "ollama":
            params_dict, r_code = extract_and_generate_ollama(
                md_content, model_extract, model_generate, image_paths, step, input_json_str, dump_prompts_dir)
        else:
            raise ValueError(f"Unknown backend: {backend}")

        if dump_prompts_dir:
            return # Skip saving json/r_code if we just dumped prompts

        # Save params JSON
        if params_dict:
            with open(output_json_path, "w", encoding="utf-8") as f:
                json.dump(params_dict, f, indent=4)
            print(f"✅ Parameters saved to '{output_json_path}'")

        # Save R script
        if output_r_path and r_code:
            with open(output_r_path, "w", encoding="utf-8") as f:
                f.write(r_code)
            print(f"✅ R model saved to '{output_r_path}'")

    except Exception as e:
        print(f"❌ Error: {e}")
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract PBPK parameters and generate R model from paper."
    )
    parser.add_argument("-i", "--input", required=True,
                        help="Path to the input markdown file")
    parser.add_argument("-o", "--output", default="pbpk_parameters.json",
                        help="Path to save the output JSON file")
    parser.add_argument("--output-r", default=None,
                        help="Path to save the generated R script")
    parser.add_argument("--model-extract", default="google/gemma-4-31b-it",
                        help="Model name for parameter extraction")
    parser.add_argument("--model-generate", default="google/gemma-4-31b-it",
                        help="Model name for R script generation")
    parser.add_argument("-b", "--backend", choices=["vllm", "ollama"],
                        default="vllm", help="Inference backend (default: vllm)")
    parser.add_argument("-tp", "--tensor-parallel-size", type=int, default=1,
                        help="Tensor parallel size for vllm")
    parser.add_argument("--image-dir", default=None,
                        help="Directory containing page/figure images")
    parser.add_argument("--step", choices=["extract", "generate", "all"], default="all",
                        help="Step to run: extract, generate, or all")
    parser.add_argument("--input-json", default=None,
                        help="Path to input JSON file for generation step")
    parser.add_argument("--dump-prompts-dir", default=None,
                        help="If set, save the LLM prompts to this directory and exit without making inference calls.")
    parser.add_argument("--page-images", default=None,
                        help="Comma-separated list of page image paths (from ColPali retrieval). When provided, these are used as primary multimodal input instead of text.")

    args = parser.parse_args()
    page_image_list = None
    if args.page_images:
        page_image_list = [p.strip() for p in args.page_images.split(",") if p.strip()]

    extract_pbpk_parameters(
        md_file_path=args.input,
        output_json_path=args.output,
        output_r_path=args.output_r,
        model_extract=args.model_extract,
        model_generate=args.model_generate,
        backend=args.backend,
        tensor_parallel_size=args.tensor_parallel_size,
        image_dir=args.image_dir,
        step=args.step,
        input_json_path=args.input_json,
        dump_prompts_dir=args.dump_prompts_dir,
        page_image_paths=page_image_list,
    )
