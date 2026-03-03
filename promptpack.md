# PromptPack Output

**Root:** `/Users/swapnil/Documents/Projects/adaptive-user-response-assistant`
**Generated:** 2026-03-02T23:12:05.324Z

---

## 1) Folder Structure

```txt
.
├─ ARCHITECTURE.md
├─ audio/
│  ├─ __init__.py
│  ├─ gate/
│  │  ├─ __init__.py
│  │  ├─ amplitude.py
│  │  ├─ rms.py
│  │  └─ zcr.py
│  ├─ io/
│  │  ├─ __init__.py
│  │  ├─ mic.py
│  │  ├─ read.py
│  │  └─ write.py
│  └─ transform/
│     ├─ __init__.py
│     ├─ mono.py
│     ├─ normalise.py
│     └─ resample.py
├─ backup/
├─ config/
│  ├─ __init__.py
│  ├─ features.py
│  ├─ llm.py
│  ├─ paths.py
│  ├─ prompt.py
│  ├─ server.py
│  ├─ tts.py
│  ├─ vad.py
│  └─ whisper.py
├─ llm/
│  ├─ __init__.py
│  ├─ download/
│  │  ├─ __init__.py
│  │  ├─ hf.py
│  │  └─ resolver.py
│  ├─ history/
│  │  ├─ __init__.py
│  │  ├─ add.py
│  │  ├─ clear.py
│  │  ├─ read.py
│  │  ├─ state.py
│  │  └─ trim.py
│  ├─ inference/
│  │  ├─ __init__.py
│  │  ├─ error.py
│  │  ├─ params.py
│  │  └─ stream.py
│  ├─ model/
│  │  ├─ __init__.py
│  │  ├─ load.py
│  │  └─ singleton.py
│  └─ prompt/
│     ├─ __init__.py
│     ├─ build.py
│     └─ system.py
├─ logs/
├─ main.py
├─ requirements.txt
├─ server/
│  ├─ __init__.py
│  ├─ app.py
│  ├─ logger.py
│  ├─ routes/
│  │  ├─ __init__.py
│  │  ├─ health.py
│  │  ├─ transcribe.py
│  │  └─ websocket.py
│  └─ ws/
│     ├─ __init__.py
│     ├─ handler.py
│     ├─ pipeline/
│     │  ├─ __init__.py
│     │  ├─ eos.py
│     │  └─ llm_runner.py
│     ├─ receive/
│     │  ├─ __init__.py
│     │  ├─ audio.py
│     │  ├─ commands.py
│     │  └─ router.py
│     ├─ send/
│     │  ├─ __init__.py
│     │  ├─ core.py
│     │  ├─ llm.py
│     │  ├─ stt.py
│     │  └─ tts.py
│     └─ session/
│        ├─ __init__.py
│        ├─ create.py
│        └─ teardown.py
├─ transcription/
│  ├─ __init__.py
│  ├─ download/
│  │  ├─ __init__.py
│  │  └─ whisper.py
│  ├─ hallucination/
│  │  ├─ __init__.py
│  │  ├─ confidence.py
│  │  ├─ noise.py
│  │  └─ repetition.py
│  ├─ model/
│  │  ├─ __init__.py
│  │  ├─ device.py
│  │  ├─ load.py
│  │  ├─ lock.py
│  │  └─ singleton.py
│  ├─ stream/
│  │  ├─ __init__.py
│  │  ├─ buffer.py
│  │  ├─ final.py
│  │  ├─ partial.py
│  │  └─ worker.py
│  ├─ transcribe/
│  │  ├─ __init__.py
│  │  ├─ batch.py
│  │  └─ options.py
│  └─ vad/
│     ├─ __init__.py
│     ├─ energy.py
│     ├─ processor.py
│     ├─ session.py
│     └─ state.py
├─ tts/
│  ├─ __init__.py
│  ├─ download/
│  │  ├─ __init__.py
│  │  └─ supertonic.py
│  ├─ engine/
│  │  ├─ __init__.py
│  │  ├─ control.py
│  │  ├─ feed.py
│  │  ├─ queue.py
│  │  ├─ state.py
│  │  ├─ status.py
│  │  └─ worker.py
│  ├─ generate/
│  │  ├─ __init__.py
│  │  ├─ canvas.py
│  │  ├─ decode.py
│  │  ├─ denoise.py
│  │  ├─ encode.py
│  │  ├─ pad.py
│  │  └─ pipeline.py
│  ├─ model/
│  │  ├─ __init__.py
│  │  ├─ load.py
│  │  ├─ singleton.py
│  │  └─ voices.py
│  ├─ playback/
│  │  ├─ __init__.py
│  │  ├─ stop.py
│  │  └─ stream.py
│  └─ text/
│     ├─ __init__.py
│     ├─ clean.py
│     ├─ normalise.py
│     └─ split.py
└─ ui/
   ├─ __init__.py
   └─ console.py
```

<!-- PAGE BREAK: FILE CONTENTS BELOW -->

## 2) File Contents


### ARCHITECTURE.md

```markdown


# Adaptive Assistant Architecture Guide

## CRITICAL FILE: config/vad.py

This is THE most important file for fixing STT (speech-to-text) problems.

### Quick Parameter Reference

| Parameter | Default | Problem | Solution |
|-----------|---------|---------|----------|
| ENERGY_THRESHOLD | 0.045 | Hallucinating | Increase to 0.06-0.10 |
| NO_SPEECH_THRESHOLD | 0.92 | "I'm sorry" on silence | Increase to 0.94-0.98 |
| LOGPROB_THRESHOLD | -0.4 | Low confidence outputs | Make less negative: -0.2 to 0.0 |
| PREROLL_SECONDS | 0.15 | First word clipped | Increase to 0.20-0.30 |
| MIN_SPEECH_SEC | 0.48 | Missing words | Decrease to 0.25-0.35 |
| MIN_AUDIO_SEC | 0.65 | Short hallucinations | Increase to 0.80-1.0 |
| COMPRESSION_RATIO_THRESHOLD | 1.5 | Music transcribing | Decrease to 0.8-1.2 |
| TRANSCRIBE_EVERY | 0.6 | Slow feedback | Decrease to 0.3-0.4 |

---

## Key Configuration Files (In Priority Order)

### 1. config/vad.py (CRITICAL - STT Quality)
File: `/Users/swapnil/Documents/Projects/adaptive-user-response-assistant/config/vad.py`

**What it controls:**
- VAD (Voice Activity Detection) sensitivity → when to start/stop transcription
- Whisper confidence thresholds → accept/reject transcriptions
- Preroll buffer → capture audio before speech detected

**To fix:**

**Hallucinating on silence:**
\`\`\`python
NO_SPEECH_THRESHOLD = 0.96        # was 0.92
LOGPROB_THRESHOLD = -0.2          # was -0.4  
COMPRESSION_RATIO_THRESHOLD = 1.0 # was 1.5
\`\`\`

**Missing words from real speech:**
\`\`\`python
ENERGY_THRESHOLD = 0.03        # was 0.045
MIN_SPEECH_SEC = 0.35          # was 0.48
PREROLL_SECONDS = 0.25         # was 0.15
\`\`\`

**Background music transcribing:**
\`\`\`python
COMPRESSION_RATIO_THRESHOLD = 0.8  # was 1.5
NO_SPEECH_THRESHOLD = 0.95         # was 0.92
ENERGY_THRESHOLD = 0.07            # was 0.045
\`\`\`

---

### 2. config/features.py (Mode Selection)
File: `/Users/swapnil/Documents/Projects/adaptive-user-response-assistant/config/features.py`

**What it controls:**
- Which mode to run: stt_only, tts_only, text_to_text_chat, voice_to_text_chat, full, server

**To change mode:**
\`\`\`python
MODE = "voice_to_text_chat"  # Change to: "stt_only", "tts_only", "full", etc.
\`\`\`

---

### 3. config/llm.py (LLM Quality)
File: `/Users/swapnil/Documents/Projects/adaptive-user-response-assistant/config/llm.py`

**What it controls:**
- TEMPERATURE: 0.0=boring, 1.0+=creative
- n_ctx: context size (2048=default, reduce to 1024 for speed)
- MODEL_PATH: which LLM to use

**To make responses more creative:**
\`\`\`python
TEMPERATURE = 1.2  # was 0.7
\`\`\`

**To speed up LLM:**
\`\`\`python
N_CTX = 1024  # was 2048
\`\`\`

---

### 4. config/tts.py (TTS Voice)
File: `/Users/swapnil/Documents/Projects/adaptive-user-response-assistant/config/tts.py`

**What it controls:**
- SUPERTONIC_SPEED: 0.5=slow, 1.0=normal, 1.5=fast
- SUPERTONIC_STEPS: 50=fast/lower quality, 150=slow/best quality
- SUPERTONIC_VOICE: which voice to use

**To make TTS slower & clearer:**
\`\`\`python
SUPERTONIC_SPEED = 0.7    # was 1.0
SUPERTONIC_STEPS = 120    # was 100
\`\`\`

**To make TTS faster:**
\`\`\`python
SUPERTONIC_SPEED = 1.3    # was 1.0
SUPERTONIC_STEPS = 50     # was 100
\`\`\`

---

## All Files & What They Do

### Entry Point
- **main.py** — Determines which mode to run
  - Imports MODE from config/features.py
  - Calls _run_stt_only(), _run_voice_chat(), _run_full(), etc.

### Configuration (Edit These To Tune)
- **config/features.py** — MODE selection
- **config/vad.py** — Speech detection tuning (CRITICAL!)
- **config/llm.py** — LLM settings (temperature, context size)
- **config/tts.py** — TTS settings (speed, quality, voice)
- **config/whisper.py** — Whisper STT settings
- **config/server.py** — Server settings

### Microphone & Audio (Understand These)
- **audio/io/mic.py** — Opens mic at 44.1kHz
- **audio/transform/resample.py** — Converts 44.1kHz → 16kHz (MUST NOT REMOVE!)
- **transcription/vad/session.py** — Mic loop with VAD & preroll
- **transcription/vad/processor.py** — Detects speech vs silence
- **transcription/vad/energy.py** — RMS + ZCR algorithm

### Whisper (Speech-to-Text)
- **transcription/stream/buffer.py** — Buffers 16kHz audio
- **transcription/stream/worker.py** — Thread that transcribes periodically
- **transcription/stream/partial.py** — Real-time streaming text
- **transcription/stream/final.py** — Final transcription (when speech ends)
- **transcription/hallucination/confidence.py** — Filters by Whisper confidence
- **transcription/hallucination/repetition.py** — Filters repetitive/music audio

### LLM (Language Model)
- **llm/model/singleton.py** — Load Qwen once
- **llm/inference/stream.py** — Stream tokens
- **llm/history/state.py** — Keep conversation context

### TTS (Text-to-Speech)
- **tts/model/singleton.py** — Load Supertonic once
- **tts/engine/worker.py** — Generate audio from tokens
- **tts/engine/control.py** — interrupt, resume, speak_filler

### Utilities
- **ui/console.py** — Colored terminal output
- **server/logger.py** — Log to file with latency metrics

---

## 6 Operating Modes

Change MODE in config/features.py to switch:

- **stt_only** — Speak → Whisper → Text (test STT)
- **tts_only** — Type → TTS → Speaker (test TTS)
- **text_to_text_chat** — Type → LLM → Type (test LLM)
- **voice_to_text_chat** — Speak → Whisper → LLM → Type
- **full** — Speak → Whisper → LLM → TTS → Speaker (complete voice loop)
- **server** — WebSocket API server

---

## Common Fixes

### Fix 1: Stop Hallucinating "I'm sorry", "Thank you", "Okay"
**File:** config/vad.py
**Changes:**
\`\`\`python
NO_SPEECH_THRESHOLD = 0.98        # Increase from 0.92
LOGPROB_THRESHOLD = 0.0           # Increase from -0.4
COMPRESSION_RATIO_THRESHOLD = 0.8 # Decrease from 1.5
\`\`\`

### Fix 2: Capture First Word (Not Clipped)
**File:** config/vad.py
**Changes:**
\`\`\`python
PREROLL_SECONDS = 0.25  # Increase from 0.15
\`\`\`

### Fix 3: Don't Miss Words from Real Speech
**File:** config/vad.py
**Changes:**
\`\`\`python
ENERGY_THRESHOLD = 0.03   # Decrease from 0.045
MIN_SPEECH_SEC = 0.35     # Decrease from 0.48
\`\`\`

### Fix 4: Stop Music Being Transcribed
**File:** config/vad.py
**Changes:**
\`\`\`python
COMPRESSION_RATIO_THRESHOLD = 0.8  # Decrease from 1.5
NO_SPEECH_THRESHOLD = 0.95         # Increase from 0.92
\`\`\`

### Fix 5: More Creative LLM
**File:** config/llm.py
**Changes:**
\`\`\`python
TEMPERATURE = 1.2  # Increase from 0.7
\`\`\`

### Fix 6: Faster LLM Response
**File:** config/llm.py
**Changes:**
\`\`\`python
N_CTX = 1024  # Decrease from 2048
\`\`\`

### Fix 7: Better TTS Quality
**File:** config/tts.py
**Changes:**
\`\`\`python
SUPERTONIC_STEPS = 120  # Increase from 100
SUPERTONIC_SPEED = 0.7  # Decrease from 1.0
\`\`\`

---

## Logging & Metrics

Each interaction is logged to: `logs/conversation_YYYY-MM-DD_HH-MM-SS.log`

**Format:**
\`\`\`
[HH:MM:SS] #02  YOU:what user said  AI:what AI responded  whisper:1.206s  ft:0.348s  llm:2.514s  e2e:3.742s
\`\`\`

**Metrics:**
- **whisper:X.XXs** — Time for speech-to-text
- **ft:X.XXs** — Time until LLM gives first token
- **llm:X.XXs** — Time for full LLM response
- **e2e:X.XXs** — Total time from speech input to final response

---

## When to Use Each Mode

- **stt_only** — Testing mic quality and Whisper accuracy
- **tts_only** — Testing voice output quality
- **text_to_text_chat** — Testing LLM reasoning without audio
- **voice_to_text_chat** — Voice input, text output (quiet environments)
- **full** — Production mode (full voice assistant)
- **server** — Running as API server

---

## Quick Checklist for Problems

- [ ] Hallucinating on silence? → Increase NO_SPEECH_THRESHOLD in config/vad.py
- [ ] First word clipped? → Increase PREROLL_SECONDS in config/vad.py
- [ ] Missing words? → Decrease ENERGY_THRESHOLD in config/vad.py
- [ ] Music transcribing? → Decrease COMPRESSION_RATIO_THRESHOLD in config/vad.py
- [ ] Boring LLM? → Increase TEMPERATURE in config/llm.py
- [ ] Slow LLM? → Decrease N_CTX in config/llm.py
- [ ] Poor TTS? → Increase SUPERTONIC_STEPS in config/tts.py
- [ ] Slow TTS? → Decrease SUPERTONIC_STEPS in config/tts.py

```

### audio/__init__.py

```python
from audio.io.read import read_wav
from audio.io.write import write_wav
from audio.transform.mono import to_mono
from audio.transform.resample import resample
from audio.transform.normalise import normalise
from audio.gate.rms import rms
from audio.gate.amplitude import mean_amplitude
from audio.gate.zcr import zero_crossing_rate

```

### audio/gate/__init__.py

```python
from audio.gate.rms import rms
from audio.gate.amplitude import mean_amplitude
from audio.gate.zcr import zero_crossing_rate

```

### audio/gate/amplitude.py

```python
import numpy as np


def mean_amplitude(audio: np.ndarray) -> float:
    """Mean absolute amplitude."""
    return float(np.abs(audio.astype(np.float32)).mean())


if __name__ == "__main__":
    import numpy as np

    print(mean_amplitude(np.array([-0.5, 0.2, 0.8], dtype=np.float32)))

```

### audio/gate/rms.py

```python
import numpy as np


def rms(audio: np.ndarray) -> float:
    """Root mean square energy."""
    return float(np.sqrt(np.mean(audio.astype(np.float32) ** 2)))


if __name__ == "__main__":
    import numpy as np

    print(f"silence: {rms(np.zeros(1000)):.4f}")
    print(f"speech:  {rms(np.random.randn(1000).astype(np.float32) * 0.3):.4f}")

```

### audio/gate/zcr.py

```python
import numpy as np


def zero_crossing_rate(audio: np.ndarray) -> float:
    """Fraction of samples where sign changes."""
    if len(audio) <= 1:
        return 0.0
    return float(np.mean(np.abs(np.diff(np.sign(audio.astype(np.float32)))) / 2))


if __name__ == "__main__":
    import numpy as np

    tone = np.sin(np.linspace(0, 2 * np.pi * 10, 1000)).astype(np.float32)
    noise = np.random.randn(1000).astype(np.float32)
    print(
        f"tone ZCR: {zero_crossing_rate(tone):.4f}  noise ZCR: {zero_crossing_rate(noise):.4f}"
    )

```

### audio/io/__init__.py

```python
from audio.io.read import read_wav
from audio.io.write import write_wav
from audio.io.mic import open_mic

```

### audio/io/mic.py

```python
"""
audio/io/mic.py — Microphone input

Provides open_mic() which returns a MicStream object:

    mic = open_mic(callback)   # callback(chunk: np.ndarray) called per block
    mic.start()
    mic.stop()
    mic.close()

Uses sounddevice InputStream at RECORD_SAMPLE_RATE (44100 Hz) as set in
config/vad.py.  Delivers float32 chunks to the callback so SmartVAD and
the transcription pipeline can consume them directly.
"""

import threading
import numpy as np
import sounddevice as sd

from config.vad import RECORD_SAMPLE_RATE

# Chunk size: ~20 ms at the recording sample rate
_BLOCK_SIZE = int(RECORD_SAMPLE_RATE * 0.02)  # 882 samples @ 44100


class MicStream:
    """Thin wrapper around a sounddevice InputStream."""

    def __init__(self, callback):
        """
        Parameters
        ----------
        callback : callable(chunk: np.ndarray)
            Called from the audio thread with a float32 mono array for
            each captured block.
        """
        self._callback = callback
        self._stream: sd.InputStream | None = None
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def start(self) -> None:
        """Open and start the InputStream."""
        with self._lock:
            if self._stream is not None:
                return  # already running
            self._stream = sd.InputStream(
                samplerate=RECORD_SAMPLE_RATE,
                channels=1,
                dtype="float32",
                blocksize=_BLOCK_SIZE,
                callback=self._sd_callback,
            )
            self._stream.start()
            print(f"[Mic] Started — {RECORD_SAMPLE_RATE} Hz, block={_BLOCK_SIZE}")

    def stop(self) -> None:
        """Stop the stream (keeps device open for a clean close)."""
        with self._lock:
            if self._stream is not None:
                try:
                    self._stream.stop()
                except Exception:
                    pass

    def close(self) -> None:
        """Stop and release the audio device."""
        with self._lock:
            if self._stream is not None:
                try:
                    self._stream.stop()
                    self._stream.close()
                except Exception:
                    pass
                finally:
                    self._stream = None
                    print("[Mic] Closed.")

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _sd_callback(
        self,
        indata: np.ndarray,
        frames: int,
        time_info,
        status: sd.CallbackFlags,
    ) -> None:
        """sounddevice calls this from a dedicated C thread — keep it fast."""
        if status:
            print(f"[Mic] {status}", flush=True)
        chunk = indata[:, 0].copy()  # mono float32
        try:
            self._callback(chunk)
        except Exception as e:
            print(f"[Mic] callback error: {e}")


def open_mic(callback) -> MicStream:
    """
    Create a MicStream bound to `callback`.

    Parameters
    ----------
    callback : callable(chunk: np.ndarray)
        Receives a float32 mono ndarray for every ~20 ms block.

    Returns
    -------
    MicStream
        Call .start() to begin recording, .stop()/.close() to finish.
    """
    return MicStream(callback)

```

### audio/io/read.py

```python
import numpy as np
import soundfile as sf


def read_wav(path: str) -> tuple[np.ndarray, int]:
    """Read a WAV file. Returns (audio_array, sample_rate)."""
    audio, sr = sf.read(path)
    return audio, sr


if __name__ == "__main__":
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "test.wav"
    audio, sr = read_wav(path)
    print(f"Loaded: shape={audio.shape}, sr={sr}, dtype={audio.dtype}")

```

### audio/io/write.py

```python
import numpy as np
import soundfile as sf


def write_wav(audio: np.ndarray, path: str, sample_rate: int) -> str:
    """Write numpy array to WAV. Returns path."""
    sf.write(path, audio, sample_rate)
    return path


if __name__ == "__main__":
    import numpy as np

    audio = np.zeros(16000, dtype=np.float32)
    print(write_wav(audio, "/tmp/test_out.wav", 16000))

```

### audio/transform/__init__.py

```python
from audio.transform.mono import to_mono
from audio.transform.resample import resample
from audio.transform.normalise import normalise

```

### audio/transform/mono.py

```python
import numpy as np


def to_mono(audio: np.ndarray) -> np.ndarray:
    """Convert stereo/multi-channel to mono by averaging channels."""
    if len(audio.shape) > 1:
        return audio.mean(axis=1)
    return audio


if __name__ == "__main__":
    import numpy as np

    stereo = np.random.randn(16000, 2).astype(np.float32)
    print(f"stereo {stereo.shape} → mono {to_mono(stereo).shape}")

```

### audio/transform/normalise.py

```python
import numpy as np


def normalise(audio: np.ndarray) -> np.ndarray:
    """Peak-normalise to [-1, 1]. No-op if silent."""
    peak = np.abs(audio).max()
    if peak > 0:
        return (audio / peak).astype(np.float32)
    return audio.astype(np.float32)


if __name__ == "__main__":
    import numpy as np

    a = np.array([0.1, -0.5, 0.8], dtype=np.float32)
    print(f"before: {a}  after: {normalise(a)}")

```

### audio/transform/resample.py

```python
import numpy as np
import resampy


def resample(audio: np.ndarray, from_sr: int, to_sr: int) -> np.ndarray:
    """Resample audio. No-op if rates match."""
    if from_sr == to_sr:
        return audio.astype(np.float32)
    return resampy.resample(audio, from_sr, to_sr).astype(np.float32)


if __name__ == "__main__":
    import numpy as np

    a = np.random.randn(44100).astype(np.float32)
    r = resample(a, 44100, 16000)
    print(f"44100 ({len(a)}) → 16000 ({len(r)})")

```

### config/__init__.py

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

### config/features.py

```python
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

### config/llm.py

```python
import os

ACTIVE_LLM_MODEL = "qwen2.5-3b"
GPU_LAYERS = 36
CONTEXT_SIZE = 2048
CPU_THREADS = max(1, os.cpu_count() // 2)

```

### config/paths.py

```python
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

### config/prompt.py

```python
VOICE_SYSTEM_PROMPT = (
    "You are a helpful voice assistant. "
    "Keep responses short and conversational, 1-3 sentences max."
)
VOICE_MAX_TOKENS = 150
VOICE_TEMPERATURE = 0.7
VOICE_MAX_HISTORY_TURNS = 10

```

### config/server.py

```python
SERVER_PORT = 5001
SERVER_HOST = "0.0.0.0"

```

### config/tts.py

```python
TTS_MODE = "server"  # "server" | "client"
TTS_SERVER_BACKEND = "supertonic2"

SUPERTONIC_VOICE = "F1"
SUPERTONIC_LANGUAGE = "en"
SUPERTONIC_STEPS = 15
SUPERTONIC_SPEED = 1.2

```

### config/vad.py

```python
RECORD_SAMPLE_RATE = 44100
PREROLL_SECONDS = 0.15
SILENCE_THRESHOLD = 0.02
SILENCE_DURATION = 1.2
MIN_SPEECH = 0.45
ROLLING_WINDOW_SEC = 8.0

ENERGY_THRESHOLD = (
    0.055  # Increased: rejects background music, needs stronger signal for speech
)
MIN_SPEECH_SEC = (
    0.65  # Increased: requires longer speech burst (music pauses are short)
)
PAUSE_SECONDS = 1.2

MIN_AUDIO_SEC = 0.4
NO_SPEECH_THRESHOLD = (
    0.75  # Increased: Whisper requires higher confidence (rejects music hallucinations)
)
LOGPROB_THRESHOLD = (
    -0.3
)  # Increased (less negative): stricter confidence for transcription acceptance
TRANSCRIBE_EVERY = 0.6
COMPRESSION_RATIO_THRESHOLD = (
    1.8  # Lowered: more aggressive at rejecting repetitive content (music)
)

```

### config/whisper.py

```python
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

### llm/__init__.py

```python
from llm.model.singleton import get_model, is_loaded
from llm.inference.stream import stream_response
from llm.history.state import create_history
from llm.history.add import add_user, add_assistant
from llm.history.clear import clear_history

```

### llm/download/__init__.py

```python
from llm.download.resolver import find_gguf
from llm.download.hf import download_from_hf

```

### llm/download/hf.py

```python
import warnings
from pathlib import Path


def download_from_hf(repo_id: str, dest: Path, filename: str | None = None) -> Path:
    """Download model from HuggingFace Hub into dest/."""
    from huggingface_hub import snapshot_download, hf_hub_download

    dest.mkdir(parents=True, exist_ok=True)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        if filename:
            hf_hub_download(repo_id=repo_id, filename=filename, local_dir=str(dest))
        else:
            snapshot_download(repo_id=repo_id, local_dir=str(dest))
    print(f"[HF] {repo_id} → {dest}")
    return dest


if __name__ == "__main__":
    print("Usage: download_from_hf('org/model', Path('./models/llm/my-model'))")

```

### llm/download/resolver.py

```python
from pathlib import Path

_PREFERENCE = ["Q4_K_M", "Q4_K_S", "Q4", "Q5_K_M", "Q5", "Q8", "q4", "q5", "q8"]


def find_gguf(model_dir: Path) -> Path:
    """Find best GGUF in model_dir, preferring Q4_K_M → Q8."""
    if not model_dir.exists():
        raise FileNotFoundError(f"Model dir not found: {model_dir}")
    gguf_files = sorted(model_dir.glob("*.gguf"))
    if not gguf_files:
        raise FileNotFoundError(f"No .gguf in {model_dir}")
    for pref in _PREFERENCE:
        for f in gguf_files:
            if pref.lower() in f.name.lower():
                return f
    return gguf_files[0]


if __name__ == "__main__":
    from config.paths import LLM_DIR
    from config.llm import ACTIVE_LLM_MODEL

    try:
        print(find_gguf(LLM_DIR / ACTIVE_LLM_MODEL))
    except FileNotFoundError as e:
        print(e)

```

### llm/history/__init__.py

```python
from llm.history.state import create_history
from llm.history.add import add_user, add_assistant
from llm.history.clear import clear_history
from llm.history.read import get_messages

```

### llm/history/add.py

```python
from llm.history.trim import trim_history


def add_user(history: dict, text: str) -> None:
    history["turns"].append({"role": "user", "content": text})
    trim_history(history)


def add_assistant(history: dict, text: str) -> None:
    history["turns"].append({"role": "assistant", "content": text})
    trim_history(history)

```

### llm/history/clear.py

```python
def clear_history(history: dict) -> None:
    history["turns"] = []

```

### llm/history/read.py

```python
def get_messages(history: dict) -> list[dict]:
    from llm.prompt.system import get_system_prompt

    return [{"role": "system", "content": get_system_prompt()}] + history["turns"]

```

### llm/history/state.py

```python
from config.prompt import VOICE_MAX_HISTORY_TURNS


def create_history(max_turns: int = VOICE_MAX_HISTORY_TURNS) -> dict:
    return {"turns": [], "max_turns": max_turns}

```

### llm/history/trim.py

```python
def trim_history(history: dict) -> None:
    limit = history["max_turns"] * 2
    if len(history["turns"]) > limit:
        history["turns"] = history["turns"][-limit:]

```

### llm/inference/__init__.py

```python
from llm.inference.stream import stream_response
from llm.inference.params import build_inference_params
from llm.inference.error import handle_inference_error

```

### llm/inference/error.py

```python
def handle_inference_error(e: Exception) -> str:
    msg = f"[LLM error: {e}]"
    print(msg)
    return msg

```

### llm/inference/params.py

```python
from config.prompt import VOICE_MAX_TOKENS, VOICE_TEMPERATURE


def build_inference_params() -> dict:
    return {
        "max_tokens": VOICE_MAX_TOKENS,
        "temperature": VOICE_TEMPERATURE,
        "stream": True,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(build_inference_params(), indent=2))

```

### llm/inference/stream.py

```python
from typing import Generator

from llm.model.singleton import get_model
from llm.history.add import add_user, add_assistant
from llm.prompt.build import build_messages
from llm.inference.params import build_inference_params
from llm.inference.error import handle_inference_error


def stream_response(
    user_text: str,
    history: dict | None = None,
) -> Generator[str, None, None]:
    """Yield tokens one by one. Logs exchange to history if provided."""
    llm = get_model()
    if history:
        add_user(history, user_text)
    messages = build_messages(user_text, history)
    params = build_inference_params()
    full = ""
    try:
        for chunk in llm.create_chat_completion(messages=messages, **params):
            token = chunk["choices"][0]["delta"].get("content", "")
            if token:
                full += token
                yield token
    except Exception as e:
        err = handle_inference_error(e)
        yield err
        full = err
    if history and full:
        add_assistant(history, full)


if __name__ == "__main__":
    from llm.history.state import create_history

    h = create_history()
    print("Response: ", end="", flush=True)
    for tok in stream_response("Hello, who are you?", h):
        print(tok, end="", flush=True)
    print()

```

### llm/model/__init__.py

```python
from llm.model.singleton import get_model, is_loaded, get_model_path

```

### llm/model/load.py

```python
import os
import sys
from pathlib import Path
from contextlib import contextmanager
from llama_cpp import Llama
from config.llm import GPU_LAYERS, CONTEXT_SIZE, CPU_THREADS


@contextmanager
def _suppress_native_startup_output(enabled: bool = True):
    """Temporarily redirect process stdout/stderr to /dev/null.

    This suppresses verbose native llama.cpp / ggml startup logs on macOS.
    """
    if not enabled:
        yield
        return

    sys.stdout.flush()
    sys.stderr.flush()

    devnull_fd = os.open(os.devnull, os.O_WRONLY)
    saved_stdout_fd = os.dup(1)
    saved_stderr_fd = os.dup(2)
    try:
        os.dup2(devnull_fd, 1)
        os.dup2(devnull_fd, 2)
        yield
    finally:
        os.dup2(saved_stdout_fd, 1)
        os.dup2(saved_stderr_fd, 2)
        os.close(saved_stdout_fd)
        os.close(saved_stderr_fd)
        os.close(devnull_fd)


def load_llm(
    path: str | Path,
    gpu_layers: int = GPU_LAYERS,
    ctx: int = CONTEXT_SIZE,
    threads: int = CPU_THREADS,
) -> Llama:

    print(f"[LLM] Loading: {path} \n")
    print(f"[LLM] GPU={gpu_layers}  ctx={ctx}  threads={threads}")
    with _suppress_native_startup_output(enabled=True):
        model = Llama(
            model_path=str(path),
            n_gpu_layers=gpu_layers,
            n_ctx=ctx,
            n_threads=threads,
            verbose=False,
        )
    print("[LLM] Ready.")
    return model

```

### llm/model/singleton.py

```python
import threading
from typing import Optional

_model = None
_model_path: Optional[str] = None
_lock = threading.Lock()


def get_model():
    global _model, _model_path
    if _model is not None:
        return _model
    with _lock:
        if _model is not None:
            return _model
        from config.paths import LLM_DIR
        from config.llm import ACTIVE_LLM_MODEL
        from llm.download.resolver import find_gguf
        from llm.model.load import load_llm

        model_dir = LLM_DIR / ACTIVE_LLM_MODEL
        if not model_dir.exists():
            raise FileNotFoundError(
                f"LLM dir not found: {model_dir}\n"
                f"Place a .gguf file at {model_dir}/"
            )
        path = find_gguf(model_dir)
        _model_path = str(path)
        _model = load_llm(path)
    return _model


def is_loaded() -> bool:
    return _model is not None


def get_model_path() -> Optional[str]:
    return _model_path

```

### llm/prompt/__init__.py

```python
from llm.prompt.system import get_system_prompt
from llm.prompt.build import build_messages

```

### llm/prompt/build.py

```python
from llm.prompt.system import get_system_prompt


def build_messages(user_text: str, history: dict | None = None) -> list[dict]:
    if history:
        from llm.history.read import get_messages

        return get_messages(history)
    return [
        {"role": "system", "content": get_system_prompt()},
        {"role": "user", "content": user_text},
    ]

```

### llm/prompt/system.py

```python
from config.prompt import VOICE_SYSTEM_PROMPT


def get_system_prompt() -> str:
    return VOICE_SYSTEM_PROMPT


if __name__ == "__main__":
    print(get_system_prompt())

```

### main.py

```python
"""
main.py — Single entry point. Behaviour controlled by config/features.py MODE.
"""

import time
from config.features import MODE
from server.logger import create_logger, log_request


def main():
    print(f"\n  MODE: {MODE}\n")

    if MODE == "server":
        _run_server()
    elif MODE == "stt_only":
        _run_stt_only()
    elif MODE == "tts_only":
        _run_tts_only()
    elif MODE == "text_to_text_chat":
        _run_text_chat()
    elif MODE == "voice_to_text_chat":
        _run_voice_chat()
    elif MODE == "full":
        _run_full()
    else:
        print(f"  Unknown MODE '{MODE}'. Check config/features.py")


# ── Modes ──────────────────────────────────────────────────────


def _run_server():
    from config.server import SERVER_HOST, SERVER_PORT
    from config.features import ENABLE_STT
    from server.app import create_app

    print(f"  Starting server on {SERVER_HOST}:{SERVER_PORT}")
    if ENABLE_STT:
        from transcription.model.singleton import get_model

        get_model()
    create_app().run(host=SERVER_HOST, port=SERVER_PORT, debug=False, threaded=True)


def _run_stt_only():
    from transcription.model.singleton import get_model
    from transcription.stream import create_stream, start_stream, end_of_speech
    from transcription.vad.state import create_vad_state, reset_vad_state
    from config.vad import RECORD_SAMPLE_RATE
    from transcription.vad.session import run_mic_session
    from ui.console import show_partial, show_speaking, show_stt_final

    print("  Loading Whisper...")
    get_model()
    print("  Ready.\n")

    logger = create_logger()

    def on_partial(t):
        show_partial(t)

    transcriber = create_stream(on_partial=on_partial, on_final=lambda t: None)
    start_stream(transcriber)

    vad_state = create_vad_state(sample_rate=RECORD_SAMPLE_RATE)

    def on_speech_start():
        show_speaking()

    def on_speech_end():
        t_start = time.time()
        text = end_of_speech(transcriber)
        whisper_latency = time.time() - t_start
        if text:
            show_stt_final(text)
            log_request(logger, text, "", whisper_latency, 0.0, 0.0, whisper_latency)
        reset_vad_state(vad_state)

    run_mic_session(
        transcriber=transcriber,
        vad_state=vad_state,
        on_speech_start=on_speech_start,
        on_speech_end=on_speech_end,
    )


def _run_tts_only():
    from config.tts import (
        SUPERTONIC_VOICE,
        SUPERTONIC_SPEED,
        SUPERTONIC_STEPS,
        SUPERTONIC_LANGUAGE,
    )
    from tts.engine.state import create_engine
    from tts.engine.worker import start_worker
    from tts.engine.feed import feed_token, flush
    from tts.engine.status import shutdown
    from tts.model.singleton import get_model as get_tts_model
    from ui.console import prompt_you

    print("  Loading TTS model [Supertonic]...")
    engine = create_engine(
        voice=SUPERTONIC_VOICE,
        speed=SUPERTONIC_SPEED,
        steps=SUPERTONIC_STEPS,
        language=SUPERTONIC_LANGUAGE,
    )
    start_worker(engine)
    get_tts_model()  # Pre-warm the model before showing "Ready"
    print("  Ready. Type text to speak. Empty line to quit.\n")

    logger = create_logger()
    try:
        while True:
            prompt_you()
            text = input().strip()
            if not text:
                break
            t_start = time.time()
            for word in text.split():
                feed_token(engine, word + " ")
            flush(engine)
            tts_latency = time.time() - t_start
            log_request(logger, text, "", 0.0, 0.0, tts_latency, tts_latency)
    finally:
        shutdown(engine)


def _run_text_chat():
    from llm.model.singleton import get_model
    from llm.inference.stream import stream_response
    from llm.history.state import create_history
    from ui.console import prompt_you

    print("  Loading LLM...")
    get_model()
    print("  Ready. Type to chat. Empty line to quit.\n")

    logger = create_logger()
    history = create_history()
    while True:
        prompt_you()
        user_text = input().strip()
        if not user_text:
            break
        t_start = time.time()
        print("  AI : ", end="", flush=True)
        ai_response = ""
        first_token_time = None
        for token in stream_response(user_text, history):
            if first_token_time is None:
                first_token_time = time.time() - t_start
            print(token, end="", flush=True)
            ai_response += token
        print()
        llm_total = time.time() - t_start
        llm_first_token = first_token_time if first_token_time else llm_total
        log_request(
            logger, user_text, ai_response, 0.0, llm_first_token, llm_total, llm_total
        )


def _run_voice_chat():
    from llm.model.singleton import get_model
    from llm.inference.stream import stream_response
    from llm.history.state import create_history
    from transcription.model.singleton import get_model as load_whisper
    from transcription.stream import create_stream, start_stream, end_of_speech
    from transcription.vad.state import create_vad_state, reset_vad_state
    from config.vad import RECORD_SAMPLE_RATE
    from transcription.vad.session import run_mic_session
    from ui.console import show_partial, show_speaking, show_you, start_ai_line
    import threading

    print("  Loading Whisper + LLM...")
    load_whisper()
    get_model()
    print("  Ready.\n")

    logger = create_logger()
    history = create_history()
    lock = threading.Lock()
    vad_state = create_vad_state(sample_rate=RECORD_SAMPLE_RATE)

    def on_partial(t):
        show_partial(t)

    transcriber = create_stream(on_partial=on_partial, on_final=lambda t: None)
    start_stream(transcriber)

    def on_speech_start():
        show_speaking()

    def on_speech_end():
        if not lock.acquire(blocking=False):
            return
        reset_vad_state(vad_state)

        def _run():
            try:
                e2e_start = time.time()
                whisper_start = time.time()
                text = end_of_speech(transcriber)
                whisper_latency = time.time() - whisper_start
                if not text:
                    lock.release()
                    return
                show_you(text)
                start_ai_line()
                llm_start = time.time()
                ai_response = ""
                first_token_time = None
                for token in stream_response(text, history):
                    if first_token_time is None:
                        first_token_time = time.time() - llm_start
                    print(token, end="", flush=True)
                    ai_response += token
                print()
                llm_total = time.time() - llm_start
                llm_first_token = first_token_time if first_token_time else llm_total
                e2e_total = time.time() - e2e_start
                log_request(
                    logger,
                    text,
                    ai_response,
                    whisper_latency,
                    llm_first_token,
                    llm_total,
                    e2e_total,
                )
            finally:
                lock.release()

        threading.Thread(target=_run, daemon=True).start()

    run_mic_session(
        transcriber=transcriber,
        vad_state=vad_state,
        on_speech_start=on_speech_start,
        on_speech_end=on_speech_end,
    )


def _run_full():
    from config.tts import (
        SUPERTONIC_VOICE,
        SUPERTONIC_SPEED,
        SUPERTONIC_STEPS,
        SUPERTONIC_LANGUAGE,
    )
    from llm.model.singleton import get_model
    from llm.inference.stream import stream_response
    from llm.history.state import create_history
    from transcription.model.singleton import get_model as load_whisper
    from transcription.stream import create_stream, start_stream, end_of_speech
    from transcription.vad.state import create_vad_state, reset_vad_state
    from transcription.vad.session import run_mic_session
    from tts.engine.state import create_engine
    from tts.engine.worker import start_worker
    from tts.engine.feed import feed_token, flush as tts_flush
    from tts.engine.control import interrupt, resume, speak_filler
    from tts.engine.status import is_speaking, shutdown
    from config.vad import RECORD_SAMPLE_RATE
    from ui.console import show_partial, show_speaking, show_you, start_ai_line
    import threading

    print("  Loading all models...")
    load_whisper()
    get_model()
    engine = create_engine(
        voice=SUPERTONIC_VOICE,
        speed=SUPERTONIC_SPEED,
        steps=SUPERTONIC_STEPS,
        language=SUPERTONIC_LANGUAGE,
    )
    start_worker(engine)
    print("  All ready.\n")

    logger = create_logger()
    history = create_history()
    lock = threading.Lock()
    vad_state = create_vad_state(sample_rate=RECORD_SAMPLE_RATE)

    def on_partial(t):
        show_partial(t)

    transcriber = create_stream(on_partial=on_partial, on_final=lambda t: None)
    start_stream(transcriber)

    def on_speech_start():
        interrupt(engine)
        show_speaking()

    def on_speech_end():
        if not lock.acquire(blocking=False):
            return
        reset_vad_state(vad_state)

        def _run():
            try:
                e2e_start = time.time()
                whisper_start = time.time()
                text = end_of_speech(transcriber)
                whisper_latency = time.time() - whisper_start
                if not text:
                    lock.release()
                    return
                show_you(text)
                resume(engine)
                speak_filler(engine)
                start_ai_line()
                llm_start = time.time()
                ai_response = ""
                first_token_time = None
                for token in stream_response(text, history):
                    if first_token_time is None:
                        first_token_time = time.time() - llm_start
                    print(token, end="", flush=True)
                    ai_response += token
                    feed_token(engine, token)
                tts_flush(engine)
                print()
                llm_total = time.time() - llm_start
                llm_first_token = first_token_time if first_token_time else llm_total
                e2e_total = time.time() - e2e_start
                log_request(
                    logger,
                    text,
                    ai_response,
                    whisper_latency,
                    llm_first_token,
                    llm_total,
                    e2e_total,
                )
            finally:
                lock.release()

        threading.Thread(target=_run, daemon=True).start()

    run_mic_session(
        transcriber=transcriber,
        vad_state=vad_state,
        on_speech_start=on_speech_start,
        on_speech_end=on_speech_end,
        should_process_chunk=lambda: not is_speaking(engine),
    )
    shutdown(engine)


if __name__ == "__main__":
    main()

```

### requirements.txt

```text
# Voice Server dependencies
flask
flask-cors
torch
openai-whisper
gTTS

# llama-cpp-python

# CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python --no-cache-dir

Pillow
requests
numpy
resampy
soundfile

# Voice Client dependencies
sounddevice
pygame
flask-sock 
websocket-client
pyttsx3 
sounddevice
onnxruntime 
transformers

```

### server/__init__.py

```python
from server.app import create_app

```

### server/app.py

```python
from flask import Flask
from flask_cors import CORS
from flask_sock import Sock

from server.routes.health import health_handler
from server.routes.transcribe import transcribe_handler
from server.routes.websocket import register_ws


def create_app() -> Flask:
    app = Flask(__name__)
    sock = Sock(app)
    CORS(app)
    app.add_url_rule("/health", "health", health_handler, methods=["GET"])
    app.add_url_rule("/transcribe", "transcribe", transcribe_handler, methods=["POST"])
    register_ws(sock)
    return app

```

### server/logger.py

```python
import threading
import time
from datetime import datetime
from config.paths import LOGS_DIR


def create_logger() -> dict:
    LOGS_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = LOGS_DIR / f"conversation_{ts}.log"
    with open(path, "w") as f:
        f.write("╔══════════════════════════════════════════════════════╗\n")
        f.write(f"  Session started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("╚══════════════════════════════════════════════════════╝\n\n")
    print(f"[LOG] {path}")
    return {
        "path": path,
        "req_num": 0,
        "session_start": time.time(),
        "lock": threading.Lock(),
    }


def log_request(
    logger: dict,
    user_text: str,
    ai_response: str,
    whisper_latency: float,
    llm_first_token: float,
    llm_total: float,
    end_to_end: float,
) -> None:
    with logger["lock"]:
        logger["req_num"] += 1
        n = logger["req_num"]
        ts = datetime.now().strftime("%H:%M:%S")
        st = time.time() - logger["session_start"]
        sep = "─" * 54
        print(f"\n  {sep}\n  Request #{n:02d}  [{ts}]  (+{st:.0f}s)\n  {sep}")
        print(f"  YOU : {user_text}\n  AI  : {ai_response}\n  {sep}")
        print(
            f"  ⏱  Whisper:{whisper_latency:.3f}s  FirstToken:{llm_first_token:.3f}s  LLM:{llm_total:.3f}s  E2E:{end_to_end:.3f}s\n  {sep}\n"
        )
        with open(logger["path"], "a") as f:
            f.write(
                f"[{ts}] #{n:02d}  YOU:{user_text}  AI:{ai_response}  "
                f"whisper:{whisper_latency:.3f}s  ft:{llm_first_token:.3f}s  "
                f"llm:{llm_total:.3f}s  e2e:{end_to_end:.3f}s\n\n"
            )


def log_event(logger: dict, event: str) -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    with logger["lock"]:
        print(f"  [LOG] {event}")
        with open(logger["path"], "a") as f:
            f.write(f"[{ts}] EVENT: {event}\n\n")


def close_logger(logger: dict) -> None:
    dur = time.time() - logger["session_start"]
    with open(logger["path"], "a") as f:
        f.write(f"  Session ended — {logger['req_num']} requests in {dur:.0f}s\n")
    print(f"[LOG] Closed — {logger['req_num']} requests in {dur:.0f}s")

```

### server/routes/__init__.py

```python
from server.routes.health import health_handler
from server.routes.transcribe import transcribe_handler
from server.routes.websocket import register_ws

```

### server/routes/health.py

```python
from flask import jsonify
from config.whisper import WHISPER_MODEL_NAME
from config.features import ENABLE_STT, ENABLE_TTS
from config.tts import TTS_MODE, TTS_SERVER_BACKEND
from transcription.model.singleton import is_loaded as whisper_loaded
from llm.model.singleton import is_loaded as llm_loaded


def health_handler():
    return jsonify(
        {
            "status": "ok",
            "whisper_loaded": whisper_loaded(),
            "whisper_model": WHISPER_MODEL_NAME,
            "llm_loaded": llm_loaded(),
            "enable_stt": ENABLE_STT,
            "enable_tts": ENABLE_TTS,
            "tts_mode": TTS_MODE,
            "tts_backend": TTS_SERVER_BACKEND if TTS_MODE == "server" else "n/a",
        }
    )

```

### server/routes/transcribe.py

```python
import os, time, tempfile
from flask import request, jsonify
from config.features import ENABLE_STT
from config.whisper import WHISPER_SAMPLE_RATE
from audio.io.read import read_wav
from audio.transform.mono import to_mono
from audio.transform.resample import resample
from transcription.model.singleton import get_model
from transcription.transcribe.batch import transcribe_audio


def transcribe_handler():
    if not ENABLE_STT:
        return jsonify({"error": "STT disabled"}), 503
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    f = request.files["file"]
    tmp = os.path.join(tempfile.gettempdir(), f"stt_{int(time.time()*1000)}.wav")
    f.save(tmp)
    try:
        get_model()
        audio, sr = read_wav(tmp)
        audio = to_mono(audio)
        audio = resample(audio, sr, WHISPER_SAMPLE_RATE)
        return jsonify({"text": transcribe_audio(audio)})
    except Exception as e:
        import traceback

        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            os.unlink(tmp)
        except Exception:
            pass

```

### server/routes/websocket.py

```python
from server.ws.handler import handle_ws


def register_ws(sock, path: str = "/ws/transcribe"):
    @sock.route(path)
    def ws_transcribe(ws):
        handle_ws(ws)

```

### server/ws/__init__.py

```python
from server.ws.handler import handle_ws

```

### server/ws/handler.py

```python
from config.features import ENABLE_STT
from transcription.model.singleton import get_model as get_whisper
from llm.model.singleton import get_model as get_llm
from server.ws.session.create import create_session
from server.ws.session.teardown import teardown_session
from server.ws.receive.router import route_message
from server.ws.pipeline.eos import trigger_eos
from server.ws.send.core import send
from server.logger import log_event


def handle_ws(ws) -> None:
    """Main WebSocket loop — orchestrates all modules, owns no logic itself."""
    session = create_session()
    log_event(session["logger"], "Client connected")

    if ENABLE_STT:
        get_whisper()
    get_llm()

    if ENABLE_STT:
        from transcription.stream import create_stream, start_stream
        from server.ws.send.stt import send_partial

        session["transcriber"] = create_stream(
            on_partial=lambda text: send_partial(ws, text),
            on_final=lambda text: None,
        )
        start_stream(session["transcriber"])

    def _eos():
        trigger_eos(session, ws)

    try:
        while True:
            msg = ws.receive()
            if msg is None:
                break
            route_message(msg, session, ws, _eos)
    except Exception as e:
        print(f"[WS] {e}")
        send(ws, {"type": "error", "message": str(e)})
    finally:
        teardown_session(session)

```

### server/ws/pipeline/__init__.py

```python
from server.ws.pipeline.eos import trigger_eos
from server.ws.pipeline.llm_runner import run_llm

```

### server/ws/pipeline/eos.py

```python
import time
import threading

from config.features import ENABLE_STT, SHOW_TEXT
from server.ws.send.stt import send_final
from server.logger import log_event


def trigger_eos(session: dict, ws) -> None:
    """
    End-of-speech orchestration:
    1. Guard — ignore if TTS is speaking
    2. Interrupt TTS
    3. Finalise transcription
    4. Enqueue filler + launch LLM thread
    """
    tts = session.get("tts")
    if tts:
        from tts.engine.status import is_speaking

        if is_speaking(tts):
            session["silence_accumulated"] = 0
            session["in_speech"] = False
            if session.get("transcriber"):
                from transcription.stream import clear_stream

                clear_stream(session["transcriber"])
            return

    if not session["eos_lock"].acquire(blocking=False):
        return
    try:
        t_eos = time.time()
        session["silence_accumulated"] = 0
        session["in_speech"] = False

        if tts:
            from tts.engine.control import interrupt

            interrupt(tts)

        text = ""
        if ENABLE_STT and session.get("transcriber"):
            from transcription.stream import end_of_speech

            text = end_of_speech(session["transcriber"])

        if text and text.strip():
            if SHOW_TEXT:
                send_final(ws, text)
            if tts:
                from tts.engine.control import resume, speak_filler

                resume(tts)
                speak_filler(tts)
            from server.ws.pipeline.llm_runner import run_llm

            threading.Thread(
                target=run_llm, args=(text, t_eos, session, ws), daemon=True
            ).start()
    finally:
        session["eos_lock"].release()

```

### server/ws/pipeline/llm_runner.py

```python
import time
import threading

from config.features import ENABLE_TTS, SHOW_TEXT
from config.tts import TTS_MODE
from llm.inference.stream import stream_response
from server.ws.send.llm import send_llm_start, send_llm_token, send_llm_done
from server.ws.send.tts import send_tts_start, send_tts_done
from server.logger import log_request


def run_llm(user_text: str, t_eos: float, session: dict, ws) -> None:
    """Run LLM + feed TTS. Intended to run in a daemon thread."""
    if not user_text.strip():
        return

    t_start = time.time()
    whisper_lat = t_start - t_eos
    first_token_t = None
    first_token = True
    full = ""
    tts = session.get("tts")

    if SHOW_TEXT:
        send_llm_start(ws)
    if tts:
        send_tts_start(ws)

    try:
        for token in stream_response(user_text, session["history"]):
            if first_token:
                first_token_t = time.time() - t_start
                first_token = False
            full += token
            if SHOW_TEXT:
                send_llm_token(ws, token)
            if tts:
                from tts.engine.feed import feed_token

                feed_token(tts, token)
    finally:
        if tts:
            from tts.engine.feed import flush

            flush(tts)
        t_done = time.time()
        llm_total = t_done - t_start
        log_request(
            session["logger"],
            user_text=user_text,
            ai_response=full,
            whisper_latency=whisper_lat,
            llm_first_token=first_token_t or llm_total,
            llm_total=llm_total,
            end_to_end=t_done - t_eos,
        )
        if SHOW_TEXT:
            send_llm_done(ws, full)
        if tts:
            send_tts_done(ws)

```

### server/ws/receive/__init__.py

```python
from server.ws.receive.router import route_message
from server.ws.receive.audio import handle_audio_frame
from server.ws.receive.commands import (
    handle_end_of_speech,
    handle_clear_history,
    handle_ping,
)

```

### server/ws/receive/audio.py

```python
import numpy as np
from config.vad import SILENCE_THRESHOLD
from config.whisper import WHISPER_SAMPLE_RATE

from config.vad import SILENCE_DURATION

_SILENCE_SAMPLES = int(SILENCE_DURATION * WHISPER_SAMPLE_RATE)


def handle_audio_frame(data: bytes, session: dict, trigger_eos_fn) -> None:
    if not session.get("transcriber"):
        return
    tts = session.get("tts")
    if tts:
        from tts.engine.status import is_speaking

        if is_speaking(tts):
            session["silence_accumulated"] = 0
            session["in_speech"] = False
            return
    chunk = np.frombuffer(data, dtype=np.float32)
    from transcription.stream import feed

    feed(session["transcriber"], chunk)
    amp = float(np.abs(chunk).mean())
    if amp > SILENCE_THRESHOLD:
        session["in_speech"] = True
        session["silence_accumulated"] = 0
    elif session["in_speech"]:
        session["silence_accumulated"] += len(chunk)
        if session["silence_accumulated"] >= _SILENCE_SAMPLES:
            trigger_eos_fn()

```

### server/ws/receive/commands.py

```python
from server.ws.send.core import send
from server.logger import log_event


def handle_end_of_speech(session: dict, trigger_eos_fn) -> None:
    trigger_eos_fn()


def handle_clear_history(session: dict, ws) -> None:
    from llm.history.clear import clear_history

    clear_history(session["history"])
    log_event(session["logger"], "History cleared")
    send(ws, {"type": "pong"})


def handle_ping(ws) -> None:
    send(ws, {"type": "pong"})

```

### server/ws/receive/router.py

```python
import json


def route_message(message, session: dict, ws, trigger_eos_fn) -> None:
    """Dispatch incoming WebSocket frame to the correct handler."""
    if isinstance(message, bytes) and len(message) >= 4:
        from server.ws.receive.audio import handle_audio_frame

        handle_audio_frame(message, session, trigger_eos_fn)
        return
    if isinstance(message, str):
        try:
            msg = json.loads(message)
        except Exception:
            return
        t = msg.get("type")
        if t == "end_of_speech":
            from server.ws.receive.commands import handle_end_of_speech

            handle_end_of_speech(session, trigger_eos_fn)
        elif t == "clear_history":
            from server.ws.receive.commands import handle_clear_history

            handle_clear_history(session, ws)
        elif t == "ping":
            from server.ws.receive.commands import handle_ping

            handle_ping(ws)

```

### server/ws/send/__init__.py

```python
from server.ws.send.core import send
from server.ws.send.stt import send_partial, send_final
from server.ws.send.llm import send_llm_start, send_llm_token, send_llm_done
from server.ws.send.tts import send_tts_start, send_tts_done

```

### server/ws/send/core.py

```python
import json


def send(ws, obj: dict) -> None:
    """Single write point for all outbound WebSocket messages."""
    try:
        ws.send(json.dumps(obj))
    except Exception:
        pass

```

### server/ws/send/llm.py

```python
from server.ws.send.core import send


def send_llm_start(ws) -> None:
    send(ws, {"type": "llm_start"})


def send_llm_token(ws, token: str) -> None:
    send(ws, {"type": "llm_token", "text": token})


def send_llm_done(ws, full: str) -> None:
    send(ws, {"type": "llm_done", "text": full})

```

### server/ws/send/stt.py

```python
from server.ws.send.core import send


def send_partial(ws, text: str) -> None:
    send(ws, {"type": "partial", "text": text})


def send_final(ws, text: str) -> None:
    send(ws, {"type": "final", "text": text})

```

### server/ws/send/tts.py

```python
from server.ws.send.core import send


def send_tts_start(ws) -> None:
    send(ws, {"type": "tts_start"})


def send_tts_done(ws) -> None:
    send(ws, {"type": "tts_done"})

```

### server/ws/session/__init__.py

```python
from server.ws.session.create import create_session
from server.ws.session.teardown import teardown_session

```

### server/ws/session/create.py

```python
import threading
from config.features import ENABLE_TTS
from config.tts import (
    TTS_MODE,
    SUPERTONIC_VOICE,
    SUPERTONIC_SPEED,
    SUPERTONIC_STEPS,
    SUPERTONIC_LANGUAGE,
)
from llm.history.state import create_history
from server.logger import create_logger


def create_session() -> dict:
    """Build per-connection state dict."""
    session = {
        "history": create_history(),
        "logger": create_logger(),
        "silence_accumulated": 0,
        "in_speech": False,
        "eos_lock": threading.Lock(),
        "tts": None,
        "transcriber": None,
    }
    if ENABLE_TTS and TTS_MODE == "server":
        from tts.engine.state import create_engine
        from tts.engine.worker import start_worker

        engine = create_engine(
            voice=SUPERTONIC_VOICE,
            speed=SUPERTONIC_SPEED,
            steps=SUPERTONIC_STEPS,
            language=SUPERTONIC_LANGUAGE,
        )
        start_worker(engine)
        session["tts"] = engine
    return session

```

### server/ws/session/teardown.py

```python
from server.logger import log_event, close_logger


def teardown_session(session: dict) -> None:
    t = session.get("transcriber")
    if t:
        from transcription.stream import stop_stream

        stop_stream(t)
    tts = session.get("tts")
    if tts:
        from tts.engine.status import shutdown

        shutdown(tts)
    log_event(session["logger"], "Client disconnected")
    close_logger(session["logger"])

```

### transcription/__init__.py

```python
from transcription.model.singleton import get_model, is_loaded
from transcription.transcribe.batch import transcribe_audio
from transcription.stream import (
    create_stream,
    start_stream,
    stop_stream,
    feed,
    end_of_speech,
    clear_stream,
)

```

### transcription/download/__init__.py

```python
from transcription.download.whisper import ensure_downloaded

```

### transcription/download/whisper.py

```python
from config.paths import WHISPER_DIR
from config.whisper import WHISPER_MODEL_NAME


def ensure_downloaded(model_name: str = WHISPER_MODEL_NAME) -> str:
    """
    Download Whisper model into models/whisper/ if missing.
    Returns path to the .pt file.
    """
    WHISPER_DIR.mkdir(parents=True, exist_ok=True)
    model_path = WHISPER_DIR / f"{model_name}.pt"
    if model_path.exists():
        print(f"[Whisper] Cached at {model_path}")
        return str(model_path)
    print(f"[Whisper] Downloading '{model_name}' → {WHISPER_DIR} ...")

    import whisper

    url = whisper._MODELS.get(model_name)
    if url is None:
        raise ValueError(
            f"Unknown model '{model_name}'. Valid: {list(whisper._MODELS)}"
        )
    whisper._download(url, str(WHISPER_DIR), in_memory=False)

    print("[Whisper] Download complete.")
    return str(model_path)


if __name__ == "__main__":
    print(ensure_downloaded())

```

### transcription/hallucination/__init__.py

```python
from transcription.hallucination.repetition import has_repetition
from transcription.hallucination.noise import is_noise_phrase, clean_text
from transcription.hallucination.confidence import passes_confidence

```

### transcription/hallucination/confidence.py

```python
from config.vad import NO_SPEECH_THRESHOLD


def passes_confidence(result: dict) -> bool:
    """True if Whisper's average no_speech_prob is below threshold."""
    segments = result.get("segments", [])
    if not segments:
        return True
    avg = sum(s.get("no_speech_prob", 0.0) for s in segments) / len(segments)
    return avg <= NO_SPEECH_THRESHOLD


if __name__ == "__main__":
    print(passes_confidence({"segments": [{"no_speech_prob": 0.9}]}))  # False
    print(passes_confidence({"segments": [{"no_speech_prob": 0.1}]}))  # True

```

### transcription/hallucination/noise.py

```python
import re

_PATTERNS = [
    re.compile(r"^\[.*\]$", re.IGNORECASE),
    re.compile(r"^\(.*\)$", re.IGNORECASE),
    re.compile(r"^[\s\.\,\!\?]*$"),
]


def is_noise_phrase(text: str) -> bool:
    t = text.strip()
    if not t:
        return True
    return any(p.match(t) for p in _PATTERNS)


def clean_text(text: str) -> str:
    t = text.strip()
    return "" if is_noise_phrase(t) else t


if __name__ == "__main__":
    for t in ["[BLANK_AUDIO]", "Hello world", "...", "(music)"]:
        print(f"'{t}' → noise={is_noise_phrase(t)}")

```

### transcription/hallucination/repetition.py

```python
REPETITION_MIN_WORDS = 4
REPETITION_COUNT_THRESHOLD = 3


def has_repetition(text: str) -> bool:
    """True if the same N-word phrase repeats 3+ times (Whisper looping)."""
    words = text.lower().split()
    n = REPETITION_MIN_WORDS
    if len(words) < n * REPETITION_COUNT_THRESHOLD:
        return False
    for start in range(len(words) - n + 1):
        phrase = tuple(words[start : start + n])
        count, pos = 0, start
        while pos <= len(words) - n:
            if tuple(words[pos : pos + n]) == phrase:
                count += 1
                pos += n
            else:
                pos += 1
        if count >= REPETITION_COUNT_THRESHOLD:
            return True
    return False


if __name__ == "__main__":
    print(has_repetition("Hello how are you"))
    print(has_repetition("I want to go there. I want to go there. I want to go there."))

```

### transcription/model/__init__.py

```python
from transcription.model.singleton import get_model, is_loaded, reset
from transcription.model.device import resolve_device
from transcription.model.lock import infer_lock

```

### transcription/model/device.py

```python
import torch


def resolve_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


if __name__ == "__main__":
    print(resolve_device())

```

### transcription/model/load.py

```python
import torch
import whisper
import whisper.model as wm

from config.paths import WHISPER_DIR
from config.whisper import WHISPER_MODEL_NAME
from transcription.model.device import resolve_device


def load_whisper(
    model_name: str = WHISPER_MODEL_NAME,
    device: str | None = None,
) -> wm.Whisper:
    """Load Whisper from models/whisper/. Downloads if missing."""
    from transcription.download.whisper import ensure_downloaded

    if device is None:
        device = resolve_device()
    ensure_downloaded(model_name)
    model_path = WHISPER_DIR / f"{model_name}.pt"
    print(f"[Whisper] Loading '{model_name}' on {device} ...")
    checkpoint = torch.load(str(model_path), map_location="cpu")
    dims = wm.ModelDimensions(**checkpoint["dims"])
    model = wm.Whisper(dims)
    model.load_state_dict(checkpoint["model_state_dict"])
    model = model.to(device)
    print(f"[Whisper] Ready on {device}.")
    return model


if __name__ == "__main__":
    m = load_whisper()
    print(type(m))

```

### transcription/model/lock.py

```python
import threading

# Single lock shared by all Whisper callers — GPU is not re-entrant
infer_lock = threading.Lock()

```

### transcription/model/singleton.py

```python
import threading
from typing import Optional
import whisper.model as wm

_model: Optional[wm.Whisper] = None
_lock = threading.Lock()


def get_model() -> wm.Whisper:
    global _model
    if _model is not None:
        return _model
    with _lock:
        if _model is not None:
            return _model
        from transcription.model.load import load_whisper

        _model = load_whisper()
    return _model


def is_loaded() -> bool:
    return _model is not None


def reset():
    global _model
    _model = None

```

### transcription/stream/__init__.py

```python
from transcription.stream.buffer import create_buffer
from transcription.stream.worker import start_worker, stop_worker
from transcription.stream.final import run_final_pass


def create_stream(on_partial, on_final, sample_rate: int = 16000) -> dict:
    return {
        "buf": create_buffer(sample_rate),
        "on_partial": on_partial,
        "on_final": on_final,
        "last_text": "",
        "running": False,
        "worker_thread": None,
    }


def start_stream(state: dict) -> None:
    start_worker(state)


def stop_stream(state: dict) -> None:
    stop_worker(state)


def feed(state: dict, chunk) -> None:
    from transcription.stream.buffer import append

    append(state["buf"], chunk)


def end_of_speech(state: dict) -> str:
    text = run_final_pass(state["buf"])
    state["last_text"] = ""
    if text:
        state["on_final"](text)
    return text


def clear_stream(state: dict) -> None:
    from transcription.stream.buffer import clear_buffer

    clear_buffer(state["buf"])
    state["last_text"] = ""

```

### transcription/stream/buffer.py

```python
import threading
import numpy as np

MAX_BUFFER_SEC = 29.0


def create_buffer(sample_rate: int = 16000) -> dict:
    return {"chunks": [], "lock": threading.Lock(), "sample_rate": sample_rate}


def append(buf: dict, chunk: np.ndarray) -> None:
    with buf["lock"]:
        buf["chunks"].append(chunk.astype(np.float32))
        _cap(buf)


def get_audio(buf: dict) -> np.ndarray | None:
    with buf["lock"]:
        if not buf["chunks"]:
            return None
        return np.concatenate(buf["chunks"]).astype(np.float32)


def clear_buffer(buf: dict) -> None:
    with buf["lock"]:
        buf["chunks"] = []


def _cap(buf: dict) -> None:
    max_samples = int(MAX_BUFFER_SEC * buf["sample_rate"])
    total = sum(len(c) for c in buf["chunks"])
    while total > max_samples and buf["chunks"]:
        total -= len(buf["chunks"].pop(0))

```

### transcription/stream/final.py

```python
import threading
import numpy as np
import whisper

from transcription.model.singleton import get_model
from transcription.transcribe.options import build_whisper_options
from transcription.hallucination.repetition import has_repetition
from transcription.hallucination.noise import clean_text
from transcription.hallucination.confidence import passes_confidence
from transcription.stream.buffer import get_audio, clear_buffer

from transcription.model.lock import infer_lock as _infer_lock


def run_final_pass(buf: dict) -> str:
    audio = get_audio(buf)
    clear_buffer(buf)
    if audio is None:
        return ""
    return _transcribe(audio)


def _transcribe(audio: np.ndarray) -> str:
    try:
        with _infer_lock:
            result = whisper.transcribe(get_model(), audio, **build_whisper_options())
        if not passes_confidence(result):
            return ""
        text = clean_text(result.get("text", ""))
        return "" if (not text or has_repetition(text)) else text
    except Exception as e:
        print(f"[Final] {e}")
        return ""


if __name__ == "__main__":
    import numpy as np
    from transcription.stream.buffer import create_buffer, append

    buf = create_buffer()
    append(buf, np.zeros(16000, dtype=np.float32))
    print(repr(run_final_pass(buf)))

```

### transcription/stream/partial.py

```python
import threading
import numpy as np
import whisper

from transcription.model.singleton import get_model
from transcription.transcribe.options import build_whisper_options
from transcription.hallucination.repetition import has_repetition
from transcription.hallucination.noise import clean_text
from transcription.hallucination.confidence import passes_confidence
from config.vad import MIN_AUDIO_SEC

from transcription.model.lock import infer_lock as _infer_lock


def run_partial_pass(buf: dict) -> str:
    from transcription.stream.buffer import get_audio

    audio = get_audio(buf)
    if audio is None or len(audio) / buf["sample_rate"] < MIN_AUDIO_SEC:
        return ""
    return _transcribe(audio)


def _transcribe(audio: np.ndarray) -> str:
    try:
        with _infer_lock:
            result = whisper.transcribe(get_model(), audio, **build_whisper_options())
        if not passes_confidence(result):
            return ""
        text = clean_text(result.get("text", ""))
        return "" if (not text or has_repetition(text)) else text
    except Exception as e:
        print(f"[Partial] {e}")
        return ""

```

### transcription/stream/worker.py

```python
import threading
import time

from config.vad import TRANSCRIBE_EVERY


def start_worker(state: dict) -> None:
    state["running"] = True
    t = threading.Thread(target=_loop, args=(state,), daemon=True)
    t.start()
    state["worker_thread"] = t


def stop_worker(state: dict) -> None:
    state["running"] = False
    t = state.get("worker_thread")
    if t:
        t.join(timeout=5)
    state["worker_thread"] = None


def _loop(state: dict) -> None:
    while state["running"]:
        time.sleep(TRANSCRIBE_EVERY)
        from transcription.stream.partial import run_partial_pass

        text = run_partial_pass(state["buf"])
        if text and text != state["last_text"]:
            state["last_text"] = text
            state["on_partial"](text)

```

### transcription/transcribe/__init__.py

```python
from transcription.transcribe.batch import transcribe_audio
from transcription.transcribe.options import build_whisper_options

```

### transcription/transcribe/batch.py

```python
import time
import threading

import numpy as np
import whisper

from transcription.model.singleton import get_model
from config.whisper import WHISPER_DEVICE

from transcription.model.lock import infer_lock as _infer_lock


def transcribe_audio(audio: np.ndarray) -> str:
    """
    One-shot transcription of a 16 kHz float32 mono array.
    Returns stripped transcript string. Raises on error.
    """
    model = get_model()
    duration = len(audio) / 16_000
    print(f"[Transcribe] {duration:.1f}s ...", flush=True)
    t0 = time.time()
    with _infer_lock:
        result = whisper.transcribe(
            model,
            audio,
            language="en",
            fp16=(WHISPER_DEVICE == "cuda"),
            temperature=0,
            condition_on_previous_text=True,
        )
    text = result["text"].strip()
    print(f"[Transcribe] '{text}'  ({time.time()-t0:.2f}s)", flush=True)
    return text


if __name__ == "__main__":
    import numpy as np

    audio = np.zeros(16000, dtype=np.float32)
    print(repr(transcribe_audio(audio)))

```

### transcription/transcribe/options.py

```python
from config.vad import (
    NO_SPEECH_THRESHOLD,
    LOGPROB_THRESHOLD,
    COMPRESSION_RATIO_THRESHOLD,
)
from config.whisper import WHISPER_DEVICE


def build_whisper_options() -> dict:
    return {
        "language": "en",
        "fp16": (WHISPER_DEVICE == "cuda"),
        "temperature": 0,
        "condition_on_previous_text": False,
        "no_speech_threshold": NO_SPEECH_THRESHOLD,
        "compression_ratio_threshold": COMPRESSION_RATIO_THRESHOLD,
        "logprob_threshold": LOGPROB_THRESHOLD,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(build_whisper_options(), indent=2))

```

### transcription/vad/__init__.py

```python
from transcription.vad.state import create_vad_state, reset_vad_state
from transcription.vad.processor import process_chunk
from transcription.vad.energy import is_speech_energy

```

### transcription/vad/energy.py

```python
import numpy as np
from config.vad import ENERGY_THRESHOLD
from audio.gate.rms import rms
from audio.gate.zcr import zero_crossing_rate

ZCR_WEIGHT = 0.4


def is_speech_energy(chunk: np.ndarray, threshold: float = ENERGY_THRESHOLD) -> bool:
    if len(chunk) == 0:
        return False
    return (rms(chunk) + ZCR_WEIGHT * zero_crossing_rate(chunk)) > threshold


if __name__ == "__main__":
    import numpy as np

    print(is_speech_energy(np.zeros(1600)))
    print(is_speech_energy(np.random.randn(1600).astype(np.float32) * 0.5))

```

### transcription/vad/processor.py

```python
import numpy as np
from config.vad import PAUSE_SECONDS, MIN_SPEECH_SEC
from transcription.vad.state import reset_vad_state
from transcription.vad.energy import is_speech_energy


def process_chunk(
    chunk: np.ndarray,
    state: dict,
    on_speech_start=None,
    on_speech_end=None,
) -> None:
    pause_samples = int(PAUSE_SECONDS * state["sample_rate"])
    min_samples = int(MIN_SPEECH_SEC * state["sample_rate"])
    is_speech = is_speech_energy(chunk)

    if is_speech:
        if not state["in_speech"]:
            state["in_speech"] = True
            state["silence_count"] = 0
            if on_speech_start:
                on_speech_start()
        state["speech_samples"] += len(chunk)
        state["silence_count"] = 0
    elif state["in_speech"]:
        state["silence_count"] += len(chunk)
        state["speech_samples"] += len(chunk)
        if state["silence_count"] >= pause_samples:
            if state["speech_samples"] >= min_samples and on_speech_end:
                on_speech_end()
            reset_vad_state(state)


if __name__ == "__main__":
    import numpy as np

    from transcription.vad.state import create_vad_state

    s = create_vad_state()
    for _ in range(20):
        process_chunk(
            np.random.randn(1600).astype(np.float32) * 0.5,
            s,
            lambda: print("START"),
            lambda: print("END"),
        )
    for _ in range(60):
        process_chunk(
            np.zeros(1600, dtype=np.float32),
            s,
            lambda: print("START"),
            lambda: print("END"),
        )

    for _ in range(20):
        process_chunk(
            np.random.randn(1600).astype(np.float32) * 0.5,
            s,
            lambda: print("START"),
            lambda: print("END"),
        )
    for _ in range(60):
        process_chunk(
            np.zeros(1600, dtype=np.float32),
            s,
            lambda: print("START"),
            lambda: print("END"),
        )

```

### transcription/vad/session.py

```python
import numpy as np

from audio.io.mic import open_mic
from audio.transform.resample import resample
from config.vad import RECORD_SAMPLE_RATE, PREROLL_SECONDS
from config.whisper import WHISPER_SAMPLE_RATE
from transcription.stream import feed
from transcription.vad.processor import process_chunk


def run_mic_session(
    transcriber: dict,
    vad_state: dict,
    on_speech_start,
    on_speech_end,
    should_process_chunk=None,
) -> None:
    """Run interactive mic capture loop with VAD/preroll + Whisper resampling."""
    preroll_target = int(PREROLL_SECONDS * RECORD_SAMPLE_RATE)
    preroll_chunks: list[np.ndarray] = []
    preroll_len = 0

    def on_chunk(chunk):
        nonlocal preroll_len

        if should_process_chunk is not None and not should_process_chunk():
            return

        was_in_speech = vad_state["in_speech"]
        process_chunk(
            chunk,
            vad_state,
            on_speech_start=on_speech_start,
            on_speech_end=on_speech_end,
        )
        now_in_speech = vad_state["in_speech"]

        if now_in_speech:
            if not was_in_speech and preroll_chunks:
                pad = np.concatenate(preroll_chunks).astype(np.float32)
                pad_16k = resample(pad, RECORD_SAMPLE_RATE, WHISPER_SAMPLE_RATE)
                feed(transcriber, pad_16k)
                preroll_chunks.clear()
                preroll_len = 0
            chunk_16k = resample(chunk, RECORD_SAMPLE_RATE, WHISPER_SAMPLE_RATE)
            feed(transcriber, chunk_16k)
        else:
            preroll_chunks.append(chunk.copy())
            preroll_len += len(chunk)
            while preroll_len > preroll_target and preroll_chunks:
                dropped = preroll_chunks.pop(0)
                preroll_len -= len(dropped)

    mic = open_mic(on_chunk)
    mic.start()
    print("  🔴 Listening... Press ENTER to stop.")
    input()
    mic.stop()

    if vad_state["in_speech"] and vad_state["speech_samples"] > 0:
        on_speech_end()

    mic.close()

```

### transcription/vad/state.py

```python
def create_vad_state(sample_rate: int = 16000) -> dict:
    return {
        "sample_rate": sample_rate,
        "in_speech": False,
        "silence_count": 0,
        "speech_samples": 0,
    }


def reset_vad_state(state: dict) -> None:
    state["in_speech"] = False
    state["silence_count"] = 0
    state["speech_samples"] = 0

```

### tts/__init__.py

```python
from tts.model.singleton import get_model, is_loaded
from tts.generate.pipeline import generate_speech, generate_one
from tts.playback.stream import play_audio
from tts.playback.stop import stop_audio
from tts.engine import (
    create_engine,
    start_worker,
    feed_token,
    flush,
    interrupt,
    resume,
    speak_filler,
    is_speaking,
    shutdown,
)

```

### tts/download/__init__.py

```python
from tts.download.supertonic import ensure_downloaded

```

### tts/download/supertonic.py

```python
import warnings
from config.paths import SUPERTONIC_DIR

MODEL_ID = "onnx-community/Supertonic-TTS-2-ONNX"


def ensure_downloaded() -> str:
    """Download Supertonic 2 ONNX into models/supertonic/ if missing."""
    marker = SUPERTONIC_DIR / "onnx" / "text_encoder.onnx"
    if marker.exists():
        return str(SUPERTONIC_DIR)
    print(f"[Supertonic] Downloading {MODEL_ID} → {SUPERTONIC_DIR}")
    print("[Supertonic] (one-time ~200 MB download)")
    from huggingface_hub import snapshot_download

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        snapshot_download(repo_id=MODEL_ID, local_dir=str(SUPERTONIC_DIR))
    print("[Supertonic] Download complete.")
    return str(SUPERTONIC_DIR)


if __name__ == "__main__":
    print(ensure_downloaded())

```

### tts/engine/__init__.py

```python
from tts.engine.state import create_engine
from tts.engine.worker import start_worker
from tts.engine.feed import feed_token, flush
from tts.engine.control import interrupt, resume, speak_filler
from tts.engine.status import is_speaking, wait_until_done, shutdown

```

### tts/engine/control.py

```python
import random


def interrupt(engine: dict) -> None:
    """Stop playback and drain pending queue."""
    engine["interrupted"].set()
    _drain(engine)
    from tts.playback.stop import stop_audio

    stop_audio()


def resume(engine: dict) -> None:
    """Clear interrupted flag before next feed_token()."""
    engine["token_buf"] = ""
    engine["interrupted"].clear()


def speak_filler(engine: dict) -> None:
    """Enqueue a random filler at priority 0 (plays immediately)."""
    from tts.engine.queue import enqueue

    enqueue(engine, random.choice(engine["fillers"]), priority=0)


def _drain(engine: dict) -> None:
    while not engine["queue"].empty():
        try:
            engine["queue"].get_nowait()
        except Exception:
            break

```

### tts/engine/feed.py

```python
from tts.text.split import split_sentence, MIN_CHUNK_CHARS
from tts.engine.queue import enqueue

WORD_FLUSH_THRESHOLD = 8


def feed_token(engine: dict, token: str) -> None:
    """Accumulate token; push complete sentences/clauses to queue."""
    if engine["interrupted"].is_set():
        return
    engine["token_buf"] += token
    while True:
        sentence, remainder = split_sentence(engine["token_buf"])
        if sentence and len(sentence) >= MIN_CHUNK_CHARS:
            engine["token_buf"] = remainder
            enqueue(engine, sentence, priority=1)
        else:
            break
    if len(engine["token_buf"].split()) >= WORD_FLUSH_THRESHOLD:
        text = engine["token_buf"].strip()
        engine["token_buf"] = ""
        if text:
            enqueue(engine, text, priority=1)


def flush(engine: dict) -> None:
    """Push any remaining buffer."""
    text = engine["token_buf"].strip()
    engine["token_buf"] = ""
    if text and len(text) >= 2:
        enqueue(engine, text, priority=1)

```

### tts/engine/queue.py

```python
def enqueue(engine: dict, text: str, priority: int = 1) -> None:
    """priority=0 → filler (plays first), priority=1 → normal."""
    engine["queue"].put((priority, text))

```

### tts/engine/state.py

```python
import threading
import queue
import random

from config.tts import (
    SUPERTONIC_VOICE,
    SUPERTONIC_LANGUAGE,
    SUPERTONIC_STEPS,
    SUPERTONIC_SPEED,
)

_FILLERS = [
    "Mm-hmm.",
    "Sure.",
    "Okay.",
    "Right.",
    "Mm.",
    "Yeah.",
    "I see.",
    "Got it.",
    "Ah.",
    "Sure thing.",
]


def create_engine(
    voice: str = SUPERTONIC_VOICE,
    speed: float = SUPERTONIC_SPEED,
    steps: int = SUPERTONIC_STEPS,
    language: str = SUPERTONIC_LANGUAGE,
) -> dict:
    """Create TTS engine state dict. Call start_worker(engine) to begin."""
    return {
        "voice": voice,
        "speed": speed,
        "steps": steps,
        "language": language,
        "token_buf": "",
        "queue": queue.PriorityQueue(),
        "interrupted": threading.Event(),
        "speaking": threading.Event(),
        "running": False,
        "worker_thread": None,
        "fillers": _FILLERS,
    }


SENTINEL = (float("inf"), None)  # sorts last, always

```

### tts/engine/status.py

```python
import time


def is_speaking(engine: dict) -> bool:
    return engine["speaking"].is_set()


def wait_until_done(engine: dict, timeout: float = 2.0) -> None:
    deadline = time.time() + timeout
    time.sleep(0.05)
    while is_speaking(engine) and time.time() < deadline:
        time.sleep(0.02)


def shutdown(engine: dict) -> None:
    from tts.engine.control import interrupt

    interrupt(engine)

    from tts.engine.state import SENTINEL

    engine["queue"].put(SENTINEL)

    t = engine.get("worker_thread")
    if t:
        t.join(timeout=3)
    engine["running"] = False

```

### tts/engine/worker.py

```python
import threading
import time

MERGE_WINDOW_SEC = 0.05


def start_worker(engine: dict) -> None:
    engine["running"] = True
    t = threading.Thread(target=_loop, args=(engine,), daemon=True)
    t.start()
    engine["worker_thread"] = t


def _loop(engine: dict) -> None:
    from tts.generate.pipeline import generate_one
    from tts.playback.stream import play_audio
    from tts.text.clean import clean_markdown
    from tts.model.singleton import get_model

    model = get_model()  # warm up in worker thread

    while True:
        item = engine["queue"].get()
        priority, text = item
        if text is None:
            break

        if engine["interrupted"].is_set():
            continue

        collected = [text]
        if priority > 0:
            deadline = time.time() + MERGE_WINDOW_SEC
            while time.time() < deadline:
                try:
                    nxt_priority, nxt_text = engine["queue"].get_nowait()
                    if nxt_priority == 0:
                        engine["queue"].put((nxt_priority, nxt_text))
                        break
                    collected.append(nxt_text)
                except Exception:
                    time.sleep(0.005)

        if engine["interrupted"].is_set():
            continue

        merged = " ".join(clean_markdown(c) for c in collected if c.strip())
        if not merged:
            continue

        engine["speaking"].set()
        try:
            audio = generate_one(
                merged,
                voice=engine["voice"],
                speed=engine["speed"],
                steps=engine["steps"],
                language=engine["language"],
            )
            play_audio(audio, model["sample_rate"])
        except Exception as e:
            print(f"[TTS Engine] {e}")
        finally:
            engine["speaking"].clear()

```

### tts/generate/__init__.py

```python
from tts.generate.pipeline import generate_speech, generate_one

```

### tts/generate/canvas.py

```python
import numpy as np

LATENT_MARGIN = 3


def build_latent_canvas(
    durations: np.ndarray,
    latent_dim: int,
    chunk_compress_factor: int,
    latent_size: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Build noisy latent canvas + boolean mask. Adds margin to prevent tail clipping."""
    lat_lens = (durations + latent_size - 1) // latent_size + LATENT_MARGIN
    max_len = lat_lens.max()
    lat_mask = (np.arange(max_len) < lat_lens[:, None]).astype(np.int64)
    batch = durations.shape[0]
    latents = np.random.randn(
        batch, latent_dim * chunk_compress_factor, max_len
    ).astype(np.float32)
    latents *= lat_mask[:, None, :]
    return latents, lat_mask

```

### tts/generate/decode.py

```python
import numpy as np


def decode_waveform(latents: np.ndarray, model: dict) -> np.ndarray:
    """Decode latents → raw waveform via voice_decoder."""
    return model["voice_decoder"].run(None, {"latents": latents})[0]

```

### tts/generate/denoise.py

```python
import numpy as np


def run_denoiser(
    latents: np.ndarray,
    lat_mask: np.ndarray,
    style: np.ndarray,
    hidden: np.ndarray,
    attn: np.ndarray,
    steps: int,
    model: dict,
) -> np.ndarray:
    """Run latent diffusion denoiser for `steps` steps."""
    batch = latents.shape[0]
    n_steps = np.full(batch, steps, dtype=np.float32)
    for step in range(steps):
        ts = np.full(batch, step, dtype=np.float32)
        latents = model["latent_denoiser"].run(
            None,
            {
                "noisy_latents": latents,
                "latent_mask": lat_mask,
                "style": style,
                "encoder_outputs": hidden,
                "attention_mask": attn,
                "timestep": ts,
                "num_inference_steps": n_steps,
            },
        )[0]
    return latents

```

### tts/generate/encode.py

```python
import numpy as np


def encode_text(
    texts: list[str],
    model: dict,
    voice: str,
    speed: float,
    language: str,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Tokenise + encode texts. Returns (hidden, durations, attn_mask, style)."""
    from tts.model.voices import load_style

    tagged = [f"<{language}>{t}</{language}>" for t in texts]
    inputs = model["tokenizer"](
        tagged, return_tensors="np", padding=True, truncation=True
    )
    ids, attn = inputs["input_ids"], inputs["attention_mask"]
    style = load_style(voice, model["model_path"]).repeat(ids.shape[0], axis=0)
    hidden, raw_dur = model["text_encoder"].run(
        None, {"input_ids": ids, "attention_mask": attn, "style": style}
    )
    durations = (raw_dur / speed * model["sample_rate"]).astype(np.int64)
    return hidden, durations, attn, style

```

### tts/generate/pad.py

```python
import numpy as np

PRE_PAD_SEC = 0.03
POST_PAD_SEC = 0.08


def apply_padding(audio: np.ndarray, sample_rate: int) -> np.ndarray:
    """Prepend 30 ms + append 80 ms of silence. Prevents clipping at both edges."""
    pre = np.zeros(int(sample_rate * PRE_PAD_SEC), dtype=np.float32)
    post = np.zeros(int(sample_rate * POST_PAD_SEC), dtype=np.float32)
    return np.concatenate([pre, audio.astype(np.float32), post])


if __name__ == "__main__":
    import numpy as np

    a = np.ones(44100, dtype=np.float32)
    p = apply_padding(a, 44100)
    print(f"original: {len(a)}  padded: {len(p)}  (+{len(p)-len(a)})")

```

### tts/generate/pipeline.py

```python
import numpy as np

from tts.model.singleton import get_model
from tts.text.normalise import normalise_text
from tts.generate.canvas import build_latent_canvas
from tts.generate.encode import encode_text
from tts.generate.denoise import run_denoiser
from tts.generate.decode import decode_waveform
from tts.generate.pad import apply_padding
from config.tts import (
    SUPERTONIC_VOICE,
    SUPERTONIC_LANGUAGE,
    SUPERTONIC_STEPS,
    SUPERTONIC_SPEED,
)

VALID_LANGUAGES = ["en", "ko", "es", "pt", "fr"]


def generate_speech(
    texts: list[str],
    voice: str = SUPERTONIC_VOICE,
    speed: float = SUPERTONIC_SPEED,
    steps: int = SUPERTONIC_STEPS,
    language: str = SUPERTONIC_LANGUAGE,
) -> list[np.ndarray]:
    """Generate audio for a list of texts. Returns list of float32 arrays."""
    if language not in VALID_LANGUAGES:
        raise ValueError(f"Language '{language}' not supported. Use: {VALID_LANGUAGES}")
    model = get_model()
    normalised = [normalise_text(t) for t in texts]
    hidden, durations, attn, style = encode_text(
        normalised, model, voice, speed, language
    )
    latents, lat_mask = build_latent_canvas(
        durations,
        model["latent_dim"],
        model["chunk_compress_factor"],
        model["latent_size"],
    )
    latents = run_denoiser(latents, lat_mask, style, hidden, attn, steps, model)
    waveforms = decode_waveform(latents, model)
    return [
        apply_padding(
            waveforms[i, : int(lat_mask.sum(axis=1)[i]) * model["latent_size"]],
            model["sample_rate"],
        )
        for i in range(len(texts))
    ]


def generate_one(
    text: str,
    voice: str = SUPERTONIC_VOICE,
    speed: float = SUPERTONIC_SPEED,
    steps: int = SUPERTONIC_STEPS,
    language: str = SUPERTONIC_LANGUAGE,
) -> np.ndarray:
    return generate_speech(
        [text], voice=voice, speed=speed, steps=steps, language=language
    )[0]


if __name__ == "__main__":
    audio = generate_one("Hello, world!")
    sr = get_model()["sample_rate"]
    print(f"Generated {len(audio)/sr:.2f}s at {sr} Hz")
    from tts.playback.stream import play_audio

    play_audio(audio, sr)

```

### tts/model/__init__.py

```python
from tts.model.singleton import get_model, is_loaded
from tts.model.voices import load_style
from tts.model.load import load_supertonic

```

### tts/model/load.py

```python
import os
import onnxruntime as ort
from transformers import PreTrainedTokenizerFast


def load_supertonic(model_path: str) -> dict:
    """Load Supertonic 2 ONNX sessions dict."""
    opts = ort.SessionOptions()
    opts.log_severity_level = 3
    onnx_dir = os.path.join(model_path, "onnx")
    tokenizer_file = os.path.join(model_path, "tokenizer.json")
    print(f"[Supertonic] Loading from {model_path} ...\n")
    sessions = {
        "tokenizer": PreTrainedTokenizerFast(
            tokenizer_file=tokenizer_file,
            model_max_length=1000,
            pad_token=" ",
        ),
        "text_encoder": ort.InferenceSession(
            os.path.join(onnx_dir, "text_encoder.onnx"), opts
        ),
        "latent_denoiser": ort.InferenceSession(
            os.path.join(onnx_dir, "latent_denoiser.onnx"), opts
        ),
        "voice_decoder": ort.InferenceSession(
            os.path.join(onnx_dir, "voice_decoder.onnx"), opts
        ),
        "model_path": model_path,
        "sample_rate": 44100,
        "chunk_compress_factor": 6,
        "base_chunk_size": 512,
        "latent_dim": 24,
        "style_dim": 128,
        "latent_size": 512 * 6,  # 3072
    }
    print("[Supertonic] Ready.")
    return sessions

```

### tts/model/singleton.py

```python
import threading

_model: dict | None = None
_lock = threading.Lock()


def get_model() -> dict:
    global _model
    if _model is not None:
        return _model
    with _lock:
        if _model is not None:
            return _model
        from tts.download.supertonic import ensure_downloaded
        from tts.model.load import load_supertonic

        _model = load_supertonic(ensure_downloaded())
    return _model


def is_loaded() -> bool:
    return _model is not None

```

### tts/model/voices.py

```python
import os
import numpy as np

VALID_VOICES = ["M1", "M2", "M3", "M4", "M5", "F1", "F2", "F3", "F4", "F5"]
STYLE_DIM = 128


def load_style(voice: str, model_path: str) -> np.ndarray:
    """Load voice style embedding → shape (1, N, 128)."""
    if voice not in VALID_VOICES:
        raise ValueError(f"Voice '{voice}' invalid. Choose from: {VALID_VOICES}")
    path = os.path.join(model_path, "voices", f"{voice}.bin")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Voice file not found: {path}")
    return np.fromfile(path, dtype=np.float32).reshape(1, -1, STYLE_DIM)


if __name__ == "__main__":
    from tts.model.singleton import get_model

    m = get_model()
    print(load_style("F1", m["model_path"]).shape)

```

### tts/playback/__init__.py

```python
from tts.playback.stream import play_audio
from tts.playback.stop import stop_audio

```

### tts/playback/stop.py

```python
def stop_audio() -> None:
    """Abort current OutputStream mid-playback."""
    import tts.playback.stream as _m

    with _m._out_stream_lock:
        stream = _m._out_stream
    if stream is not None:
        try:
            stream.abort()
        except Exception:
            pass

```

### tts/playback/stream.py

```python
import threading
import numpy as np

_out_stream = None
_out_stream_lock = threading.Lock()


def play_audio(audio: np.ndarray, sample_rate: int = 44100) -> None:
    """
    Play audio through a dedicated OutputStream (blocking).
    Coexists safely with a mic InputStream — does not touch shared HAL state.
    """
    import sounddevice as sd
    from audio.transform.normalise import normalise

    global _out_stream

    audio = normalise(audio)
    done, pos = threading.Event(), [0]

    def _cb(outdata, frames, time_info, status):
        chunk = audio[pos[0] : pos[0] + frames]
        if len(chunk) < frames:
            outdata[: len(chunk), 0] = chunk
            outdata[len(chunk) :, 0] = 0.0
            pos[0] += len(chunk)
            done.set()
            raise sd.CallbackStop
        outdata[:, 0] = chunk
        pos[0] += frames

    try:
        stream = sd.OutputStream(
            samplerate=sample_rate,
            channels=1,
            dtype="float32",
            callback=_cb,
            finished_callback=done.set,
        )
        with _out_stream_lock:
            _out_stream = stream
        with stream:
            stream.start()
            done.wait()
    except Exception:
        pass
    finally:
        with _out_stream_lock:
            _out_stream = None

```

### tts/text/__init__.py

```python
from tts.text.normalise import normalise_text
from tts.text.clean import clean_markdown
from tts.text.split import split_sentence, MIN_CHUNK_CHARS

```

### tts/text/clean.py

```python
import re


def clean_markdown(text: str) -> str:
    """Strip markdown symbols that would be spoken literally."""
    text = re.sub(r"\*+", "", text)
    text = re.sub(r"_+", "", text)
    text = re.sub(r"`+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


if __name__ == "__main__":
    print(clean_markdown("**Bold** and _italic_ with `code`"))

```

### tts/text/normalise.py

```python
def normalise_text(text: str) -> str:
    """Ensure terminal punctuation; add prosody lead-in for short inputs."""
    text = text.strip()
    if not text:
        return text
    if text[-1] not in ".!?,;:":
        text += "."
    if len(text.split()) <= 3:
        text = ", " + text
    return text


if __name__ == "__main__":
    for t in ["Hello", "How are you", "Already a sentence."]:
        print(f"'{t}' → '{normalise_text(t)}'")

```

### tts/text/split.py

```python
import re

_SENTENCE_END = re.compile(r"(?<![A-Z][a-z])(?<!\d)([.?!])(\s+|$)")
_CLAUSE_BREAK = re.compile(r"[,;:]\s+")
MIN_CHUNK_CHARS = 6


def split_sentence(buf: str) -> tuple[str, str]:
    """Split buf at first sentence/clause boundary. Returns (chunk, remainder)."""
    m = _SENTENCE_END.search(buf)
    if m:
        return buf[: m.end()].strip(), buf[m.end() :]
    m = _CLAUSE_BREAK.search(buf)
    if m and m.start() >= MIN_CHUNK_CHARS:
        return buf[: m.start()].strip(), buf[m.end() :]
    return "", buf


if __name__ == "__main__":
    print(split_sentence("Hello world. This is a test."))
    print(split_sentence("Waiting, for more"))

```

### ui/__init__.py

```python
from ui.console import (
    show_partial,
    show_speaking,
    show_stt_final,
    show_you,
    start_ai_line,
    prompt_you,
)

```

### ui/console.py

```python
def show_partial(text: str) -> None:
    print(f"\r  \033[90m... {text:<80}\033[0m", end="", flush=True)


def show_speaking() -> None:
    print(f"\r  \033[33m● Speaking...{' ' * 60}\033[0m", flush=True)


def show_stt_final(text: str) -> None:
    print(f"\r  \033[92m✓ {text:<80}\033[0m", flush=True)


def show_you(text: str) -> None:
    print(f"\r  \033[94mYOU:\033[0m {text}")


def start_ai_line() -> None:
    print("  \033[92mAI :\033[0m ", end="", flush=True)


def prompt_you() -> None:
    print("  YOU: ", end="", flush=True)

```