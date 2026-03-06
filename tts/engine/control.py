# tts/engine/control.py
import threading


def interrupt(engine: dict) -> None:
    engine["interrupted"].set()
    _drain(engine)
    from tts.playback.stop import stop_audio

    stop_audio()


def resume(engine: dict) -> None:
    engine["token_buf"] = ""
    engine["interrupted"].clear()


def speak_filler(engine: dict) -> None:
    """
    Play a cached filler non-blocking.

    Selection strategy: pick the shortest filler whose measured duration is
    >= the rolling LLM first-token estimate. This means:
      - Filler ends at roughly the same time the first LLM token arrives
      - No silent gap, no unnecessary extra wait
      - Falls back to longest available if all fillers are shorter than estimate

    Uses engine["last_llm_first_token_ms"] (EMA updated by record_llm_latency).
    """
    from config.tts import ENABLE_FILLER

    if not ENABLE_FILLER:
        return

    cached = engine["filler_audio"]
    durations = engine["filler_durations_ms"]

    if not cached:
        return  # warmup not done yet — skip

    target_ms = engine.get("last_llm_first_token_ms", 1800.0)

    # Find all fillers that cover the target (duration >= target)
    covering = {t: d for t, d in durations.items() if t in cached and d >= target_ms}

    if covering:
        # Pick the shortest one that still covers — minimises unnecessary wait
        text = min(covering, key=covering.get)
    else:
        # All fillers are shorter than LLM latency — pick the longest available
        text = max((t for t in cached), key=lambda t: durations.get(t, 0))

    audio = cached[text]
    engine["speaking"].set()

    def _play():
        try:
            from tts.playback.stream import play_audio
            from tts.model.singleton import get_model

            play_audio(audio, get_model()["sample_rate"])
        finally:
            engine["speaking"].clear()

    # Non-blocking — caller returns immediately, LLM starts streaming in parallel
    threading.Thread(target=_play, daemon=True).start()


def record_llm_latency(engine: dict, first_token_ms: float) -> None:
    """
    Update the rolling EMA of LLM first-token latency after each response.
    alpha=0.25: slow enough to smooth spikes, fast enough to track trends.
    speak_filler() uses this to pick the right filler duration next time.
    """
    prev = engine.get("last_llm_first_token_ms", first_token_ms)
    engine["last_llm_first_token_ms"] = 0.75 * prev + 0.25 * first_token_ms


def _drain(engine: dict) -> None:
    while not engine["queue"].empty():
        try:
            engine["queue"].get_nowait()
        except Exception:
            break
