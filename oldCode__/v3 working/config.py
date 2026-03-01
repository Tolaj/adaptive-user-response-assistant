"""
═══════════════════════════════════════════════════════════════
VOICE-ENABLED LLM SERVER - CONFIGURATION
═══════════════════════════════════════════════════════════════
Edit these settings to customize your server

Quick Start Guide:
1. Set WHISPER_MODEL_NAME to the model file you have (base, tiny, large-v2)
2. Set ACTIVE_LLM_MODEL to your preferred LLM (qwen2.5-3b recommended)
3. Adjust GPU_LAYERS based on your VRAM (lower = more RAM for Whisper)
4. Run: python voice_server.py
"""

import os
from pathlib import Path
import torch

# ═══════════════════════════════════════════════════════════════
# QUICK SETTINGS - CHANGE THESE!
# ═══════════════════════════════════════════════════════════════

# Which Whisper model to use (change this to match your downloaded file)
WHISPER_MODEL_NAME = (
    "base"  # Options: "tiny", "base", "small", "medium", "large-v2", "large-v3"
)

# Auto-detect best available device
if torch.cuda.is_available():
    WHISPER_DEVICE = "cuda"
elif torch.backends.mps.is_available():
    WHISPER_DEVICE = "mps"
else:
    WHISPER_DEVICE = "cpu"

# Which LLM model to load on startup
ACTIVE_LLM_MODEL = (
    "qwen2.5-3b"  # Options: "qwen2.5-3b", "qwen2.5-7b", "qwen2.5-coder-7b"
)

# GPU layers (lower = more RAM left for Whisper)
GPU_LAYERS = 20  # Range: 0-35. Try 15-20 if out of memory, 25-30 if you have plenty

# Server port
SERVER_PORT = 5001

# ═══════════════════════════════════════════════════════════════
# PATHS (Auto-detected, usually don't need to change)
# ═══════════════════════════════════════════════════════════════

BASE_DIR = Path(__file__).parent
MODELS_DIR = BASE_DIR / "../../models"
WHISPER_DIR = MODELS_DIR / "whisper"


# ═══════════════════════════════════════════════════════════════
# WHISPER (SPEECH-TO-TEXT) SETTINGS
# ═══════════════════════════════════════════════════════════════

# Full path to your Whisper model file
WHISPER_MODEL_PATH = WHISPER_DIR / f"{WHISPER_MODEL_NAME}.pt"

# Whisper model info (for reference):
WHISPER_MODEL_INFO = {
    "tiny": {"size": "75MB", "speed": "⚡⚡⚡", "accuracy": "⭐⭐"},
    "base": {"size": "142MB", "speed": "⚡⚡", "accuracy": "⭐⭐⭐"},
    "small": {"size": "466MB", "speed": "⚡", "accuracy": "⭐⭐⭐⭐"},
    "medium": {"size": "1.5GB", "speed": "🐢", "accuracy": "⭐⭐⭐⭐⭐"},
    "large-v2": {"size": "2.9GB", "speed": "🐢🐢", "accuracy": "⭐⭐⭐⭐⭐"},
}


# ═══════════════════════════════════════════════════════════════
# LLM (LANGUAGE MODEL) SETTINGS
# ═══════════════════════════════════════════════════════════════

# Available LLM models
AVAILABLE_LLM_MODELS = {
    "qwen2.5-3b": "Qwen2.5-3B-Instruct",  # Smallest, fastest
    "qwen2.5-7b": "Qwen2.5-7B-Instruct",  # Better quality
    "qwen2.5-coder-7b": "qwen2.5-coder-7b",  # Best for code
    "qwen2.5-vl-3b": "Qwen2.5-VL-3B-Instruct",  # Vision + text (small)
    "qwen2.5-vl-7b": "qwen2.5-vl-7b",  # Vision + text (better)
}

# Context window size (how much text the model remembers)
CONTEXT_SIZE = 20000

# CPU threads (auto: half of your cores)
CPU_THREADS = max(1, os.cpu_count() // 2)


# ═══════════════════════════════════════════════════════════════
# TEXT-TO-SPEECH SETTINGS
# ═══════════════════════════════════════════════════════════════

DEFAULT_TTS_LANGUAGE = "en"  # Default language code
DEFAULT_TTS_SPEED = 1.0  # 1.0 = normal, 0.8 = slower, 1.2 = faster

# Supported TTS languages
TTS_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "ru": "Russian",
    "ar": "Arabic",
    "hi": "Hindi",
}


# ═══════════════════════════════════════════════════════════════
# VOICE CHAT SETTINGS
# ═══════════════════════════════════════════════════════════════

# System prompt for voice assistant
VOICE_ASSISTANT_PROMPT = (
    "You are a helpful voice assistant. Keep responses concise and conversational."
)

# Max tokens for voice responses (shorter = faster)
VOICE_MAX_TOKENS = 512

# Temperature for voice responses (0.0 = deterministic, 1.0 = creative)
VOICE_TEMPERATURE = 0.7


# ═══════════════════════════════════════════════════════════════
# PERFORMANCE TUNING
# ═══════════════════════════════════════════════════════════════

# LLM performance settings
LLM_FLASH_ATTN = True  # Enable flash attention (faster)
LLM_F16_KV = True  # Use FP16 for key/value cache
LLM_OFFLOAD_KQV = True  # Offload KQV to GPU
LLM_BATCH_SIZE = 1024  # Batch size for processing

# Allow environment variable overrides
GPU_LAYERS = int(os.getenv("GPU_LAYERS", GPU_LAYERS))
ACTIVE_LLM_MODEL = os.getenv("MODEL", ACTIVE_LLM_MODEL)
WHISPER_MODEL_NAME = os.getenv("WHISPER_MODEL", WHISPER_MODEL_NAME)


# ═══════════════════════════════════════════════════════════════
# MEMORY OPTIMIZATION PRESETS
# ═══════════════════════════════════════════════════════════════

# Uncomment one of these presets if you're having memory issues:

# PRESET 1: Low Memory (8GB RAM + 4GB VRAM)
# WHISPER_MODEL_NAME = "tiny"
# ACTIVE_LLM_MODEL = "qwen2.5-3b"
# GPU_LAYERS = 10

# PRESET 2: Medium Memory (16GB RAM + 8GB VRAM)
# WHISPER_MODEL_NAME = "base"
# ACTIVE_LLM_MODEL = "qwen2.5-3b"
# GPU_LAYERS = 20

# PRESET 3: High Memory (32GB RAM + 12GB+ VRAM)
# WHISPER_MODEL_NAME = "base"
# ACTIVE_LLM_MODEL = "qwen2.5-7b"
# GPU_LAYERS = 30


# ═══════════════════════════════════════════════════════════════
# VALIDATION
# ═══════════════════════════════════════════════════════════════


def validate_config():
    """Validate configuration and show warnings"""
    errors = []
    warnings = []

    # Check if Whisper model exists
    if not WHISPER_MODEL_PATH.exists():
        errors.append(f"Whisper model not found: {WHISPER_MODEL_PATH}")
        warnings.append(
            f"Download from: https://openaipublic.azureedge.net/main/whisper/models/"
        )

    # Check if LLM model directory exists
    llm_dir = MODELS_DIR / ACTIVE_LLM_MODEL
    if not llm_dir.exists():
        errors.append(f"LLM model directory not found: {llm_dir}")

    # Memory warnings
    if WHISPER_MODEL_NAME in ["large-v2", "large-v3"] and GPU_LAYERS > 25:
        warnings.append(
            "Using large Whisper + high GPU layers may cause out-of-memory errors"
        )
        warnings.append("Try reducing GPU_LAYERS to 15-20")

    return errors, warnings


# ═══════════════════════════════════════════════════════════════
# DISPLAY CONFIG (for debugging)
# ═══════════════════════════════════════════════════════════════


def print_config():
    """Print current configuration"""
    print("\n" + "=" * 60)
    print("CONFIGURATION")
    print("=" * 60)
    print(f"📁 Models directory: {MODELS_DIR}")
    print(
        f"🎤 Whisper model: {WHISPER_MODEL_NAME} ({WHISPER_MODEL_PATH.name if WHISPER_MODEL_PATH.exists() else 'NOT FOUND'})"
    )
    print(f"🤖 LLM model: {ACTIVE_LLM_MODEL}")
    print(f"🎮 GPU layers: {GPU_LAYERS}")
    print(f"💾 Context size: {CONTEXT_SIZE}")
    print(f"🧵 CPU threads: {CPU_THREADS}")
    print(f"🔊 TTS language: {DEFAULT_TTS_LANGUAGE}")
    print(f"🌐 Server port: {SERVER_PORT}")
    print("=" * 60)

    # Show warnings
    errors, warnings = validate_config()
    if errors:
        print("\n❌ ERRORS:")
        for error in errors:
            print(f"   {error}")
    if warnings:
        print("\n⚠️  WARNINGS:")
        for warning in warnings:
            print(f"   {warning}")
    print()
