from flask import Flask
from flask_cors import CORS
from flask_sock import Sock

from server.routes.health import health_handler
from server.routes.transcribe import transcribe_handler
from server.routes.websocket import register_ws


def create_app() -> Flask:
    app = Flask(__name__)
    sock = Sock(app)
    CORS(app)
    app.add_url_rule("/health", "health", health_handler, methods=["GET"])
    app.add_url_rule("/transcribe", "transcribe", transcribe_handler, methods=["POST"])
    register_ws(sock)
    return app
