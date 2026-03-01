"""
client/tts_player.py

Client-side TTS — Supertonic 2 only.
"""

from client.supertonic_player import SupertonicPlayer


def create_tts_player() -> SupertonicPlayer:
    return SupertonicPlayer()
