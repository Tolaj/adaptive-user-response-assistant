# PromptPack Output

**Root:** `/Users/swapnil/Documents/Projects/adaptive-user-response-assistant`
**Generated:** 2026-03-09T14:56:32.409Z

---

## 1) Folder Structure

```txt
.
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
│     ├─ denoise.py
│     ├─ mono.py
│     ├─ normalise.py
│     └─ resample.py
├─ audio_000.wav
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
│  ├─ vlm.py
│  └─ whisper.py
├─ jobhunter/
│  ├─ actions.py
│  ├─ agent.py
│  ├─ browser.py
│  ├─ config.py
│  ├─ data/
│  │  └─ jobs.db
│  ├─ logger.py
│  ├─ profile.py
│  ├─ scheduler.py
│  ├─ snap.py
│  ├─ storage.py
│  └─ vlm_query.py
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
│  ├─ prompt/
│  │  ├─ __init__.py
│  │  ├─ build.py
│  │  └─ system.py
│  └─ tools/
├─ logs/
├─ main_jobhunter.py
├─ main.py
├─ requirements.txt
├─ sentence_04.wav
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
├─ test_audio_000.wav
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
│     ├─ ptt.py
│     ├─ session.py
│     ├─ silero.py
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
│  ├─ kokoro/
│  ├─ model/
│  │  ├─ __init__.py
│  │  ├─ load.py
│  │  ├─ singleton.py
│  │  └─ voices.py
│  ├─ orpheus/
│  ├─ playback/
│  │  ├─ __init__.py
│  │  ├─ stop.py
│  │  └─ stream.py
│  ├─ qwen/
│  └─ text/
│     ├─ __init__.py
│     ├─ clean.py
│     ├─ normalise.py
│     └─ split.py
├─ ui/
│  ├─ __init__.py
│  └─ console.py
└─ vision/
   ├─ __init__.py
   ├─ backup/
   │  ├─ app.py
   │  └─ server.py
   ├─ camera.py
   ├─ download/
   │  ├─ __init__.py
   │  └─ vlm.py
   ├─ inference/
   │  ├─ query.py
   │  └─ snap.py
   └─ model/
      ├─ load.py
      └─ singleton.py
```

<!-- PAGE BREAK: FILE CONTENTS BELOW -->

## 2) File Contents


### audio_000.wav

(Skipped: binary or unreadable file)


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
# audio/gate/__init__.py

from audio.gate.rms import rms
from audio.gate.amplitude import mean_amplitude
from audio.gate.zcr import zero_crossing_rate

```

### audio/gate/amplitude.py

```python
# audio/gate/amplitude.py
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
# audio/gate/rms.py
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
# audio/gate/zcr.py
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
# audio/io/mic.py
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
                device=sd.default.device[0],
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
# audio/transform/__init__.py
from audio.transform.mono import to_mono
from audio.transform.resample import resample
from audio.transform.normalise import normalise

```

### audio/transform/denoise.py

```python
# audio/transform/denoise.py
import numpy as np


def denoise(
    audio: np.ndarray, noise_profile: np.ndarray, sr: int = 16000
) -> np.ndarray:
    """
    Reduce noise in audio using a noise profile sample.
    noise_profile: a short clip of background noise (from preroll).
    Returns cleaned float32 array same length as audio.
    """
    try:
        import noisereduce as nr

        return nr.reduce_noise(
            y=audio.astype(np.float32),
            sr=sr,
            y_noise=noise_profile.astype(np.float32),
            stationary=False,
            prop_decrease=0.8,  # 0.8 = aggressive but keeps speech natural
        ).astype(np.float32)
    except Exception as e:
        print(f"[Denoise] {e}")
        return audio

```

### audio/transform/mono.py

```python
# audio/transform/mono.py
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
# audio/transform/normalise.py
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
# audio/transform/resample.py
import numpy as np
import resampy


def resample(audio: np.ndarray, from_sr: int, to_sr: int) -> np.ndarray:
    """Resample audio using scipy. No-op if rates match."""
    if from_sr == to_sr:
        return audio.astype(np.float32)
    from scipy.signal import resample_poly
    from math import gcd

    g = gcd(from_sr, to_sr)
    return resample_poly(audio, to_sr // g, from_sr // g).astype(np.float32)


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
# config/features.py
# ── Mode selector ─────────────────────────────────────────────
# Pick ONE mode:
#   "server"                → Flask + WebSocket server only
#   "stt_only"              → Mic → Whisper, print transcript
#   "tts_only"              → Type text → speak it aloud
#   "text_to_text_chat"     → Type text → LLM → print response (no audio)
#   "voice_to_text_chat"    → Mic → Whisper → LLM → print response (no TTS)
#   "full"                  → Mic → Whisper → LLM → TTS (everything)

MODE = "vision_text"

# ── Derived flags (do not edit) ───────────────────────────────
ENABLE_STT = MODE in ("tts_only", "voice_to_text_chat", "full")
ENABLE_TTS = MODE in ("tts_only", "full")
ENABLE_LLM = MODE in ("text_to_text_chat", "voice_to_text_chat", "full", "tts_only")
ENABLE_SERVER = MODE == "server"
ENABLE_VISION = MODE in ("vision_text", "vision_speech")
SHOW_TEXT = True

```

### config/llm.py

```python
import os

ACTIVE_LLM_MODEL = "arbllm"
GPU_LAYERS = 36
CONTEXT_SIZE = 2048
CPU_THREADS = max(1, os.cpu_count() // 2)

```

### config/paths.py

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

### config/prompt.py

```python
# config/prompt.py
VOICE_SYSTEM_PROMPT = (
    "You are a concise voice assistant. " "Never use lists or markdown."
)
VOICE_MAX_TOKENS = 60  # was 150 — prevents long multi-chunk responses
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

### config/vad.py

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
PUSH_TO_TALK = True

```

### config/vlm.py

```python
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

VLM_BACKEND = "server"  # "package" or "server"

# Model paths
VLM_MODEL_PATH = str(BASE_DIR / "models/vlm/qwen3vl2b/Qwen3VL-2B-Instruct-Q4_K_M.gguf")
VLM_MMPROJ_PATH = str(BASE_DIR / "models/vlm/qwen3vl2b/mmproj-Qwen3-VL-2B-Instruct-Q8_0.gguf")

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

```

### config/whisper.py

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

### jobhunter/actions.py

```python
# jobhunter/actions.py
# ─────────────────────────────────────────────────────────────────────────────
# Executes browser actions from VLM decisions using Playwright.
# VLM says: {"action": "click", "x": 432, "y": 287}
# This module does: page.mouse.click(432, 287)
# ─────────────────────────────────────────────────────────────────────────────

import time
from jobhunter.config import ACTION_DELAY_MS, PAGE_LOAD_WAIT_MS


def execute_action(action: dict) -> str:
    """
    Execute a single action from VLM output.
    Returns the action type executed, or "unknown" if unrecognised.
    """
    from jobhunter.browser import get_browser, navigate

    page = get_browser()
    action_type = action.get("action", "unknown")

    try:
        if action_type == "click":
            x = int(action.get("x", 0))
            y = int(action.get("y", 0))
            # Human-like: move then click
            page.mouse.move(x, y)
            time.sleep(0.1)
            page.mouse.click(x, y)
            page.wait_for_timeout(ACTION_DELAY_MS)

        elif action_type == "type":
            text = action.get("text", "")
            page.keyboard.type(text, delay=50)  # 50ms between keys = human-like
            page.wait_for_timeout(500)

        elif action_type == "scroll":
            direction = action.get("direction", "down")
            delta = 600 if direction == "down" else -600
            page.mouse.wheel(0, delta)
            page.wait_for_timeout(ACTION_DELAY_MS)

        elif action_type == "wait":
            page.wait_for_timeout(PAGE_LOAD_WAIT_MS)

        elif action_type == "navigate":
            url = action.get("url", "")
            if url:
                navigate(url)

        elif action_type in ("extract", "done"):
            pass  # handled by caller

        else:
            print(f"[Actions] Unknown action type: {action_type}")

    except Exception as e:
        print(f"[Actions] Failed to execute {action_type}: {e}")

    return action_type


def press_enter():
    """Press Enter key — useful after typing search queries."""
    from jobhunter.browser import get_browser
    page = get_browser()
    page.keyboard.press("Enter")
    page.wait_for_timeout(PAGE_LOAD_WAIT_MS)


def click_at(x: int, y: int):
    """Direct click — used for known coordinates."""
    from jobhunter.browser import get_browser
    page = get_browser()
    page.mouse.move(x, y)
    time.sleep(0.15)
    page.mouse.click(x, y)
    page.wait_for_timeout(ACTION_DELAY_MS)


def type_text(text: str):
    """Type text with human-like delay."""
    from jobhunter.browser import get_browser
    page = get_browser()
    page.keyboard.type(text, delay=60)
    page.wait_for_timeout(400)

```

### jobhunter/agent.py

```python
# jobhunter/agent.py
# ─────────────────────────────────────────────────────────────────────────────
# The core VLM agent loop.
# Takes ONE screenshot → asks VLM what to do → executes → repeats.
# This is the "eyes + brain" of the job hunter.
#
# Flow per site per query:
#   1. Navigate to site
#   2. VLM sees page → decides: type search / click / scroll / extract / done
#   3. Execute action
#   4. Repeat until VLM says "extract" or "done" or max actions reached
#   5. Extract job listings from page
#   6. Score each job against profile
#   7. Save high-scoring jobs to CSV
# ─────────────────────────────────────────────────────────────────────────────

import time
from jobhunter.config import MAX_ACTIONS_PER_PAGE, MAX_JOBS_PER_SITE, MIN_SCORE_TO_SAVE
from jobhunter.vlm_query import decide_action, extract_jobs_from_page, score_job
from jobhunter.actions import execute_action
from jobhunter.storage import save_job, is_seen
from jobhunter.logger import log


# ── Entry URLs per site ────────────────────────────────────────────────────
SITE_URLS = {
    "linkedin":  "https://www.linkedin.com/jobs",
    "indeed":    "https://www.indeed.com",
    "naukri":    "https://www.naukri.com",
    "wellfound": "https://wellfound.com/jobs",
}


def hunt_site(site: str, query: str, profile: dict) -> int:
    """
    Run the VLM agent on one site with one search query.
    Returns the number of NEW jobs saved.
    """
    from jobhunter.browser import navigate

    log(f"[{site.upper()}] Starting hunt for: '{query}'")

    # ── Step 1: Navigate to site ──────────────────────────────────────────
    url = SITE_URLS.get(site, "https://www.google.com")
    navigate(url)

    # ── Step 2: VLM action loop ───────────────────────────────────────────
    goal = (
        f"Search for '{query}' jobs on this site. "
        f"Type the query in the search box, press enter, "
        f"then scroll through results. "
        f"When you can see job listings, say action=extract."
    )

    jobs_saved = 0
    total_extracted = 0

    for step in range(MAX_ACTIONS_PER_PAGE):
        log(f"[{site.upper()}] Step {step+1}/{MAX_ACTIONS_PER_PAGE}")

        action = decide_action(goal)
        action_type = action.get("action", "unknown")

        if action_type == "done":
            log(f"[{site.upper()}] VLM says done.")
            break

        if action_type == "extract":
            # ── Step 3: Extract jobs from current page view ───────────────
            log(f"[{site.upper()}] Extracting jobs from page...")
            jobs = extract_jobs_from_page()
            total_extracted += len(jobs)

            # ── Step 4: Score and save each job ───────────────────────────
            for job in jobs:
                title   = job.get("title", "")
                company = job.get("company", "")

                if not title or not company:
                    continue

                # Skip if already seen
                if is_seen(title, company, site):
                    log(f"  [SKIP] Already seen: {title} @ {company}")
                    continue

                # Quick keyword filter before spending VLM tokens on scoring
                avoid = profile.get("avoid_keywords", [])
                combined_text = f"{title} {job.get('snippet', '')}".lower()
                if any(kw.lower() in combined_text for kw in avoid):
                    log(f"  [SKIP] Avoided keyword in: {title}")
                    continue

                # Score the job
                score_result = score_job(job, profile)
                score        = int(score_result.get("score", 5))
                reason       = score_result.get("reason", "")

                if score >= MIN_SCORE_TO_SAVE:
                    saved = save_job(job, site, score, reason)
                    if saved:
                        jobs_saved += 1
                        log(f"  [SAVED ★{score}] {title} @ {company} — {reason}")
                    else:
                        log(f"  [DUP] {title} @ {company}")
                else:
                    log(f"  [LOW ★{score}] {title} @ {company} — {reason}")

                if total_extracted >= MAX_JOBS_PER_SITE:
                    log(f"[{site.upper()}] Reached max jobs limit ({MAX_JOBS_PER_SITE})")
                    return jobs_saved

            # After extraction, scroll to see more jobs
            goal = (
                "Scroll down to see more job listings. "
                "If more listings are visible, say action=extract again. "
                "If no more listings, say action=done."
            )

        else:
            # Execute navigation action (click, type, scroll, wait, navigate)
            execute_action(action)

    log(f"[{site.upper()}] Done. Saved {jobs_saved} new jobs from '{query}'.")
    return jobs_saved


def run_full_hunt(profile: dict, search_queries: dict) -> dict:
    """
    Run the full job hunt across all sites and all queries.
    Returns a summary dict.
    """
    from jobhunter.storage import get_stats

    summary = {}
    total_new = 0

    for site, queries in search_queries.items():
        site_new = 0
        for query in queries:
            try:
                new = hunt_site(site, query, profile)
                site_new += new
                total_new += new
                # Small pause between queries — be polite to the server
                time.sleep(3)
            except Exception as e:
                log(f"[ERROR] {site} / '{query}': {e}")
        summary[site] = site_new
        log(f"[SUMMARY] {site}: {site_new} new jobs")

    stats = get_stats()
    log(
        f"\n{'='*50}\n"
        f"HUNT COMPLETE\n"
        f"  New this run:  {total_new}\n"
        f"  Found today:   {stats['today']}\n"
        f"  Total in DB:   {stats['total']}\n"
        f"{'='*50}\n"
    )

    return {"new_this_run": total_new, "stats": stats, "by_site": summary}

```

### jobhunter/browser.py

```python
# jobhunter/browser.py
# ─────────────────────────────────────────────────────────────────────────────
# Launches Playwright Chromium and injects real Chrome cookies from Keychain.
# Fixes: cookie field validation, browser stability, reconnection handling.
# ─────────────────────────────────────────────────────────────────────────────

import threading
import time
from jobhunter.config import SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT

COOKIE_DOMAINS = [
    "linkedin.com",
    "indeed.com",
    "naukri.com",
    "wellfound.com",
    "google.com",
]

_browser    = None   # keep browser alive at module level
_context    = None
_page       = None
_playwright = None
_lock       = threading.Lock()


def _clean_cookie(c) -> dict | None:
    """
    Convert a browser_cookie3 cookie into a valid Playwright cookie dict.
    Returns None if the cookie should be skipped.
    """
    import time as _time

    name  = getattr(c, "name",  None)
    value = getattr(c, "value", None)

    # Skip cookies with missing required fields
    if not name or value is None:
        return None

    # Domain: must start with dot for cross-subdomain cookies
    domain = getattr(c, "domain", "") or ""
    if not domain:
        return None
    if not domain.startswith("."):
        domain = "." + domain

    # Path
    path = getattr(c, "path", "/") or "/"

    # Expiry: must be a positive number in the future, or omitted
    expires = getattr(c, "expires", None)
    cookie = {
        "name":     name,
        "value":    str(value),
        "domain":   domain,
        "path":     path,
        "secure":   bool(getattr(c, "secure", False)),
        "httpOnly": False,
        "sameSite": "Lax",
    }

    # Only add expires if it's a valid future timestamp
    if expires and isinstance(expires, (int, float)) and expires > _time.time():
        cookie["expires"] = float(expires)

    return cookie


def _get_cookies() -> list[dict]:
    """Read Chrome cookies from macOS Keychain and clean them for Playwright."""
    try:
        import browser_cookie3
    except ImportError:
        raise RuntimeError("Run: pip install browser-cookie3")

    print("[Browser] Reading cookies from macOS Keychain...")
    all_cookies = []
    seen = set()

    for domain in COOKIE_DOMAINS:
        try:
            jar = browser_cookie3.chrome(domain_name=domain)
            for c in jar:
                cleaned = _clean_cookie(c)
                if cleaned is None:
                    continue
                # Deduplicate by name+domain
                key = (cleaned["name"], cleaned["domain"])
                if key in seen:
                    continue
                seen.add(key)
                all_cookies.append(cleaned)
        except Exception as e:
            print(f"[Browser] Skipped {domain}: {e}")

    print(f"[Browser] {len(all_cookies)} valid cookies loaded ✓")
    return all_cookies


def _create_browser_and_page():
    """Launch Playwright browser, inject cookies, return (browser, context, page)."""
    global _playwright

    from playwright.sync_api import sync_playwright

    if _playwright is None:
        _playwright = sync_playwright().start()

    cookies = _get_cookies()

    print("[Browser] Launching browser...")
    browser = _playwright.chromium.launch(
        headless=False,
        args=[
            f"--window-size={SCREENSHOT_WIDTH},{SCREENSHOT_HEIGHT}",
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-web-security",
            "--disable-features=IsolateOrigins,site-per-process",
        ],
    )

    context = browser.new_context(
        viewport={"width": SCREENSHOT_WIDTH, "height": SCREENSHOT_HEIGHT},
        user_agent=(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
    )

    # Inject cookies one by one — skip any that still fail
    injected, failed = 0, 0
    for cookie in cookies:
        try:
            context.add_cookies([cookie])
            injected += 1
        except Exception:
            failed += 1

    print(f"[Browser] Injected {injected} cookies ({failed} skipped) ✓")

    page = context.new_page()

    # Keep browser alive — attach close handler to detect crashes
    def _on_close():
        print("[Browser] Browser window was closed.")

    browser.on("disconnected", _on_close)

    return browser, context, page


def get_browser():
    """Get a ready page. Auto-recovers if browser was closed."""
    global _browser, _context, _page, _playwright

    # Fast path — check if existing page is alive
    if _page is not None:
        try:
            _ = _page.url   # lightweight liveness check (cheaper than title())
            return _page
        except Exception:
            print("[Browser] Page lost — relaunching browser...")
            _page    = None
            _context = None
            _browser = None

    with _lock:
        if _page is not None:
            return _page

        _browser, _context, _page = _create_browser_and_page()
        print(f"[Browser] Ready ✓ — logged in as swapnilhgf@gmail.com")

    return _page


def release_browser():
    """Close the job hunter browser. Your real Chrome is untouched."""
    global _browser, _context, _page, _playwright

    with _lock:
        _page = None
        _context = None

        if _browser:
            try:
                _browser.close()
            except Exception:
                pass
            _browser = None

        if _playwright:
            try:
                _playwright.stop()
            except Exception:
                pass
            _playwright = None

        print("[Browser] Closed. Your Chrome is untouched.")


def navigate(url: str) -> None:
    from jobhunter.config import PAGE_LOAD_WAIT_MS
    page = get_browser()
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(PAGE_LOAD_WAIT_MS)
    except Exception as e:
        print(f"[Browser] Navigation error: {e} — retrying...")
        time.sleep(2)
        page = get_browser()
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(PAGE_LOAD_WAIT_MS)


def current_url() -> str:
    try:
        return get_browser().url
    except Exception:
        return ""

```

### jobhunter/config.py

```python
# jobhunter/config.py
# ─────────────────────────────────────────────────────────────────────────────
# Job hunter runtime configuration — tweak these without touching core logic
# ─────────────────────────────────────────────────────────────────────────────

from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).parent
DATA_DIR    = BASE_DIR / "data"
DB_PATH     = DATA_DIR / "jobs.db"
CSV_PATH    = DATA_DIR / "jobs_found.csv"
LOG_PATH    = DATA_DIR / "jobhunter.log"

DATA_DIR.mkdir(parents=True, exist_ok=True)

# ── Scheduler ─────────────────────────────────────────────────────────────
RUN_EVERY_HOURS = 2       # how often the full hunt cycle runs

# ── VLM settings (mirrors your config/vlm.py style) ──────────────────────
VLM_SERVER_PORT = 8081    # must match your config/vlm.py VLM_SERVER_PORT
VLM_MAX_TOKENS  = 120     # slightly more than vision assistant — needs JSON
VLM_TEMPERATURE = 0.1     # low = consistent, deterministic action decisions

# ── Agent loop limits ──────────────────────────────────────────────────────
MAX_ACTIONS_PER_PAGE  = 40   # max VLM → click/type steps before giving up
MAX_JOBS_PER_SITE     = 20   # stop scrolling after collecting this many
ACTION_DELAY_MS       = 1500 # ms to wait after each action (human-like)
PAGE_LOAD_WAIT_MS     = 2500 # ms to wait after navigation

# ── Screenshot settings (mirrors your config/vlm.py camera settings) ──────
SCREENSHOT_WIDTH  = 1280
SCREENSHOT_HEIGHT = 800
JPEG_QUALITY      = 75    # higher than camera — need to read text clearly

# ── Scoring thresholds ─────────────────────────────────────────────────────
MIN_SCORE_TO_SAVE = 5     # VLM scores 1–10; only save jobs >= this score

```

### jobhunter/data/jobs.db

(Skipped: binary or unreadable file)


### jobhunter/logger.py

```python
# jobhunter/logger.py
# ─────────────────────────────────────────────────────────────────────────────
# Simple file + console logger. Mirrors server/logger.py style.
# ─────────────────────────────────────────────────────────────────────────────

from datetime import datetime
from jobhunter.config import LOG_PATH


def log(message: str) -> None:
    """Print to console and append to log file."""
    ts  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {message}"
    print(line, flush=True)
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass  # never crash because of logging

```

### jobhunter/profile.py

```python
# jobhunter/profile.py
# ─────────────────────────────────────────────────────────────────────────────
# EDIT THIS FILE with your real details before running the job hunter.
# The VLM uses this profile to score and filter jobs intelligently.
# ─────────────────────────────────────────────────────────────────────────────

PROFILE = {
    # ── Who you are ───────────────────────────────────────────────────────────
    "name": "Swapnil",
    "job_titles": [
        "Junior Software Developer",
        "Junior Python Developer",
        "Junior Backend Developer",
        "Junior Full Stack Developer",
    ],

    # ── Skills (VLM will check job descriptions for these) ───────────────────
    "skills": [
        "Python",
        "JavaScript",
        "React",
        "Node.js",
        "REST APIs",
        "SQL",
        "Git",
        "Docker",  # remove if you don't know this
    ],

    # ── Experience ────────────────────────────────────────────────────────────
    "years_experience": 1,   # 0–2 for junior
    "education": "Bachelor's in Computer Science",  # or your actual degree

    # ── Location preferences ──────────────────────────────────────────────────
    "location": "India",           # your country/city
    "remote_preference": "remote", # "remote", "hybrid", "onsite", or "any"
    "open_to_relocation": False,

    # ── Salary filter ─────────────────────────────────────────────────────────
    # Set to None to disable salary filtering
    "min_salary_lpa": None,        # e.g. 4 means ₹4 LPA minimum (for India)
    "currency": "INR",             # "INR", "USD", "EUR" etc.

    # ── Keywords to AVOID ─────────────────────────────────────────────────────
    # Jobs containing any of these will be skipped
    "avoid_keywords": [
        "senior",
        "lead",
        "10+ years",
        "5+ years",
        "unpaid",
        "internship",   # remove this if you want internships
        "blockchain",
        "web3",
    ],

    # ── Keywords you WANT ─────────────────────────────────────────────────────
    # Jobs with these get a score boost
    "prefer_keywords": [
        "python",
        "backend",
        "api",
        "startup",
        "product",
    ],
}

# ── Search queries per site ────────────────────────────────────────────────────
# These are what get typed into each job site's search box
SEARCH_QUERIES = {
    "linkedin": [
        "junior python developer remote",
        "junior backend developer india",
        "junior software developer remote india",
    ],
    "indeed": [
        "junior python developer",
        "junior software developer remote",
        "entry level backend developer",
    ],
    "naukri": [
        "junior python developer",
        "junior software developer",
        "entry level developer",
    ],
    "wellfound": [
        "junior engineer python",
        "software engineer junior remote",
    ],
}

# ── Site credentials (needed for LinkedIn login) ──────────────────────────────
CREDENTIALS = {
    "linkedin": {
        "email": "your_email@gmail.com",     # ← EDIT THIS
        "password": "your_password_here",     # ← EDIT THIS
    },
    # Indeed, Naukri, Wellfound work without login for basic search
}

```

### jobhunter/scheduler.py

```python
# jobhunter/scheduler.py
# ─────────────────────────────────────────────────────────────────────────────
# Keeps the job hunt running all day.
# Runs immediately on start, then every RUN_EVERY_HOURS hours.
# ─────────────────────────────────────────────────────────────────────────────

import time
import schedule
from datetime import datetime

from jobhunter.config import RUN_EVERY_HOURS
from jobhunter.logger import log


def _run_hunt():
    """Single hunt cycle — called by scheduler."""
    from jobhunter.profile import PROFILE, SEARCH_QUERIES
    from jobhunter.agent import run_full_hunt

    log(f"\n{'='*50}")
    log(f"HUNT CYCLE STARTING — {datetime.now().strftime('%A %d %b %Y, %H:%M')}")
    log(f"{'='*50}")

    try:
        result = run_full_hunt(PROFILE, SEARCH_QUERIES)
        log(f"Cycle complete. {result['new_this_run']} new jobs saved.")
    except Exception as e:
        log(f"[ERROR] Hunt cycle crashed: {e}")
        import traceback
        log(traceback.format_exc())


def start_scheduler():
    """
    Run immediately, then repeat every RUN_EVERY_HOURS hours.
    Blocks forever — call from main_jobhunter.py.
    """
    log(f"Job hunter scheduler starting.")
    log(f"Will run every {RUN_EVERY_HOURS} hour(s). Press Ctrl+C to stop.\n")

    # Run once immediately
    _run_hunt()

    # Then schedule repeating runs
    schedule.every(RUN_EVERY_HOURS).hours.do(_run_hunt)

    while True:
        schedule.run_pending()
        time.sleep(60)  # check every minute

```

### jobhunter/snap.py

```python
# jobhunter/snap.py
# ─────────────────────────────────────────────────────────────────────────────
# Captures the current browser page as a base64 JPEG.
# Mirrors vision/inference/snap.py — same interface, different source.
# Instead of webcam → we capture the Playwright browser page.
# ─────────────────────────────────────────────────────────────────────────────

import base64
from jobhunter.config import JPEG_QUALITY


def snap_browser_b64() -> str:
    """
    Screenshot the current browser page → base64 JPEG string.
    Drop-in replacement for vision/inference/snap.py snap_b64().
    """
    from jobhunter.browser import get_browser

    page = get_browser()

    # Full PNG screenshot from Playwright
    png_bytes = page.screenshot(full_page=False)  # viewport only — faster

    # Convert PNG → JPEG for smaller payload (same as camera pipeline)
    from PIL import Image
    import io

    img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=JPEG_QUALITY)
    return base64.b64encode(buf.getvalue()).decode()

```

### jobhunter/storage.py

```python
# jobhunter/storage.py
# ─────────────────────────────────────────────────────────────────────────────
# SQLite for deduplication + CSV for your readable output.
# Every job gets a unique ID (hash of title+company+site).
# If the same job is found again, it's silently skipped.
# ─────────────────────────────────────────────────────────────────────────────

import csv
import hashlib
import sqlite3
from datetime import datetime
from pathlib import Path

from jobhunter.config import DB_PATH, CSV_PATH


# ── Schema ─────────────────────────────────────────────────────────────────
_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS jobs (
    id          TEXT PRIMARY KEY,
    title       TEXT,
    company     TEXT,
    location    TEXT,
    salary      TEXT,
    posted      TEXT,
    url         TEXT,
    snippet     TEXT,
    site        TEXT,
    score       INTEGER,
    score_reason TEXT,
    found_at    TEXT
);
"""

_CSV_HEADERS = [
    "found_at", "site", "score", "title", "company",
    "location", "salary", "posted", "url", "snippet", "score_reason"
]


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute(_CREATE_TABLE)
    conn.commit()
    return conn


def _job_id(title: str, company: str, site: str) -> str:
    """Stable hash — same job from same site always gets same ID."""
    raw = f"{title.lower().strip()}|{company.lower().strip()}|{site.lower()}"
    return hashlib.md5(raw.encode()).hexdigest()


def is_seen(title: str, company: str, site: str) -> bool:
    """Return True if this job is already in the database."""
    job_id = _job_id(title, company, site)
    conn = _get_conn()
    row = conn.execute("SELECT 1 FROM jobs WHERE id=?", (job_id,)).fetchone()
    conn.close()
    return row is not None


def save_job(job: dict, site: str, score: int, score_reason: str) -> bool:
    """
    Save a job to SQLite + append to CSV.
    Returns True if saved (new), False if duplicate (skipped).
    """
    title   = job.get("title", "Unknown")
    company = job.get("company", "Unknown")

    if is_seen(title, company, site):
        return False  # already have this one

    job_id   = _job_id(title, company, site)
    found_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    row = {
        "id":           job_id,
        "title":        title,
        "company":      company,
        "location":     job.get("location", ""),
        "salary":       job.get("salary", ""),
        "posted":       job.get("posted", ""),
        "url":          job.get("url", ""),
        "snippet":      job.get("snippet", ""),
        "site":         site,
        "score":        score,
        "score_reason": score_reason,
        "found_at":     found_at,
    }

    # ── Write to SQLite ──────────────────────────────────────────────────
    conn = _get_conn()
    conn.execute(
        """INSERT OR IGNORE INTO jobs
           (id,title,company,location,salary,posted,url,snippet,site,score,score_reason,found_at)
           VALUES (:id,:title,:company,:location,:salary,:posted,:url,:snippet,:site,:score,:score_reason,:found_at)""",
        row,
    )
    conn.commit()
    conn.close()

    # ── Append to CSV ────────────────────────────────────────────────────
    csv_exists = CSV_PATH.exists()
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=_CSV_HEADERS)
        if not csv_exists:
            writer.writeheader()
        writer.writerow({k: row.get(k, "") for k in _CSV_HEADERS})

    return True


def get_stats() -> dict:
    """Return summary stats for logging."""
    conn = _get_conn()
    total = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
    today = conn.execute(
        "SELECT COUNT(*) FROM jobs WHERE found_at >= date('now')"
    ).fetchone()[0]
    top = conn.execute(
        "SELECT title, company, score FROM jobs ORDER BY score DESC LIMIT 3"
    ).fetchall()
    conn.close()
    return {"total": total, "today": today, "top_3": top}

```

### jobhunter/vlm_query.py

```python
# jobhunter/vlm_query.py
# ─────────────────────────────────────────────────────────────────────────────
# Sends browser screenshots to your VLM server and gets back structured actions.
# Mirrors vision/inference/query.py — same HTTP call to your llama-server.
# ─────────────────────────────────────────────────────────────────────────────

import json
import re
import requests

from jobhunter.snap import snap_browser_b64
from jobhunter.config import VLM_SERVER_PORT, VLM_MAX_TOKENS, VLM_TEMPERATURE


# ── System prompt for navigation decisions ─────────────────────────────────
_NAV_SYSTEM = """You are a browser automation agent controlling a web browser to find job listings.
You see a screenshot of the current browser page.
Your job is to take ONE action to make progress toward the goal.

You MUST respond with ONLY a JSON object — no explanation, no markdown, no extra text.

JSON format:
{
  "action": "click" | "type" | "scroll" | "wait" | "extract" | "done" | "navigate",
  "x": <pixel x, only for click>,
  "y": <pixel y, only for click>,
  "text": "<text to type, only for type action>",
  "url": "<url, only for navigate action>",
  "direction": "down" | "up",
  "reason": "<one short sentence why>"
}

Rules:
- click: click at pixel coordinates (x, y)
- type: type text (assumes an input is already focused)
- scroll: scroll the page
- wait: wait for page to load (use after clicks that trigger navigation)
- extract: the page now shows job listings you can read — extract them now
- navigate: go directly to a URL
- done: no more jobs to find on this page
"""

# ── System prompt for job data extraction ──────────────────────────────────
_EXTRACT_SYSTEM = """You are a job listing extractor. You see a screenshot of a job search results page.
Extract ALL visible job listings into a JSON array.

Respond with ONLY a JSON array — no markdown, no explanation.

Each item format:
{
  "title": "<job title>",
  "company": "<company name>",
  "location": "<location or Remote>",
  "salary": "<salary if shown, else null>",
  "posted": "<time posted if shown, else null>",
  "url": "<job URL if visible in browser address or links, else null>",
  "snippet": "<brief description if visible, else null>"
}

If you cannot see any job listings, return an empty array: []
"""

# ── System prompt for VLM job scoring ──────────────────────────────────────
_SCORE_SYSTEM = """You are a job relevance scorer for a junior software developer.
Given a job listing and a candidate profile, score the job from 1-10.

Respond with ONLY a JSON object:
{
  "score": <1-10>,
  "reason": "<one sentence why>",
  "good_match": true | false
}

Score guide:
10 = perfect match (title, skills, level all match)
7-9 = strong match (most criteria match)
5-6 = partial match (some skills missing but worth applying)
1-4 = poor match (wrong level, wrong skills, or flagged keywords)
"""


def _call_vlm(screenshot_b64: str, system_prompt: str, user_prompt: str) -> str:
    """
    Single HTTP call to your llama-server.
    Mirrors _query_server() in vision/inference/query.py — same endpoint.
    """
    try:
        response = requests.post(
            f"http://localhost:{VLM_SERVER_PORT}/v1/chat/completions",
            json={
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{screenshot_b64}"
                                },
                            },
                            {"type": "text", "text": user_prompt},
                        ],
                    },
                ],
                "max_tokens": VLM_MAX_TOKENS,
                "temperature": VLM_TEMPERATURE,
                "stream": False,
            },
            timeout=30,
        )
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[VLM] Call failed: {e}")
        return "{}"


def _parse_json(raw: str) -> dict | list:
    """Robustly extract JSON from VLM response — handles stray markdown."""
    raw = raw.strip()
    # Strip markdown code fences if present
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    try:
        return json.loads(raw)
    except Exception:
        # Try to find JSON object/array inside the text
        match = re.search(r"(\{.*\}|\[.*\])", raw, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except Exception:
                pass
    return {}


def decide_action(goal: str) -> dict:
    """
    Take a screenshot of the current page and ask the VLM what to do next.
    Returns a parsed action dict.
    """
    screenshot = snap_browser_b64()
    prompt = f"Goal: {goal}\n\nWhat is the single next action to take? Respond in JSON only."
    raw = _call_vlm(screenshot, _NAV_SYSTEM, prompt)
    action = _parse_json(raw)
    print(f"[VLM→Action] {action.get('action','?')} — {action.get('reason','')}")
    return action if isinstance(action, dict) else {}


def extract_jobs_from_page() -> list[dict]:
    """
    Take a screenshot and ask the VLM to extract all visible job listings.
    Returns a list of job dicts.
    """
    screenshot = snap_browser_b64()
    prompt = "Extract all visible job listings from this screenshot as a JSON array."
    raw = _call_vlm(screenshot, _EXTRACT_SYSTEM, prompt)
    result = _parse_json(raw)
    jobs = result if isinstance(result, list) else []
    print(f"[VLM→Extract] Found {len(jobs)} jobs on this page")
    return jobs


def score_job(job: dict, profile: dict) -> dict:
    """
    Ask VLM to score a single job against the candidate profile.
    Returns {score, reason, good_match}.
    """
    screenshot = snap_browser_b64()
    prompt = (
        f"Job listing:\n{json.dumps(job, indent=2)}\n\n"
        f"Candidate profile:\n"
        f"- Titles looking for: {', '.join(profile.get('job_titles', []))}\n"
        f"- Skills: {', '.join(profile.get('skills', []))}\n"
        f"- Experience: {profile.get('years_experience', 1)} year(s)\n"
        f"- Prefers: {profile.get('remote_preference', 'any')}\n"
        f"- Avoid keywords: {', '.join(profile.get('avoid_keywords', []))}\n\n"
        f"Score this job 1–10. Respond in JSON only."
    )
    raw = _call_vlm(screenshot, _SCORE_SYSTEM, prompt)
    result = _parse_json(raw)
    return result if isinstance(result, dict) else {"score": 5, "reason": "unknown", "good_match": True}

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

### main_jobhunter.py

```python
#!/usr/bin/env python3
# main_jobhunter.py
# ─────────────────────────────────────────────────────────────────────────────
# Entry point for the job hunter.
# Mirrors main.py style — same project, new MODE.
#
# Usage:
#   python main_jobhunter.py             ← runs full scheduled hunt (all day)
#   python main_jobhunter.py --once      ← runs one cycle then exits
#   python main_jobhunter.py --site linkedin  ← hunt one site only
#   python main_jobhunter.py --stats     ← show DB stats and exit
# ─────────────────────────────────────────────────────────────────────────────

import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description="AI Job Hunter")
    parser.add_argument("--once",  action="store_true", help="Run one hunt cycle then exit")
    parser.add_argument("--site",  type=str, default=None, help="Hunt one specific site only")
    parser.add_argument("--stats", action="store_true", help="Show DB stats and exit")
    args = parser.parse_args()

    # ── Stats mode ─────────────────────────────────────────────────────────
    if args.stats:
        from jobhunter.storage import get_stats
        from jobhunter.config import CSV_PATH, DB_PATH
        stats = get_stats()
        print(f"\n{'='*40}")
        print(f"  Job Hunter Stats")
        print(f"{'='*40}")
        print(f"  Total jobs in DB : {stats['total']}")
        print(f"  Found today      : {stats['today']}")
        print(f"  CSV file         : {CSV_PATH}")
        print(f"  DB file          : {DB_PATH}")
        if stats["top_3"]:
            print(f"\n  Top matches:")
            for title, company, score in stats["top_3"]:
                print(f"    ★{score}  {title} @ {company}")
        print(f"{'='*40}\n")
        return

    # ── Ensure VLM server is running ────────────────────────────────────────
    _check_vlm_server()

    # ── Load profile ────────────────────────────────────────────────────────
    from jobhunter.profile import PROFILE, SEARCH_QUERIES
    from jobhunter.logger import log

    log(f"Profile loaded: {PROFILE['name']}")
    log(f"Looking for: {', '.join(PROFILE['job_titles'][:2])}...")

    # ── Single site mode ────────────────────────────────────────────────────
    if args.site:
        site = args.site.lower()
        queries = SEARCH_QUERIES.get(site)
        if not queries:
            print(f"Unknown site '{site}'. Available: {list(SEARCH_QUERIES.keys())}")
            sys.exit(1)
        from jobhunter.agent import hunt_site
        from jobhunter.browser import release_browser
        try:
            total = 0
            for q in queries:
                total += hunt_site(site, q, PROFILE)
            log(f"Done. {total} new jobs saved from {site}.")
        finally:
            release_browser()
        return

    # ── One-shot mode ───────────────────────────────────────────────────────
    if args.once:
        from jobhunter.agent import run_full_hunt
        from jobhunter.browser import release_browser
        try:
            result = run_full_hunt(PROFILE, SEARCH_QUERIES)
            print(f"\nDone. {result['new_this_run']} new jobs saved.")
            print(f"Check: {__import__('jobhunter.config', fromlist=['CSV_PATH']).CSV_PATH}")
        finally:
            release_browser()
        return

    # ── Scheduled all-day mode (default) ────────────────────────────────────
    from jobhunter.scheduler import start_scheduler
    from jobhunter.browser import release_browser
    try:
        start_scheduler()
    except KeyboardInterrupt:
        print("\n\nStopped by user.")
    finally:
        release_browser()


def _check_vlm_server():
    """Verify your llama-server (VLM) is running before we start."""
    import requests
    from jobhunter.config import VLM_SERVER_PORT

    url = f"http://localhost:{VLM_SERVER_PORT}/health"
    try:
        r = requests.get(url, timeout=3)
        if r.status_code == 200:
            print(f"[VLM] Server running on port {VLM_SERVER_PORT} ✓")
            return
    except Exception:
        pass

    print(f"\n[ERROR] VLM server not running on port {VLM_SERVER_PORT}.")
    print("Start it first with:")
    print(f"  llama-server -m <your-model.gguf> --mmproj <mmproj.gguf> -ngl 99 -c 2048 --port {VLM_SERVER_PORT}")
    print("\nOr run your existing app first with MODE='vision_text' which starts the server.")
    sys.exit(1)


if __name__ == "__main__":
    main()

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
    elif MODE == "vision_text":
        _run_vision_text()
    elif MODE == "vision_speech":
        _run_vision_speech()
    else:
        print(f"  Unknown MODE '{MODE}'. Check config/features.py")


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
    get_tts_model()
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
        log_request(
            logger,
            user_text,
            ai_response,
            0.0,
            first_token_time or llm_total,
            llm_total,
            llm_total,
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
                text = end_of_speech(transcriber)
                whisper_latency = time.time() - e2e_start
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
                log_request(
                    logger,
                    text,
                    ai_response,
                    whisper_latency,
                    first_token_time or llm_total,
                    llm_total,
                    time.time() - e2e_start,
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
    from tts.engine.control import interrupt, resume, speak_filler, record_llm_latency
    from tts.engine.status import is_speaking, shutdown
    from config.vad import RECORD_SAMPLE_RATE
    from ui.console import show_partial, show_speaking, show_you, start_ai_line
    import threading

    print("  Loading all models...")
    load_whisper()
    get_model()
    print("  All ready.\n")

    logger = create_logger()
    history = create_history()
    lock = threading.Lock()
    vad_state = create_vad_state(sample_rate=RECORD_SAMPLE_RATE)

    def on_partial(t):
        show_partial(t)

    # ✅ Mic FIRST — before TTS engine opens audio output
    transcriber = create_stream(on_partial=on_partial, on_final=lambda t: None)
    start_stream(transcriber)

    # ✅ TTS engine AFTER mic is open
    engine = create_engine(
        voice=SUPERTONIC_VOICE,
        speed=SUPERTONIC_SPEED,
        steps=SUPERTONIC_STEPS,
        language=SUPERTONIC_LANGUAGE,
    )
    start_worker(engine)
    from tts.model.singleton import get_model as get_tts_model
    get_tts_model()

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
                if first_token_time is not None:
                    record_llm_latency(engine, first_token_time * 1000)
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



def _run_vision_text():
    from vision.model.singleton import get_model, shutdown
    from vision.inference.query import query_stream
    from vision.camera import release_camera
    from config.vlm import VLM_BACKEND
    from ui.console import prompt_you

    print(f"  Loading VLM (backend={VLM_BACKEND})...")
    get_model()
    print("  Ready. Type a question, 'w' to watch, 'q' to quit.\n")

    try:
        while True:
            prompt_you()
            user_input = input().strip()

            if user_input.lower() == "q":
                break

            elif user_input.lower() == "w":
                print("👁️  Watching... (Ctrl+C to stop)\n")
                try:
                    while True:
                        print("  \033[92mAI :\033[0m ", end="", flush=True)
                        for token in query_stream(
                            "In one sentence, describe what the person is doing right now."
                        ):
                            print(token, end="", flush=True)
                        print()
                        time.sleep(2)
                except KeyboardInterrupt:
                    print("\n⏹️  Stopped watching\n")

            elif user_input:
                print("  \033[92mAI :\033[0m ", end="", flush=True)
                for token in query_stream(user_input):
                    print(token, end="", flush=True)
                print()
    finally:
        release_camera()
        shutdown()



def _run_vision_speech():
    import threading
    from config.tts import (
        SUPERTONIC_VOICE,
        SUPERTONIC_SPEED,
        SUPERTONIC_STEPS,
        SUPERTONIC_LANGUAGE,
    )
    from config.vad import RECORD_SAMPLE_RATE
    from config.vlm import VLM_BACKEND
    from vision.model.singleton import get_model as get_vlm, shutdown as vlm_shutdown
    from vision.inference.query import query_stream
    from vision.camera import release_camera
    from transcription.model.singleton import get_model as load_whisper
    from transcription.stream import create_stream, start_stream, end_of_speech
    from transcription.vad.state import create_vad_state, reset_vad_state
    from transcription.vad.session import run_mic_session
    from tts.engine.state import create_engine
    from tts.engine.worker import start_worker
    from tts.engine.feed import feed_token, flush as tts_flush
    from tts.engine.control import interrupt, resume, speak_filler, record_llm_latency
    from tts.engine.status import is_speaking, shutdown as tts_shutdown
    from tts.model.singleton import get_model as get_tts_model
    from ui.console import show_partial, show_speaking, show_you, start_ai_line

    print(f"  Loading Whisper + VLM (backend={VLM_BACKEND}) + TTS...")
    load_whisper()
    get_vlm()
    print("  All ready.\n")

    logger = create_logger()
    lock = threading.Lock()
    vad_state = create_vad_state(sample_rate=RECORD_SAMPLE_RATE)

    def on_partial(t):
        show_partial(t)

    # ✅ Mic FIRST — before TTS engine opens audio output
    transcriber = create_stream(on_partial=on_partial, on_final=lambda t: None)
    start_stream(transcriber)

    # ✅ TTS engine AFTER mic is open
    engine = create_engine(
        voice=SUPERTONIC_VOICE,
        speed=SUPERTONIC_SPEED,
        steps=SUPERTONIC_STEPS,
        language=SUPERTONIC_LANGUAGE,
    )
    start_worker(engine)
    get_tts_model()

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
                    return
                show_you(text)
                resume(engine)
                speak_filler(engine)
                start_ai_line()
                llm_start = time.time()
                ai_response = ""
                first_token_time = None
                for token in query_stream(text):  # VLM with camera frame
                    if first_token_time is None:
                        first_token_time = time.time() - llm_start
                    print(token, end="", flush=True)
                    ai_response += token
                    feed_token(engine, token)
                tts_flush(engine)
                print()
                llm_total = time.time() - llm_start
                llm_first_token = first_token_time if first_token_time else llm_total
                if first_token_time is not None:
                    record_llm_latency(engine, first_token_time * 1000)
                log_request(
                    logger,
                    text,
                    ai_response,
                    whisper_latency,
                    llm_first_token,
                    llm_total,
                    time.time() - e2e_start,
                )
            finally:
                lock.release()

        threading.Thread(target=_run, daemon=True).start()

    try:
        run_mic_session(
            transcriber=transcriber,
            vad_state=vad_state,
            on_speech_start=on_speech_start,
            on_speech_end=on_speech_end,
            should_process_chunk=lambda: not is_speaking(engine),
        )
    finally:
        release_camera()
        vlm_shutdown()
        tts_shutdown(engine)


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
colorama
jiwer
silero-vad
noisereduce
pynput
mlx-audio
opencv-python
playwright 
schedule 
# playwright install chromium
browser-cookie3

```

### sentence_04.wav

(Skipped: binary or unreadable file)


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
    printInConsole: bool = False,
) -> None:
    with logger["lock"]:
        logger["req_num"] += 1
        n = logger["req_num"]
        ts = datetime.now().strftime("%H:%M:%S")
        st = time.time() - logger["session_start"]
        sep = "─" * 54
        if printInConsole == True:
            print(f"\n[{ts}] #{n:02d}  YOU: {user_text}")
            print(f"  AI: {ai_response}")
            print(
                f"  Timings (s) → whisper: {whisper_latency:.3f} | "
                f"LLM first token: {llm_first_token:.3f} | LLM total: {llm_total:.3f} | "
                f"End-to-end: {end_to_end:.3f} | Session time: {st:.0f}s"
            )
            print(sep)
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
        # added this might cause issues ----
        from tts.model.singleton import get_model as get_tts_model

        get_tts_model()
        # ----------------------------------
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

### test_audio_000.wav

(Skipped: binary or unreadable file)


### transcription/__init__.py

```python
# transcription/__init__.py
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
# transcription/download/whisper.py
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
# transcription/hallucination/__init__.py
from transcription.hallucination.repetition import has_repetition
from transcription.hallucination.noise import is_noise_phrase, clean_text
from transcription.hallucination.confidence import passes_confidence

```

### transcription/hallucination/confidence.py

```python
# transcription/hallucination/confidence.py
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
#
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
#
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
# transcription/model/__init__.py
from transcription.model.singleton import get_model, is_loaded, reset
from transcription.model.device import resolve_device
from transcription.model.lock import infer_lock

```

### transcription/model/device.py

```python
# transcription/model/device.py
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
# transcription/model/load.py
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

    # warm up Metal kernels — kills the 5s cold-start on first real call
    print("[Whisper] Warming up...")
    import whisper as _w
    import numpy as np

    # 480000 = 30s at 16kHz — Whisper's full window
    # pre-compiles the Metal kernel for the largest possible input
    _w.transcribe(
        model,
        np.zeros(480000, dtype=np.float32),
        language="en",
        fp16=(device == "cuda"),
    )
    print(f"[Whisper] Ready on {device}.")
    return model


if __name__ == "__main__":
    m = load_whisper()
    print(type(m))

```

### transcription/model/lock.py

```python
# transcription/model/lock.py
import threading

# Single lock shared by all Whisper callers — GPU is not re-entrant
infer_lock = threading.Lock()

```

### transcription/model/singleton.py

```python
# transcription/model/singleton.py
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
# transcription/stream/__init__.py
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
        "is_transcribing": False,
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
# transcription/stream/buffer.py

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
# transcription/stream/final.py
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
# transcription/stream/partial.py
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
        # Don't skip — just run in a thread so the loop stays on schedule
        if state["is_transcribing"]:
            continue
        threading.Thread(target=_run_partial, args=(state,), daemon=True).start()


def _run_partial(state: dict) -> None:
    if state["is_transcribing"]:
        return
    state["is_transcribing"] = True
    try:
        from transcription.stream.partial import run_partial_pass

        text = run_partial_pass(state["buf"])
        if text and text != state["last_text"]:
            state["last_text"] = text
            state["on_partial"](text)
    finally:
        state["is_transcribing"] = False

```

### transcription/transcribe/__init__.py

```python
# transcription/transcribe/__init__.py
from transcription.transcribe.batch import transcribe_audio
from transcription.transcribe.options import build_whisper_options

```

### transcription/transcribe/batch.py

```python
# transcription/transcribe/batch.py
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
# transcription/options.py
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
# transcription/vad/__init__.py
from transcription.vad.state import create_vad_state, reset_vad_state
from transcription.vad.processor import process_chunk
from transcription.vad.energy import is_speech_energy
from transcription.vad.silero import is_speech

```

### transcription/vad/energy.py

```python
# transcription/vad/energy.py
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
# transcription/vad/processor.py
import numpy as np
from config.vad import PAUSE_SECONDS, MIN_SPEECH_SEC
from transcription.vad.state import reset_vad_state
from transcription.vad.silero import is_speech as _is_speech


def process_chunk(
    chunk: np.ndarray,
    state: dict,
    on_speech_start=None,
    on_speech_end=None,
) -> None:
    pause_samples = int(PAUSE_SECONDS * state["sample_rate"])
    min_samples = int(MIN_SPEECH_SEC * state["sample_rate"])
    is_speech = _is_speech(chunk, state["sample_rate"])

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

### transcription/vad/ptt.py

```python
import threading
import sys
import tty
import termios
from pynput import keyboard

_pressed = False
_listener = None
_on_press_cb = None
_on_release_cb = None


def _on_press(key):
    global _pressed
    if key == keyboard.Key.space and not _pressed:
        _pressed = True
        if _on_press_cb:
            _on_press_cb()


def _on_release(key):
    global _pressed
    if key == keyboard.Key.space and _pressed:
        _pressed = False
        if _on_release_cb:
            _on_release_cb()


def start_ptt(on_press, on_release):
    global _listener, _on_press_cb, _on_release_cb
    _on_press_cb = on_press
    _on_release_cb = on_release

    # Suppress terminal echo so SPACE doesn't move the cursor
    if sys.stdin.isatty():
        fd = sys.stdin.fileno()
        attrs = termios.tcgetattr(fd)
        attrs[3] &= ~termios.ECHO   # turn off echo
        termios.tcsetattr(fd, termios.TCSANOW, attrs)

    _listener = keyboard.Listener(on_press=_on_press, on_release=_on_release)
    _listener.start()
    print("  🎙️  Push-to-talk enabled — hold SPACE to speak")


def stop_ptt():
    global _listener
    if _listener:
        _listener.stop()
        _listener = None

    # Restore terminal echo
    if sys.stdin.isatty():
        fd = sys.stdin.fileno()
        attrs = termios.tcgetattr(fd)
        attrs[3] |= termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, attrs)


def is_pressed() -> bool:
    return _pressed

```

### transcription/vad/session.py

```python
# transcription/vad/session.py
import numpy as np

from audio.io.mic import open_mic
from audio.transform.resample import resample
from config.vad import RECORD_SAMPLE_RATE, PREROLL_SECONDS, PUSH_TO_TALK
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
    if PUSH_TO_TALK:
        _run_ptt_session(transcriber, vad_state, on_speech_start, on_speech_end, should_process_chunk)
    else:
        _run_vad_session(transcriber, vad_state, on_speech_start, on_speech_end, should_process_chunk)


def _run_vad_session(
    transcriber, vad_state, on_speech_start, on_speech_end, should_process_chunk
) -> None:
    """Original auto-VAD session — unchanged."""
    resample(np.zeros(882, dtype=np.float32), RECORD_SAMPLE_RATE, WHISPER_SAMPLE_RATE)

    preroll_target = int(PREROLL_SECONDS * RECORD_SAMPLE_RATE)
    preroll_chunks = []
    preroll_len = 0

    def on_chunk(chunk):
        nonlocal preroll_len
        if should_process_chunk is not None and not should_process_chunk():
            return
        was_in_speech = vad_state["in_speech"]
        process_chunk(chunk, vad_state, on_speech_start=on_speech_start, on_speech_end=on_speech_end)
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


def _run_ptt_session(
    transcriber, vad_state, on_speech_start, on_speech_end, should_process_chunk
) -> None:
    """Push-to-talk session — hold SPACE to record."""
    from transcription.vad.ptt import start_ptt, stop_ptt
    from transcription.vad.state import reset_vad_state
    from transcription.stream import clear_stream

    resample(np.zeros(882, dtype=np.float32), RECORD_SAMPLE_RATE, WHISPER_SAMPLE_RATE)

    _recording = [False]  # mutable flag accessible in closure

    def on_press():
        if should_process_chunk is not None and not should_process_chunk():
            return
        _recording[0] = True
        clear_stream(transcriber)
        reset_vad_state(vad_state)
        on_speech_start()

    def on_release():
        _recording[0] = False
        on_speech_end()

    def on_chunk(chunk):
        if not _recording[0]:
            return
        chunk_16k = resample(chunk, RECORD_SAMPLE_RATE, WHISPER_SAMPLE_RATE)
        feed(transcriber, chunk_16k)

    start_ptt(on_press, on_release)
    mic = open_mic(on_chunk)
    mic.start()
    print("  🔴 Listening... Press ENTER to stop.")
    input()
    mic.stop()
    mic.close()
    stop_ptt()

```

### transcription/vad/silero.py

```python
import threading
import numpy as np
import torch
from audio.transform.resample import resample
from config.vad import SILERO_THRESHOLD

_model = None
_load_lock = threading.Lock()  # only for initial load
_infer_lock = threading.Lock()  # only for inference
_sample_rate = 16000
_MIN_SAMPLES = 512
_accumulator = np.array([], dtype=np.float32)


def _get_model():
    global _model
    if _model is not None:
        return _model
    with _load_lock:
        if _model is not None:
            return _model
        from silero_vad import load_silero_vad

        _model = load_silero_vad()
        _model.reset_states()
    return _model


def is_speech(chunk: np.ndarray, source_sr: int) -> bool:
    global _accumulator
    if len(chunk) == 0:
        return False
    audio = (
        resample(chunk, source_sr, _sample_rate)
        if source_sr != _sample_rate
        else chunk.astype(np.float32)
    )
    _accumulator = np.concatenate([_accumulator, audio])
    if len(_accumulator) < _MIN_SAMPLES:
        return False
    tensor = torch.from_numpy(_accumulator[:_MIN_SAMPLES]).float()
    _accumulator = _accumulator[_MIN_SAMPLES:]
    model = _get_model()
    with _infer_lock:
        prob = model(tensor, _sample_rate).item()
    return prob >= SILERO_THRESHOLD

```

### transcription/vad/state.py

```python
# transcription/vad/state.py
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

_REQUIRED_FILES = [
    "onnx/text_encoder.onnx",
    "onnx/text_encoder.onnx_data",
    "onnx/latent_denoiser.onnx",
    "onnx/latent_denoiser.onnx_data",
    "onnx/voice_decoder.onnx",
    "onnx/voice_decoder.onnx_data",
    "tokenizer.json",
]


def ensure_downloaded() -> str:
    missing = [f for f in _REQUIRED_FILES if not (SUPERTONIC_DIR / f).exists()]
    
    if not missing:
        return str(SUPERTONIC_DIR)
    
    print(f"[Supertonic] Missing files: {missing}")
    print(f"[Supertonic] Downloading {MODEL_ID} → {SUPERTONIC_DIR}")
    print("[Supertonic] (one-time ~200 MB download)")
    
    from huggingface_hub import snapshot_download
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        snapshot_download(repo_id=MODEL_ID, local_dir=str(SUPERTONIC_DIR))
    
    # verify all files are now present
    still_missing = [f for f in _REQUIRED_FILES if not (SUPERTONIC_DIR / f).exists()]
    if still_missing:
        raise RuntimeError(f"[Supertonic] Download incomplete, still missing: {still_missing}")
    
    print("[Supertonic] Download complete.")
    return str(SUPERTONIC_DIR)


if __name__ == "__main__":
    print(ensure_downloaded())

```

### tts/engine/__init__.py

```python
# tts/engine/__init__.py
from tts.engine.state import create_engine
from tts.engine.worker import start_worker
from tts.engine.feed import feed_token, flush
from tts.engine.control import interrupt, resume, speak_filler
from tts.engine.status import is_speaking, wait_until_done, shutdown

```

### tts/engine/control.py

```python
# tts/engine/control.py
import threading


def interrupt(engine: dict) -> None:
    engine["interrupted"].set()
    _drain(engine)
    from tts.playback.stop import stop_audio

    stop_audio()


def resume(engine: dict) -> None:
    engine["token_buf"] = ""
    engine["interrupted"].clear()


def speak_filler(engine: dict) -> None:
    """
    Play a cached filler non-blocking.

    Selection strategy: pick the shortest filler whose measured duration is
    >= the rolling LLM first-token estimate. This means:
      - Filler ends at roughly the same time the first LLM token arrives
      - No silent gap, no unnecessary extra wait
      - Falls back to longest available if all fillers are shorter than estimate

    Uses engine["last_llm_first_token_ms"] (EMA updated by record_llm_latency).
    """
    from config.tts import ENABLE_FILLER

    if not ENABLE_FILLER:
        return

    cached = engine["filler_audio"]
    durations = engine["filler_durations_ms"]

    if not cached:
        return  # warmup not done yet — skip

    target_ms = engine.get("last_llm_first_token_ms", 1800.0)

    # Find all fillers that cover the target (duration >= target)
    covering = {t: d for t, d in durations.items() if t in cached and d >= target_ms}

    if covering:
        # Pick the shortest one that still covers — minimises unnecessary wait
        text = min(covering, key=covering.get)
    else:
        # All fillers are shorter than LLM latency — pick the longest available
        text = max((t for t in cached), key=lambda t: durations.get(t, 0))

    audio = cached[text]
    engine["speaking"].set()

    def _play():
        try:
            from tts.playback.stream import play_audio
            from tts.model.singleton import get_model

            play_audio(audio, get_model()["sample_rate"])
        finally:
            engine["speaking"].clear()

    # Non-blocking — caller returns immediately, LLM starts streaming in parallel
    threading.Thread(target=_play, daemon=True).start()


def record_llm_latency(engine: dict, first_token_ms: float) -> None:
    """
    Update the rolling EMA of LLM first-token latency after each response.
    alpha=0.25: slow enough to smooth spikes, fast enough to track trends.
    speak_filler() uses this to pick the right filler duration next time.
    """
    prev = engine.get("last_llm_first_token_ms", first_token_ms)
    engine["last_llm_first_token_ms"] = 0.75 * prev + 0.25 * first_token_ms


def _drain(engine: dict) -> None:
    while not engine["queue"].empty():
        try:
            engine["queue"].get_nowait()
        except Exception:
            break

```

### tts/engine/feed.py

```python
# tts/engine/feed.py
from tts.text.split import split_sentence, MIN_CHUNK_CHARS
from tts.engine.queue import enqueue
from config.tts import WORD_FLUSH_THRESHOLD, MIN_SEND_CHARS as _MIN_SEND_CHARS


def feed_token(engine: dict, token: str) -> None:
    if engine["interrupted"].is_set():
        return
    engine["token_buf"] += token

    # Sentence/clause boundary split
    while True:
        sentence, remainder = split_sentence(engine["token_buf"])
        if sentence and len(sentence) >= _MIN_SEND_CHARS:
            engine["token_buf"] = remainder
            enqueue(engine, sentence, priority=1)
        else:
            break

    # Word-count flush
    if len(engine["token_buf"].split()) >= WORD_FLUSH_THRESHOLD:
        text = engine["token_buf"].strip()
        engine["token_buf"] = ""
        if text:
            enqueue(engine, text, priority=1)


def flush(engine: dict) -> None:
    """
    Called after LLM finishes streaming.

    The [6, 1] trailing chunk problem:
      LLM outputs "Check latest air news sites for updates."
      Word-flush fires at "Check latest air news sites for" (6 words) → chunk 1
      Remainder: "updates." → 1 word, has terminal punct → was sent as chunk 2

    Fix: append the short tail onto the PREVIOUS chunk that's already queued,
    rather than sending it standalone. We do this by peeking at what's in the
    queue and merging if the last item is recent and short tail qualifies.

    If queue is empty (whole response fit in one flush), just send normally.

    Minimum standalone flush = 4 words OR the buffer is the entire response
    (i.e. nothing was enqueued yet during feed_token — short responses).
    """
    text = engine["token_buf"].strip()
    engine["token_buf"] = ""

    if not text:
        return

    words = text.split()

    # Short tail (< 4 words) — try to merge with last queued chunk instead
    if len(words) < 4:
        merged = _try_merge_with_last(engine, text)
        if merged:
            return  # successfully appended to previous chunk

    # Either long enough to stand alone, or nothing in queue to merge with
    enqueue(engine, text, priority=1)


def _try_merge_with_last(engine: dict, tail: str) -> bool:
    """
    Pop the last item from the priority queue, append tail, re-enqueue.
    Returns True if merge succeeded, False if queue was empty or wrong type.

    PriorityQueue doesn't support peek/pop-last, so we drain into a list,
    modify the last item, and re-fill. This is safe because flush() is called
    after the LLM loop ends — no concurrent feed_token() calls at this point.
    """
    q = engine["queue"]
    items = []
    while not q.empty():
        try:
            items.append(q.get_nowait())
        except Exception:
            break

    if not items:
        return False

    # Find the last normal-priority item (priority=1)
    last_idx = None
    for i in range(len(items) - 1, -1, -1):
        if items[i][0] == 1:  # normal priority
            last_idx = i
            break

    if last_idx is None:
        # Only filler items in queue — put everything back, send tail standalone
        for item in items:
            q.put(item)
        return False

    # Merge tail onto the last chunk
    priority, seq, prev_text = items[last_idx]
    merged_text = (prev_text.rstrip(".!?,;:") + " " + tail).strip()
    items[last_idx] = (priority, seq, merged_text)

    for item in items:
        q.put(item)

    return True

```

### tts/engine/queue.py

```python
# tts/engine/queue.py
def enqueue(engine: dict, text: str, priority: int = 1) -> None:
    """priority=0 → filler (plays first), priority=1 → normal."""
    seq = next(engine["seq"])
    engine["queue"].put((priority, seq, text))

```

### tts/engine/state.py

```python
# tts/engine/state.py
import threading
import queue
import itertools

from config.tts import (
    SUPERTONIC_VOICE,
    SUPERTONIC_LANGUAGE,
    SUPERTONIC_STEPS,
    SUPERTONIC_SPEED,
)

# Filler range designed to cover the observed LLM first-token distribution:
#   min observed: 1287ms  max observed: 2189ms  avg: 1728ms
# We need fillers from ~1300ms to ~2200ms so adaptive selection can always
# find one that lands just above the current rolling estimate.
_FILLERS = [
    "Got it.",  # ~700ms  — short fallback
    "Sure.",  # ~650ms  — short fallback
    "Okay.",  # ~680ms  — short fallback
    "Sure thing.",  # ~1050ms
    "Right, on it.",  # ~1200ms
    "Sure, let me check.",  # ~1500ms
    "Okay, one moment.",  # ~1550ms
    "Let me look at that.",  # ~1700ms
    "Sure, one moment please.",  # ~1850ms
    "Okay, let me check that.",  # ~1900ms
    "Sure, give me just a moment.",  # ~2100ms
]

SENTINEL = (float("inf"), float("inf"), None)


def create_engine(
    voice: str = SUPERTONIC_VOICE,
    speed: float = SUPERTONIC_SPEED,
    steps: int = SUPERTONIC_STEPS,
    language: str = SUPERTONIC_LANGUAGE,
) -> dict:
    return {
        "voice": voice,
        "speed": speed,
        "steps": steps,
        "language": language,
        "token_buf": "",
        "queue": queue.PriorityQueue(),
        "seq": itertools.count(),
        "interrupted": threading.Event(),
        "speaking": threading.Event(),
        "running": False,
        "worker_thread": None,
        "fillers": _FILLERS,
        "filler_audio": {},  # text → np.ndarray
        "filler_durations_ms": {},  # text → float ms (measured at warmup)
        # Rolling EMA of LLM first-token latency — used by speak_filler()
        # to pick a filler that covers the gap. Seeded at 1800ms (slightly
        # above the 1728ms avg) so first response is covered conservatively.
        "last_llm_first_token_ms": 1800.0,
    }


def warm_fillers(engine: dict) -> None:
    """Pre-generate all filler audio and record exact durations."""
    from tts.generate.pipeline import generate_one
    from tts.model.singleton import get_model

    sr = get_model()["sample_rate"]
    print("[TTS] Pre-generating fillers...")
    for text in _FILLERS:
        try:
            audio = generate_one(
                text,
                voice=engine["voice"],
                speed=engine["speed"],
                steps=engine["steps"],
                language=engine["language"],
            )
            engine["filler_audio"][text] = audio
            engine["filler_durations_ms"][text] = len(audio) / sr * 1000
        except Exception as e:
            print(f"[TTS] Filler warmup failed for '{text}': {e}")

    dur = engine["filler_durations_ms"]
    print(
        f"[TTS] {len(engine['filler_audio'])} fillers ready  "
        f"range: {min(dur.values()):.0f}–{max(dur.values()):.0f}ms"
    )

```

### tts/engine/status.py

```python
# tts/engine/status.py
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
# tts/engine/worker.py
"""
Pipelined TTS worker.

Generator thread: text queue → generate_one() → audio_queue
Player thread:    audio_queue → play_audio()

While chunk N is playing, chunk N+1 is already being generated.
Eliminates the inter-chunk silence that caused "stuck between words".
"""
import threading
import time
import queue as _queue
from config.tts import MERGE_WINDOW_SEC


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
    from tts.engine.state import warm_fillers

    model = get_model()
    warm_fillers(engine)
    sr = model["sample_rate"]

    # maxsize=2: current + 1 lookahead. Blocks generator if player falls behind.
    audio_queue: _queue.Queue = _queue.Queue(maxsize=2)

    def _player():
        while True:
            item = audio_queue.get()
            if item is None:
                break
            engine["speaking"].set()
            try:
                play_audio(item, sr)
            except Exception as e:
                print(f"[TTS Player] {e}")
            finally:
                if audio_queue.empty():
                    engine["speaking"].clear()

    player = threading.Thread(target=_player, daemon=True)
    player.start()

    is_first = True

    try:
        while True:
            item = engine["queue"].get()
            priority, _, text = item
            if text is None:
                break

            if engine["interrupted"].is_set():
                while not audio_queue.empty():
                    try:
                        audio_queue.get_nowait()
                    except Exception:
                        pass
                engine["speaking"].clear()
                is_first = True
                continue

            collected = [text]
            if not is_first and priority > 0:
                deadline = time.time() + MERGE_WINDOW_SEC
                while time.time() < deadline:
                    try:
                        nxt = engine["queue"].get_nowait()
                        if nxt[0] == 0:
                            engine["queue"].put(nxt)
                            break
                        collected.append(nxt[2])
                    except Exception:
                        time.sleep(0.003)

            if engine["interrupted"].is_set():
                is_first = True
                continue

            merged = " ".join(clean_markdown(c) for c in collected if c and c.strip())
            if not merged:
                continue

            is_first = False
            try:
                audio = generate_one(
                    merged,
                    voice=engine["voice"],
                    speed=engine["speed"],
                    steps=engine["steps"],
                    language=engine["language"],
                )
                audio_queue.put(audio)  # blocks if player is 2 chunks behind
            except Exception as e:
                print(f"[TTS Generator] {e}")

            if engine["queue"].empty():
                is_first = True

    finally:
        audio_queue.put(None)
        player.join(timeout=5)

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
# tts/text/split.py
import re

_SENTENCE_END = re.compile(r"(?<![A-Z][a-z])(?<!\d)([.?!])(\s+|$)")
_CLAUSE_BREAK = re.compile(r"[,;:]\s+")

# Why 30 not 25:
# "Today's weather:" is 17 chars — was triggering a clause split and creating
# a micro-chunk. At 30 chars, clause breaks only fire on genuinely long phrases,
# keeping short conversational sentences as single chunks.
MIN_CHUNK_CHARS = 30  # was 25


def split_sentence(buf: str) -> tuple[str, str]:
    m = _SENTENCE_END.search(buf)
    if m:
        return buf[: m.end()].strip(), buf[m.end() :]
    m = _CLAUSE_BREAK.search(buf)
    if m and m.start() >= MIN_CHUNK_CHARS:
        return buf[: m.start()].strip(), buf[m.end() :]
    return "", buf

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

### vision/__init__.py

```python
from vision.model.singleton import get_model, is_loaded
from vision.inference.query import query_stream
from vision.camera import release_camera

```

### vision/backup/app.py

```python
import cv2
import base64
import time
from llama_cpp import Llama


from llama_cpp.llama_chat_format import Qwen3VLChatHandler

# CMAKE_ARGS="-DCMAKE_OSX_ARCHITECTURES=arm64 -DGGML_METAL=on" \
# pip install "llama-cpp-python @ git+https://github.com/JamePeng/llama-cpp-python.git" \
#   --force-reinstall --no-cache-dir


chat_handler = Qwen3VLChatHandler(
    clip_model_path="../models/vlm/qwen3vl2b/mmproj-Qwen3VL-2B-Instruct-Q8_0.gguf"
)
llm = Llama(
    model_path="../models/vlm/qwen3vl2b/Qwen3VL-2B-Instruct-Q4_K_M.gguf",
    chat_handler=chat_handler,
    n_ctx=1024,
    n_gpu_layers=-1,
    n_batch=512,
    n_threads=8,
    verbose=False,
)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)


def snap_b64():
    cap.grab()
    _, frame = cap.read()
    frame = cv2.resize(frame, (320, 240))
    _, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
    return base64.b64encode(buf).decode()


def query(prompt):
    img = snap_b64()
    stream = llm.create_chat_completion(
        messages=[
            {
                "role": "system",
                "content": "You are a vision AI with access to a live camera. Answer concisely in 1-2 sentences. No lists, no numbering, no speculation. Speak naturally as if you can see the person in real time.",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{img}"},
                    },
                    {"type": "text", "text": prompt},
                ],
            },
        ],
        max_tokens=60,
        temperature=0.7,
        top_p=0.8,
        top_k=20,
        repeat_penalty=1.0,  # Qwen3 uses presence_penalty instead
        stream=True,
    )
    print("\n🤖 ", end="", flush=True)
    for chunk in stream:
        delta = chunk["choices"][0]["delta"].get("content", "")
        if delta:
            print(delta, end="", flush=True)
    print("\n")


print("👁️  Commands: 'w' = watch mode, 'q' = quit, or just type a question\n")

try:
    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "q":
            break

        elif user_input.lower() == "w":
            # continuous watch mode
            print("👁️  Watching... (press Ctrl+C to stop)\n")
            try:
                while True:
                    query(
                        "In one sentence, describe what the person is doing right now."
                    )
                    time.sleep(2)
            except KeyboardInterrupt:
                print("\n⏹️  Stopped watching\n")

        elif user_input:
            # ask a question
            query(user_input)

finally:
    cap.release()

```

### vision/backup/server.py

```python
import cv2
import base64
import json
import requests
import subprocess
import time

# Start llama-server
server = subprocess.Popen(
    [
        "llama-server",
        "-m",
        "../models/vlm/qwen3vl2b/Qwen3VL-2B-Instruct-Q4_K_M.gguf",
        "--mmproj",
        "../models/vlm/qwen3vl2b/mmproj-Qwen3VL-2B-Instruct-Q8_0.gguf",
        "-ngl",
        "99",
        "-c",
        "2048",
        "--port",
        "8080",
    ],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)

# Wait for server to be ready
print("⏳ Starting Qwen3-VL server...", flush=True)
for _ in range(60):
    try:
        if requests.get("http://localhost:8080/health").status_code == 200:
            break
    except:
        time.sleep(1)
print("✅ Server ready!\n")

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)


def snap_b64():
    cap.grab()
    _, frame = cap.read()
    frame = cv2.resize(frame, (320, 240))
    _, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
    return base64.b64encode(buf).decode()


def query(prompt):
    img = snap_b64()
    response = requests.post(
        "http://localhost:8080/v1/chat/completions",
        json={
            "messages": [
                {
                    "role": "system",
                    "content": "You are a vision AI with access to a live camera. Answer concisely in 1-2 sentences. No lists, no numbering, no speculation.",
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{img}"},
                        },
                        {"type": "text", "text": prompt},
                    ],
                },
            ],
            "max_tokens": 80,
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 20,
            "presence_penalty": 1.5,
            "stream": True,
        },
        stream=True,
    )

    print("\n🤖 ", end="", flush=True)
    for line in response.iter_lines():
        if line and line != b"data: [DONE]":
            try:
                chunk = json.loads(line.decode().replace("data: ", ""))
                delta = chunk["choices"][0]["delta"].get("content", "")
                if delta:
                    print(delta, end="", flush=True)
            except:
                pass
    print("\n")


print("👁️  Commands: 'w' = watch mode, 'q' = quit, or just type a question\n")
try:
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "q":
            break
        elif user_input.lower() == "w":
            print("👁️  Watching... (Ctrl+C to stop)\n")
            try:
                while True:
                    query(
                        "In one sentence, describe what the person is doing right now."
                    )
                    time.sleep(2)
            except KeyboardInterrupt:
                print("\n⏹️  Stopped watching\n")
        elif user_input:
            query(user_input)
finally:
    cap.release()
    server.terminate()
    print("👋 Stopped")

```

### vision/camera.py

```python
import cv2
from config.vlm import VLM_CAMERA_INDEX, VLM_FRAME_WIDTH, VLM_FRAME_HEIGHT

_cap = None


def get_camera():
    global _cap
    if _cap is not None:
        return _cap
    _cap = cv2.VideoCapture(VLM_CAMERA_INDEX)
    _cap.set(cv2.CAP_PROP_FRAME_WIDTH, VLM_FRAME_WIDTH)
    _cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VLM_FRAME_HEIGHT)
    _cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    return _cap


def release_camera():
    global _cap
    if _cap:
        _cap.release()
        _cap = None

```

### vision/download/__init__.py

```python
from vision.download.vlm import ensure_downloaded

```

### vision/download/vlm.py

```python
from vision.model.load import _ensure_downloaded as ensure_downloaded

```

### vision/inference/query.py

```python
from config.vlm import (
    VLM_BACKEND,
    VLM_SYSTEM_PROMPT,
    VLM_MAX_TOKENS,
    VLM_TEMPERATURE,
    VLM_TOP_P,
    VLM_TOP_K,
    VLM_PRESENCE_PENALTY,
    VLM_SERVER_PORT,
)
from vision.inference.snap import snap_b64


def query_stream(prompt: str):
    img = snap_b64()
    messages = [
        {"role": "system", "content": VLM_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{img}"},
                },
                {"type": "text", "text": prompt},
            ],
        },
    ]
    params = dict(
        max_tokens=VLM_MAX_TOKENS,
        temperature=VLM_TEMPERATURE,
        top_p=VLM_TOP_P,
        top_k=VLM_TOP_K,
        presence_penalty=VLM_PRESENCE_PENALTY,
        stream=True,
    )

    if VLM_BACKEND == "package":
        yield from _query_package(messages, params)
    else:
        yield from _query_server(messages, params)


def _query_package(messages, params):
    from vision.model.singleton import get_model

    llm = get_model()
    for chunk in llm.create_chat_completion(messages=messages, **params):
        token = chunk["choices"][0]["delta"].get("content", "")
        if token:
            yield token


def _query_server(messages, params):
    import json
    import requests

    params.pop("top_k", None)  # openai API doesn't support top_k
    response = requests.post(
        f"http://localhost:{VLM_SERVER_PORT}/v1/chat/completions",
        json={"messages": messages, **params},
        stream=True,
        timeout=30,
    )
    for line in response.iter_lines():
        if line and line != b"data: [DONE]":
            try:
                chunk = json.loads(line.decode().replace("data: ", ""))
                token = chunk["choices"][0]["delta"].get("content", "")
                if token:
                    yield token
            except:
                pass

```

### vision/inference/snap.py

```python
import cv2
import base64
from config.vlm import VLM_FRAME_WIDTH, VLM_FRAME_HEIGHT, VLM_JPEG_QUALITY
from vision.camera import get_camera


def snap_b64() -> str:
    cap = get_camera()
    cap.grab()
    _, frame = cap.read()
    frame = cv2.resize(frame, (VLM_FRAME_WIDTH, VLM_FRAME_HEIGHT))
    _, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, VLM_JPEG_QUALITY])
    return base64.b64encode(buf).decode()

```

### vision/model/load.py

```python
import subprocess
import sys
from pathlib import Path
from config.vlm import VLM_BACKEND


def _ensure_downloaded() -> None:
    from config.vlm import VLM_MODEL_PATH, VLM_MMPROJ_PATH
    import warnings

    model_path = Path(VLM_MODEL_PATH)
    mmproj_path = Path(VLM_MMPROJ_PATH)

    if model_path.exists() and mmproj_path.exists():
        return

    print("[VLM] Model files not found — downloading from HuggingFace...")
    model_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        from huggingface_hub import hf_hub_download
    except ImportError:
        raise RuntimeError("huggingface_hub not installed. Run: pip install huggingface_hub")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        if not model_path.exists():
            print(f"[VLM] Downloading {model_path.name} (~1.5 GB)...")
            hf_hub_download(
                repo_id="Qwen/Qwen3-VL-2B-Instruct-GGUF",
                filename="Qwen3VL-2B-Instruct-Q4_K_M.gguf",
                local_dir=str(model_path.parent),
            )
            print(f"[VLM] Downloaded {model_path.name}")

        if not mmproj_path.exists():
            print(f"[VLM] Downloading {mmproj_path.name} (~445 MB)...")
            hf_hub_download(
                repo_id="ggml-org/Qwen3-VL-2B-Instruct-GGUF",
                filename="mmproj-Qwen3-VL-2B-Instruct-Q8_0.gguf",
                local_dir=str(mmproj_path.parent),
            )
            print(f"[VLM] Downloaded {mmproj_path.name}")

    print("[VLM] All model files ready.")


    
def load_vlm():
    if VLM_BACKEND == "package":
        return _load_package()
    elif VLM_BACKEND == "server":
        return _load_server()
    else:
        raise ValueError(f"Unknown VLM_BACKEND: {VLM_BACKEND}")


def _load_package():
    from llama_cpp import Llama
    from llama_cpp.llama_chat_format import Qwen3VLChatHandler
    from config.vlm import VLM_MODEL_PATH, VLM_MMPROJ_PATH

    _ensure_downloaded()
    print("[VLM] Loading Qwen3-VL via package...")
    chat_handler = Qwen3VLChatHandler(clip_model_path=VLM_MMPROJ_PATH)
    llm = Llama(
        model_path=VLM_MODEL_PATH,
        chat_handler=chat_handler,
        n_ctx=2048,
        n_gpu_layers=-1,
        n_batch=512,
        n_threads=8,
        verbose=False,
    )
    print("[VLM] Ready.")
    return llm


def _load_server():
    import time
    import requests
    from config.vlm import (
        VLM_MODEL_PATH, VLM_MMPROJ_PATH,
        VLM_SERVER_PORT, VLM_SERVER_BINARY
    )

    _ensure_downloaded()

    print("[VLM] Starting llama-server subprocess...")
    proc = subprocess.Popen(
        [
            VLM_SERVER_BINARY,
            "-m", VLM_MODEL_PATH,
            "--mmproj", VLM_MMPROJ_PATH,
            "-ngl", "99",
            "-c", "2048",
            "--port", str(VLM_SERVER_PORT),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    url = f"http://localhost:{VLM_SERVER_PORT}/health"
    print("[VLM] Waiting for server to be ready (may take 2-3 min on first run)...")
    i = 0
    while True:
        if proc.poll() is not None:
            raise RuntimeError(f"[VLM] Server process died with code {proc.poll()}")
        try:
            if requests.get(url, timeout=1).status_code == 200:
                print(f"[VLM] Server ready after {i}s")
                return proc
        except:
            pass
        if i % 15 == 0 and i > 0:
            print(f"[VLM] Still loading... ({i}s)")
        time.sleep(1)
        i += 1

```

### vision/model/singleton.py

```python
import threading
from config.vlm import VLM_BACKEND

_model = None
_server_proc = None
_lock = threading.Lock()


def get_model():
    global _model, _server_proc
    if _model is not None:
        return _model
    with _lock:
        if _model is not None:
            return _model
        from vision.model.load import load_vlm

        result = load_vlm()
        if VLM_BACKEND == "server":
            _server_proc = result
            _model = True  # sentinel — actual calls go via HTTP
        else:
            _model = result
    return _model


def get_server_proc():
    return _server_proc


def is_loaded() -> bool:
    return _model is not None


def shutdown():
    global _model, _server_proc
    if _server_proc:
        _server_proc.terminate()
        _server_proc = None
    _model = None

```