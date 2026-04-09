# PromptPack Output

**Root:** `/Users/swapnil/Documents/Projects/adaptive-user-response-assistant/config`
**Generated:** 2026-04-09T05:38:44.840Z

---

## 1) Folder Structure

```txt
.
├─ __init__.py
├─ __pycache__/
│  ├─ __init__.cpython-311.pyc
│  ├─ __init__.cpython-313.pyc
│  ├─ agent.cpython-311.pyc
│  ├─ features.cpython-311.pyc
│  ├─ features.cpython-313.pyc
│  ├─ llm.cpython-311.pyc
│  ├─ llm.cpython-313.pyc
│  ├─ orpheus.cpython-313.pyc
│  ├─ paths.cpython-311.pyc
│  ├─ paths.cpython-313.pyc
│  ├─ prompt.cpython-311.pyc
│  ├─ prompt.cpython-313.pyc
│  ├─ qwen_tts.cpython-313.pyc
│  ├─ server.cpython-311.pyc
│  ├─ server.cpython-313.pyc
│  ├─ tts.cpython-311.pyc
│  ├─ tts.cpython-313.pyc
│  ├─ vad.cpython-311.pyc
│  ├─ vad.cpython-313.pyc
│  ├─ vision.cpython-313.pyc
│  ├─ vlm.cpython-311.pyc
│  ├─ vlm.cpython-313.pyc
│  ├─ whisper.cpython-311.pyc
│  └─ whisper.cpython-313.pyc
├─ features.py
├─ llm.py
├─ paths.py
├─ prompt.py
├─ server.py
├─ tts.py
├─ vad.py
└─ whisper.py
```

<!-- PAGE BREAK: FILE CONTENTS BELOW -->

## 2) File Contents


### __init__.py

```python
from config.paths import (
    BASE_DIR,
    MODELS_DIR,
    LOGS_DIR,
    WHISPER_DIR,
    LLM_DIR,
    SUPERTONIC_DIR,
)
from config.whisper import WHISPER_MODEL_NAME, WHISPER_SAMPLE_RATE, WHISPER_DEVICE
from config.llm import ACTIVE_LLM_MODEL, GPU_LAYERS, CONTEXT_SIZE, CPU_THREADS
from config.tts import (
    TTS_MODE,
    TTS_SERVER_BACKEND,
    SUPERTONIC_VOICE,
    SUPERTONIC_LANGUAGE,
    SUPERTONIC_STEPS,
    SUPERTONIC_SPEED,
)
from config.vad import (
    RECORD_SAMPLE_RATE,
    SILENCE_THRESHOLD,
    SILENCE_DURATION,
    MIN_SPEECH,
    ROLLING_WINDOW_SEC,
    ENERGY_THRESHOLD,
    MIN_SPEECH_SEC,
    PAUSE_SECONDS,
    MIN_AUDIO_SEC,
    NO_SPEECH_THRESHOLD,
    LOGPROB_THRESHOLD,
    TRANSCRIBE_EVERY,
    COMPRESSION_RATIO_THRESHOLD,
)
from config.server import SERVER_PORT, SERVER_HOST
from config.features import ENABLE_STT, ENABLE_TTS, SHOW_TEXT
from config.prompt import (
    VOICE_SYSTEM_PROMPT,
    VOICE_MAX_TOKENS,
    VOICE_TEMPERATURE,
    VOICE_MAX_HISTORY_TURNS,
)

```

### __pycache__/__init__.cpython-311.pyc

(Skipped: binary or unreadable file)


### __pycache__/__init__.cpython-313.pyc

(Skipped: binary or unreadable file)


### __pycache__/agent.cpython-311.pyc

(Skipped: binary or unreadable file)


### __pycache__/features.cpython-311.pyc

(Skipped: binary or unreadable file)


### __pycache__/features.cpython-313.pyc

(Skipped: binary or unreadable file)


### __pycache__/llm.cpython-311.pyc

(Skipped: binary or unreadable file)


### __pycache__/llm.cpython-313.pyc

(Skipped: binary or unreadable file)


### __pycache__/orpheus.cpython-313.pyc

(Skipped: binary or unreadable file)


### __pycache__/paths.cpython-311.pyc

(Skipped: binary or unreadable file)


### __pycache__/paths.cpython-313.pyc

(Skipped: binary or unreadable file)


### __pycache__/prompt.cpython-311.pyc

(Skipped: binary or unreadable file)


### __pycache__/prompt.cpython-313.pyc

(Skipped: binary or unreadable file)


### __pycache__/qwen_tts.cpython-313.pyc

(Skipped: binary or unreadable file)


### __pycache__/server.cpython-311.pyc

(Skipped: binary or unreadable file)


### __pycache__/server.cpython-313.pyc

(Skipped: binary or unreadable file)


### __pycache__/tts.cpython-311.pyc

(Skipped: binary or unreadable file)


### __pycache__/tts.cpython-313.pyc

(Skipped: binary or unreadable file)


### __pycache__/vad.cpython-311.pyc

(Skipped: binary or unreadable file)


### __pycache__/vad.cpython-313.pyc

(Skipped: binary or unreadable file)


### __pycache__/vision.cpython-313.pyc

(Skipped: binary or unreadable file)


### __pycache__/vlm.cpython-311.pyc

(Skipped: binary or unreadable file)


### __pycache__/vlm.cpython-313.pyc

(Skipped: binary or unreadable file)


### __pycache__/whisper.cpython-311.pyc

(Skipped: binary or unreadable file)


### __pycache__/whisper.cpython-313.pyc

(Skipped: binary or unreadable file)


### features.py

```python
# config/features.py
# ── Mode selector ─────────────────────────────────────────────
# Pick ONE mode:
#   "server"                → Flask + WebSocket server only
#   "stt_only"              → Mic → Whisper, print transcript
#   "tts_only"              → Type text → speak it aloud
#   "text_to_text_chat"     → Type text → LLM → print response (no audio)
#   "voice_to_text_chat"    → Mic → Whisper → LLM → print response (no TTS)
#   "full"                  → Mic → Whisper → LLM → TTS (everything)

MODE = "full"

# ── Derived flags (do not edit) ───────────────────────────────
ENABLE_STT = MODE in ("stt_only", "voice_to_text_chat", "full")
ENABLE_TTS = MODE in ("tts_only", "full")
ENABLE_LLM = MODE in ("text_to_text_chat", "voice_to_text_chat", "full", "tts_only")
ENABLE_SERVER = MODE == "server"
SHOW_TEXT = True

```

### llm.py

```python
import os

ACTIVE_LLM_MODEL = "qwen2.5-3b"
LLM_REPO_ID = "Qwen/Qwen2.5-3B-Instruct-GGUF"
LLM_FILENAME = "qwen2.5-3b-instruct-q4_k_m.gguf"

GPU_LAYERS = 36
CONTEXT_SIZE = 2048
CPU_THREADS = max(1, os.cpu_count() // 2)

```

### paths.py

```python
# config/paths.py
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
MODELS_DIR = BASE_DIR / "models"
LOGS_DIR = BASE_DIR / "logs"
WHISPER_DIR = MODELS_DIR / "whisper"
LLM_DIR = MODELS_DIR / "llm"
SUPERTONIC_DIR = MODELS_DIR / "supertonic"

for _d in (LOGS_DIR, MODELS_DIR, WHISPER_DIR, LLM_DIR, SUPERTONIC_DIR):
    _d.mkdir(parents=True, exist_ok=True)

```

### prompt.py

```python
# config/prompt.py
VOICE_SYSTEM_PROMPT = (
    "You are a concise voice assistant. "
    "Reply in 1 sentence, 10 words max. "
    "Never use lists or markdown."
)
VOICE_MAX_TOKENS = 60  # was 150 — prevents long multi-chunk responses
VOICE_TEMPERATURE = 0.7
VOICE_MAX_HISTORY_TURNS = 10

```

### server.py

```python
SERVER_PORT = 5001
SERVER_HOST = "0.0.0.0"

```

### tts.py

```python
# config/tts.py
TTS_MODE = "server"
TTS_SERVER_BACKEND = "supertonic2"

SUPERTONIC_VOICE = "F1"
SUPERTONIC_LANGUAGE = "en"
SUPERTONIC_STEPS = 10  # was 15 → benchmark: 685ms first chunk avg
SUPERTONIC_SPEED = 1
ENABLE_FILLER = False

# Speech smoothness — how text is chunked before TTS generation
# Higher WORD_FLUSH_THRESHOLD = fewer, longer chunks = smoother but slightly more latency
# Lower  WORD_FLUSH_THRESHOLD = more, shorter chunks = faster first word but choppier
WORD_FLUSH_THRESHOLD = 10  # words buffered before a mid-sentence force-flush

# Minimum chars a sentence-split piece must be before it's sent standalone
# Lower = more splits (choppier), Higher = fewer splits (smoother)
MIN_SEND_CHARS = 35

# How long the worker waits to merge back-to-back chunks into one generation call
# Higher = smoother (fewer ONNX calls), but adds that many ms of latency per chunk
MERGE_WINDOW_SEC = 0.04

```

### vad.py

```python
# config/vad.py
RECORD_SAMPLE_RATE = 44100
PREROLL_SECONDS = 0.25
SILENCE_THRESHOLD = 0.02
SILENCE_DURATION = 0.6
MIN_SPEECH = 0.3
ROLLING_WINDOW_SEC = 8.0

ENERGY_THRESHOLD = (
    0.025  # Increased: rejects background music, needs stronger signal for speech
)
MIN_SPEECH_SEC = (
    0.25  # Increased: requires longer speech burst (music pauses are short)
)
PAUSE_SECONDS = 0.65

MIN_AUDIO_SEC = 0.30
NO_SPEECH_THRESHOLD = (
    0.45  # Increased: Whisper requires higher confidence (rejects music hallucinations)
)
LOGPROB_THRESHOLD = (
    -0.8  # Increased (less negative): stricter confidence for transcription acceptance
)
TRANSCRIBE_EVERY = 0.8
COMPRESSION_RATIO_THRESHOLD = (
    2.0  # Lowered: more aggressive at rejecting repetitive content (music)
)

SILERO_THRESHOLD = 0.45  # was 0.5 — only triggers on high-confidence speech

DENOISE_ENABLED = False

```

### whisper.py

```python
# config/whisper.py
import torch

WHISPER_MODEL_NAME = "base"
WHISPER_SAMPLE_RATE = 16000


def _resolve_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


WHISPER_DEVICE = _resolve_device()
print(f"[Config] Whisper device: {WHISPER_DEVICE}")

```