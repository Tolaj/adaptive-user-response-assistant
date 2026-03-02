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
