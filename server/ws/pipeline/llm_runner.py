import time
import threading

from config.features import ENABLE_TTS, SHOW_TEXT
from config.tts import TTS_MODE
from llm.inference.stream import stream_response
from server.ws.send.llm import send_llm_start, send_llm_token, send_llm_done
from server.ws.send.tts import send_tts_start, send_tts_done
from server.logger import log_request


def run_llm(user_text: str, t_eos: float, session: dict, ws) -> None:
    """Run LLM + feed TTS. Intended to run in a daemon thread."""
    if not user_text.strip():
        return

    t_start = time.time()
    whisper_lat = t_start - t_eos
    first_token_t = None
    first_token = True
    full = ""
    tts = session.get("tts")

    if SHOW_TEXT:
        send_llm_start(ws)
    if tts:
        send_tts_start(ws)

    try:
        for token in stream_response(user_text, session["history"]):
            if first_token:
                first_token_t = time.time() - t_start
                first_token = False
            full += token
            if SHOW_TEXT:
                send_llm_token(ws, token)
            if tts:
                from tts.engine.feed import feed_token

                feed_token(tts, token)
    finally:
        if tts:
            from tts.engine.feed import flush

            flush(tts)
        t_done = time.time()
        llm_total = t_done - t_start
        log_request(
            session["logger"],
            user_text=user_text,
            ai_response=full,
            whisper_latency=whisper_lat,
            llm_first_token=first_token_t or llm_total,
            llm_total=llm_total,
            end_to_end=t_done - t_eos,
        )
        if SHOW_TEXT:
            send_llm_done(ws, full)
        if tts:
            send_tts_done(ws)
