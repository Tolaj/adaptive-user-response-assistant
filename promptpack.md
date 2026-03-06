# PromptPack Output

**Root:** `/Users/swapnil/Documents/Projects/adaptive-user-response-assistant`
**Generated:** 2026-03-06T04:27:18.766Z

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
│  ├─ prompt/
│  │  ├─ __init__.py
│  │  ├─ build.py
│  │  └─ system.py
│  └─ tools/
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
├─ tests/
│  ├─ benchmark_stt.py
│  ├─ benchmark_tts.py
│  └─ recordings/
│     ├─ sentence_01.wav
│     ├─ sentence_02.wav
│     ├─ sentence_03.wav
│     ├─ sentence_04.wav
│     ├─ sentence_05.wav
│     ├─ sentence_06.wav
│     ├─ sentence_07.wav
│     ├─ sentence_08.wav
│     ├─ sentence_09.wav
│     └─ sentence_10.wav
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
    "You are a concise voice assistant. "
    "Reply in 1 sentence, 10 words max. "
    "Never use lists or markdown."
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
SUPERTONIC_STEPS = 7  # was 15 → benchmark: 685ms first chunk avg
SUPERTONIC_SPEED = 1.2

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
    engine = create_engine(
        voice=SUPERTONIC_VOICE,
        speed=SUPERTONIC_SPEED,
        steps=SUPERTONIC_STEPS,
        language=SUPERTONIC_LANGUAGE,
    )
    start_worker(engine)
    from tts.model.singleton import get_model as get_tts_model

    get_tts_model()
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
                    return
                show_you(text)
                resume(engine)
                speak_filler(engine)  # non-blocking — returns immediately
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

                # Update rolling LLM latency so speak_filler() picks the right
                # filler duration on the next response
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

### tests/benchmark_stt.py

```python
"""
tests/benchmark_stt.py
======================
Record ONCE, benchmark FOREVER.

First run  → records your voice for each sentence, saves to tests/recordings/
Every run after → loads the saved WAVs and runs them through the live pipeline

This means every time you tweak config/vad.py or the pipeline, you re-run
the same audio and get apples-to-apples latency + accuracy numbers.

Usage:
    python tests/benchmark_stt.py              # auto: record if missing, else replay
    python tests/benchmark_stt.py --record     # force re-record everything
    python tests/benchmark_stt.py --replay     # force replay only (no mic needed)
    python tests/benchmark_stt.py --sentence 3 # only sentence #3
"""

import sys
import time
import argparse
import threading
from pathlib import Path

# ── always run from project root ──────────────────────────────
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

RECORDINGS_DIR = ROOT / "tests" / "recordings"
RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)

import numpy as np
import sounddevice as sd
import soundfile as sf
from colorama import Fore, Style, init as colorama_init

colorama_init()

# ── project imports ────────────────────────────────────────────
from config.vad import (
    RECORD_SAMPLE_RATE,
    PAUSE_SECONDS,
    MIN_SPEECH_SEC,
    PREROLL_SECONDS,
    ENERGY_THRESHOLD,
    SILERO_THRESHOLD,
    TRANSCRIBE_EVERY,
)
from config.whisper import WHISPER_SAMPLE_RATE
from audio.transform.resample import resample
from audio.transform.normalise import normalise
from transcription.model.singleton import get_model
from transcription.stream.final import run_final_pass
from transcription.stream.buffer import (
    create_buffer,
    append as buf_append,
    clear_buffer,
)
from transcription.hallucination.confidence import passes_confidence
from transcription.hallucination.noise import clean_text
from transcription.hallucination.repetition import has_repetition
import whisper as _whisper

# ── sentences ──────────────────────────────────────────────────
SENTENCES = [
    "open the calendar and show me this week",
    "what is the weather like today",
    "set a reminder for tomorrow at nine am",
    "send a message to John saying I will be late",
    "search the web for latest AI news",
    "turn off the lights in the living room",
    "call mom when you get a chance",
    "how long does it take to drive to the airport",
    "play some music on spotify",
    "the quick brown fox jumps over the lazy dog",
]

RECORD_SECONDS = 5  # window given to speak each sentence
COUNTDOWN_SEC = 3


# ── terminal helpers ───────────────────────────────────────────
def c(color, msg):
    return f"{color}{msg}{Style.RESET_ALL}"


def ok(m):
    print(f"  {c(Fore.GREEN,  '✓')}  {m}")


def fail(m):
    print(f"  {c(Fore.RED,    '✗')}  {m}")


def info(m):
    print(f"  {c(Fore.CYAN,   '→')}  {m}")


def warn(m):
    print(f"  {c(Fore.YELLOW, '!')}  {m}")


def head(m):
    print(f"\n  {c(Fore.YELLOW + Style.BRIGHT, m)}")


def rule():
    print(f"  {'─' * 60}")


def countdown(n: int) -> None:
    for i in range(n, 0, -1):
        print(f"\r  {c(Fore.RED, f'Starting in {i}...')}", end="", flush=True)
        time.sleep(1)
    print("\r" + " " * 30 + "\r", end="")


# ── WER ────────────────────────────────────────────────────────
def _norm(text: str) -> str:
    import re

    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    text = text.replace("i'll", "i will").replace("i'm", "i am")
    text = text.replace("9am", "nine am").replace("9 am", "nine am")
    return text


def wer_score(ref: str, hyp: str) -> float:
    if not hyp:
        return 1.0
    try:
        import jiwer

        return jiwer.wer(_norm(ref), _norm(hyp))
    except ImportError:
        r, h = _norm(ref).split(), _norm(hyp).split()
        d = [[0] * (len(h) + 1) for _ in range(len(r) + 1)]
        for i in range(len(r) + 1):
            d[i][0] = i
        for j in range(len(h) + 1):
            d[0][j] = j
        for i in range(1, len(r) + 1):
            for j in range(1, len(h) + 1):
                d[i][j] = min(
                    d[i - 1][j] + 1,
                    d[i][j - 1] + 1,
                    d[i - 1][j - 1] + (0 if r[i - 1] == h[j - 1] else 1),
                )
        return d[len(r)][len(h)] / max(len(r), 1)


# ── recording path for a sentence index ───────────────────────
def wav_path(idx: int) -> Path:
    return RECORDINGS_DIR / f"sentence_{idx+1:02d}.wav"


# ── record one sentence to disk ────────────────────────────────
def record_sentence(idx: int, sentence: str) -> np.ndarray:
    path = wav_path(idx)
    print(f"\n  [{idx+1}/{len(SENTENCES)}] Say: {c(Fore.CYAN, sentence)}")
    countdown(COUNTDOWN_SEC)
    print(f"  {c(Fore.RED, '● REC')}  speak now ({RECORD_SECONDS}s)", flush=True)

    audio = sd.rec(
        int(RECORD_SECONDS * RECORD_SAMPLE_RATE),
        samplerate=RECORD_SAMPLE_RATE,
        channels=1,
        dtype="float32",
    )
    sd.wait()
    audio = audio[:, 0]

    sf.write(str(path), audio, RECORD_SAMPLE_RATE)
    ok(f"Saved → {path.relative_to(ROOT)}")
    return audio


# ── load saved recording ───────────────────────────────────────
def load_sentence(idx: int) -> np.ndarray:
    audio, sr = sf.read(str(wav_path(idx)), dtype="float32")
    if audio.ndim > 1:
        audio = audio[:, 0]
    if sr != RECORD_SAMPLE_RATE:
        audio = resample(audio, sr, RECORD_SAMPLE_RATE)
    return audio


# ── silence trimmer — mimics what VAD does in real use ────────
def trim_silence(audio: np.ndarray, sr: int, pad_ms: int = 150) -> np.ndarray:
    """
    Adaptive silence trim based on the recording's own noise floor.
    Uses bottom 20% of frame energies as silence baseline, cuts frames
    below 4x that level. Matches what VAD actually sends to Whisper.
    """
    frame = int(sr * 0.02)  # 20ms
    hop = frame // 2
    pad = int(sr * pad_ms / 1000)

    frames = [audio[i : i + frame] for i in range(0, len(audio) - frame, hop)]
    if not frames:
        return audio

    energies = np.array([np.sqrt(np.mean(f**2)) for f in frames])

    # noise floor = 20th percentile of all frame energies
    noise_floor = np.percentile(energies, 20)
    threshold = max(noise_floor * 4.0, 1e-4)  # 4x noise floor, minimum guard

    speech = energies > threshold
    if not speech.any():
        return audio  # nothing above noise — return as-is

    first = max(0, speech.argmax() * hop - pad)
    last = min(len(audio), (len(speech) - speech[::-1].argmax()) * hop + pad)
    return audio[first:last]


# ── run audio through the live pipeline, measure everything ───
def run_pipeline(audio: np.ndarray) -> dict:
    """
    Feed raw recorded audio (at RECORD_SAMPLE_RATE) through the real
    resample → normalise → whisper pipeline and return timing + text.
    Silence is trimmed first to match what VAD sends at runtime.
    """
    # 1. trim silence — matches real VAD behaviour
    audio_trimmed = trim_silence(audio, RECORD_SAMPLE_RATE)
    audio_duration_ms = len(audio_trimmed) / RECORD_SAMPLE_RATE * 1000

    # 2. resample + normalise
    t_pre = time.perf_counter()
    audio_16k = resample(audio_trimmed, RECORD_SAMPLE_RATE, WHISPER_SAMPLE_RATE)
    audio_16k = normalise(audio_16k)
    preprocess_ms = (time.perf_counter() - t_pre) * 1000

    # 2. whisper inference
    model = get_model()
    from config.vad import (
        NO_SPEECH_THRESHOLD,
        LOGPROB_THRESHOLD,
        COMPRESSION_RATIO_THRESHOLD,
    )
    from config.whisper import WHISPER_DEVICE

    t_whisper = time.perf_counter()
    from transcription.model.lock import infer_lock

    with infer_lock:
        result = _whisper.transcribe(
            model,
            audio_16k,
            language="en",
            fp16=(WHISPER_DEVICE == "cuda"),
            temperature=0,
            condition_on_previous_text=False,
            no_speech_threshold=NO_SPEECH_THRESHOLD,
            compression_ratio_threshold=COMPRESSION_RATIO_THRESHOLD,
            logprob_threshold=LOGPROB_THRESHOLD,
        )
    whisper_ms = (time.perf_counter() - t_whisper) * 1000

    # 3. hallucination filters
    text = ""
    passed_confidence = passes_confidence(result)
    raw_text = clean_text(result.get("text", ""))
    if passed_confidence and raw_text and not has_repetition(raw_text):
        text = raw_text

    # no_speech_prob from segments
    segs = result.get("segments", [])
    avg_no_speech = (
        sum(s.get("no_speech_prob", 0) for s in segs) / len(segs) if segs else 0.0
    )

    return {
        "text": text,
        "raw_text": result.get("text", "").strip(),
        "whisper_ms": whisper_ms,
        "preprocess_ms": preprocess_ms,
        "audio_duration_ms": audio_duration_ms,
        "passed_confidence": passed_confidence,
        "avg_no_speech": avg_no_speech,
        "segments": len(segs),
    }


# ── benchmark one sentence ─────────────────────────────────────
def benchmark_sentence(idx: int, audio: np.ndarray) -> dict:
    sentence = SENTENCES[idx]
    r = run_pipeline(audio)
    score = wer_score(sentence, r["text"])

    # e2e = preprocess + whisper  (VAD pause is real-world overhead, not pipeline)
    e2e_ms = r["preprocess_ms"] + r["whisper_ms"]

    r["ref"] = sentence
    r["wer"] = score
    r["e2e_ms"] = e2e_ms
    return r


# ── print one result ───────────────────────────────────────────
def print_result(idx: int, r: dict) -> None:
    ref = SENTENCES[idx]
    hyp = r["text"]

    wer_c = (
        Fore.GREEN if r["wer"] < 0.1 else Fore.YELLOW if r["wer"] < 0.3 else Fore.RED
    )
    wsp_c = (
        Fore.GREEN
        if r["whisper_ms"] < 600
        else Fore.YELLOW if r["whisper_ms"] < 1200 else Fore.RED
    )
    e2e_c = (
        Fore.GREEN
        if r["e2e_ms"] < 700
        else Fore.YELLOW if r["e2e_ms"] < 1400 else Fore.RED
    )
    nsp_c = (
        Fore.GREEN
        if r["avg_no_speech"] < 0.3
        else Fore.YELLOW if r["avg_no_speech"] < 0.45 else Fore.RED
    )

    print(f"\n  [{idx+1}] {c(Fore.CYAN, ref)}")
    if hyp:
        print(f"       {c(Fore.WHITE, hyp)}")
    else:
        print(f"       {c(Fore.RED, '(no transcript)')}")
        if r["raw_text"]:
            print(f"       raw: {c(Fore.YELLOW, r['raw_text'])}")

    dur_str = f"{r['audio_duration_ms']:.0f} ms"
    wsp_str = f"{r['whisper_ms']:.0f} ms"
    e2e_str = f"{r['e2e_ms']:.0f} ms"
    wer_str = f"{r['wer']:.0%}"
    nsp_str = f"{r['avg_no_speech']:.2f}  (limit={__import__('config.vad', fromlist=['NO_SPEECH_THRESHOLD']).NO_SPEECH_THRESHOLD})"

    info(f"Audio to Whisper  : {dur_str}  (trimmed from 5s)")
    info(f"Whisper inference : {c(wsp_c, wsp_str)}")
    info(f"Preprocess        : {r['preprocess_ms']:.0f} ms")
    info(f"Pipeline total    : {c(e2e_c, e2e_str)}")
    info(f"no_speech_prob    : {c(nsp_c, nsp_str)}")
    info(f"WER               : {c(wer_c, wer_str)}")
    if not r["passed_confidence"]:
        warn(
            f"REJECTED by confidence filter — speak louder/clearer or raise NO_SPEECH_THRESHOLD"
        )


# ── summary ────────────────────────────────────────────────────
def print_summary(results: list[dict]) -> None:
    head("SUMMARY")
    print()

    detected = [r for r in results if r["text"]]
    wsp = [r["whisper_ms"] for r in detected]
    e2e = [r["e2e_ms"] for r in detected]
    wers = [r["wer"] for r in detected]

    def stat(vals, unit="ms"):
        if not vals:
            return "no data"
        avg = sum(vals) / len(vals)
        mn = min(vals)
        mx = max(vals)
        return f"avg {avg:.0f}{unit}  min {mn:.0f}{unit}  max {mx:.0f}{unit}"

    rule()
    print(f"  {'Whisper inference':<26} {stat(wsp)}")
    print(f"  {'Pipeline total (no VAD)':<26} {stat(e2e)}")
    if wers:
        avg_wer = sum(wers) / len(wers)
        wer_c = (
            Fore.GREEN if avg_wer < 0.1 else Fore.YELLOW if avg_wer < 0.3 else Fore.RED
        )
        print(f"  {'WER':<26} {c(wer_c, f'avg {avg_wer:.1%}')}")
    print(f"  {'Detection rate':<26} {len(detected)}/{len(results)}")
    rule()

    # real-world E2E estimate
    pause_ms = PAUSE_SECONDS * 1000
    avg_wsp = sum(wsp) / len(wsp) if wsp else 0
    est_e2e = pause_ms + avg_wsp
    print(f"\n  Real-world E2E estimate:")
    print(f"    PAUSE_SECONDS overhead : {pause_ms:.0f} ms   (config/vad.py)")
    print(f"    Whisper avg            : {avg_wsp:.0f} ms")
    print(f"    ─────────────────────────────────")
    e2e_color = (
        Fore.GREEN if est_e2e < 1200 else Fore.YELLOW if est_e2e < 2000 else Fore.RED
    )
    print(f"    Estimated felt latency : {c(e2e_color, f'{est_e2e:.0f} ms')}")

    # diagnosis
    head("DIAGNOSIS")
    print()
    any_rec = False

    if wsp:
        avg = sum(wsp) / len(wsp)
        if avg > 1200:
            warn(
                f"Whisper is SLOW ({avg:.0f}ms). Try WHISPER_MODEL_NAME='tiny' in config/whisper.py"
            )
            any_rec = True
        elif avg > 600:
            warn(f"Whisper is moderate ({avg:.0f}ms). 'tiny' model would cut this ~50%")
            any_rec = True
        else:
            ok(f"Whisper is fast ({avg:.0f}ms avg)")

    if PAUSE_SECONDS > 0.6:
        warn(
            f"PAUSE_SECONDS={PAUSE_SECONDS} — dominates latency. Lower to 0.4–0.5 for ~{(PAUSE_SECONDS-0.45)*1000:.0f}ms gain"
        )
        any_rec = True
    elif PAUSE_SECONDS > 0.4:
        warn(f"PAUSE_SECONDS={PAUSE_SECONDS} — try 0.4 for tighter cutoff")
        any_rec = True
    else:
        ok(f"PAUSE_SECONDS={PAUSE_SECONDS} is aggressive (good)")

    miss = len(results) - len(detected)
    if miss > 0:
        warn(
            f"{miss} sentences not detected — VAD may be too strict or recordings too quiet"
        )
        any_rec = True

    if not any_rec:
        ok("Pipeline is well tuned. Paste numbers below to get further advice.")

    # paste block
    head("NUMBERS TO PASTE")
    print()
    print(
        f"  PAUSE_SECONDS={PAUSE_SECONDS}  SILERO_THRESHOLD={SILERO_THRESHOLD}  TRANSCRIBE_EVERY={TRANSCRIBE_EVERY}"
    )
    if wsp:
        print(
            f"  whisper_avg={sum(wsp)/len(wsp):.0f}ms  min={min(wsp):.0f}ms  max={max(wsp):.0f}ms"
        )
    if e2e:
        print(f"  pipeline_avg={sum(e2e)/len(e2e):.0f}ms  felt_e2e_est={est_e2e:.0f}ms")
    if wers:
        print(
            f"  wer_avg={sum(wers)/len(wers):.1%}  detection={len(detected)}/{len(results)}"
        )
    print()


# ── main ───────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--record",
        action="store_true",
        help="Force re-record all sentences (overwrites saved WAVs)",
    )
    parser.add_argument(
        "--replay", action="store_true", help="Force replay mode — never touch the mic"
    )
    parser.add_argument(
        "--sentence",
        type=int,
        default=0,
        help="Only run sentence N (1-based). Default: all.",
    )
    args = parser.parse_args()

    # figure out which sentences to process
    indices = [args.sentence - 1] if args.sentence else list(range(len(SENTENCES)))

    # print config header
    head("STT BENCHMARK  —  record-once, replay-forever")
    print()
    print(f"  Recordings dir : {RECORDINGS_DIR.relative_to(ROOT)}")
    print(f"  Config snapshot:")
    print(
        f"    PAUSE_SECONDS    = {c(Fore.CYAN, PAUSE_SECONDS)}   ← adds this to every utterance"
    )
    print(f"    SILERO_THRESHOLD = {c(Fore.CYAN, SILERO_THRESHOLD)}")
    print(f"    TRANSCRIBE_EVERY = {c(Fore.CYAN, TRANSCRIBE_EVERY)}")
    print(
        f"    WHISPER_MODEL    = {c(Fore.CYAN, __import__('config.whisper', fromlist=['WHISPER_MODEL_NAME']).WHISPER_MODEL_NAME)}"
    )
    rule()

    # load whisper
    print(f"\n  Loading Whisper...")
    get_model()
    ok("Whisper ready")
    # warm up scipy resampler — kills JIT hit on first sentence
    resample(
        np.zeros(int(RECORD_SAMPLE_RATE * 0.02), dtype=np.float32),
        RECORD_SAMPLE_RATE,
        WHISPER_SAMPLE_RATE,
    )
    ok("Resampler warmed up")

    results: list[dict] = [None] * len(SENTENCES)

    for idx in indices:
        sentence = SENTENCES[idx]
        path = wav_path(idx)

        # decide: record or load
        if args.replay and not path.exists():
            warn(f"[{idx+1}] No recording found at {path.name} — skipping")
            continue

        if args.record or not path.exists():
            # record mode
            if args.replay:
                warn(f"[{idx+1}] --replay set but no file — skipping")
                continue
            if not path.exists():
                info(f"[{idx+1}] No recording found — recording now")
            audio = record_sentence(idx, sentence)
        else:
            info(f"[{idx+1}] Loading saved recording: {path.name}")
            audio = load_sentence(idx)

        # benchmark
        r = benchmark_sentence(idx, audio)
        results[idx] = r
        print_result(idx, r)
        rule()

    # summary over completed results
    completed = [r for r in results if r is not None]
    if len(completed) > 1:
        print_summary(completed)
    elif len(completed) == 1:
        # single sentence — still show estimate
        r = completed[0]
        pause_ms = PAUSE_SECONDS * 1000
        est = pause_ms + r["whisper_ms"]
        print(
            f"\n  Felt latency estimate: {pause_ms:.0f}ms (pause) + {r['whisper_ms']:.0f}ms (whisper) = {c(Fore.CYAN, f'{est:.0f}ms')}"
        )


if __name__ == "__main__":
    main()

```

### tests/benchmark_tts.py

```python
"""
tests/benchmark_tts.py
======================
Full end-to-end pipeline benchmark: WAV → Whisper → LLM → TTS → playback

Mirrors _run_full() in main.py exactly, but:
  - Feeds pre-recorded WAVs instead of live mic (uses tests/recordings/)
  - Captures every latency segment
  - Measures TTS smoothness: chunk count, inter-chunk gaps, words-per-chunk
  - Prints a colour-coded report with diagnosis + tuning advice

Usage:
    python tests/benchmark_tts.py                  # all 10 sentences
    python tests/benchmark_tts.py --sentence 3     # only sentence #3
    python tests/benchmark_tts.py --no-audio       # skip actual playback (latency only)
    python tests/benchmark_tts.py --no-llm         # feed fixed text directly to TTS
    python tests/benchmark_tts.py --steps 8        # override TTS diffusion steps
    python tests/benchmark_tts.py --tts-text "Hello world, this is a test."

Pre-requisite: run benchmark_stt.py first so tests/recordings/ exists.
"""

import sys
import time
import argparse
import threading
from pathlib import Path
from dataclasses import dataclass, field

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import numpy as np
import soundfile as sf
from colorama import Fore, Style, init as colorama_init

colorama_init()

from config.vad import RECORD_SAMPLE_RATE, PAUSE_SECONDS
from config.whisper import WHISPER_SAMPLE_RATE
from config.tts import (
    SUPERTONIC_VOICE,
    SUPERTONIC_SPEED,
    SUPERTONIC_STEPS,
    SUPERTONIC_LANGUAGE,
)

RECORDINGS_DIR = ROOT / "tests" / "recordings"

SENTENCES = [
    "open the calendar and show me this week",
    "what is the weather like today",
    "set a reminder for tomorrow at nine am",
    "send a message to John saying I will be late",
    "search the web for latest AI news",
    "turn off the lights in the living room",
    "call mom when you get a chance",
    "how long does it take to drive to the airport",
    "play some music on spotify",
    "the quick brown fox jumps over the lazy dog",
]


# ─────────────────────────────────────────────────────────────
# Terminal helpers
# ─────────────────────────────────────────────────────────────


def c(color, msg):
    return f"{color}{msg}{Style.RESET_ALL}"


def ok(m):
    print(f"  {c(Fore.GREEN,  '✓')}  {m}")


def fail(m):
    print(f"  {c(Fore.RED,    '✗')}  {m}")


def info(m):
    print(f"  {c(Fore.CYAN,   '→')}  {m}")


def warn(m):
    print(f"  {c(Fore.YELLOW, '!')}  {m}")


def head(m):
    print(f"\n  {c(Fore.YELLOW + Style.BRIGHT, m)}")


def rule():
    print(f"  {'─' * 66}")


def ms_c(ms, green=300, yellow=700):
    return Fore.GREEN if ms < green else Fore.YELLOW if ms < yellow else Fore.RED


def tag(label, val, color=Fore.WHITE):
    print(f"  {label:<36} {c(color, val)}")


# ─────────────────────────────────────────────────────────────
# Result container
# ─────────────────────────────────────────────────────────────


@dataclass
class BenchResult:
    sentence_idx: int
    input_text: str
    stt_text: str = ""
    llm_text: str = ""

    stt_ms: float = 0.0
    llm_first_token_ms: float = 0.0
    llm_total_ms: float = 0.0
    tts_first_chunk_ms: float = 0.0
    tts_total_ms: float = 0.0
    e2e_ms: float = 0.0

    chunk_count: int = 0
    chunk_sizes_words: list = field(default_factory=list)
    chunk_gen_times_ms: list = field(default_factory=list)
    inter_chunk_gaps_ms: list = field(default_factory=list)

    filler_text: str = ""
    filler_gen_ms: float = 0.0
    filler_duration_ms: float = 0.0
    filler_covers_llm: bool = False

    stt_passed: bool = True
    error: str = ""


# ─────────────────────────────────────────────────────────────
# Instrumented TTS engine
# ─────────────────────────────────────────────────────────────


class InstrumentedTTSEngine:
    def __init__(self, voice, speed, steps, language, play_fn):
        self.voice = voice
        self.speed = speed
        self.steps = steps
        self.language = language
        self.play_fn = play_fn
        self._chunks: list[str] = []

    def enqueue(self, text: str):
        if text.strip():
            self._chunks.append(text.strip())

    def run(self) -> dict:
        from tts.generate.pipeline import generate_one
        from tts.model.singleton import get_model
        from tts.text.clean import clean_markdown

        sr = get_model()["sample_rate"]
        chunk_gen_times, inter_chunk_gaps = [], []
        prev_end = None
        total_start = time.perf_counter()

        for text in self._chunks:
            cleaned = clean_markdown(text)
            if not cleaned:
                continue
            if prev_end is not None:
                inter_chunk_gaps.append((time.perf_counter() - prev_end) * 1000)

            t0 = time.perf_counter()
            audio = generate_one(
                cleaned,
                voice=self.voice,
                speed=self.speed,
                steps=self.steps,
                language=self.language,
            )
            gen_ms = (time.perf_counter() - t0) * 1000
            chunk_gen_times.append(gen_ms)
            self.play_fn(audio, sr)
            prev_end = time.perf_counter()

        return {
            "chunk_count": len(self._chunks),
            "chunk_sizes_words": [len(ch.split()) for ch in self._chunks],
            "chunk_gen_times_ms": chunk_gen_times,
            "inter_chunk_gaps_ms": inter_chunk_gaps,
            "tts_first_chunk_ms": chunk_gen_times[0] if chunk_gen_times else 0.0,
            "tts_total_ms": (time.perf_counter() - total_start) * 1000,
        }


# ─────────────────────────────────────────────────────────────
# Feed LLM tokens to engine (mirrors optimised feed.py)
# ─────────────────────────────────────────────────────────────


def feed_tokens_to_engine(engine: InstrumentedTTSEngine, token_gen) -> tuple:
    from tts.text.split import split_sentence, MIN_CHUNK_CHARS

    WORD_FLUSH_THRESHOLD = 6
    MIN_SEND_CHARS = 20

    buf, full = "", ""
    first_token_ms = None
    t_start = time.perf_counter()

    for token in token_gen:
        if first_token_ms is None:
            first_token_ms = (time.perf_counter() - t_start) * 1000
        buf += token
        full += token

        while True:
            sentence, remainder = split_sentence(buf)
            if sentence and len(sentence) >= MIN_SEND_CHARS:
                engine.enqueue(sentence)
                buf = remainder
            else:
                break

        if len(buf.split()) >= WORD_FLUSH_THRESHOLD:
            engine.enqueue(buf.strip())
            buf = ""

    if buf.strip() and len(buf.strip()) >= 2:
        engine.enqueue(buf.strip())

    llm_total_ms = (time.perf_counter() - t_start) * 1000
    return full, first_token_ms or llm_total_ms, llm_total_ms


# ─────────────────────────────────────────────────────────────
# STT
# ─────────────────────────────────────────────────────────────


def run_stt(wav_path: Path) -> tuple:
    from audio.transform.resample import resample
    from audio.transform.normalise import normalise
    from transcription.model.singleton import get_model
    from transcription.model.lock import infer_lock
    from transcription.hallucination.confidence import passes_confidence
    from transcription.hallucination.noise import clean_text
    from transcription.hallucination.repetition import has_repetition
    from transcription.transcribe.options import build_whisper_options
    import whisper as _whisper

    audio, sr = sf.read(str(wav_path), dtype="float32")
    if audio.ndim > 1:
        audio = audio[:, 0]
    if sr != RECORD_SAMPLE_RATE:
        audio = resample(audio, sr, RECORD_SAMPLE_RATE)
    audio_16k = resample(audio, RECORD_SAMPLE_RATE, WHISPER_SAMPLE_RATE)
    audio_16k = normalise(audio_16k)

    model = get_model()
    opts = build_whisper_options()
    t0 = time.perf_counter()
    with infer_lock:
        result = _whisper.transcribe(model, audio_16k, **opts)
    stt_ms = (time.perf_counter() - t0) * 1000

    passed = passes_confidence(result)
    text = ""
    if passed:
        raw = clean_text(result.get("text", ""))
        if raw and not has_repetition(raw):
            text = raw
    return text, stt_ms, passed


# ─────────────────────────────────────────────────────────────
# Full pipeline for one sentence
# ─────────────────────────────────────────────────────────────


def benchmark_one(idx: int, args, play_fn) -> BenchResult:
    r = BenchResult(sentence_idx=idx, input_text=SENTENCES[idx])
    wav = RECORDINGS_DIR / f"sentence_{idx+1:02d}.wav"

    if not wav.exists():
        r.error = f"No recording at {wav.name} — run benchmark_stt.py first"
        return r

    e2e_start = time.perf_counter()

    # ── STT ─────────────────────────────────────────────────
    if args.no_llm and args.tts_text:
        r.stt_text = args.tts_text
    else:
        try:
            r.stt_text, r.stt_ms, r.stt_passed = run_stt(wav)
        except Exception as e:
            r.error = f"STT error: {e}"
            return r
        if not r.stt_text:
            r.error = "STT: no transcript"
            return r

    # ── Filler measurement ───────────────────────────────────
    try:
        from tts.generate.pipeline import generate_one
        from tts.model.singleton import get_model

        # Pick the longest filler to test coverage
        from tts.engine.state import _FILLERS

        filler_text = max(_FILLERS, key=len)
        r.filler_text = filler_text
        t_fil = time.perf_counter()
        filler_audio = generate_one(
            filler_text,
            voice=args.voice,
            speed=args.speed,
            steps=args.steps,
            language=args.language,
        )
        r.filler_gen_ms = (time.perf_counter() - t_fil) * 1000
        sr = get_model()["sample_rate"]
        r.filler_duration_ms = len(filler_audio) / sr * 1000
    except Exception as e:
        warn(f"Filler measurement failed: {e}")

    # ── LLM + TTS feed ──────────────────────────────────────
    engine = InstrumentedTTSEngine(
        voice=args.voice,
        speed=args.speed,
        steps=args.steps,
        language=args.language,
        play_fn=play_fn,
    )

    if args.no_llm:

        def _fixed():
            for w in (args.tts_text or r.stt_text).split():
                yield w + " "

        token_gen = _fixed()
    else:
        from llm.inference.stream import stream_response
        from llm.history.state import create_history

        token_gen = stream_response(r.stt_text, create_history())

    try:
        r.llm_text, r.llm_first_token_ms, r.llm_total_ms = feed_tokens_to_engine(
            engine, token_gen
        )
    except Exception as e:
        r.error = f"LLM error: {e}"
        return r

    # ── TTS generation ───────────────────────────────────────
    try:
        tts_info = engine.run()
    except Exception as e:
        r.error = f"TTS error: {e}"
        return r

    r.chunk_count = tts_info["chunk_count"]
    r.chunk_sizes_words = tts_info["chunk_sizes_words"]
    r.chunk_gen_times_ms = tts_info["chunk_gen_times_ms"]
    r.inter_chunk_gaps_ms = tts_info["inter_chunk_gaps_ms"]
    r.tts_first_chunk_ms = tts_info["tts_first_chunk_ms"]
    r.tts_total_ms = tts_info["tts_total_ms"]
    r.e2e_ms = (time.perf_counter() - e2e_start) * 1000
    r.filler_covers_llm = r.filler_duration_ms >= r.llm_first_token_ms

    return r


# ─────────────────────────────────────────────────────────────
# Print one result
# ─────────────────────────────────────────────────────────────


def print_result(r: BenchResult, args) -> None:
    n = r.sentence_idx + 1
    print(f"\n  [{n}] {c(Fore.CYAN, r.input_text)}")
    if r.error:
        fail(r.error)
        return

    if not args.no_llm:
        print(f"       STT : {c(Fore.WHITE, r.stt_text or '(empty)')}")
    llm_preview = r.llm_text[:110] + ("…" if len(r.llm_text) > 110 else "")
    print(f"       LLM : {c(Fore.WHITE, llm_preview)}")
    print()

    rule()
    if not args.no_llm:
        tag("STT (Whisper)", f"{r.stt_ms:.0f} ms", ms_c(r.stt_ms, 600, 1200))
    tag(
        "LLM → first token",
        f"{r.llm_first_token_ms:.0f} ms",
        ms_c(r.llm_first_token_ms, 500, 1500),
    )
    tag(
        "LLM → full response",
        f"{r.llm_total_ms:.0f} ms",
        ms_c(r.llm_total_ms, 800, 2000),
    )

    if r.filler_duration_ms:
        cover = (
            "✓ covers LLM"
            if r.filler_covers_llm
            else f"✗ {r.llm_first_token_ms - r.filler_duration_ms:.0f}ms gap"
        )
        fil_color = Fore.GREEN if r.filler_covers_llm else Fore.RED
        tag(
            f"Filler ({r.filler_text!r})",
            f"{r.filler_duration_ms:.0f} ms  [{cover}]",
            fil_color,
        )

    tag(
        "TTS first chunk generation",
        f"{r.tts_first_chunk_ms:.0f} ms",
        ms_c(r.tts_first_chunk_ms, 300, 700),
    )
    tag(
        "TTS total generation",
        f"{r.tts_total_ms:.0f} ms",
        ms_c(r.tts_total_ms, 2000, 5000),
    )

    if not args.no_llm:
        tag("End-to-end", f"{r.e2e_ms:.0f} ms", ms_c(r.e2e_ms, 4000, 8000))
    rule()

    print(f"\n  TTS Smoothness")
    rule()
    tag(
        "Chunks generated",
        str(r.chunk_count),
        (
            Fore.GREEN
            if r.chunk_count <= 4
            else Fore.YELLOW if r.chunk_count <= 7 else Fore.RED
        ),
    )

    if r.chunk_sizes_words:
        avg_w = sum(r.chunk_sizes_words) / len(r.chunk_sizes_words)
        tag(
            "Avg words per chunk",
            f"{avg_w:.1f}",
            Fore.GREEN if avg_w >= 5 else Fore.YELLOW if avg_w >= 3 else Fore.RED,
        )
        tag("Chunk word distribution", str(r.chunk_sizes_words))

    if r.chunk_gen_times_ms:
        avg_gen = sum(r.chunk_gen_times_ms) / len(r.chunk_gen_times_ms)
        tag("Avg chunk gen time", f"{avg_gen:.0f} ms", ms_c(avg_gen, 300, 600))
        tag(
            "Per-chunk gen times (ms)",
            "  ".join(f"{v:.0f}" for v in r.chunk_gen_times_ms),
        )

    if r.inter_chunk_gaps_ms:
        avg_gap = sum(r.inter_chunk_gaps_ms) / len(r.inter_chunk_gaps_ms)
        max_gap = max(r.inter_chunk_gaps_ms)
        tag(
            "Avg / max inter-chunk gap",
            f"{avg_gap:.0f} ms / {max_gap:.0f} ms",
            Fore.GREEN if max_gap < 60 else Fore.YELLOW if max_gap < 150 else Fore.RED,
        )
    rule()


# ─────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────


def print_summary(results: list[BenchResult], args) -> None:
    good = [r for r in results if not r.error and r.chunk_count > 0]
    if not good:
        warn("No successful results.")
        return

    head("SUMMARY")
    print()
    rule()

    def avg(vals):
        return sum(vals) / len(vals) if vals else 0

    stt_vals = [r.stt_ms for r in good]
    ft_vals = [r.llm_first_token_ms for r in good]
    llm_vals = [r.llm_total_ms for r in good]
    tts1_vals = [r.tts_first_chunk_ms for r in good]
    ttst_vals = [r.tts_total_ms for r in good]
    e2e_vals = [r.e2e_ms for r in good]
    gap_vals = [g for r in good for g in r.inter_chunk_gaps_ms]
    fil_vals = [r.filler_duration_ms for r in good if r.filler_duration_ms]
    cw_vals = [w for r in good for w in r.chunk_sizes_words]

    if stt_vals and not args.no_llm:
        a = avg(stt_vals)
        tag("STT avg", f"{a:.0f} ms", ms_c(a, 600, 1200))
    if ft_vals:
        a = avg(ft_vals)
        tag("LLM first token avg", f"{a:.0f} ms", ms_c(a, 500, 1500))
    if llm_vals:
        a = avg(llm_vals)
        tag("LLM total avg", f"{a:.0f} ms", ms_c(a, 800, 2000))
    if fil_vals:
        a = avg(fil_vals)
        tag("Filler duration avg", f"{a:.0f} ms")
    if tts1_vals:
        a = avg(tts1_vals)
        tag("TTS first chunk avg", f"{a:.0f} ms", ms_c(a, 300, 700))
    if ttst_vals:
        a = avg(ttst_vals)
        tag("TTS total avg", f"{a:.0f} ms", ms_c(a, 2000, 5000))
    if cw_vals:
        a = avg(cw_vals)
        tag(
            "Avg words/chunk",
            f"{a:.1f}",
            Fore.GREEN if a >= 5 else Fore.YELLOW if a >= 3 else Fore.RED,
        )
    if gap_vals:
        a = avg(gap_vals)
        mx = max(gap_vals)
        tag(
            "Inter-chunk gap avg/max",
            f"{a:.0f} ms / {mx:.0f} ms",
            Fore.GREEN if mx < 60 else Fore.YELLOW,
        )
    if e2e_vals and not args.no_llm:
        a = avg(e2e_vals)
        tag("End-to-end avg", f"{a:.0f} ms", ms_c(a, 4000, 8000))
    rule()

    head("DIAGNOSIS & TUNING ADVICE")
    print()
    any_rec = False

    # TTS first chunk
    if tts1_vals:
        a = avg(tts1_vals)
        if a > 700:
            warn(
                f"TTS first chunk slow ({a:.0f}ms). "
                f"Reduce SUPERTONIC_STEPS: currently {args.steps}, try {max(6, args.steps - 3)}"
            )
            any_rec = True
        elif a > 300:
            warn(
                f"TTS first chunk moderate ({a:.0f}ms). "
                f"Try steps={max(6, args.steps - 2)} to cut ~30%"
            )
            any_rec = True
        else:
            ok(f"TTS first chunk fast ({a:.0f}ms)")

    # Chunk fragmentation
    if cw_vals:
        a = avg(cw_vals)
        counts = [r.chunk_count for r in good]
        ac = avg(counts)
        if a < 3:
            warn(
                f"Avg {a:.1f} words/chunk ({ac:.1f} chunks/response) — "
                f"too fragmented, each chunk wastes ~350ms ONNX overhead. "
                f"Raise WORD_FLUSH_THRESHOLD in tts/engine/feed.py"
            )
            any_rec = True
        elif a >= 5:
            ok(f"Chunk size good ({a:.1f} words avg, {ac:.1f} chunks/response)")
        else:
            warn(f"Chunks borderline ({a:.1f} words avg). Aim for 6+ words/chunk")
            any_rec = True

    # Filler coverage
    if fil_vals and ft_vals:
        avg_fil = avg(fil_vals)
        avg_ft = avg(ft_vals)
        if avg_fil >= avg_ft * 0.9:
            ok(f"Filler ({avg_fil:.0f}ms) covers LLM first-token ({avg_ft:.0f}ms)")
        else:
            gap = avg_ft - avg_fil
            warn(
                f"Filler ({avg_fil:.0f}ms) shorter than LLM first-token ({avg_ft:.0f}ms) "
                f"— {gap:.0f}ms silence gap. Longer fillers added to state.py fix this."
            )
            any_rec = True

    # LLM speed
    if ft_vals:
        a = avg(ft_vals)
        if a > 1500:
            warn(
                f"LLM first token {a:.0f}ms — try GPU_LAYERS=36 (max) in config/llm.py "
                f"or a smaller model (qwen2.5-1.5b)"
            )
            any_rec = True

    if not any_rec:
        ok("Pipeline is well tuned!")

    head("NUMBERS TO PASTE")
    print()
    print(f"  voice={args.voice}  speed={args.speed}  steps={args.steps}")
    if tts1_vals:
        print(
            f"  tts_first_chunk_avg={avg(tts1_vals):.0f}ms  tts_total_avg={avg(ttst_vals):.0f}ms"
        )
    if cw_vals:
        print(
            f"  words_per_chunk_avg={avg(cw_vals):.1f}  chunk_count_avg={avg([r.chunk_count for r in good]):.1f}"
        )
    if ft_vals:
        print(
            f"  llm_first_token_avg={avg(ft_vals):.0f}ms  llm_total_avg={avg(llm_vals):.0f}ms"
        )
    if fil_vals:
        print(f"  filler_duration_avg={avg(fil_vals):.0f}ms")
    if e2e_vals:
        print(f"  e2e_avg={avg(e2e_vals):.0f}ms")
    print()


# ─────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sentence", type=int, default=0)
    parser.add_argument("--no-audio", action="store_true")
    parser.add_argument("--no-llm", action="store_true")
    parser.add_argument("--tts-text", type=str, default="")
    parser.add_argument("--steps", type=int, default=SUPERTONIC_STEPS)
    parser.add_argument("--voice", type=str, default=SUPERTONIC_VOICE)
    parser.add_argument("--speed", type=float, default=SUPERTONIC_SPEED)
    parser.add_argument("--language", type=str, default=SUPERTONIC_LANGUAGE)
    args = parser.parse_args()

    if args.tts_text:
        args.no_llm = True

    head("FULL PIPELINE TTS BENCHMARK")
    print()
    print(f"  Recordings : {RECORDINGS_DIR.relative_to(ROOT)}")
    print(f"  Mode       : {'TTS-only' if args.no_llm else 'STT → LLM → TTS'}")
    print(f"  Playback   : {'disabled' if args.no_audio else 'enabled'}")
    print(f"  TTS config : voice={args.voice}  speed={args.speed}  steps={args.steps}")
    rule()
    print()

    if not args.no_llm:
        print("  Loading Whisper...")
        from transcription.model.singleton import get_model as load_whisper

        load_whisper()
        ok("Whisper ready")
        print("  Loading LLM...")
        from llm.model.singleton import get_model as load_llm

        load_llm()
        ok("LLM ready")

    print("  Loading TTS model...")
    from tts.model.singleton import get_model as load_tts

    load_tts()
    ok("TTS ready")

    print("  Warming up TTS...")
    from tts.generate.pipeline import generate_one

    _ = generate_one(
        "Warming up.",
        voice=args.voice,
        speed=args.speed,
        steps=args.steps,
        language=args.language,
    )
    ok("TTS warmed up")
    print()

    play_fn = (
        (lambda a, sr: None)
        if args.no_audio
        else __import__("tts.playback.stream", fromlist=["play_audio"]).play_audio
    )

    indices = [args.sentence - 1] if args.sentence else list(range(len(SENTENCES)))
    results: list[BenchResult] = []

    for idx in indices:
        print(f"\n  Running [{idx+1}/{len(SENTENCES)}]: {c(Fore.CYAN, SENTENCES[idx])}")
        r = benchmark_one(idx, args, play_fn)
        results.append(r)
        print_result(r, args)
        rule()

    completed = [r for r in results if not r.error]
    if len(completed) > 1:
        print_summary(completed, args)
    elif len(completed) == 1:
        r = completed[0]
        print(f"\n  TTS first chunk : {r.tts_first_chunk_ms:.0f} ms")
        print(f"  TTS total       : {r.tts_total_ms:.0f} ms")
        print(f"  Chunks          : {r.chunk_count}  ({r.chunk_sizes_words})")


if __name__ == "__main__":
    main()

```

### tests/recordings/sentence_01.wav

(Skipped: binary or unreadable file)


### tests/recordings/sentence_02.wav

(Skipped: binary or unreadable file)


### tests/recordings/sentence_03.wav

(Skipped: binary or unreadable file)


### tests/recordings/sentence_04.wav

(Skipped: binary or unreadable file)


### tests/recordings/sentence_05.wav

(Skipped: binary or unreadable file)


### tests/recordings/sentence_06.wav

(Skipped: binary or unreadable file)


### tests/recordings/sentence_07.wav

(Skipped: binary or unreadable file)


### tests/recordings/sentence_08.wav

(Skipped: binary or unreadable file)


### tests/recordings/sentence_09.wav

(Skipped: binary or unreadable file)


### tests/recordings/sentence_10.wav

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

### transcription/vad/session.py

```python
# transcription/vad/session.py
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
    # kills the 2s resampy JIT hit on first chunk
    resample(np.zeros(882, dtype=np.float32), RECORD_SAMPLE_RATE, WHISPER_SAMPLE_RATE)

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

WORD_FLUSH_THRESHOLD = 6  # words before force-flush mid-sentence
_MIN_SEND_CHARS = 20  # sentence splits shorter than this are held


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

MERGE_WINDOW_SEC = 0.02


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