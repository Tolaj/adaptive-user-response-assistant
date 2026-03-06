from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

VLM_BACKEND = "server"  # "package" or "server"

# Model paths
VLM_MODEL_PATH = str(BASE_DIR / "models/vlm/qwen3vl2b/Qwen3VL-2B-Instruct-Q4_K_M.gguf")
VLM_MMPROJ_PATH = str(
    BASE_DIR / "models/vlm/qwen3vl2b/mmproj-Qwen3VL-2B-Instruct-Q8_0.gguf"
)

# Server backend settings
VLM_SERVER_PORT = 8081
VLM_SERVER_HOST = "localhost"
VLM_SERVER_BINARY = "/opt/homebrew/bin/llama-server"  # must be in PATH

# Inference settings
VLM_SYSTEM_PROMPT = (
    "You are a vision AI with access to a live camera. "
    "Answer concisely in 1-2 sentences. No lists, no numbering, no speculation. "
    "Speak naturally as if you can see the person in real time."
)
VLM_MAX_TOKENS = 80
VLM_TEMPERATURE = 0.7
VLM_TOP_P = 0.8
VLM_TOP_K = 20
VLM_PRESENCE_PENALTY = 1.5

# Camera settings
VLM_CAMERA_INDEX = 0
VLM_FRAME_WIDTH = 240
VLM_FRAME_HEIGHT = 240
VLM_JPEG_QUALITY = 60

VLM_CONTINUOUS_VISION = True    # fresh frame every 10 tokens
VLM_REFRESH_EVERY_N_TOKENS = 10 # lower = more responsive, higher = more coherent
