"""
server.py
Flask app + all routes.
Run via:  python main.py
"""

import os
import time
import tempfile

from flask import Flask, request, jsonify
from flask_cors import CORS

from config import WHISPER_MODEL_NAME
from audio.audio_utils import load_audio_as_array
from transcription.whisper_loader import get_model, is_loaded
from transcription.transcriber import transcribe_audio

# ── Future: uncomment when LLM is ready ───────────────
# from llm.llm import generate_response


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({
            "status":         "ok",
            "whisper_loaded": is_loaded(),
            "whisper_model":  WHISPER_MODEL_NAME,
        })

    @app.route("/transcribe", methods=["POST"])
    def transcribe():
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        f = request.files["file"]
        tmp = os.path.join(tempfile.gettempdir(), f"stt_{int(time.time()*1000)}.wav")
        f.save(tmp)

        try:
            get_model()
            audio = load_audio_as_array(tmp)
            text  = transcribe_audio(audio)
            return jsonify({"text": text})
        except Exception as e:
            import traceback; traceback.print_exc()
            return jsonify({"error": str(e)}), 500
        finally:
            try: os.unlink(tmp)
            except: pass

    # ── Future: LLM chat endpoint ──────────────────────
    # @app.route("/chat", methods=["POST"])
    # def chat():
    #     text = request.json.get("text", "")
    #     reply = generate_response(text)
    #     return jsonify({"reply": reply})

    return app