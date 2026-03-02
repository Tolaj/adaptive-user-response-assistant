import json


def send(ws, obj: dict) -> None:
    """Single write point for all outbound WebSocket messages."""
    try:
        ws.send(json.dumps(obj))
    except Exception:
        pass
