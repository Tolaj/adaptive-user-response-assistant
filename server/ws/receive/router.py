import json


def route_message(message, session: dict, ws, trigger_eos_fn) -> None:
    """Dispatch incoming WebSocket frame to the correct handler."""
    if isinstance(message, bytes) and len(message) >= 4:
        from server.ws.receive.audio import handle_audio_frame

        handle_audio_frame(message, session, trigger_eos_fn)
        return
    if isinstance(message, str):
        try:
            msg = json.loads(message)
        except Exception:
            return
        t = msg.get("type")
        if t == "end_of_speech":
            from server.ws.receive.commands import handle_end_of_speech

            handle_end_of_speech(session, trigger_eos_fn)
        elif t == "clear_history":
            from server.ws.receive.commands import handle_clear_history

            handle_clear_history(session, ws)
        elif t == "ping":
            from server.ws.receive.commands import handle_ping

            handle_ping(ws)
