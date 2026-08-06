"""
extract_pbpk_params.py — Extract PBPK parameters from cleaned OCR markdown.

Supports two inference backends:
  • vllm  (default) — GPU-accelerated, with guided JSON generation
  • ollama           — fallback for smaller setups
"""

import os
import json
import argparse
from typing import Dict, Any
from pydantic import BaseModel, Field


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

SYSTEM_PROMPT = (
    "You are an expert pharmacometrician. Your task is to extract PBPK "
    "(Physiologically Based Pharmacokinetic) parameters from the OCR text of "
    "a scientific paper. Extract organ blood flow fractions, organ volume "
    "fractions, tissue:plasma partition coefficients, and any biochemical "
    "parameters (clearance, Vmax, Km, absorption rates, etc.). Also extract "
    "any relevant kinetic equations mentioned.\n\n"
    "You MUST respond with ONLY valid JSON matching this EXACT schema "
    "(no wrapper keys, no extra nesting):\n"
    f"{EXPECTED_SCHEMA}"
)


def _build_prompt(md_content: str) -> str:
    return (
        f"Read the following OCR text from a scientific paper and extract "
        f"the PBPK parameters.\n\nPaper text:\n\n{md_content}"
    )

# ── JSON Schema Normalisation ────────────────────────────────────────────────

REQUIRED_KEYS = {"blood_flow_fraction", "volume_fraction", "biochemical_parameters", "equations"}

def _flatten_to_schema(data: dict) -> dict:
    """Unwrap nested JSON structures into the expected flat schema.
    
    Some models wrap the output in a single parent key like
    ``{"PBPK_parameters": {...}}``.  This helper digs one level
    deep to find the four required keys.
    """
    if REQUIRED_KEYS.issubset(data.keys()):
        return data  # Already matches

    # Try unwrapping a single top-level wrapper key
    for key, value in data.items():
        if isinstance(value, dict) and REQUIRED_KEYS.issubset(value.keys()):
            return value

    # Try searching one more level deep
    for key, value in data.items():
        if isinstance(value, dict):
            for k2, v2 in value.items():
                if isinstance(v2, dict) and REQUIRED_KEYS.issubset(v2.keys()):
                    return v2

    # Give up — return as-is and let Pydantic raise a clear error
    return data


# ── vLLM backend ─────────────────────────────────────────────────────────────

def extract_with_vllm(md_content: str, model_name: str, tensor_parallel_size: int = 1) -> dict:
    # Ensure the venv's bin dir is on PATH so FlashInfer JIT can find 'ninja'
    import sys
    venv_bin = os.path.join(os.path.dirname(sys.executable))
    if venv_bin not in os.environ.get("PATH", ""):
        os.environ["PATH"] = venv_bin + os.pathsep + os.environ.get("PATH", "")

    from vllm import LLM, SamplingParams

    import torch
    num_gpus = torch.cuda.device_count()
    if tensor_parallel_size > num_gpus:
        print(f"  [Notice] Requested tensor_parallel_size={tensor_parallel_size}, but only {num_gpus} GPU(s) available. Using {max(1, num_gpus)}.")
        tensor_parallel_size = max(1, num_gpus)

    print(f"  Loading model '{model_name}' with vLLM (Tensor Parallelism: {tensor_parallel_size}) …")
    llm = LLM(
        model=model_name,
        trust_remote_code=True,
        max_model_len=32768,
        gpu_memory_utilization=0.85,
        tensor_parallel_size=tensor_parallel_size,
    )

    sampling = SamplingParams(
        temperature=0.0,
        max_tokens=4096,
    )

    # Build conversation for chat template
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": _build_prompt(md_content)},
    ]

    # Use the chat interface for proper tokenization
    outputs = llm.chat(
        messages=[messages],
        sampling_params=sampling,
        use_tqdm=True,
    )

    response_text = outputs[0].outputs[0].text.strip()

    # Try to parse JSON from the response (handle markdown code fences)
    json_text = response_text
    if "```json" in json_text:
        json_text = json_text.split("```json")[1].split("```")[0].strip()
    elif "```" in json_text:
        json_text = json_text.split("```")[1].split("```")[0].strip()

    parsed = json.loads(json_text)
    return _flatten_to_schema(parsed)


# ── Ollama backend (fallback) ────────────────────────────────────────────────

def extract_with_ollama(md_content: str, model_name: str) -> dict:
    import ollama

    prompt = _build_prompt(md_content)

    response = ollama.chat(
        model=model_name,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        format=PBPKParameters.model_json_schema(),
        options={"temperature": 0.0},
    )
    parsed = json.loads(response["message"]["content"])
    return _flatten_to_schema(parsed)


# ── Main entry point ─────────────────────────────────────────────────────────

def extract_pbpk_parameters(
    md_file_path: str,
    output_json_path: str,
    model_name: str = "google/gemma-4-31b-it",
    backend: str = "vllm",
    tensor_parallel_size: int = 1,
):
    print(f"Reading markdown from: {md_file_path}")
    if not os.path.exists(md_file_path):
        print(f"Error: File '{md_file_path}' not found.")
        return

    with open(md_file_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Strip chunk-break markers if present (from clean_markdown.py)
    md_content = md_content.replace("\n\n---CHUNK_BREAK---\n\n", "\n\n")

    print(f"Extracting parameters using {backend.upper()} (model: {model_name}) …")

    try:
        if backend == "vllm":
            extracted_data = extract_with_vllm(md_content, model_name, tensor_parallel_size)
        elif backend == "ollama":
            extracted_data = extract_with_ollama(md_content, model_name)
        else:
            raise ValueError(f"Unknown backend: {backend}")

        # Validate against Pydantic schema
        validated = PBPKParameters(**extracted_data)
        result = validated.model_dump()

        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4)

        print(f"✅ Extraction successful! Parameters saved to '{output_json_path}'")

    except Exception as e:
        print(f"❌ Error during extraction: {e}")
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract PBPK parameters from paper OCR markdown."
    )
    parser.add_argument("-i", "--input", required=True, help="Path to the input markdown file")
    parser.add_argument("-o", "--output", default="pbpk_parameters.json", help="Path to save the output JSON file")
    parser.add_argument(
        "-m", "--model",
        default="google/gemma-4-31b-it",
        help="Model name (HuggingFace ID for vllm, or Ollama tag for ollama)",
    )
    parser.add_argument(
        "-b", "--backend",
        choices=["vllm", "ollama"],
        default="vllm",
        help="Inference backend (default: vllm)",
    )
    parser.add_argument(
        "-t", "--tensor-parallel-size",
        type=int,
        default=1,
        help="Number of GPUs to shard the model across (vLLM only)",
    )

    args = parser.parse_args()
    extract_pbpk_parameters(args.input, args.output, args.model, args.backend, args.tensor_parallel_size)
