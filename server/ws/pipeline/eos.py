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
