"""
inference/vllm_worker.py — vLLM-backed MULTIMODAL inference worker.

Uses the OpenAI python client to talk to a local vLLM API server.
"""

import base64
import io
import json
import os
import openai

from ..schemas.pbpk_schema import ExtractedTablePayload
from ..config import OLLAMA_MODEL_ID, OLLAMA_HOST
from ..templates.template_loader import build_prompt

class VllmWorker:
    def __init__(self):
        host = os.environ.get("VLLM_HOST", "http://localhost:8000/v1")
        self.client = openai.OpenAI(base_url=host, api_key="EMPTY")
        self.model = os.environ.get("VLLM_MODEL_ID", "unsloth/Qwen3.8-27B-NVFP4")
        print(f"[VllmWorker] Using model \"{self.model}\" at {host}")
        
        # Pydantic JSON Schema for guided decoding
        self.json_schema = ExtractedTablePayload.model_json_schema()

    def extract_table_data(
        self,
        table_image,         # PIL Image of the page or cropped table
        table_text: str,     # Markdown text context from MinerU
        metadata: dict,
        paper_id: str = "unknown",
        table_id: str = "Table ?",
    ) -> dict:
        img_bytes = io.BytesIO()
        table_image.save(img_bytes, format="PNG")
        img_b64 = base64.b64encode(img_bytes.getvalue()).decode("utf-8")
        data_url = f"data:image/png;base64,{img_b64}"

        prompt = build_prompt(
            "pharmacometrics_table",
            paper_id=paper_id,
            table_id=table_id,
            table_text=table_text[:3000],
        )
        prompt += (
            "\n\nNOTE: You also have access to the PAGE IMAGE above. "
            "Carefully examine the image for tables — use both the image AND the text above."
        )

        print(f"  [VllmWorker] Calling \"{self.model}\" (multimodal, image + text)...")

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": data_url}}
                    ],
                }
            ],
            response_format={
                "type": "json_schema", 
                "json_schema": {"name": "extract", "schema": self.json_schema, "strict": False}
            },
            temperature=0.0,
            max_tokens=4096,
        )

        result_text = response.choices[0].message.content

        try:
            validated = ExtractedTablePayload.model_validate_json(result_text)
            return validated.model_dump()
        except Exception as e:
            print(f"  [VllmWorker] Validation warning: {e}")
            return json.loads(result_text)

    def chat(self, prompt: str = None, messages: list = None, format: dict = None, **kwargs) -> str:
        if messages is None:
            if prompt is None:
                raise ValueError("Either prompt or messages must be provided")
            messages = [{"role": "user", "content": prompt}]

        extra_kwargs = {}
        target_schema = format or kwargs.get("response_format")
        if target_schema:
            if isinstance(target_schema, dict) and target_schema.get("type") == "json_schema":
                extra_kwargs["response_format"] = target_schema
            elif isinstance(target_schema, dict):
                extra_kwargs["response_format"] = {
                    "type": "json_schema",
                    "json_schema": {"name": "extract", "schema": target_schema, "strict": False}
                }

        max_tokens = kwargs.get("max_tokens", 4096)
        if "options" in kwargs and isinstance(kwargs["options"], dict):
            if "num_predict" in kwargs["options"]:
                max_tokens = kwargs["options"]["num_predict"]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=kwargs.get("temperature", 0.0),
            max_tokens=max_tokens,
            **extra_kwargs
        )
        return response.choices[0].message.content
