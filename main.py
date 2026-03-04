"""
main.py — Single entry point. Behaviour controlled by config/features.py MODE.
"""

import time
from config.features import MODE
from server.logger import create_logger, log_request


def main():
    print(f"\n  MODE: {MODE}\n")

    if MODE == "server":
        _run_server()
    elif MODE == "stt_only":
        _run_stt_only()
    elif MODE == "tts_only":
        _run_tts_only()
    elif MODE == "text_to_text_chat":
        _run_text_chat()
    elif MODE == "voice_to_text_chat":
        _run_voice_chat()
    elif MODE == "full":
        _run_full()
    else:
        print(f"  Unknown MODE '{MODE}'. Check config/features.py")


# ── Modes ──────────────────────────────────────────────────────


def _run_server():
    from config.server import SERVER_HOST, SERVER_PORT
    from config.features import ENABLE_STT
    from server.app import create_app

    print(f"  Starting server on {SERVER_HOST}:{SERVER_PORT}")
    if ENABLE_STT:
        from transcription.model.singleton import get_model

        get_model()
    create_app().run(host=SERVER_HOST, port=SERVER_PORT, debug=False, threaded=True)


def _run_stt_only():
    from transcription.model.singleton import get_model
    from transcription.stream import create_stream, start_stream, end_of_speech
    from transcription.vad.state import create_vad_state, reset_vad_state
    from config.vad import RECORD_SAMPLE_RATE
    from transcription.vad.session import run_mic_session
    from ui.console import show_partial, show_speaking, show_stt_final

    print("  Loading Whisper...")
    get_model()
    print("  Ready.\n")

    logger = create_logger()

    def on_partial(t):
        show_partial(t)

    transcriber = create_stream(on_partial=on_partial, on_final=lambda t: None)
    start_stream(transcriber)

    vad_state = create_vad_state(sample_rate=RECORD_SAMPLE_RATE)

    def on_speech_start():
        show_speaking()

    def on_speech_end():
        t_start = time.time()
        text = end_of_speech(transcriber)
        whisper_latency = time.time() - t_start
        if text:
            show_stt_final(text)
            log_request(logger, text, "", whisper_latency, 0.0, 0.0, whisper_latency)
        reset_vad_state(vad_state)

    run_mic_session(
        transcriber=transcriber,
        vad_state=vad_state,
        on_speech_start=on_speech_start,
        on_speech_end=on_speech_end,
    )


def _run_tts_only():
    from config.tts import (
        SUPERTONIC_VOICE,
        SUPERTONIC_SPEED,
        SUPERTONIC_STEPS,
        SUPERTONIC_LANGUAGE,
    )
    from tts.engine.state import create_engine
    from tts.engine.worker import start_worker
    from tts.engine.feed import feed_token, flush
    from tts.engine.status import shutdown
    from tts.model.singleton import get_model as get_tts_model
    from ui.console import prompt_you

    print("  Loading TTS model [Supertonic]...")
    engine = create_engine(
        voice=SUPERTONIC_VOICE,
        speed=SUPERTONIC_SPEED,
        steps=SUPERTONIC_STEPS,
        language=SUPERTONIC_LANGUAGE,
    )
    start_worker(engine)
    get_tts_model()  # Pre-warm the model before showing "Ready"
    print("  Ready. Type text to speak. Empty line to quit.\n")

    logger = create_logger()
    try:
        while True:
            prompt_you()
            text = input().strip()
            if not text:
                break
            t_start = time.time()
            for word in text.split():
                feed_token(engine, word + " ")
            flush(engine)
            tts_latency = time.time() - t_start
            log_request(logger, text, "", 0.0, 0.0, tts_latency, tts_latency)
    finally:
        shutdown(engine)


def _run_text_chat():
    from llm.model.singleton import get_model
    from llm.inference.stream import stream_response
    from llm.history.state import create_history
    from ui.console import prompt_you

    print("  Loading LLM...")
    get_model()
    print("  Ready. Type to chat. Empty line to quit.\n")

    logger = create_logger()
    history = create_history()
    while True:
        prompt_you()
        user_text = input().strip()
        if not user_text:
            break
        t_start = time.time()
        print("  AI : ", end="", flush=True)
        ai_response = ""
        first_token_time = None
        for token in stream_response(user_text, history):
            if first_token_time is None:
                first_token_time = time.time() - t_start
            print(token, end="", flush=True)
            ai_response += token
        print()
        llm_total = time.time() - t_start
        llm_first_token = first_token_time if first_token_time else llm_total
        log_request(
            logger, user_text, ai_response, 0.0, llm_first_token, llm_total, llm_total
        )


def _run_voice_chat():
    from llm.model.singleton import get_model
    from llm.inference.stream import stream_response
    from llm.history.state import create_history
    from transcription.model.singleton import get_model as load_whisper
    from transcription.stream import create_stream, start_stream, end_of_speech
    from transcription.vad.state import create_vad_state, reset_vad_state
    from config.vad import RECORD_SAMPLE_RATE
    from transcription.vad.session import run_mic_session
    from ui.console import show_partial, show_speaking, show_you, start_ai_line
    import threading

    print("  Loading Whisper + LLM...")
    load_whisper()
    get_model()
    print("  Ready.\n")

    logger = create_logger()
    history = create_history()
    lock = threading.Lock()
    vad_state = create_vad_state(sample_rate=RECORD_SAMPLE_RATE)

    def on_partial(t):
        show_partial(t)

    transcriber = create_stream(on_partial=on_partial, on_final=lambda t: None)
    start_stream(transcriber)

    def on_speech_start():
        show_speaking()

    def on_speech_end():
        if not lock.acquire(blocking=False):
            return
        reset_vad_state(vad_state)

        def _run():
            try:
                e2e_start = time.time()
                whisper_start = time.time()
                text = end_of_speech(transcriber)
                whisper_latency = time.time() - whisper_start
                if not text:
                    lock.release()
                    return
                show_you(text)
                start_ai_line()
                llm_start = time.time()
                ai_response = ""
                first_token_time = None
                for token in stream_response(text, history):
                    if first_token_time is None:
                        first_token_time = time.time() - llm_start
                    print(token, end="", flush=True)
                    ai_response += token
                print()
                llm_total = time.time() - llm_start
                llm_first_token = first_token_time if first_token_time else llm_total
                e2e_total = time.time() - e2e_start
                log_request(
                    logger,
                    text,
                    ai_response,
                    whisper_latency,
                    llm_first_token,
                    llm_total,
                    e2e_total,
                )
            finally:
                lock.release()

        threading.Thread(target=_run, daemon=True).start()

    run_mic_session(
        transcriber=transcriber,
        vad_state=vad_state,
        on_speech_start=on_speech_start,
        on_speech_end=on_speech_end,
    )


def _run_full():
    from config.tts import (
        SUPERTONIC_VOICE,
        SUPERTONIC_SPEED,
        SUPERTONIC_STEPS,
        SUPERTONIC_LANGUAGE,
    )
    from llm.model.singleton import get_model
    from llm.inference.stream import stream_response
    from llm.history.state import create_history
    from transcription.model.singleton import get_model as load_whisper
    from transcription.stream import create_stream, start_stream, end_of_speech
    from transcription.vad.state import create_vad_state, reset_vad_state
    from transcription.vad.session import run_mic_session
    from tts.engine.state import create_engine
    from tts.engine.worker import start_worker
    from tts.engine.feed import feed_token, flush as tts_flush
    from tts.engine.control import interrupt, resume, speak_filler
    from tts.engine.status import is_speaking, shutdown
    from config.vad import RECORD_SAMPLE_RATE
    from ui.console import show_partial, show_speaking, show_you, start_ai_line
    import threading

    print("  Loading all models...")
    load_whisper()
    get_model()
    engine = create_engine(
        voice=SUPERTONIC_VOICE,
        speed=SUPERTONIC_SPEED,
        steps=SUPERTONIC_STEPS,
        language=SUPERTONIC_LANGUAGE,
    )
    start_worker(engine)
    print("  All ready.\n")

    logger = create_logger()
    history = create_history()
    lock = threading.Lock()
    vad_state = create_vad_state(sample_rate=RECORD_SAMPLE_RATE)

    def on_partial(t):
        show_partial(t)

    transcriber = create_stream(on_partial=on_partial, on_final=lambda t: None)
    start_stream(transcriber)

    def on_speech_start():
        interrupt(engine)
        show_speaking()

    def on_speech_end():
        if not lock.acquire(blocking=False):
            return
        reset_vad_state(vad_state)

        def _run():
            try:
                e2e_start = time.time()
                whisper_start = time.time()
                text = end_of_speech(transcriber)
                whisper_latency = time.time() - whisper_start
                if not text:
                    return
                show_you(text)
                resume(engine)
                speak_filler(engine)
                start_ai_line()
                llm_start = time.time()
                ai_response = ""
                first_token_time = None
                for token in stream_response(text, history):
                    if first_token_time is None:
                        first_token_time = time.time() - llm_start
                    print(token, end="", flush=True)
                    ai_response += token
                    feed_token(engine, token)
                tts_flush(engine)
                print()
                llm_total = time.time() - llm_start
                llm_first_token = first_token_time if first_token_time else llm_total
                e2e_total = time.time() - e2e_start
                log_request(
                    logger,
                    text,
                    ai_response,
                    whisper_latency,
                    llm_first_token,
                    llm_total,
                    e2e_total,
                )
            finally:
                lock.release()

        threading.Thread(target=_run, daemon=True).start()

    run_mic_session(
        transcriber=transcriber,
        vad_state=vad_state,
        on_speech_start=on_speech_start,
        on_speech_end=on_speech_end,
        should_process_chunk=lambda: not is_speaking(engine),
    )
    shutdown(engine)


if __name__ == "__main__":
    main()
