# tts/engine/worker.py
import threading
import time

MERGE_WINDOW_SEC = 0.05


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

    model = get_model()  # warm up in worker thread

    while True:
        item = engine["queue"].get()
        priority, _, text = item
        if text is None:
            break

        if engine["interrupted"].is_set():
            continue

        collected = [text]
        if priority > 0:
            deadline = time.time() + MERGE_WINDOW_SEC
            while time.time() < deadline:
                try:
                    nxt = engine["queue"].get_nowait()
                    if nxt[0] == 0:
                        engine["queue"].put(nxt)
                        break
                    collected.append(nxt[2])
                except Exception:
                    time.sleep(0.005)
        if engine["interrupted"].is_set():
            continue

        merged = " ".join(clean_markdown(c) for c in collected if c.strip())
        if not merged:
            continue

        engine["speaking"].set()
        try:
            audio = generate_one(
                merged,
                voice=engine["voice"],
                speed=engine["speed"],
                steps=engine["steps"],
                language=engine["language"],
            )
            play_audio(audio, model["sample_rate"])
        except Exception as e:
            print(f"[TTS Engine] {e}")
        finally:
            engine["speaking"].clear()
