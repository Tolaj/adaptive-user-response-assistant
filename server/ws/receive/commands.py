from server.ws.send.core import send
from server.logger import log_event


def handle_end_of_speech(session: dict, trigger_eos_fn) -> None:
    trigger_eos_fn()


def handle_clear_history(session: dict, ws) -> None:
    from llm.history.clear import clear_history

    clear_history(session["history"])
    log_event(session["logger"], "History cleared")
    send(ws, {"type": "pong"})


def handle_ping(ws) -> None:
    send(ws, {"type": "pong"})
