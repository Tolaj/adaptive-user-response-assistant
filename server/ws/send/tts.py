from server.ws.send.core import send


def send_tts_start(ws) -> None:
    send(ws, {"type": "tts_start"})


def send_tts_done(ws) -> None:
    send(ws, {"type": "tts_done"})
