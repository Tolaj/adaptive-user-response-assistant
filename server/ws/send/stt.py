from server.ws.send.core import send


def send_partial(ws, text: str) -> None:
    send(ws, {"type": "partial", "text": text})


def send_final(ws, text: str) -> None:
    send(ws, {"type": "final", "text": text})
