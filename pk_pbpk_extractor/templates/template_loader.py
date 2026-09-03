"""
pk_pbpk_extractor/templates/template_loader.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Loads YAML extraction templates and interpolates variables into prompt strings.
Inspired by Hyper-Extract's YAML-driven template system, adapted for PBPK.
"""
from __future__ import annotations
import os
import re
from functools import lru_cache
from typing import Any

try:
    import yaml
    _YAML_OK = True
except ImportError:
    _YAML_OK = False

_TEMPLATES_DIR = os.path.dirname(__file__)


@lru_cache(maxsize=8)
def load_template(name: str) -> dict:
    """
    Load a YAML template by name (without .yaml extension).
    Results are cached so the file is only read once per process.

    Example:
        tmpl = load_template("pharmacometrics_table")
    """
    path = os.path.join(_TEMPLATES_DIR, f"{name}.yaml")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Template not found: {path}")

    if _YAML_OK:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    else:
        # Minimal fallback: return raw text as a dict with a 'raw' key
        with open(path, "r", encoding="utf-8") as f:
            return {"raw": f.read()}


def _format_guidelines(tmpl: dict) -> str:
    """Turn the guidelines list into a numbered string."""
    guidelines = tmpl.get("guidelines") or tmpl.get("extraction_rules", [])
    return "\n".join(f"  {i+1}. {g}" for i, g in enumerate(guidelines))


def _format_parameters(tmpl: dict) -> str:
    """Turn target_parameters into a readable description block."""
    tp = tmpl.get("target_parameters", {})
    lines = []
    for key, val in tp.items():
        if isinstance(val, dict):
            desc = val.get("description", "")
            cats = val.get("categories", [])
            lines.append(f"  [{key}]: {desc}")
            for cat in cats:
                lines.append(f"    - {cat}")
        elif isinstance(val, str):
            lines.append(f"  {val}")
    return "\n".join(lines)


def build_prompt(template_name: str, **kwargs: Any) -> str:
    """
    Build a complete LLM prompt from a named template, interpolating kwargs.

    Usage (table extraction):
        prompt = build_prompt(
            "pharmacometrics_table",
            paper_id="10.1234/example",
            table_id="Table 3",
            table_text="| Parameter | Value |\n| CL | 12.3 L/h |"
        )

    Usage (prose extraction):
        prompt = build_prompt(
            "pharmacometrics_text",
            paper_id="10.1234/example",
            chunk_id="chunk_5",
            text_chunk="The oral bioavailability was determined to be 60%..."
        )
    """
    tmpl = load_template(template_name)

    # Resolve persona (may be a multiline block scalar from YAML)
    persona = str(tmpl.get("persona", "You are a pharmacometrics expert.")).strip()

    # Pre-build the formatted sections
    guidelines_text = _format_guidelines(tmpl)
    parameters_text = _format_parameters(tmpl)

    # Build the full kwargs dict for interpolation
    interp = {
        "persona": persona,
        "guidelines_text": guidelines_text,
        "parameters_text": parameters_text,
        "rules_text": guidelines_text,   # alias for text template
        **kwargs,
    }

    # Get the prompt_template string
    prompt_template = tmpl.get("prompt_template", "{persona}\n\n{table_text}")

    # Interpolate — use re.sub so unresolved {vars} don't crash
    def _replace(match):
        key = match.group(1)
        return str(interp.get(key, match.group(0)))  # leave unresolved as-is

    return re.sub(r"\{(\w+)\}", _replace, prompt_template)
