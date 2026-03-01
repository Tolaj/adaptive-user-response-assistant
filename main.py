"""
main.py
Server entry point.  Run:  python main.py
"""

from config import SERVER_PORT
from server import create_app
from transcription.whisper_loader import get_model

if __name__ == "__main__":
    print("=" * 50)
    print("  VOICE AI SERVER")
    print("=" * 50)
    print(f"POST http://localhost:{SERVER_PORT}/transcribe")
    print(f"GET  http://localhost:{SERVER_PORT}/health")
    print("=" * 50)

    # Pre-warm Whisper so the first request is instant
    try:
        get_model()
    except Exception as e:
        print(f"WARNING: Could not pre-load Whisper: {e}")

    app = create_app()
    app.run(host="0.0.0.0", port=SERVER_PORT, debug=False, threaded=True)