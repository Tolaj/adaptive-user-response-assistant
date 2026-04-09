import os

ACTIVE_LLM_MODEL = "qwen2.5-3b"
LLM_REPO_ID = "Qwen/Qwen2.5-3B-Instruct-GGUF"
LLM_FILENAME = "qwen2.5-3b-instruct-q4_k_m.gguf"

GPU_LAYERS = 36
CONTEXT_SIZE = 2048
CPU_THREADS = max(1, os.cpu_count() // 2)
