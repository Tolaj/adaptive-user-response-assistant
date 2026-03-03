from server.logger import log_event, close_logger


def teardown_session(session: dict) -> None:
    t = session.get("transcriber")
    if t:
        from transcription.stream import stop_stream

        stop_stream(t)
    tts = session.get("tts")
    if tts:
        from tts.engine.status import shutdown

        shutdown(tts)
    log_event(session["logger"], "Client disconnected")
    close_logger(session["logger"])
