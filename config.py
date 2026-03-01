"""
config.py  —  single source of truth for all tunable values.
"""

import os
import torch
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
MODELS_DIR = BASE_DIR / "models"
WHISPER_DIR = MODELS_DIR / "whisper"

# ── Whisper ────────────────────────────────────────────────────────────────────
WHISPER_MODEL_NAME = "base"
WHISPER_MODEL_PATH = WHISPER_DIR / f"{WHISPER_MODEL_NAME}.pt"

if torch.cuda.is_available():
    WHISPER_DEVICE = "cuda"
elif torch.backends.mps.is_available():
    WHISPER_DEVICE = "mps"
else:
    WHISPER_DEVICE = "cpu"

print(f"[Config] Using device: {WHISPER_DEVICE}")

# ── LLM ────────────────────────────────────────────────────────────────────────
ACTIVE_LLM_MODEL = "qwen2.5-3b"
GPU_LAYERS = -1  # -1 = all layers on Metal GPU
CONTEXT_SIZE = 2048
CPU_THREADS = max(1, os.cpu_count() // 2)

# ── Server ─────────────────────────────────────────────────────────────────────
SERVER_PORT = 5001

# ── Voice / LLM prompt ────────────────────────────────────────────────────────
VOICE_SYSTEM_PROMPT = (
    "You are a helpful voice assistant. "
    "Keep responses short and conversational, 1-3 sentences max."
)
VOICE_MAX_TOKENS = 150
VOICE_TEMPERATURE = 0.7

# ── Audio ──────────────────────────────────────────────────────────────────────
RECORD_SAMPLE_RATE = 44100
WHISPER_SAMPLE_RATE = 16000

# ── VAD ────────────────────────────────────────────────────────────────────────
SILENCE_THRESHOLD = 0.008
SILENCE_DURATION = 0.5
MIN_SPEECH = 0.3
ROLLING_WINDOW_SEC = 8.0

# ── TTS ────────────────────────────────────────────────────────────────────────
# Switch between "native" (macOS pyttsx3) and "kokoro" (neural voice)
TTS_ENGINE = "native"  # ← change to "kokoro" for high-quality neural voice

# Native engine settings (used when TTS_ENGINE = "native")
TTS_RATE = 185  # words per minute — try 150-220
TTS_VOLUME = 1.0  # 0.0 to 1.0
TTS_VOICE_INDEX = (
    138  # 138=Samantha (natural American female) — change to 112 for Reed male
)

# Kokoro engine settings (used when TTS_ENGINE = "kokoro")
# Voices: af_heart, af_bella, af_sarah, am_adam, am_michael,
#         bf_emma, bf_isabella, bm_george, bm_lewis
TTS_KOKORO_VOICE = "af_heart"
TTS_KOKORO_SPEED = 1.0  # 0.5 = slow, 1.0 = normal, 1.3 = fast
