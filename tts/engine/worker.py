# tts/engine/worker.py
"""
Pipelined TTS worker.

Generator thread: text queue → generate_one() → audio_queue
Player thread:    audio_queue → play_audio()

While chunk N is playing, chunk N+1 is already being generated.
Eliminates the inter-chunk silence that caused "stuck between words".
"""
import threading
import time
import queue as _queue
from config.tts import MERGE_WINDOW_SEC


def start_worker(engine: dict) -> None:
    engine["running"] = True
    t = threading.Thread(target=_loop, args=(engine,), daemon=True)
    t.start()
    engine["worker_thread"] = t


def _loop(engine: dict) -> None:
    from tts.generate.pipeline import generate_one
    from tts.playback.stream import play_audio
    from tts.text.clean import clean_markdown
    from tts.model.singleton import get_model
    from tts.engine.state import warm_fillers

    model = get_model()
    warm_fillers(engine)
    sr = model["sample_rate"]

    # maxsize=2: current + 1 lookahead. Blocks generator if player falls behind.
    audio_queue: _queue.Queue = _queue.Queue(maxsize=2)

    def _player():
        while True:
            item = audio_queue.get()
            if item is None:
                break
            engine["speaking"].set()
            try:
                play_audio(item, sr)
            except Exception as e:
                print(f"[TTS Player] {e}")
            finally:
                if audio_queue.empty():
                    engine["speaking"].clear()

    player = threading.Thread(target=_player, daemon=True)
    player.start()

    is_first = True

    try:
        while True:
            item = engine["queue"].get()
            priority, _, text = item
            if text is None:
                break

            if engine["interrupted"].is_set():
                while not audio_queue.empty():
                    try:
                        audio_queue.get_nowait()
                    except Exception:
                        pass
                engine["speaking"].clear()
                is_first = True
                continue

            collected = [text]
            if not is_first and priority > 0:
                deadline = time.time() + MERGE_WINDOW_SEC
                while time.time() < deadline:
                    try:
                        nxt = engine["queue"].get_nowait()
                        if nxt[0] == 0:
                            engine["queue"].put(nxt)
                            break
                        collected.append(nxt[2])
                    except Exception:
                        time.sleep(0.003)

            if engine["interrupted"].is_set():
                is_first = True
                continue

            merged = " ".join(clean_markdown(c) for c in collected if c and c.strip())
            if not merged:
                continue

            is_first = False
            try:
                audio = generate_one(
                    merged,
                    voice=engine["voice"],
                    speed=engine["speed"],
                    steps=engine["steps"],
                    language=engine["language"],
                )
                audio_queue.put(audio)  # blocks if player is 2 chunks behind
            except Exception as e:
                print(f"[TTS Generator] {e}")

            if engine["queue"].empty():
                is_first = True

    finally:
        audio_queue.put(None)
        player.join(timeout=5)
