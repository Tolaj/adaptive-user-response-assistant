# PromptPack Output

**Root:** `/Users/swapnil/Documents/Projects/adaptive-user-response-assistant/audio`
**Generated:** 2026-04-09T05:37:25.417Z

---

## 1) Folder Structure

```txt
.
├─ __init__.py
├─ __pycache__/
│  ├─ __init__.cpython-311.pyc
│  ├─ __init__.cpython-313.pyc
│  └─ audio_utils.cpython-313.pyc
├─ gate/
│  ├─ __init__.py
│  ├─ __pycache__/
│  │  ├─ __init__.cpython-311.pyc
│  │  ├─ __init__.cpython-313.pyc
│  │  ├─ amplitude.cpython-311.pyc
│  │  ├─ amplitude.cpython-313.pyc
│  │  ├─ rms.cpython-311.pyc
│  │  ├─ rms.cpython-313.pyc
│  │  ├─ zcr.cpython-311.pyc
│  │  └─ zcr.cpython-313.pyc
│  ├─ amplitude.py
│  ├─ rms.py
│  └─ zcr.py
├─ io/
│  ├─ __init__.py
│  ├─ __pycache__/
│  │  ├─ __init__.cpython-311.pyc
│  │  ├─ __init__.cpython-313.pyc
│  │  ├─ mic.cpython-311.pyc
│  │  ├─ mic.cpython-313.pyc
│  │  ├─ read.cpython-311.pyc
│  │  ├─ read.cpython-313.pyc
│  │  ├─ write.cpython-311.pyc
│  │  └─ write.cpython-313.pyc
│  ├─ mic.py
│  ├─ read.py
│  └─ write.py
└─ transform/
   ├─ __init__.py
   ├─ __pycache__/
   │  ├─ __init__.cpython-311.pyc
   │  ├─ __init__.cpython-313.pyc
   │  ├─ denoise.cpython-311.pyc
   │  ├─ mono.cpython-311.pyc
   │  ├─ mono.cpython-313.pyc
   │  ├─ normalise.cpython-311.pyc
   │  ├─ normalise.cpython-313.pyc
   │  ├─ resample.cpython-311.pyc
   │  └─ resample.cpython-313.pyc
   ├─ denoise.py
   ├─ mono.py
   ├─ normalise.py
   └─ resample.py
```

<!-- PAGE BREAK: FILE CONTENTS BELOW -->

## 2) File Contents


### __init__.py

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

### __pycache__/__init__.cpython-311.pyc

(Skipped: binary or unreadable file)


### __pycache__/__init__.cpython-313.pyc

(Skipped: binary or unreadable file)


### __pycache__/audio_utils.cpython-313.pyc

(Skipped: binary or unreadable file)


### gate/__init__.py

```python
# audio/gate/__init__.py

from audio.gate.rms import rms
from audio.gate.amplitude import mean_amplitude
from audio.gate.zcr import zero_crossing_rate

```

### gate/__pycache__/__init__.cpython-311.pyc

(Skipped: binary or unreadable file)


### gate/__pycache__/__init__.cpython-313.pyc

(Skipped: binary or unreadable file)


### gate/__pycache__/amplitude.cpython-311.pyc

(Skipped: binary or unreadable file)


### gate/__pycache__/amplitude.cpython-313.pyc

(Skipped: binary or unreadable file)


### gate/__pycache__/rms.cpython-311.pyc

(Skipped: binary or unreadable file)


### gate/__pycache__/rms.cpython-313.pyc

(Skipped: binary or unreadable file)


### gate/__pycache__/zcr.cpython-311.pyc

(Skipped: binary or unreadable file)


### gate/__pycache__/zcr.cpython-313.pyc

(Skipped: binary or unreadable file)


### gate/amplitude.py

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

### gate/rms.py

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

### gate/zcr.py

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

### io/__init__.py

```python
from audio.io.read import read_wav
from audio.io.write import write_wav
from audio.io.mic import open_mic

```

### io/__pycache__/__init__.cpython-311.pyc

(Skipped: binary or unreadable file)


### io/__pycache__/__init__.cpython-313.pyc

(Skipped: binary or unreadable file)


### io/__pycache__/mic.cpython-311.pyc

(Skipped: binary or unreadable file)


### io/__pycache__/mic.cpython-313.pyc

(Skipped: binary or unreadable file)


### io/__pycache__/read.cpython-311.pyc

(Skipped: binary or unreadable file)


### io/__pycache__/read.cpython-313.pyc

(Skipped: binary or unreadable file)


### io/__pycache__/write.cpython-311.pyc

(Skipped: binary or unreadable file)


### io/__pycache__/write.cpython-313.pyc

(Skipped: binary or unreadable file)


### io/mic.py

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

### io/read.py

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

### io/write.py

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

### transform/__init__.py

```python
# audio/transform/__init__.py
from audio.transform.mono import to_mono
from audio.transform.resample import resample
from audio.transform.normalise import normalise

```

### transform/__pycache__/__init__.cpython-311.pyc

(Skipped: binary or unreadable file)


### transform/__pycache__/__init__.cpython-313.pyc

(Skipped: binary or unreadable file)


### transform/__pycache__/denoise.cpython-311.pyc

(Skipped: binary or unreadable file)


### transform/__pycache__/mono.cpython-311.pyc

(Skipped: binary or unreadable file)


### transform/__pycache__/mono.cpython-313.pyc

(Skipped: binary or unreadable file)


### transform/__pycache__/normalise.cpython-311.pyc

(Skipped: binary or unreadable file)


### transform/__pycache__/normalise.cpython-313.pyc

(Skipped: binary or unreadable file)


### transform/__pycache__/resample.cpython-311.pyc

(Skipped: binary or unreadable file)


### transform/__pycache__/resample.cpython-313.pyc

(Skipped: binary or unreadable file)


### transform/denoise.py

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

### transform/mono.py

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

### transform/normalise.py

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

### transform/resample.py

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