#!/bin/bash
# Start vLLM server for unsloth/Qwen3.8-27B-NVFP4

MODEL="unsloth/Qwen3.8-27B-NVFP4"
PORT=8000
GPU_UTIL=${VLLM_GPU_UTIL:-0.85}

echo "[vLLM] Starting $MODEL on port $PORT (gpu_util=$GPU_UTIL)..."

.venv/bin/python3 -m vllm.entrypoints.openai.api_server \
    --model "$MODEL" \
    --port $PORT \
    --gpu-memory-utilization $GPU_UTIL \
    --max-model-len 32768 \
    --max-num-seqs 30 \
    --trust-remote-code
