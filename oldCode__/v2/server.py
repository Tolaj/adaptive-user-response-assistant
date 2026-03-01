"""
Voice Server - Step 1
Endpoints:
  POST /transcribe  - audio file -> text
  GET  /health      - status check
"""

import os
import tempfile
import time
import threading
from pathlib import Path

import torch
import numpy as np
import whisper
from flask import Flask, request, jsonify
from flask_cors import CORS

from config import *

app = Flask(__name__)
CORS(app)

# ── GLOBALS ────────────────────────────────────────────
WHISPER_MODEL = None
whisper_lock = threading.Lock()


# ── LOAD WHISPER ───────────────────────────────────────
def load_whisper():
    global WHISPER_MODEL
    if WHISPER_MODEL is not None:
        return
    print(f"Loading Whisper ({WHISPER_MODEL_NAME}) from {WHISPER_MODEL_PATH} ...")
    checkpoint = torch.load(str(WHISPER_MODEL_PATH), map_location="cpu")
    dims = whisper.model.ModelDimensions(**checkpoint["dims"])
    model = whisper.model.Whisper(dims)
    model.load_state_dict(checkpoint["model_state_dict"])
    model = model.to(WHISPER_DEVICE)
    WHISPER_MODEL = model
    print(f"Whisper ready on {WHISPER_DEVICE}.")


# ── AUDIO LOADING ──────────────────────────────────────
def load_audio_as_array(path: str) -> np.ndarray:
    """
    Load a WAV file and return a 16kHz float32 mono numpy array.
    Uses soundfile + resampy, no ffmpeg needed.
    """
    import soundfile as sf
    import resampy

    audio, sr = sf.read(path)

    # Mono
    if len(audio.shape) > 1:
        audio = audio.mean(axis=1)

    audio = audio.astype(np.float32)

    # Resample to 16kHz
    if sr != WHISPER_SAMPLE_RATE:
        audio = resampy.resample(audio, sr, WHISPER_SAMPLE_RATE)

    return audio


# ── ROUTES ─────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "whisper_loaded": WHISPER_MODEL is not None,
        "whisper_model": WHISPER_MODEL_NAME,
    })


@app.route("/transcribe", methods=["POST"])
def transcribe():
    """Receive a WAV file, return transcribed text."""
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    f = request.files["file"]

    # Save to temp WAV
    tmp_path = os.path.join(tempfile.gettempdir(), f"stt_{int(time.time()*1000)}.wav")
    f.save(tmp_path)

    try:
        load_whisper()
        audio = load_audio_as_array(tmp_path)
        t0 = time.time()

        print(f"Transcribing: {len(audio)/WHISPER_SAMPLE_RATE:.1f}s of audio ...", flush=True)

        with whisper_lock:
            result = whisper.transcribe(
                WHISPER_MODEL,
                audio,
                language="en",
                fp16=(WHISPER_DEVICE == "cuda"),
                temperature=0,
                condition_on_previous_text=False,
            )
        text = result["text"].strip()
        print(f"Result: '{text}' ({time.time()-t0:.2f}s)", flush=True)

        return jsonify({"text": text})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

    finally:
        try:
            os.unlink(tmp_path)
        except:
            pass


# ── MAIN ───────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("VOICE SERVER - Step 1 (transcription only)")
    print("=" * 50)
    print(f"POST http://localhost:{SERVER_PORT}/transcribe")
    print(f"GET  http://localhost:{SERVER_PORT}/health")
    print("=" * 50)

    # Pre-load whisper so first request is fast
    try:
        load_whisper()
    except Exception as e:
        print(f"WARNING: Could not pre-load Whisper: {e}")

    app.run(host="0.0.0.0", port=SERVER_PORT, debug=False, threaded=True)