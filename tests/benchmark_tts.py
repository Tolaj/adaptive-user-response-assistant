"""
tests/benchmark_tts.py
======================
Full end-to-end pipeline benchmark: WAV → Whisper → LLM → TTS → playback

Mirrors _run_full() in main.py exactly, but:
  - Feeds pre-recorded WAVs instead of live mic (uses tests/recordings/)
  - Captures every latency segment
  - Measures TTS smoothness: chunk count, inter-chunk gaps, words-per-chunk
  - Prints a colour-coded report with diagnosis + tuning advice

Usage:
    python tests/benchmark_tts.py                  # all 10 sentences
    python tests/benchmark_tts.py --sentence 3     # only sentence #3
    python tests/benchmark_tts.py --no-audio       # skip actual playback (latency only)
    python tests/benchmark_tts.py --no-llm         # feed fixed text directly to TTS
    python tests/benchmark_tts.py --steps 8        # override TTS diffusion steps
    python tests/benchmark_tts.py --tts-text "Hello world, this is a test."

Pre-requisite: run benchmark_stt.py first so tests/recordings/ exists.
"""

import sys
import time
import argparse
import threading
from pathlib import Path
from dataclasses import dataclass, field

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import numpy as np
import soundfile as sf
from colorama import Fore, Style, init as colorama_init

colorama_init()

from config.vad import RECORD_SAMPLE_RATE, PAUSE_SECONDS
from config.whisper import WHISPER_SAMPLE_RATE
from config.tts import (
    SUPERTONIC_VOICE,
    SUPERTONIC_SPEED,
    SUPERTONIC_STEPS,
    SUPERTONIC_LANGUAGE,
)

RECORDINGS_DIR = ROOT / "tests" / "recordings"

SENTENCES = [
    "open the calendar and show me this week",
    "what is the weather like today",
    "set a reminder for tomorrow at nine am",
    "send a message to John saying I will be late",
    "search the web for latest AI news",
    "turn off the lights in the living room",
    "call mom when you get a chance",
    "how long does it take to drive to the airport",
    "play some music on spotify",
    "the quick brown fox jumps over the lazy dog",
]


# ─────────────────────────────────────────────────────────────
# Terminal helpers
# ─────────────────────────────────────────────────────────────


def c(color, msg):
    return f"{color}{msg}{Style.RESET_ALL}"


def ok(m):
    print(f"  {c(Fore.GREEN,  '✓')}  {m}")


def fail(m):
    print(f"  {c(Fore.RED,    '✗')}  {m}")


def info(m):
    print(f"  {c(Fore.CYAN,   '→')}  {m}")


def warn(m):
    print(f"  {c(Fore.YELLOW, '!')}  {m}")


def head(m):
    print(f"\n  {c(Fore.YELLOW + Style.BRIGHT, m)}")


def rule():
    print(f"  {'─' * 66}")


def ms_c(ms, green=300, yellow=700):
    return Fore.GREEN if ms < green else Fore.YELLOW if ms < yellow else Fore.RED


def tag(label, val, color=Fore.WHITE):
    print(f"  {label:<36} {c(color, val)}")


# ─────────────────────────────────────────────────────────────
# Result container
# ─────────────────────────────────────────────────────────────


@dataclass
class BenchResult:
    sentence_idx: int
    input_text: str
    stt_text: str = ""
    llm_text: str = ""

    stt_ms: float = 0.0
    llm_first_token_ms: float = 0.0
    llm_total_ms: float = 0.0
    tts_first_chunk_ms: float = 0.0
    tts_total_ms: float = 0.0
    e2e_ms: float = 0.0

    chunk_count: int = 0
    chunk_sizes_words: list = field(default_factory=list)
    chunk_gen_times_ms: list = field(default_factory=list)
    inter_chunk_gaps_ms: list = field(default_factory=list)

    filler_text: str = ""
    filler_gen_ms: float = 0.0
    filler_duration_ms: float = 0.0
    filler_covers_llm: bool = False

    stt_passed: bool = True
    error: str = ""


# ─────────────────────────────────────────────────────────────
# Instrumented TTS engine
# ─────────────────────────────────────────────────────────────


class InstrumentedTTSEngine:
    def __init__(self, voice, speed, steps, language, play_fn):
        self.voice = voice
        self.speed = speed
        self.steps = steps
        self.language = language
        self.play_fn = play_fn
        self._chunks: list[str] = []

    def enqueue(self, text: str):
        if text.strip():
            self._chunks.append(text.strip())

    def run(self) -> dict:
        from tts.generate.pipeline import generate_one
        from tts.model.singleton import get_model
        from tts.text.clean import clean_markdown

        sr = get_model()["sample_rate"]
        chunk_gen_times, inter_chunk_gaps = [], []
        prev_end = None
        total_start = time.perf_counter()

        for text in self._chunks:
            cleaned = clean_markdown(text)
            if not cleaned:
                continue
            if prev_end is not None:
                inter_chunk_gaps.append((time.perf_counter() - prev_end) * 1000)

            t0 = time.perf_counter()
            audio = generate_one(
                cleaned,
                voice=self.voice,
                speed=self.speed,
                steps=self.steps,
                language=self.language,
            )
            gen_ms = (time.perf_counter() - t0) * 1000
            chunk_gen_times.append(gen_ms)
            self.play_fn(audio, sr)
            prev_end = time.perf_counter()

        return {
            "chunk_count": len(self._chunks),
            "chunk_sizes_words": [len(ch.split()) for ch in self._chunks],
            "chunk_gen_times_ms": chunk_gen_times,
            "inter_chunk_gaps_ms": inter_chunk_gaps,
            "tts_first_chunk_ms": chunk_gen_times[0] if chunk_gen_times else 0.0,
            "tts_total_ms": (time.perf_counter() - total_start) * 1000,
        }


# ─────────────────────────────────────────────────────────────
# Feed LLM tokens to engine (mirrors optimised feed.py)
# ─────────────────────────────────────────────────────────────


def feed_tokens_to_engine(engine: InstrumentedTTSEngine, token_gen) -> tuple:
    from tts.text.split import split_sentence, MIN_CHUNK_CHARS

    WORD_FLUSH_THRESHOLD = 6
    MIN_SEND_CHARS = 20

    buf, full = "", ""
    first_token_ms = None
    t_start = time.perf_counter()

    for token in token_gen:
        if first_token_ms is None:
            first_token_ms = (time.perf_counter() - t_start) * 1000
        buf += token
        full += token

        while True:
            sentence, remainder = split_sentence(buf)
            if sentence and len(sentence) >= MIN_SEND_CHARS:
                engine.enqueue(sentence)
                buf = remainder
            else:
                break

        if len(buf.split()) >= WORD_FLUSH_THRESHOLD:
            engine.enqueue(buf.strip())
            buf = ""

    if buf.strip() and len(buf.strip()) >= 2:
        engine.enqueue(buf.strip())

    llm_total_ms = (time.perf_counter() - t_start) * 1000
    return full, first_token_ms or llm_total_ms, llm_total_ms


# ─────────────────────────────────────────────────────────────
# STT
# ─────────────────────────────────────────────────────────────


def run_stt(wav_path: Path) -> tuple:
    from audio.transform.resample import resample
    from audio.transform.normalise import normalise
    from transcription.model.singleton import get_model
    from transcription.model.lock import infer_lock
    from transcription.hallucination.confidence import passes_confidence
    from transcription.hallucination.noise import clean_text
    from transcription.hallucination.repetition import has_repetition
    from transcription.transcribe.options import build_whisper_options
    import whisper as _whisper

    audio, sr = sf.read(str(wav_path), dtype="float32")
    if audio.ndim > 1:
        audio = audio[:, 0]
    if sr != RECORD_SAMPLE_RATE:
        audio = resample(audio, sr, RECORD_SAMPLE_RATE)
    audio_16k = resample(audio, RECORD_SAMPLE_RATE, WHISPER_SAMPLE_RATE)
    audio_16k = normalise(audio_16k)

    model = get_model()
    opts = build_whisper_options()
    t0 = time.perf_counter()
    with infer_lock:
        result = _whisper.transcribe(model, audio_16k, **opts)
    stt_ms = (time.perf_counter() - t0) * 1000

    passed = passes_confidence(result)
    text = ""
    if passed:
        raw = clean_text(result.get("text", ""))
        if raw and not has_repetition(raw):
            text = raw
    return text, stt_ms, passed


# ─────────────────────────────────────────────────────────────
# Full pipeline for one sentence
# ─────────────────────────────────────────────────────────────


def benchmark_one(idx: int, args, play_fn) -> BenchResult:
    r = BenchResult(sentence_idx=idx, input_text=SENTENCES[idx])
    wav = RECORDINGS_DIR / f"sentence_{idx+1:02d}.wav"

    if not wav.exists():
        r.error = f"No recording at {wav.name} — run benchmark_stt.py first"
        return r

    e2e_start = time.perf_counter()

    # ── STT ─────────────────────────────────────────────────
    if args.no_llm and args.tts_text:
        r.stt_text = args.tts_text
    else:
        try:
            r.stt_text, r.stt_ms, r.stt_passed = run_stt(wav)
        except Exception as e:
            r.error = f"STT error: {e}"
            return r
        if not r.stt_text:
            r.error = "STT: no transcript"
            return r

    # ── Filler measurement ───────────────────────────────────
    try:
        from tts.generate.pipeline import generate_one
        from tts.model.singleton import get_model

        # Pick the longest filler to test coverage
        from tts.engine.state import _FILLERS

        filler_text = max(_FILLERS, key=len)
        r.filler_text = filler_text
        t_fil = time.perf_counter()
        filler_audio = generate_one(
            filler_text,
            voice=args.voice,
            speed=args.speed,
            steps=args.steps,
            language=args.language,
        )
        r.filler_gen_ms = (time.perf_counter() - t_fil) * 1000
        sr = get_model()["sample_rate"]
        r.filler_duration_ms = len(filler_audio) / sr * 1000
    except Exception as e:
        warn(f"Filler measurement failed: {e}")

    # ── LLM + TTS feed ──────────────────────────────────────
    engine = InstrumentedTTSEngine(
        voice=args.voice,
        speed=args.speed,
        steps=args.steps,
        language=args.language,
        play_fn=play_fn,
    )

    if args.no_llm:

        def _fixed():
            for w in (args.tts_text or r.stt_text).split():
                yield w + " "

        token_gen = _fixed()
    else:
        from llm.inference.stream import stream_response
        from llm.history.state import create_history

        token_gen = stream_response(r.stt_text, create_history())

    try:
        r.llm_text, r.llm_first_token_ms, r.llm_total_ms = feed_tokens_to_engine(
            engine, token_gen
        )
    except Exception as e:
        r.error = f"LLM error: {e}"
        return r

    # ── TTS generation ───────────────────────────────────────
    try:
        tts_info = engine.run()
    except Exception as e:
        r.error = f"TTS error: {e}"
        return r

    r.chunk_count = tts_info["chunk_count"]
    r.chunk_sizes_words = tts_info["chunk_sizes_words"]
    r.chunk_gen_times_ms = tts_info["chunk_gen_times_ms"]
    r.inter_chunk_gaps_ms = tts_info["inter_chunk_gaps_ms"]
    r.tts_first_chunk_ms = tts_info["tts_first_chunk_ms"]
    r.tts_total_ms = tts_info["tts_total_ms"]
    r.e2e_ms = (time.perf_counter() - e2e_start) * 1000
    r.filler_covers_llm = r.filler_duration_ms >= r.llm_first_token_ms

    return r


# ─────────────────────────────────────────────────────────────
# Print one result
# ─────────────────────────────────────────────────────────────


def print_result(r: BenchResult, args) -> None:
    n = r.sentence_idx + 1
    print(f"\n  [{n}] {c(Fore.CYAN, r.input_text)}")
    if r.error:
        fail(r.error)
        return

    if not args.no_llm:
        print(f"       STT : {c(Fore.WHITE, r.stt_text or '(empty)')}")
    llm_preview = r.llm_text[:110] + ("…" if len(r.llm_text) > 110 else "")
    print(f"       LLM : {c(Fore.WHITE, llm_preview)}")
    print()

    rule()
    if not args.no_llm:
        tag("STT (Whisper)", f"{r.stt_ms:.0f} ms", ms_c(r.stt_ms, 600, 1200))
    tag(
        "LLM → first token",
        f"{r.llm_first_token_ms:.0f} ms",
        ms_c(r.llm_first_token_ms, 500, 1500),
    )
    tag(
        "LLM → full response",
        f"{r.llm_total_ms:.0f} ms",
        ms_c(r.llm_total_ms, 800, 2000),
    )

    if r.filler_duration_ms:
        cover = (
            "✓ covers LLM"
            if r.filler_covers_llm
            else f"✗ {r.llm_first_token_ms - r.filler_duration_ms:.0f}ms gap"
        )
        fil_color = Fore.GREEN if r.filler_covers_llm else Fore.RED
        tag(
            f"Filler ({r.filler_text!r})",
            f"{r.filler_duration_ms:.0f} ms  [{cover}]",
            fil_color,
        )

    tag(
        "TTS first chunk generation",
        f"{r.tts_first_chunk_ms:.0f} ms",
        ms_c(r.tts_first_chunk_ms, 300, 700),
    )
    tag(
        "TTS total generation",
        f"{r.tts_total_ms:.0f} ms",
        ms_c(r.tts_total_ms, 2000, 5000),
    )

    if not args.no_llm:
        tag("End-to-end", f"{r.e2e_ms:.0f} ms", ms_c(r.e2e_ms, 4000, 8000))
    rule()

    print(f"\n  TTS Smoothness")
    rule()
    tag(
        "Chunks generated",
        str(r.chunk_count),
        (
            Fore.GREEN
            if r.chunk_count <= 4
            else Fore.YELLOW if r.chunk_count <= 7 else Fore.RED
        ),
    )

    if r.chunk_sizes_words:
        avg_w = sum(r.chunk_sizes_words) / len(r.chunk_sizes_words)
        tag(
            "Avg words per chunk",
            f"{avg_w:.1f}",
            Fore.GREEN if avg_w >= 5 else Fore.YELLOW if avg_w >= 3 else Fore.RED,
        )
        tag("Chunk word distribution", str(r.chunk_sizes_words))

    if r.chunk_gen_times_ms:
        avg_gen = sum(r.chunk_gen_times_ms) / len(r.chunk_gen_times_ms)
        tag("Avg chunk gen time", f"{avg_gen:.0f} ms", ms_c(avg_gen, 300, 600))
        tag(
            "Per-chunk gen times (ms)",
            "  ".join(f"{v:.0f}" for v in r.chunk_gen_times_ms),
        )

    if r.inter_chunk_gaps_ms:
        avg_gap = sum(r.inter_chunk_gaps_ms) / len(r.inter_chunk_gaps_ms)
        max_gap = max(r.inter_chunk_gaps_ms)
        tag(
            "Avg / max inter-chunk gap",
            f"{avg_gap:.0f} ms / {max_gap:.0f} ms",
            Fore.GREEN if max_gap < 60 else Fore.YELLOW if max_gap < 150 else Fore.RED,
        )
    rule()


# ─────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────


def print_summary(results: list[BenchResult], args) -> None:
    good = [r for r in results if not r.error and r.chunk_count > 0]
    if not good:
        warn("No successful results.")
        return

    head("SUMMARY")
    print()
    rule()

    def avg(vals):
        return sum(vals) / len(vals) if vals else 0

    stt_vals = [r.stt_ms for r in good]
    ft_vals = [r.llm_first_token_ms for r in good]
    llm_vals = [r.llm_total_ms for r in good]
    tts1_vals = [r.tts_first_chunk_ms for r in good]
    ttst_vals = [r.tts_total_ms for r in good]
    e2e_vals = [r.e2e_ms for r in good]
    gap_vals = [g for r in good for g in r.inter_chunk_gaps_ms]
    fil_vals = [r.filler_duration_ms for r in good if r.filler_duration_ms]
    cw_vals = [w for r in good for w in r.chunk_sizes_words]

    if stt_vals and not args.no_llm:
        a = avg(stt_vals)
        tag("STT avg", f"{a:.0f} ms", ms_c(a, 600, 1200))
    if ft_vals:
        a = avg(ft_vals)
        tag("LLM first token avg", f"{a:.0f} ms", ms_c(a, 500, 1500))
    if llm_vals:
        a = avg(llm_vals)
        tag("LLM total avg", f"{a:.0f} ms", ms_c(a, 800, 2000))
    if fil_vals:
        a = avg(fil_vals)
        tag("Filler duration avg", f"{a:.0f} ms")
    if tts1_vals:
        a = avg(tts1_vals)
        tag("TTS first chunk avg", f"{a:.0f} ms", ms_c(a, 300, 700))
    if ttst_vals:
        a = avg(ttst_vals)
        tag("TTS total avg", f"{a:.0f} ms", ms_c(a, 2000, 5000))
    if cw_vals:
        a = avg(cw_vals)
        tag(
            "Avg words/chunk",
            f"{a:.1f}",
            Fore.GREEN if a >= 5 else Fore.YELLOW if a >= 3 else Fore.RED,
        )
    if gap_vals:
        a = avg(gap_vals)
        mx = max(gap_vals)
        tag(
            "Inter-chunk gap avg/max",
            f"{a:.0f} ms / {mx:.0f} ms",
            Fore.GREEN if mx < 60 else Fore.YELLOW,
        )
    if e2e_vals and not args.no_llm:
        a = avg(e2e_vals)
        tag("End-to-end avg", f"{a:.0f} ms", ms_c(a, 4000, 8000))
    rule()

    head("DIAGNOSIS & TUNING ADVICE")
    print()
    any_rec = False

    # TTS first chunk
    if tts1_vals:
        a = avg(tts1_vals)
        if a > 700:
            warn(
                f"TTS first chunk slow ({a:.0f}ms). "
                f"Reduce SUPERTONIC_STEPS: currently {args.steps}, try {max(6, args.steps - 3)}"
            )
            any_rec = True
        elif a > 300:
            warn(
                f"TTS first chunk moderate ({a:.0f}ms). "
                f"Try steps={max(6, args.steps - 2)} to cut ~30%"
            )
            any_rec = True
        else:
            ok(f"TTS first chunk fast ({a:.0f}ms)")

    # Chunk fragmentation
    if cw_vals:
        a = avg(cw_vals)
        counts = [r.chunk_count for r in good]
        ac = avg(counts)
        if a < 3:
            warn(
                f"Avg {a:.1f} words/chunk ({ac:.1f} chunks/response) — "
                f"too fragmented, each chunk wastes ~350ms ONNX overhead. "
                f"Raise WORD_FLUSH_THRESHOLD in tts/engine/feed.py"
            )
            any_rec = True
        elif a >= 5:
            ok(f"Chunk size good ({a:.1f} words avg, {ac:.1f} chunks/response)")
        else:
            warn(f"Chunks borderline ({a:.1f} words avg). Aim for 6+ words/chunk")
            any_rec = True

    # Filler coverage
    if fil_vals and ft_vals:
        avg_fil = avg(fil_vals)
        avg_ft = avg(ft_vals)
        if avg_fil >= avg_ft * 0.9:
            ok(f"Filler ({avg_fil:.0f}ms) covers LLM first-token ({avg_ft:.0f}ms)")
        else:
            gap = avg_ft - avg_fil
            warn(
                f"Filler ({avg_fil:.0f}ms) shorter than LLM first-token ({avg_ft:.0f}ms) "
                f"— {gap:.0f}ms silence gap. Longer fillers added to state.py fix this."
            )
            any_rec = True

    # LLM speed
    if ft_vals:
        a = avg(ft_vals)
        if a > 1500:
            warn(
                f"LLM first token {a:.0f}ms — try GPU_LAYERS=36 (max) in config/llm.py "
                f"or a smaller model (qwen2.5-1.5b)"
            )
            any_rec = True

    if not any_rec:
        ok("Pipeline is well tuned!")

    head("NUMBERS TO PASTE")
    print()
    print(f"  voice={args.voice}  speed={args.speed}  steps={args.steps}")
    if tts1_vals:
        print(
            f"  tts_first_chunk_avg={avg(tts1_vals):.0f}ms  tts_total_avg={avg(ttst_vals):.0f}ms"
        )
    if cw_vals:
        print(
            f"  words_per_chunk_avg={avg(cw_vals):.1f}  chunk_count_avg={avg([r.chunk_count for r in good]):.1f}"
        )
    if ft_vals:
        print(
            f"  llm_first_token_avg={avg(ft_vals):.0f}ms  llm_total_avg={avg(llm_vals):.0f}ms"
        )
    if fil_vals:
        print(f"  filler_duration_avg={avg(fil_vals):.0f}ms")
    if e2e_vals:
        print(f"  e2e_avg={avg(e2e_vals):.0f}ms")
    print()


# ─────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sentence", type=int, default=0)
    parser.add_argument("--no-audio", action="store_true")
    parser.add_argument("--no-llm", action="store_true")
    parser.add_argument("--tts-text", type=str, default="")
    parser.add_argument("--steps", type=int, default=SUPERTONIC_STEPS)
    parser.add_argument("--voice", type=str, default=SUPERTONIC_VOICE)
    parser.add_argument("--speed", type=float, default=SUPERTONIC_SPEED)
    parser.add_argument("--language", type=str, default=SUPERTONIC_LANGUAGE)
    args = parser.parse_args()

    if args.tts_text:
        args.no_llm = True

    head("FULL PIPELINE TTS BENCHMARK")
    print()
    print(f"  Recordings : {RECORDINGS_DIR.relative_to(ROOT)}")
    print(f"  Mode       : {'TTS-only' if args.no_llm else 'STT → LLM → TTS'}")
    print(f"  Playback   : {'disabled' if args.no_audio else 'enabled'}")
    print(f"  TTS config : voice={args.voice}  speed={args.speed}  steps={args.steps}")
    rule()
    print()

    if not args.no_llm:
        print("  Loading Whisper...")
        from transcription.model.singleton import get_model as load_whisper

        load_whisper()
        ok("Whisper ready")
        print("  Loading LLM...")
        from llm.model.singleton import get_model as load_llm

        load_llm()
        ok("LLM ready")

    print("  Loading TTS model...")
    from tts.model.singleton import get_model as load_tts

    load_tts()
    ok("TTS ready")

    print("  Warming up TTS...")
    from tts.generate.pipeline import generate_one

    _ = generate_one(
        "Warming up.",
        voice=args.voice,
        speed=args.speed,
        steps=args.steps,
        language=args.language,
    )
    ok("TTS warmed up")
    print()

    play_fn = (
        (lambda a, sr: None)
        if args.no_audio
        else __import__("tts.playback.stream", fromlist=["play_audio"]).play_audio
    )

    indices = [args.sentence - 1] if args.sentence else list(range(len(SENTENCES)))
    results: list[BenchResult] = []

    for idx in indices:
        print(f"\n  Running [{idx+1}/{len(SENTENCES)}]: {c(Fore.CYAN, SENTENCES[idx])}")
        r = benchmark_one(idx, args, play_fn)
        results.append(r)
        print_result(r, args)
        rule()

    completed = [r for r in results if not r.error]
    if len(completed) > 1:
        print_summary(completed, args)
    elif len(completed) == 1:
        r = completed[0]
        print(f"\n  TTS first chunk : {r.tts_first_chunk_ms:.0f} ms")
        print(f"  TTS total       : {r.tts_total_ms:.0f} ms")
        print(f"  Chunks          : {r.chunk_count}  ({r.chunk_sizes_words})")


if __name__ == "__main__":
    main()
