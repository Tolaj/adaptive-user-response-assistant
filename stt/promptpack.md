# PromptPack Output

**Root:** `/Users/swapnil/Documents/Projects/adaptive-user-response-assistant/stt`
**Generated:** 2026-04-09T05:37:59.625Z

---

## 1) Folder Structure

```txt
.
├─ __init__.py
├─ __pycache__/
│  ├─ __init__.cpython-311.pyc
│  ├─ __init__.cpython-313.pyc
│  ├─ denoise.cpython-311.pyc
│  ├─ diarize.cpython-311.pyc
│  ├─ streaming_transcriber.cpython-313.pyc
│  ├─ transcriber.cpython-313.pyc
│  └─ whisper_loader.cpython-313.pyc
├─ download/
│  ├─ __init__.py
│  ├─ __pycache__/
│  │  ├─ __init__.cpython-311.pyc
│  │  ├─ __init__.cpython-313.pyc
│  │  ├─ whisper.cpython-311.pyc
│  │  └─ whisper.cpython-313.pyc
│  └─ whisper.py
├─ hallucination/
│  ├─ __init__.py
│  ├─ __pycache__/
│  │  ├─ __init__.cpython-311.pyc
│  │  ├─ __init__.cpython-313.pyc
│  │  ├─ confidence.cpython-311.pyc
│  │  ├─ confidence.cpython-313.pyc
│  │  ├─ noise.cpython-311.pyc
│  │  ├─ noise.cpython-313.pyc
│  │  ├─ repetition.cpython-311.pyc
│  │  └─ repetition.cpython-313.pyc
│  ├─ confidence.py
│  ├─ noise.py
│  └─ repetition.py
├─ model/
│  ├─ __init__.py
│  ├─ __pycache__/
│  │  ├─ __init__.cpython-311.pyc
│  │  ├─ __init__.cpython-313.pyc
│  │  ├─ device.cpython-311.pyc
│  │  ├─ device.cpython-313.pyc
│  │  ├─ load.cpython-311.pyc
│  │  ├─ load.cpython-313.pyc
│  │  ├─ lock.cpython-311.pyc
│  │  ├─ lock.cpython-313.pyc
│  │  ├─ singleton.cpython-311.pyc
│  │  └─ singleton.cpython-313.pyc
│  ├─ device.py
│  ├─ load.py
│  ├─ lock.py
│  └─ singleton.py
├─ stream/
│  ├─ __init__.py
│  ├─ __pycache__/
│  │  ├─ __init__.cpython-311.pyc
│  │  ├─ __init__.cpython-313.pyc
│  │  ├─ buffer.cpython-311.pyc
│  │  ├─ buffer.cpython-313.pyc
│  │  ├─ final.cpython-311.pyc
│  │  ├─ final.cpython-313.pyc
│  │  ├─ partial.cpython-311.pyc
│  │  ├─ partial.cpython-313.pyc
│  │  ├─ worker.cpython-311.pyc
│  │  └─ worker.cpython-313.pyc
│  ├─ buffer.py
│  ├─ final.py
│  ├─ partial.py
│  └─ worker.py
├─ transcribe/
│  ├─ __init__.py
│  ├─ __pycache__/
│  │  ├─ __init__.cpython-311.pyc
│  │  ├─ __init__.cpython-313.pyc
│  │  ├─ batch.cpython-311.pyc
│  │  ├─ batch.cpython-313.pyc
│  │  ├─ options.cpython-311.pyc
│  │  └─ options.cpython-313.pyc
│  ├─ batch.py
│  └─ options.py
└─ vad/
   ├─ __init__.py
   ├─ __pycache__/
   │  ├─ __init__.cpython-311.pyc
   │  ├─ __init__.cpython-313.pyc
   │  ├─ energy.cpython-311.pyc
   │  ├─ energy.cpython-313.pyc
   │  ├─ processor.cpython-311.pyc
   │  ├─ processor.cpython-313.pyc
   │  ├─ ptt.cpython-311.pyc
   │  ├─ ptt.cpython-313.pyc
   │  ├─ session.cpython-311.pyc
   │  ├─ session.cpython-313.pyc
   │  ├─ silero.cpython-311.pyc
   │  ├─ silero.cpython-313.pyc
   │  ├─ state.cpython-311.pyc
   │  └─ state.cpython-313.pyc
   ├─ energy.py
   ├─ processor.py
   ├─ session.py
   ├─ silero.py
   └─ state.py
```

<!-- PAGE BREAK: FILE CONTENTS BELOW -->

## 2) File Contents


### __init__.py

```python
# transcription/__init__.py
from stt.model.singleton import get_model, is_loaded
from stt.transcribe.batch import transcribe_audio
from stt.stream import (
    create_stream,
    start_stream,
    stop_stream,
    feed,
    end_of_speech,
    clear_stream,
)

```

### __pycache__/__init__.cpython-311.pyc

(Skipped: binary or unreadable file)


### __pycache__/__init__.cpython-313.pyc

(Skipped: binary or unreadable file)


### __pycache__/denoise.cpython-311.pyc

(Skipped: binary or unreadable file)


### __pycache__/diarize.cpython-311.pyc

(Skipped: binary or unreadable file)


### __pycache__/streaming_transcriber.cpython-313.pyc

(Skipped: binary or unreadable file)


### __pycache__/transcriber.cpython-313.pyc

(Skipped: binary or unreadable file)


### __pycache__/whisper_loader.cpython-313.pyc

(Skipped: binary or unreadable file)


### download/__init__.py

```python
from stt.download.whisper import ensure_downloaded

```

### download/__pycache__/__init__.cpython-311.pyc

(Skipped: binary or unreadable file)


### download/__pycache__/__init__.cpython-313.pyc

(Skipped: binary or unreadable file)


### download/__pycache__/whisper.cpython-311.pyc

(Skipped: binary or unreadable file)


### download/__pycache__/whisper.cpython-313.pyc

(Skipped: binary or unreadable file)


### download/whisper.py

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

### hallucination/__init__.py

```python
# transcription/hallucination/__init__.py
from stt.hallucination.repetition import has_repetition
from stt.hallucination.noise import is_noise_phrase, clean_text
from stt.hallucination.confidence import passes_confidence

```

### hallucination/__pycache__/__init__.cpython-311.pyc

(Skipped: binary or unreadable file)


### hallucination/__pycache__/__init__.cpython-313.pyc

(Skipped: binary or unreadable file)


### hallucination/__pycache__/confidence.cpython-311.pyc

(Skipped: binary or unreadable file)


### hallucination/__pycache__/confidence.cpython-313.pyc

(Skipped: binary or unreadable file)


### hallucination/__pycache__/noise.cpython-311.pyc

(Skipped: binary or unreadable file)


### hallucination/__pycache__/noise.cpython-313.pyc

(Skipped: binary or unreadable file)


### hallucination/__pycache__/repetition.cpython-311.pyc

(Skipped: binary or unreadable file)


### hallucination/__pycache__/repetition.cpython-313.pyc

(Skipped: binary or unreadable file)


### hallucination/confidence.py

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

### hallucination/noise.py

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

### hallucination/repetition.py

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

### model/__init__.py

```python
# transcription/model/__init__.py
from stt.model.singleton import get_model, is_loaded, reset
from stt.model.device import resolve_device
from stt.model.lock import infer_lock

```

### model/__pycache__/__init__.cpython-311.pyc

(Skipped: binary or unreadable file)


### model/__pycache__/__init__.cpython-313.pyc

(Skipped: binary or unreadable file)


### model/__pycache__/device.cpython-311.pyc

(Skipped: binary or unreadable file)


### model/__pycache__/device.cpython-313.pyc

(Skipped: binary or unreadable file)


### model/__pycache__/load.cpython-311.pyc

(Skipped: binary or unreadable file)


### model/__pycache__/load.cpython-313.pyc

(Skipped: binary or unreadable file)


### model/__pycache__/lock.cpython-311.pyc

(Skipped: binary or unreadable file)


### model/__pycache__/lock.cpython-313.pyc

(Skipped: binary or unreadable file)


### model/__pycache__/singleton.cpython-311.pyc

(Skipped: binary or unreadable file)


### model/__pycache__/singleton.cpython-313.pyc

(Skipped: binary or unreadable file)


### model/device.py

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

### model/load.py

```python
# transcription/model/load.py
import torch
import whisper
import whisper.model as wm

from config.paths import WHISPER_DIR
from config.whisper import WHISPER_MODEL_NAME
from stt.model.device import resolve_device


def load_whisper(
    model_name: str = WHISPER_MODEL_NAME,
    device: str | None = None,
) -> wm.Whisper:
    """Load Whisper from models/whisper/. Downloads if missing."""
    from stt.download.whisper import ensure_downloaded

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

### model/lock.py

```python
# transcription/model/lock.py
import threading

# Single lock shared by all Whisper callers — GPU is not re-entrant
infer_lock = threading.Lock()

```

### model/singleton.py

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
        from stt.model.load import load_whisper

        _model = load_whisper()
    return _model


def is_loaded() -> bool:
    return _model is not None


def reset():
    global _model
    _model = None

```

### stream/__init__.py

```python
# transcription/stream/__init__.py
from stt.stream.buffer import create_buffer
from stt.stream.worker import start_worker, stop_worker
from stt.stream.final import run_final_pass


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
    from stt.stream.buffer import append

    append(state["buf"], chunk)


def end_of_speech(state: dict) -> str:
    text = run_final_pass(state["buf"])
    state["last_text"] = ""
    if text:
        state["on_final"](text)
    return text


def clear_stream(state: dict) -> None:
    from stt.stream.buffer import clear_buffer

    clear_buffer(state["buf"])
    state["last_text"] = ""

```

### stream/__pycache__/__init__.cpython-311.pyc

(Skipped: binary or unreadable file)


### stream/__pycache__/__init__.cpython-313.pyc

(Skipped: binary or unreadable file)


### stream/__pycache__/buffer.cpython-311.pyc

(Skipped: binary or unreadable file)


### stream/__pycache__/buffer.cpython-313.pyc

(Skipped: binary or unreadable file)


### stream/__pycache__/final.cpython-311.pyc

(Skipped: binary or unreadable file)


### stream/__pycache__/final.cpython-313.pyc

(Skipped: binary or unreadable file)


### stream/__pycache__/partial.cpython-311.pyc

(Skipped: binary or unreadable file)


### stream/__pycache__/partial.cpython-313.pyc

(Skipped: binary or unreadable file)


### stream/__pycache__/worker.cpython-311.pyc

(Skipped: binary or unreadable file)


### stream/__pycache__/worker.cpython-313.pyc

(Skipped: binary or unreadable file)


### stream/buffer.py

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

### stream/final.py

```python
# transcription/stream/final.py
import threading
import numpy as np
import whisper

from stt.model.singleton import get_model
from stt.transcribe.options import build_whisper_options
from stt.hallucination.repetition import has_repetition
from stt.hallucination.noise import clean_text
from stt.hallucination.confidence import passes_confidence
from stt.stream.buffer import get_audio, clear_buffer

from stt.model.lock import infer_lock as _infer_lock


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
    from stt.stream.buffer import create_buffer, append

    buf = create_buffer()
    append(buf, np.zeros(16000, dtype=np.float32))
    print(repr(run_final_pass(buf)))

```

### stream/partial.py

```python
# transcription/stream/partial.py
import threading
import numpy as np
import whisper

from stt.model.singleton import get_model
from stt.transcribe.options import build_whisper_options
from stt.hallucination.repetition import has_repetition
from stt.hallucination.noise import clean_text
from stt.hallucination.confidence import passes_confidence
from config.vad import MIN_AUDIO_SEC

from stt.model.lock import infer_lock as _infer_lock


def run_partial_pass(buf: dict) -> str:
    from stt.stream.buffer import get_audio

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

### stream/worker.py

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
        from stt.stream.partial import run_partial_pass

        text = run_partial_pass(state["buf"])
        if text and text != state["last_text"]:
            state["last_text"] = text
            state["on_partial"](text)
    finally:
        state["is_transcribing"] = False

```

### transcribe/__init__.py

```python
# transcription/transcribe/__init__.py
from stt.transcribe.batch import transcribe_audio
from stt.transcribe.options import build_whisper_options

```

### transcribe/__pycache__/__init__.cpython-311.pyc

(Skipped: binary or unreadable file)


### transcribe/__pycache__/__init__.cpython-313.pyc

(Skipped: binary or unreadable file)


### transcribe/__pycache__/batch.cpython-311.pyc

(Skipped: binary or unreadable file)


### transcribe/__pycache__/batch.cpython-313.pyc

(Skipped: binary or unreadable file)


### transcribe/__pycache__/options.cpython-311.pyc

(Skipped: binary or unreadable file)


### transcribe/__pycache__/options.cpython-313.pyc

(Skipped: binary or unreadable file)


### transcribe/batch.py

```python
# transcription/transcribe/batch.py
import time
import threading

import numpy as np
import whisper

from stt.model.singleton import get_model
from config.whisper import WHISPER_DEVICE

from stt.model.lock import infer_lock as _infer_lock


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

### transcribe/options.py

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

### vad/__init__.py

```python
# transcription/vad/__init__.py
from stt.vad.state import create_vad_state, reset_vad_state
from stt.vad.processor import process_chunk
from stt.vad.energy import is_speech_energy
from stt.vad.silero import is_speech

```

### vad/__pycache__/__init__.cpython-311.pyc

(Skipped: binary or unreadable file)


### vad/__pycache__/__init__.cpython-313.pyc

(Skipped: binary or unreadable file)


### vad/__pycache__/energy.cpython-311.pyc

(Skipped: binary or unreadable file)


### vad/__pycache__/energy.cpython-313.pyc

(Skipped: binary or unreadable file)


### vad/__pycache__/processor.cpython-311.pyc

(Skipped: binary or unreadable file)


### vad/__pycache__/processor.cpython-313.pyc

(Skipped: binary or unreadable file)


### vad/__pycache__/ptt.cpython-311.pyc

(Skipped: binary or unreadable file)


### vad/__pycache__/ptt.cpython-313.pyc

(Skipped: binary or unreadable file)


### vad/__pycache__/session.cpython-311.pyc

(Skipped: binary or unreadable file)


### vad/__pycache__/session.cpython-313.pyc

(Skipped: binary or unreadable file)


### vad/__pycache__/silero.cpython-311.pyc

(Skipped: binary or unreadable file)


### vad/__pycache__/silero.cpython-313.pyc

(Skipped: binary or unreadable file)


### vad/__pycache__/state.cpython-311.pyc

(Skipped: binary or unreadable file)


### vad/__pycache__/state.cpython-313.pyc

(Skipped: binary or unreadable file)


### vad/energy.py

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

### vad/processor.py

```python
# transcription/vad/processor.py
import numpy as np
from config.vad import PAUSE_SECONDS, MIN_SPEECH_SEC
from stt.vad.state import reset_vad_state
from stt.vad.silero import is_speech as _is_speech


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

    from stt.vad.state import create_vad_state

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

### vad/session.py

```python
# transcription/vad/session.py
import numpy as np

from audio.io.mic import open_mic
from audio.transform.resample import resample
from config.vad import RECORD_SAMPLE_RATE, PREROLL_SECONDS
from config.whisper import WHISPER_SAMPLE_RATE
from stt.stream import feed
from stt.vad.processor import process_chunk


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

### vad/silero.py

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

### vad/state.py

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