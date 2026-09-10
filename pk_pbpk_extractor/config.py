import os

# ── Ollama Config ─────────────────────────────────────────────────────────────
# Ollama model tag as shown by `ollama list`
OLLAMA_MODEL_ID = os.getenv("OLLAMA_MODEL_ID", "qwen3.8:latest")

# Ollama server endpoint. Override to point at remote DGX:
#   export OLLAMA_HOST="http://<DGX_IP>:11434"
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# ── ColPali Config ────────────────────────────────────────────────────────────
COLPALI_MODEL_ID = os.getenv("COLPALI_MODEL_ID", "vidore/colpali-v1.3-hf")
SKIP_COLPALI = os.getenv("SKIP_COLPALI", "false").lower() in ("true", "1", "yes")

# ── Database Config ───────────────────────────────────────────────────────────
DB_PATH = os.getenv("DB_PATH", "sqlite:///pk_parameters.db")

# ── Inference parameters ──────────────────────────────────────────────────────
VLLM_TEMPERATURE = 0.0
VLLM_MAX_TOKENS = 4096

# ── vLLM Config ─────────────────────────────────────────────────────────────
VLLM_HOST = os.getenv("VLLM_HOST", "http://localhost:8000/v1")
VLLM_MODEL_ID = os.getenv("VLLM_MODEL_ID", "unsloth/Qwen3.8-27B-NVFP4")
VLLM_MAX_WORKERS = int(os.getenv("VLLM_MAX_WORKERS", "30"))
