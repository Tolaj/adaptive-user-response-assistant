from config.features import ENABLE_STT
from transcription.model.singleton import get_model as get_whisper
from llm.model.singleton import get_model as get_llm
from server.ws.session.create import create_session
from server.ws.session.teardown import teardown_session
from server.ws.receive.router import route_message
from server.ws.pipeline.eos import trigger_eos
from server.ws.send.core import send
from server.logger import log_event


def handle_ws(ws) -> None:
    """Main WebSocket loop — orchestrates all modules, owns no logic itself."""
    session = create_session()
    log_event(session["logger"], "Client connected")

    if ENABLE_STT:
        get_whisper()
    get_llm()

    if ENABLE_STT:
        from transcription.stream import create_stream, start_stream
        from server.ws.send.stt import send_partial

        session["transcriber"] = create_stream(
            on_partial=lambda text: send_partial(ws, text),
            on_final=lambda text: None,
        )
        start_stream(session["transcriber"])

    def _eos():
        trigger_eos(session, ws)

    try:
        while True:
            msg = ws.receive()
            if msg is None:
                break
            route_message(msg, session, ws, _eos)
    except Exception as e:
        print(f"[WS] {e}")
        send(ws, {"type": "error", "message": str(e)})
    finally:
        teardown_session(session)
