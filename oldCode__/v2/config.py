from pathlib import Path
import os

# ── PATHS ──────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
MODELS_DIR = BASE_DIR / "models"
WHISPER_DIR = MODELS_DIR / "whisper"

# ── WHISPER ────────────────────────────────────────────
WHISPER_MODEL_NAME = "base"          # "base" or "large-v2"
WHISPER_MODEL_PATH = WHISPER_DIR / f"{WHISPER_MODEL_NAME}.pt"

# ── WHISPER DEVICE ────────────────────────────────────
WHISPER_DEVICE = "cuda"           # "cuda" or "cpu"
# WHISPER_COMPUTE_TYPE = "int8_float16"  # "int8_float16" for GPU, "int8" for CPU
# WHISPER_BEAM_SIZE = 1

# ── LLM ───────────────────────────────────────────────
ACTIVE_LLM_MODEL = "qwen2.5-3b"
GPU_LAYERS = 20
CONTEXT_SIZE = 4096
CPU_THREADS = max(1, os.cpu_count() // 2)

# ── SERVER ────────────────────────────────────────────
SERVER_PORT = 5001

# ── VOICE ─────────────────────────────────────────────
VOICE_SYSTEM_PROMPT = "You are a helpful voice assistant. Keep responses short and conversational, 1-3 sentences max."
VOICE_MAX_TOKENS = 150
VOICE_TEMPERATURE = 0.7

# ── AUDIO ─────────────────────────────────────────────
RECORD_SAMPLE_RATE = 44100   # Record at native device rate
WHISPER_SAMPLE_RATE = 16000  # Whisper always needs 16kHz

