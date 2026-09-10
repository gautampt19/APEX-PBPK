import os
import ollama
from pk_pbpk_extractor.schemas.pbpk_schema import ExtractedTablePayload
from pk_pbpk_extractor.config import OLLAMA_HOST, OLLAMA_MODEL_ID

class OllamaWorker:
    def __init__(self, host: str = None, model: str = None):
        self.host = host or OLLAMA_HOST
        self.model = model or OLLAMA_MODEL_ID
        self.client = ollama.Client(host=self.host)
        self.json_schema = ExtractedTablePayload.model_json_schema()
        print(f"[OllamaWorker] Connected to Ollama at {self.host} (model: {self.model})")

    def chat(self, messages: list, model: str = None, format=None, options: dict = None) -> str:
        model = model or self.model
        format = format or self.json_schema
        options = options or {"temperature": 0.0}
        
        # Inject reasoning settings to drastically reduce extraction time for reasoning models
        options["chat_template_kwargs"] = {"enable_thinking": True, "reasoning_effort": "low"}
        
        response = self.client.chat(
            model=model,
            messages=messages,
            format=format,
            options=options,
        )
        return response["message"]["content"]
