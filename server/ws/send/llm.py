from server.ws.send.core import send


def send_llm_start(ws) -> None:
    send(ws, {"type": "llm_start"})


def send_llm_token(ws, token: str) -> None:
    send(ws, {"type": "llm_token", "text": token})


def send_llm_done(ws, full: str) -> None:
    send(ws, {"type": "llm_done", "text": full})
