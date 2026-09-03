"""
inference/vllm_worker.py — Ollama-backed MULTIMODAL inference worker.

qwen3.8:latest supports native vision (image + text), so we send both
the page image AND the cleaned markdown text for maximum table coverage.

Structured output is enforced using Ollama's `format` parameter (JSON Schema)
for guaranteed valid JSON on every call.

Set OLLAMA_HOST env var to point to a remote DGX server, e.g.:
    export OLLAMA_HOST="http://<DGX_IP>:11434"
"""

import base64
import io
import json
import os

import ollama
from ..schemas.pbpk_schema import ExtractedTablePayload
from ..config import OLLAMA_MODEL_ID, OLLAMA_HOST
from ..templates.template_loader import build_prompt


class OllamaWorker:
    def __init__(self):
        host = OLLAMA_HOST or "http://localhost:11434"
        self.client = ollama.Client(host=host)
        self.model = OLLAMA_MODEL_ID
        print(f"[OllamaWorker] Using multimodal model \"{self.model}\" at {host}")
        # Pre-build the JSON schema for Ollama structured output
        self.json_schema = ExtractedTablePayload.model_json_schema()

    def extract_table_data(
        self,
        table_image,         # PIL Image of the page or cropped table
        table_text: str,     # Markdown text context from MinerU
        metadata: dict,
        paper_id: str = "unknown",
        table_id: str = "Table ?",
    ) -> dict:
        """
        Sends a MULTIMODAL request (image + text) to the Ollama server.
        The model sees both the visual page layout AND the markdown text,
        giving it the best possible chance to find all table rows.
        """
        # Convert PIL image to base64 for Ollama multimodal input
        img_bytes = io.BytesIO()
        table_image.save(img_bytes, format="PNG")
        img_b64 = base64.b64encode(img_bytes.getvalue()).decode("utf-8")

        prompt = build_prompt(
            "pharmacometrics_table",
            paper_id=paper_id,
            table_id=table_id,
            table_text=table_text[:3000],
        )
        # Append image instruction since this is multimodal
        prompt += (
            "\n\nNOTE: You also have access to the PAGE IMAGE above. "
            "Carefully examine the image for tables — use both the image AND the text above."
        )

        print(f"  [OllamaWorker] Calling \"{self.model}\" (multimodal, image + text)...")

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                    "images": [img_b64],   # Pass the page image for visual reading
                }
            ],
            format=self.json_schema,       # Enforced structured JSON output
            options={
                "temperature": 0.0,
                "num_predict": 4096,
            },
        )

        result_text = response["message"]["content"]

        # Validate with Pydantic V2
        try:
            validated = ExtractedTablePayload.model_validate_json(result_text)
            return validated.model_dump()
        except Exception as e:
            print(f"  [OllamaWorker] Validation warning: {e}")
            return json.loads(result_text)

    def chat(self, prompt: str) -> str:
        response = self.client.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.0}
        )
        return response["message"]["content"]
