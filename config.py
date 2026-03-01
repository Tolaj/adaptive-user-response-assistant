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
GPU_LAYERS = 36  # -1 = all layers on Metal GPU
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
SILENCE_THRESHOLD = 0.035  # was 0.008
SILENCE_DURATION = 1.8  # was 0.5
MIN_SPEECH = 0.8  # was 0.3
ROLLING_WINDOW_SEC = 8.0

# ── Feature toggles ───────────────────────────────────────────────────────────
# ENABLE_STT : True  → mic captured, sent to server, Whisper runs normally.
#              False → voice input disabled; server skips loading Whisper.
ENABLE_STT = True

# ENABLE_TTS : True  → AI responses are spoken aloud.
#              False → text-only; no TTS engine created anywhere.
ENABLE_TTS = True

# ── Output mode ───────────────────────────────────────────────────────────────
# SHOW_TEXT : True  → response text is streamed to the client terminal.
SHOW_TEXT = True

# ── TTS mode ──────────────────────────────────────────────────────────────────
# TTS_MODE (only relevant when ENABLE_TTS = True):
#   "server" → server speaks through its own speakers.
#   "client" → client receives llm_token stream and speaks locally.
TTS_MODE = "server"
TTS_SERVER_BACKEND = "supertonic2"  # "supertonic2" or "vibevoice"
# ── TTS backend ───────────────────────────────────────────────────────────────
# Supertonic 2 ONNX is used for all TTS (server and client).
# Requires: pip install onnxruntime transformers huggingface_hub sounddevice soundfile

# Voice presets : M1 M2 M3 M4 M5  F1 F2 F3 F4 F5
# Languages     : en  ko  es  pt  fr
SUPERTONIC_VOICE = "F1"  # voice preset
SUPERTONIC_LANGUAGE = "en"  # language tag
SUPERTONIC_STEPS = 15  # denoising steps — more = higher quality (max 50)
SUPERTONIC_SPEED = 1.2  # 0.5 = slow · 1.0 = normal · 1.3 = fast


# voice_client---------------------------

# ENERGY_THRESHOLD = 0.015  # too low, picks up breath/hum/keyboard
# MIN_SPEECH_SEC   = 0.4    # too short, sends noise bursts to Whisper
# PAUSE_SECONDS    = 1.5    # slightly short, cuts off trailing words

ENERGY_THRESHOLD = 0.035
MIN_SPEECH_SEC = 0.8
PAUSE_SECONDS = 1.8


# streaming_transcriber---------------------------

MIN_AUDIO_SEC = 0.8  # too short — Whisper hallucinates on short clips
NO_SPEECH_THRESHOLD = 0.45  # too lenient — still passes borderline audio
LOGPROB_THRESHOLD = -0.5  # default, not helping at all
TRANSCRIBE_EVERY = 1.0  # partials fire too fast, wastes Whisper cycles


# ===================== STT / VAD TUNING PARAMETERS =====================
#
# Parameter              | Old Value | New Value | Purpose
# ------------------------------------------------------------------------
# ENERGY_THRESHOLD       | 0.015     | 0.035     | Stops VAD triggering on background noise
# MIN_SPEECH_SEC         | 0.4       | 0.8       | Stops tiny noise bursts reaching Whisper
# PAUSE_SECONDS          | 1.5       | 1.8       | Prevents cutting off trailing words
# NO_SPEECH_THRESHOLD    | 0.6       | 0.45      | Stricter silence rejection
# logprob_threshold      | -1.0      | -0.5      | Rejects low-confidence guessed tokens
# MIN_AUDIO_SEC          | 0.4       | 0.8       | Rejects short clips (aligned with VAD)
# RMS gate (_get_audio)  | N/A       | Enabled   | Final defense before Whisper sees audio
# TRANSCRIBE_EVERY       | 0.6       | 1.0       | Fewer partial passes → less hallucination surface
#
# ====================================see it might need to change back====================================
