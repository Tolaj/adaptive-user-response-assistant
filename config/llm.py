import os

ACTIVE_LLM_MODEL = "qwen2.5-3b"
GPU_LAYERS = 36
CONTEXT_SIZE = 2048
CPU_THREADS = max(1, os.cpu_count() // 2)
