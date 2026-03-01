"""
Voice Client - VAD based streaming
Sends audio the moment you pause speaking.
"""

import os
import sys
import time
import tempfile
import threading
import queue

import numpy as np
import sounddevice as sd
import soundfile as sf
import requests
import resampy

SERVER = "http://localhost:5001"
RECORD_SAMPLE_RATE = 44100
WHISPER_SAMPLE_RATE = 16000

SILENCE_THRESHOLD = 0.008  # tune this if mic is too sensitive
SILENCE_DURATION  = 0.5    # seconds of silence = end of utterance
MIN_SPEECH        = 0.3    # ignore anything shorter than this


def transcribe_chunk(audio: np.ndarray) -> str:
    audio_16k = resampy.resample(audio, RECORD_SAMPLE_RATE, WHISPER_SAMPLE_RATE)
    tmp = os.path.join(tempfile.gettempdir(), f"chunk_{int(time.time()*1000)}.wav")
    sf.write(tmp, audio_16k, WHISPER_SAMPLE_RATE)
    try:
        with open(tmp, "rb") as f:
            r = requests.post(
                f"{SERVER}/transcribe",
                files={"file": ("audio.wav", f, "audio/wav")},
                timeout=30,
            )
        if r.status_code == 200:
            return r.json().get("text", "").strip()
        return ""
    except Exception as e:
        return f"[error: {e}]"
    finally:
        try: os.unlink(tmp)
        except: pass


def run():
    audio_queue = queue.Queue()
    running = [True]

    # ── background transcription thread ──────────────
    def worker():
        while running[0] or not audio_queue.empty():
            try:
                chunk = audio_queue.get(timeout=0.3)
            except queue.Empty:
                continue
            text = transcribe_chunk(chunk)
            if text:
                print(f"  >>> {text}", flush=True)

    t = threading.Thread(target=worker, daemon=True)
    t.start()

    # ── VAD state ─────────────────────────────────────
    speech_buf   = []
    silence_buf  = []
    in_speech    = False
    silence_need = int(SILENCE_DURATION * RECORD_SAMPLE_RATE)
    speech_need  = int(MIN_SPEECH * RECORD_SAMPLE_RATE)

    def callback(indata, frames, time_info, status):
        nonlocal in_speech, speech_buf, silence_buf
        flat = indata.copy().flatten()
        amp  = float(np.abs(flat).mean())

        if amp > SILENCE_THRESHOLD:
            in_speech = True
            speech_buf.append(flat)
            silence_buf = []
        else:
            if in_speech:
                silence_buf.append(flat)
                speech_buf.append(flat)
                silence_len = sum(len(f) for f in silence_buf)
                if silence_len >= silence_need:
                    audio = np.concatenate(speech_buf)
                    if len(audio) >= speech_need:
                        audio_queue.put(audio.astype(np.float32))
                    speech_buf  = []
                    silence_buf = []
                    in_speech   = False

    stream = sd.InputStream(
        samplerate=RECORD_SAMPLE_RATE,
        channels=1,
        dtype="float32",
        callback=callback,
        blocksize=512,
    )

    stream.start()
    print("🔴 Listening... speak naturally\n   Press ENTER to stop\n", flush=True)
    input()
    stream.stop()
    stream.close()

    if speech_buf:
        audio = np.concatenate(speech_buf)
        if len(audio) >= speech_need:
            audio_queue.put(audio.astype(np.float32))

    running[0] = False
    t.join(timeout=15)


def main():
    print("\n" + "="*50)
    print("  REAL-TIME VOICE TRANSCRIPTION")
    print("="*50)

    try:
        r = requests.get(f"{SERVER}/health", timeout=3)
        d = r.json()
        print(f"Server OK | Whisper: {d['whisper_model']}")
    except Exception as e:
        print(f"Cannot reach server: {e}")
        sys.exit(1)

    print("\nCtrl+C to quit\n")

    try:
        while True:
            input("[ Press ENTER to start listening ]")
            print()
            run()
            print()
    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == "__main__":
    main()