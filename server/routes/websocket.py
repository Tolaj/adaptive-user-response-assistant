from server.ws.handler import handle_ws


def register_ws(sock, path: str = "/ws/transcribe"):
    @sock.route(path)
    def ws_transcribe(ws):
        handle_ws(ws)
