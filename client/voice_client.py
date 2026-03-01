"""
client/voice_client.py
Microphone → VAD → server → printed transcript.
Run directly:  python -m client.voice_client
"""

import os
import sys
import time
import tempfile
import threading
import queue

import numpy as np
import sounddevice as sd
import requests
import resampy

from config import RECORD_SAMPLE_RATE, WHISPER_SAMPLE_RATE
from audio.audio_utils import numpy_to_wav
from client.vad import VADProcessor

SERVER = "http://localhost:5001"


# ── Networking ────────────────────────────────────────────────────────────────

def transcribe_chunk(audio: np.ndarray) -> str:
    """Resample, write WAV, POST to /transcribe, return text."""
    audio_16k = resampy.resample(audio, RECORD_SAMPLE_RATE, WHISPER_SAMPLE_RATE)
    tmp = os.path.join(tempfile.gettempdir(), f"chunk_{int(time.time() * 1000)}.wav")
    numpy_to_wav(audio_16k, tmp, WHISPER_SAMPLE_RATE)
    try:
        with open(tmp, "rb") as f:
            r = requests.post(
                f"{SERVER}/transcribe",
                files={"file": ("audio.wav", f, "audio/wav")},
                timeout=30,
            )
        if r.status_code == 200:
            return r.json().get("text", "").strip()
        return f"[server error {r.status_code}]"
    except Exception as e:
        return f"[network error: {e}]"
    finally:
        try:
            os.unlink(tmp)
        except OSError:
            pass


# ── Recording session ─────────────────────────────────────────────────────────

def run_session() -> None:
    """
    Open the microphone, run VAD, send speech chunks to the server,
    and print transcriptions until the user presses ENTER.
    """
    audio_queue: queue.Queue[np.ndarray] = queue.Queue()
    running = [True]

    # Worker thread: drains the queue and calls the server
    def worker():
        while running[0] or not audio_queue.empty():
            try:
                chunk = audio_queue.get(timeout=0.3)
            except queue.Empty:
                continue
            text = transcribe_chunk(chunk)
            if text:
                print(f"  >>> {text}", flush=True)

    worker_thread = threading.Thread(target=worker, daemon=True)
    worker_thread.start()

    # VAD: puts complete utterances onto the queue
    vad = VADProcessor(on_speech_end=audio_queue.put)

    def audio_callback(indata, frames, time_info, status):
        vad.process_chunk(indata.copy())

    stream = sd.InputStream(
        samplerate=RECORD_SAMPLE_RATE,
        channels=1,
        dtype="float32",
        callback=audio_callback,
        blocksize=512,
    )

    stream.start()
    print("🔴 Listening... speak naturally\n   Press ENTER to stop\n", flush=True)
    input()
    stream.stop()
    stream.close()

    # Flush any trailing speech
    vad.flush()

    running[0] = False
    worker_thread.join(timeout=15)


# ── Entry point ───────────────────────────────────────────────────────────────

def check_server() -> None:
    try:
        r = requests.get(f"{SERVER}/health", timeout=3)
        d = r.json()
        print(f"Server OK | Whisper: {d['whisper_model']}")
    except Exception as e:
        print(f"Cannot reach server: {e}")
        sys.exit(1)


def main() -> None:
    print("\n" + "=" * 50)
    print("  REAL-TIME VOICE TRANSCRIPTION")
    print("=" * 50)
    check_server()
    print("\nCtrl+C to quit\n")
    try:
        while True:
            input("[ Press ENTER to start listening ]")
            print()
            run_session()
            print()
    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == "__main__":
    main()