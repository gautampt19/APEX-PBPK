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

class ParameterSet(BaseModel):
    """One block of parameters bound to its experimental context (species + formulation).

    Grouping parameters under species/formulation prevents rat organ volumes
    being mixed with human PK values when a paper evaluates multiple cohorts.
    """
    species: str = Field(
        description="Species studied (e.g., 'rat', 'human', 'mouse', 'dog'). Use 'unknown' if not specified."
    )
    formulation: Optional[str] = Field(
        None,
        description="Formulation name if multiple are tested (e.g., 'ASD', 'Rilutor', 'IV bolus', 'oral suspension'). None if only one formulation."
    )
    route: Optional[str] = Field(
        None,
        description="Route of administration (e.g., 'oral', 'IV', 'SC', 'IM'). None if not reported."
    )
    dose: Optional[float] = Field(
        None,
        description="Numeric dose value if reported."
    )
    dose_unit: Optional[str] = Field(
        None,
        description="Unit for the dose value (e.g., 'mg/kg', 'mg', 'mg/m2')."
    )
    blood_flow_fraction: Dict[str, float] = Field(
        default_factory=dict,
        description="Organ names mapped to blood flow as a fraction of cardiac output."
    )
    volume_fraction: Dict[str, float] = Field(
        default_factory=dict,
        description="Organ names mapped to volume as a fraction of body weight."
    )
    biochemical_parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="All other biochemical parameters: Kp, Vmax, Km, Cl, fu, HCT, GE, Kabs, etc."
    )
    equations: Dict[str, str] = Field(
        default_factory=dict,
        description="Key mathematical equations identified (e.g., metabolism, allometric scaling)."
    )


class PBPKParameters(BaseModel):
    """Top-level extraction result.  A list of parameter sets, one per species/formulation cohort."""
    parameter_sets: List[ParameterSet] = Field(
        description=(
            "List of parameter blocks. Each block is specific to one species and formulation. "
            "If the paper reports data for only one species/formulation, return a list with one element."
        )
    )

    # ── Compatibility helpers ──────────────────────────────────────────────
    @property
    def blood_flow_fraction(self) -> Dict[str, float]:
        """Return blood_flow_fraction from the first parameter set (back-compat)."""
        return self.parameter_sets[0].blood_flow_fraction if self.parameter_sets else {}

    @property
    def volume_fraction(self) -> Dict[str, float]:
        """Return volume_fraction from the first parameter set (back-compat)."""
        return self.parameter_sets[0].volume_fraction if self.parameter_sets else {}

    @property
    def biochemical_parameters(self) -> Dict[str, Any]:
        """Return biochemical_parameters from the first parameter set (back-compat)."""
        return self.parameter_sets[0].biochemical_parameters if self.parameter_sets else {}

    @property
    def equations(self) -> Dict[str, str]:
        """Return equations from the first parameter set (back-compat)."""
        return self.parameter_sets[0].equations if self.parameter_sets else {}


EXPECTED_SCHEMA = json.dumps(PBPKParameters.model_json_schema(), indent=2)

PARAM_EXTRACTION_SYSTEM_PROMPT = (
    "You are an expert pharmacometrician. Your task is to extract PBPK "
    "(Physiologically Based Pharmacokinetic) parameters from the OCR text AND "
    "the attached page images of a scientific paper.\n\n"
    "CRITICAL INSTRUCTIONS FOR TABLES:\n"
    "- You have been provided with images of the key pages. These pages contain complex tables.\n"
    "- You MUST carefully scan every single table on these pages row-by-row.\n"
    "- Tables usually contain the majority of the physiological parameters (Volume, Blood Flow) and biochemical parameters (Partition Coefficients Kp, Clearance, Vmax). DO NOT skip any rows or columns.\n\n"
    "CRITICAL: You must aggressively hunt for and extract:\n"
    "- Organ blood flow fractions (Q) and organ volume fractions (V).\n"
    "- Tissue:plasma partition coefficients (Kp).\n"
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


def _build_r_generation_prompt(md_content: str, params_json: str,
                               previous_r: str = None, error_msg: str = None) -> str:
    # For very long papers, truncate to key sections to leave room for output
    # Max ~10000 words for the R generation call
    words = md_content.split()
    if len(words) > 10000:
        md_content = " ".join(words[:10000]) + "\n\n[... truncated for length ...]"

    base = (
        f"Read the following scientific paper and generate a complete R/deSolve "
        f"script that faithfully implements the PBPK/PD model described in it. "
        f"Use the extracted parameter values provided in the system prompt.\n\n"
        f"Paper text:\n\n{md_content}"
    )

    if previous_r and error_msg:
        base += (
            f"\n\n--- CORRECTION REQUEST ---\n"
            f"You previously generated the following R code which has a syntax error:\n\n"
            f"```r\n{previous_r}\n```\n\n"
            f"The R syntax checker reported this error:\n\n"
            f"{error_msg}\n\n"
            f"Please fix ALL syntax errors and return a COMPLETE, corrected R script. "
            f"Do NOT just return the fixed lines -- return the full script."
        )

    return base


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


def _vllm_chat(
    llm,
    SamplingParams,
    system_prompt: str,
    user_content,
    max_tokens: int = 4096,
    temperature: float = 0.0,
    guided_json_schema: dict = None,
) -> str:
    """Run a single chat completion on the already-loaded vLLM model.

    Args:
        guided_json_schema: If provided, enables grammar-constrained decoding
            (vLLM guided_json).  The model's token sampler will only emit tokens
            that satisfy the JSON schema, guaranteeing 100% valid JSON on the
            first pass without any retry loop.  Pass None to disable (default).
    """
    sampling_kwargs = {"temperature": temperature, "max_tokens": max_tokens}

    if guided_json_schema is not None:
        try:
            from vllm.sampling_params import GuidedDecodingParams
            sampling_kwargs["guided_decoding"] = GuidedDecodingParams(
                json_schema=guided_json_schema
            )
            logging.info("  [guided_json] Grammar-constrained decoding enabled.")
        except ImportError:
            # Older vLLM (<0.4) — fall back silently
            logging.warning(
                "  [guided_json] GuidedDecodingParams not available in this vLLM version. "
                "Falling back to unconstrained decoding."
            )

    sampling = SamplingParams(**sampling_kwargs)
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
    previous_r: str = None,
    error_msg: str = None,
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
            guided_json_schema=PBPKParameters.model_json_schema(),  # constrained decoding
        )

        # Parse JSON — guided_json guarantees valid JSON, but strip fences as
        # a belt-and-suspenders fallback for non-guided runs.
        json_text = response_1
        if "```json" in json_text:
            json_text = json_text.split("```json")[1].split("```")[0].strip()
        elif "```" in json_text:
            json_text = json_text.split("```")[1].split("```")[0].strip()

        parsed = json.loads(json_text)

        # Handle both new schema (parameter_sets) and legacy flat schema
        if "parameter_sets" in parsed:
            validated = PBPKParameters(**parsed)
        else:
            # Legacy flat dict — wrap in a single ParameterSet
            ps = _flatten_to_schema(parsed)
            validated = PBPKParameters(parameter_sets=[ParameterSet(**ps)])
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
            _build_r_generation_prompt(md_content, safe_params_json, previous_r=previous_r, error_msg=error_msg), image_paths)

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
    previous_r: str = None,
    error_msg: str = None,
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
        user_msg_2 = {"role": "user", "content": _build_r_generation_prompt(md_content, safe_params_json, previous_r=previous_r, error_msg=error_msg)}
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


# ── R Code Semantic Verification ─────────────────────────────────────────────

R_REVIEW_SYSTEM_PROMPT = """\
You are an expert pharmacometrician reviewing a generated R/deSolve PBPK model script.
Your task is to compare the R code against the extracted parameters and the original paper text
and identify any scientific/structural discrepancies.

Check for:
1. COMPARTMENTS: Are all organs from the paper's model structure present as ODEs?
2. PARAMETERS: Are all extracted parameters actually used in the code with correct names?
3. ODE STRUCTURE: Are blood flow (Q), volume (V), and partition coefficients (Kp) used correctly?
4. METABOLISM: Is the metabolic rate (Vmax/Km or CLint) implemented correctly?
5. ROUTES: Is the administration route (oral/IV) handled correctly (oral absorption ODEs, etc.)?
6. SCALING: Is allometric scaling (if needed) applied correctly?
7. OUTPUTS: Does the script write simulation outputs to a CSV file?
8. UNITS: Are there any obvious unit inconsistencies?

Respond with ONLY a JSON object in this exact format:
{
  "overall_status": "PASS" | "PASS_WITH_WARNINGS" | "FAIL",
  "summary": "One sentence summary of the review",
  "checks": [
    {"category": "COMPARTMENTS", "status": "OK" | "WARNING" | "ERROR", "message": "Details here"},
    {"category": "PARAMETERS",   "status": "OK" | "WARNING" | "ERROR", "message": "Details here"},
    {"category": "ODE_STRUCTURE","status": "OK" | "WARNING" | "ERROR", "message": "Details here"},
    {"category": "METABOLISM",   "status": "OK" | "WARNING" | "ERROR", "message": "Details here"},
    {"category": "ROUTES",       "status": "OK" | "WARNING" | "ERROR", "message": "Details here"},
    {"category": "SCALING",      "status": "OK" | "WARNING" | "ERROR", "message": "Details here"},
    {"category": "OUTPUTS",      "status": "OK" | "WARNING" | "ERROR", "message": "Details here"},
    {"category": "UNITS",        "status": "OK" | "WARNING" | "ERROR", "message": "Details here"}
  ],
  "critical_issues": ["List any blocking errors here"],
  "recommendations": ["List any improvement suggestions here"]
}
"""


def verify_r_code(
    r_code: str,
    params_json: str,
    md_content: str,
    model: str,
    backend: str = "ollama",
    tensor_parallel_size: int = 1,
) -> dict:
    """
    Use the LLM to semantically verify the generated R code against the paper.
    Returns a dict with 'overall_status', 'checks', 'critical_issues', etc.
    """
    # Truncate inputs to avoid context overflow
    words = md_content.split()
    if len(words) > 6000:
        md_content = " ".join(words[:6000]) + "\n\n[... truncated ...]"
    
    r_words = r_code.split()
    if len(r_words) > 4000:
        r_code = " ".join(r_words[:4000]) + "\n\n# [... truncated ...]"

    user_prompt = (
        f"Review the following generated R PBPK script for scientific correctness.\n\n"
        f"=== EXTRACTED PARAMETERS (JSON) ===\n{params_json}\n\n"
        f"=== ORIGINAL PAPER TEXT (truncated) ===\n{md_content}\n\n"
        f"=== GENERATED R CODE ===\n```r\n{r_code}\n```\n\n"
        f"Provide your review as a JSON object matching the schema in your system prompt."
    )

    try:
        if backend == "ollama":
            import ollama
            response = ollama.chat(
                model=model,
                messages=[
                    {"role": "system", "content": R_REVIEW_SYSTEM_PROMPT},
                    {"role": "user",   "content": user_prompt},
                ],
                options={"temperature": 0.0, "num_predict": 2048},
            )
            raw = response["message"]["content"].strip()
        elif backend == "vllm":
            llm, SamplingParams = _load_vllm(model, tensor_parallel_size)
            raw = _vllm_chat(llm, SamplingParams, R_REVIEW_SYSTEM_PROMPT, user_prompt, max_tokens=2048)
        else:
            return {"overall_status": "ERROR", "summary": f"Unknown backend: {backend}", "checks": [], "critical_issues": [], "recommendations": []}

        # Parse JSON from response
        if "```json" in raw:
            raw = raw.split("```json")[1].split("```")[0].strip()
        elif "```" in raw:
            raw = raw.split("```")[1].split("```")[0].strip()
        
        # Find first { ... } block
        start = raw.find("{")
        end   = raw.rfind("}") + 1
        if start != -1 and end > start:
            raw = raw[start:end]

        result = json.loads(raw)
        return result

    except json.JSONDecodeError as e:
        return {
            "overall_status": "ERROR",
            "summary": f"LLM review response was not valid JSON: {e}",
            "checks": [],
            "critical_issues": ["Failed to parse LLM review output"],
            "recommendations": [],
            "raw_response": raw if "raw" in dir() else "No response",
        }
    except Exception as e:
        return {
            "overall_status": "ERROR",
            "summary": f"Verification failed: {e}",
            "checks": [],
            "critical_issues": [str(e)],
            "recommendations": [],
        }


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
    previous_r: str = None,
    error_msg: str = None,
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
                md_content, model_extract, model_generate, tensor_parallel_size, image_paths, step, input_json_str, dump_prompts_dir,
                previous_r=previous_r, error_msg=error_msg)
        elif backend == "ollama":
            params_dict, r_code = extract_and_generate_ollama(
                md_content, model_extract, model_generate, image_paths, step, input_json_str, dump_prompts_dir,
                previous_r=previous_r, error_msg=error_msg)
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
    parser.add_argument("--previous-r", default=None,
                        help="Path to a previously generated but broken R script. If provided with --error-msg, the LLM is asked to fix it.")
    parser.add_argument("--error-msg", default=None,
                        help="The syntax error message from the failed R script. Passed to the LLM for correction.")

    parser.add_argument("--verify-r", action="store_true",
                        help="If set, run LLM semantic review on the generated R script.")
    args = parser.parse_args()
    page_image_list = None
    if args.page_images:
        page_image_list = [p.strip() for p in args.page_images.split(",") if p.strip()]

    previous_r_code = None
    if args.previous_r and os.path.exists(args.previous_r):
        with open(args.previous_r, "r", encoding="utf-8") as f:
            previous_r_code = f.read()

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
        previous_r=previous_r_code,
        error_msg=args.error_msg,
    )

    # Optional standalone LLM review call
    if args.verify_r and args.previous_r and os.path.exists(args.previous_r):
        print("\n  ── LLM Semantic Review of R Code ──")
        params_str = open(args.output, encoding="utf-8").read() if os.path.exists(args.output) else "{}"
        md_str = open(args.input, encoding="utf-8").read() if os.path.exists(args.input) else ""
        result = verify_r_code(previous_r_code, params_str, md_str, args.model_generate, args.backend, args.tensor_parallel_size)
        print(json.dumps(result, indent=2))
