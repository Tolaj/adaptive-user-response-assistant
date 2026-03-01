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

# ── Feature toggles ───────────────────────────────────────────────────────────
# ENABLE_STT : True  → mic is captured, sent to server, Whisper runs normally.
#              False → voice input is fully disabled on the client (no mic, no
#                      audio sent). The server also skips loading Whisper.
#                      Useful for text-only / keyboard-input mode.
ENABLE_STT = True

# ENABLE_TTS : True  → AI responses are spoken aloud by the server (or client,
#                      depending on TTS_MODE).
#              False → no TTS engine is created anywhere; responses are
#                      text-only. Fillers are also suppressed.
#                      Useful for silent / screen-reader environments.
ENABLE_TTS = True

# ── Output mode ───────────────────────────────────────────────────────────────
# SHOW_TEXT : True  → response text is streamed to the client terminal.
# PLAY_SPEECH: True → response is spoken aloud (also requires ENABLE_TTS=True).
SHOW_TEXT = True
PLAY_SPEECH = True

# ── TTS ────────────────────────────────────────────────────────────────────────
# TTS_MODE (only relevant when ENABLE_TTS = True):
#   "server" → server speaks directly through its own speakers (default).
#   "client" → client receives llm_token stream and speaks locally.
TTS_MODE = "server"

# Server TTS backend (only used when TTS_MODE = "server")
#   "native"  — macOS `say` command, works out of the box.
#   "kokoro"  — neural voice, requires: pip install kokoro-onnx
TTS_SERVER_BACKEND = "native"

# Client TTS engine (only used when TTS_MODE = "client")
#   "native"  — macOS say-based player.
#   "kokoro"  — neural voice.
TTS_ENGINE = "native"

# Native TTS settings
TTS_RATE = 170  # words per minute — 160-180 sounds most natural
TTS_VOLUME = 1.0  # 0.0 – 1.0
TTS_VOICE_INDEX = 138  # 138=Samantha | 86=Karen (AU) | 171=Tessa | 112=Reed (♂)

# Kokoro TTS settings
# Voices: af_heart, af_bella, af_sarah, am_adam, am_michael,
#         bf_emma, bf_isabella, bm_george, bm_lewis
TTS_KOKORO_VOICE = "af_heart"
TTS_KOKORO_SPEED = 1.0  # 0.5=slow  1.0=normal  1.3=fast
