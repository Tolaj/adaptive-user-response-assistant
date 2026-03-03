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
