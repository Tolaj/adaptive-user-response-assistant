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
WHISPER_MODEL_NAME = "base"  # "base" | "large-v2"
WHISPER_MODEL_PATH = WHISPER_DIR / f"{WHISPER_MODEL_NAME}.pt"

# Auto-detect best available device
if torch.cuda.is_available():
    WHISPER_DEVICE = "cuda"
elif torch.backends.mps.is_available():
    WHISPER_DEVICE = "mps"
else:
    WHISPER_DEVICE = "cpu"

print(f"[Config] Using device: {WHISPER_DEVICE}")

# ── LLM (future) ───────────────────────────────────────────────────────────────
ACTIVE_LLM_MODEL = "qwen2.5-3b"
GPU_LAYERS = 36
CONTEXT_SIZE = 4096
CPU_THREADS = max(1, os.cpu_count() // 2)

# ── Server ─────────────────────────────────────────────────────────────────────
SERVER_PORT = 5001

# ── Voice / LLM prompt (future) ────────────────────────────────────────────────
VOICE_SYSTEM_PROMPT = (
    "You are a helpful voice assistant. "
    "Keep responses short and conversational, 1-3 sentences max."
)
VOICE_MAX_TOKENS = 150
VOICE_TEMPERATURE = 0.7

# ── Audio ──────────────────────────────────────────────────────────────────────
RECORD_SAMPLE_RATE = 44100  # native mic sample rate
WHISPER_SAMPLE_RATE = 16000  # Whisper always needs 16 kHz

# ── VAD ────────────────────────────────────────────────────────────────────────
SILENCE_THRESHOLD = 0.008  # mean absolute amplitude below = silence
SILENCE_DURATION = 0.5  # seconds of silence → end of utterance
MIN_SPEECH = 0.3  # discard utterances shorter than this (seconds)
ROLLING_WINDOW_SEC = 8.0  # emit a chunk every N seconds during continuous speech
