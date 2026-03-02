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
