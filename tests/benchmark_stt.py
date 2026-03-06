"""
tests/benchmark_stt.py
======================
Record ONCE, benchmark FOREVER.

First run  → records your voice for each sentence, saves to tests/recordings/
Every run after → loads the saved WAVs and runs them through the live pipeline

This means every time you tweak config/vad.py or the pipeline, you re-run
the same audio and get apples-to-apples latency + accuracy numbers.

Usage:
    python tests/benchmark_stt.py              # auto: record if missing, else replay
    python tests/benchmark_stt.py --record     # force re-record everything
    python tests/benchmark_stt.py --replay     # force replay only (no mic needed)
    python tests/benchmark_stt.py --sentence 3 # only sentence #3
"""

import sys
import time
import argparse
import threading
from pathlib import Path

# ── always run from project root ──────────────────────────────
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

RECORDINGS_DIR = ROOT / "tests" / "recordings"
RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)

import numpy as np
import sounddevice as sd
import soundfile as sf
from colorama import Fore, Style, init as colorama_init

colorama_init()

# ── project imports ────────────────────────────────────────────
from config.vad import (
    RECORD_SAMPLE_RATE,
    PAUSE_SECONDS,
    MIN_SPEECH_SEC,
    PREROLL_SECONDS,
    ENERGY_THRESHOLD,
    SILERO_THRESHOLD,
    TRANSCRIBE_EVERY,
)
from config.whisper import WHISPER_SAMPLE_RATE
from audio.transform.resample import resample
from audio.transform.normalise import normalise
from transcription.model.singleton import get_model
from transcription.stream.final import run_final_pass
from transcription.stream.buffer import (
    create_buffer,
    append as buf_append,
    clear_buffer,
)
from transcription.hallucination.confidence import passes_confidence
from transcription.hallucination.noise import clean_text
from transcription.hallucination.repetition import has_repetition
import whisper as _whisper

# ── sentences ──────────────────────────────────────────────────
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

RECORD_SECONDS = 5  # window given to speak each sentence
COUNTDOWN_SEC = 3


# ── terminal helpers ───────────────────────────────────────────
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
    print(f"  {'─' * 60}")


def countdown(n: int) -> None:
    for i in range(n, 0, -1):
        print(f"\r  {c(Fore.RED, f'Starting in {i}...')}", end="", flush=True)
        time.sleep(1)
    print("\r" + " " * 30 + "\r", end="")


# ── WER ────────────────────────────────────────────────────────
def _norm(text: str) -> str:
    import re

    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    text = text.replace("i'll", "i will").replace("i'm", "i am")
    text = text.replace("9am", "nine am").replace("9 am", "nine am")
    return text


def wer_score(ref: str, hyp: str) -> float:
    if not hyp:
        return 1.0
    try:
        import jiwer

        return jiwer.wer(_norm(ref), _norm(hyp))
    except ImportError:
        r, h = _norm(ref).split(), _norm(hyp).split()
        d = [[0] * (len(h) + 1) for _ in range(len(r) + 1)]
        for i in range(len(r) + 1):
            d[i][0] = i
        for j in range(len(h) + 1):
            d[0][j] = j
        for i in range(1, len(r) + 1):
            for j in range(1, len(h) + 1):
                d[i][j] = min(
                    d[i - 1][j] + 1,
                    d[i][j - 1] + 1,
                    d[i - 1][j - 1] + (0 if r[i - 1] == h[j - 1] else 1),
                )
        return d[len(r)][len(h)] / max(len(r), 1)


# ── recording path for a sentence index ───────────────────────
def wav_path(idx: int) -> Path:
    return RECORDINGS_DIR / f"sentence_{idx+1:02d}.wav"


# ── record one sentence to disk ────────────────────────────────
def record_sentence(idx: int, sentence: str) -> np.ndarray:
    path = wav_path(idx)
    print(f"\n  [{idx+1}/{len(SENTENCES)}] Say: {c(Fore.CYAN, sentence)}")
    countdown(COUNTDOWN_SEC)
    print(f"  {c(Fore.RED, '● REC')}  speak now ({RECORD_SECONDS}s)", flush=True)

    audio = sd.rec(
        int(RECORD_SECONDS * RECORD_SAMPLE_RATE),
        samplerate=RECORD_SAMPLE_RATE,
        channels=1,
        dtype="float32",
    )
    sd.wait()
    audio = audio[:, 0]

    sf.write(str(path), audio, RECORD_SAMPLE_RATE)
    ok(f"Saved → {path.relative_to(ROOT)}")
    return audio


# ── load saved recording ───────────────────────────────────────
def load_sentence(idx: int) -> np.ndarray:
    audio, sr = sf.read(str(wav_path(idx)), dtype="float32")
    if audio.ndim > 1:
        audio = audio[:, 0]
    if sr != RECORD_SAMPLE_RATE:
        audio = resample(audio, sr, RECORD_SAMPLE_RATE)
    return audio


# ── silence trimmer — mimics what VAD does in real use ────────
def trim_silence(audio: np.ndarray, sr: int, pad_ms: int = 150) -> np.ndarray:
    """
    Adaptive silence trim based on the recording's own noise floor.
    Uses bottom 20% of frame energies as silence baseline, cuts frames
    below 4x that level. Matches what VAD actually sends to Whisper.
    """
    frame = int(sr * 0.02)  # 20ms
    hop = frame // 2
    pad = int(sr * pad_ms / 1000)

    frames = [audio[i : i + frame] for i in range(0, len(audio) - frame, hop)]
    if not frames:
        return audio

    energies = np.array([np.sqrt(np.mean(f**2)) for f in frames])

    # noise floor = 20th percentile of all frame energies
    noise_floor = np.percentile(energies, 20)
    threshold = max(noise_floor * 4.0, 1e-4)  # 4x noise floor, minimum guard

    speech = energies > threshold
    if not speech.any():
        return audio  # nothing above noise — return as-is

    first = max(0, speech.argmax() * hop - pad)
    last = min(len(audio), (len(speech) - speech[::-1].argmax()) * hop + pad)
    return audio[first:last]


# ── run audio through the live pipeline, measure everything ───
def run_pipeline(audio: np.ndarray) -> dict:
    """
    Feed raw recorded audio (at RECORD_SAMPLE_RATE) through the real
    resample → normalise → whisper pipeline and return timing + text.
    Silence is trimmed first to match what VAD sends at runtime.
    """
    # 1. trim silence — matches real VAD behaviour
    audio_trimmed = trim_silence(audio, RECORD_SAMPLE_RATE)
    audio_duration_ms = len(audio_trimmed) / RECORD_SAMPLE_RATE * 1000

    # 2. resample + normalise
    t_pre = time.perf_counter()
    audio_16k = resample(audio_trimmed, RECORD_SAMPLE_RATE, WHISPER_SAMPLE_RATE)
    audio_16k = normalise(audio_16k)
    preprocess_ms = (time.perf_counter() - t_pre) * 1000

    # 2. whisper inference
    model = get_model()
    from config.vad import (
        NO_SPEECH_THRESHOLD,
        LOGPROB_THRESHOLD,
        COMPRESSION_RATIO_THRESHOLD,
    )
    from config.whisper import WHISPER_DEVICE

    t_whisper = time.perf_counter()
    from transcription.model.lock import infer_lock

    with infer_lock:
        result = _whisper.transcribe(
            model,
            audio_16k,
            language="en",
            fp16=(WHISPER_DEVICE == "cuda"),
            temperature=0,
            condition_on_previous_text=False,
            no_speech_threshold=NO_SPEECH_THRESHOLD,
            compression_ratio_threshold=COMPRESSION_RATIO_THRESHOLD,
            logprob_threshold=LOGPROB_THRESHOLD,
        )
    whisper_ms = (time.perf_counter() - t_whisper) * 1000

    # 3. hallucination filters
    text = ""
    passed_confidence = passes_confidence(result)
    raw_text = clean_text(result.get("text", ""))
    if passed_confidence and raw_text and not has_repetition(raw_text):
        text = raw_text

    # no_speech_prob from segments
    segs = result.get("segments", [])
    avg_no_speech = (
        sum(s.get("no_speech_prob", 0) for s in segs) / len(segs) if segs else 0.0
    )

    return {
        "text": text,
        "raw_text": result.get("text", "").strip(),
        "whisper_ms": whisper_ms,
        "preprocess_ms": preprocess_ms,
        "audio_duration_ms": audio_duration_ms,
        "passed_confidence": passed_confidence,
        "avg_no_speech": avg_no_speech,
        "segments": len(segs),
    }


# ── benchmark one sentence ─────────────────────────────────────
def benchmark_sentence(idx: int, audio: np.ndarray) -> dict:
    sentence = SENTENCES[idx]
    r = run_pipeline(audio)
    score = wer_score(sentence, r["text"])

    # e2e = preprocess + whisper  (VAD pause is real-world overhead, not pipeline)
    e2e_ms = r["preprocess_ms"] + r["whisper_ms"]

    r["ref"] = sentence
    r["wer"] = score
    r["e2e_ms"] = e2e_ms
    return r


# ── print one result ───────────────────────────────────────────
def print_result(idx: int, r: dict) -> None:
    ref = SENTENCES[idx]
    hyp = r["text"]

    wer_c = (
        Fore.GREEN if r["wer"] < 0.1 else Fore.YELLOW if r["wer"] < 0.3 else Fore.RED
    )
    wsp_c = (
        Fore.GREEN
        if r["whisper_ms"] < 600
        else Fore.YELLOW if r["whisper_ms"] < 1200 else Fore.RED
    )
    e2e_c = (
        Fore.GREEN
        if r["e2e_ms"] < 700
        else Fore.YELLOW if r["e2e_ms"] < 1400 else Fore.RED
    )
    nsp_c = (
        Fore.GREEN
        if r["avg_no_speech"] < 0.3
        else Fore.YELLOW if r["avg_no_speech"] < 0.45 else Fore.RED
    )

    print(f"\n  [{idx+1}] {c(Fore.CYAN, ref)}")
    if hyp:
        print(f"       {c(Fore.WHITE, hyp)}")
    else:
        print(f"       {c(Fore.RED, '(no transcript)')}")
        if r["raw_text"]:
            print(f"       raw: {c(Fore.YELLOW, r['raw_text'])}")

    dur_str = f"{r['audio_duration_ms']:.0f} ms"
    wsp_str = f"{r['whisper_ms']:.0f} ms"
    e2e_str = f"{r['e2e_ms']:.0f} ms"
    wer_str = f"{r['wer']:.0%}"
    nsp_str = f"{r['avg_no_speech']:.2f}  (limit={__import__('config.vad', fromlist=['NO_SPEECH_THRESHOLD']).NO_SPEECH_THRESHOLD})"

    info(f"Audio to Whisper  : {dur_str}  (trimmed from 5s)")
    info(f"Whisper inference : {c(wsp_c, wsp_str)}")
    info(f"Preprocess        : {r['preprocess_ms']:.0f} ms")
    info(f"Pipeline total    : {c(e2e_c, e2e_str)}")
    info(f"no_speech_prob    : {c(nsp_c, nsp_str)}")
    info(f"WER               : {c(wer_c, wer_str)}")
    if not r["passed_confidence"]:
        warn(
            f"REJECTED by confidence filter — speak louder/clearer or raise NO_SPEECH_THRESHOLD"
        )


# ── summary ────────────────────────────────────────────────────
def print_summary(results: list[dict]) -> None:
    head("SUMMARY")
    print()

    detected = [r for r in results if r["text"]]
    wsp = [r["whisper_ms"] for r in detected]
    e2e = [r["e2e_ms"] for r in detected]
    wers = [r["wer"] for r in detected]

    def stat(vals, unit="ms"):
        if not vals:
            return "no data"
        avg = sum(vals) / len(vals)
        mn = min(vals)
        mx = max(vals)
        return f"avg {avg:.0f}{unit}  min {mn:.0f}{unit}  max {mx:.0f}{unit}"

    rule()
    print(f"  {'Whisper inference':<26} {stat(wsp)}")
    print(f"  {'Pipeline total (no VAD)':<26} {stat(e2e)}")
    if wers:
        avg_wer = sum(wers) / len(wers)
        wer_c = (
            Fore.GREEN if avg_wer < 0.1 else Fore.YELLOW if avg_wer < 0.3 else Fore.RED
        )
        print(f"  {'WER':<26} {c(wer_c, f'avg {avg_wer:.1%}')}")
    print(f"  {'Detection rate':<26} {len(detected)}/{len(results)}")
    rule()

    # real-world E2E estimate
    pause_ms = PAUSE_SECONDS * 1000
    avg_wsp = sum(wsp) / len(wsp) if wsp else 0
    est_e2e = pause_ms + avg_wsp
    print(f"\n  Real-world E2E estimate:")
    print(f"    PAUSE_SECONDS overhead : {pause_ms:.0f} ms   (config/vad.py)")
    print(f"    Whisper avg            : {avg_wsp:.0f} ms")
    print(f"    ─────────────────────────────────")
    e2e_color = (
        Fore.GREEN if est_e2e < 1200 else Fore.YELLOW if est_e2e < 2000 else Fore.RED
    )
    print(f"    Estimated felt latency : {c(e2e_color, f'{est_e2e:.0f} ms')}")

    # diagnosis
    head("DIAGNOSIS")
    print()
    any_rec = False

    if wsp:
        avg = sum(wsp) / len(wsp)
        if avg > 1200:
            warn(
                f"Whisper is SLOW ({avg:.0f}ms). Try WHISPER_MODEL_NAME='tiny' in config/whisper.py"
            )
            any_rec = True
        elif avg > 600:
            warn(f"Whisper is moderate ({avg:.0f}ms). 'tiny' model would cut this ~50%")
            any_rec = True
        else:
            ok(f"Whisper is fast ({avg:.0f}ms avg)")

    if PAUSE_SECONDS > 0.6:
        warn(
            f"PAUSE_SECONDS={PAUSE_SECONDS} — dominates latency. Lower to 0.4–0.5 for ~{(PAUSE_SECONDS-0.45)*1000:.0f}ms gain"
        )
        any_rec = True
    elif PAUSE_SECONDS > 0.4:
        warn(f"PAUSE_SECONDS={PAUSE_SECONDS} — try 0.4 for tighter cutoff")
        any_rec = True
    else:
        ok(f"PAUSE_SECONDS={PAUSE_SECONDS} is aggressive (good)")

    miss = len(results) - len(detected)
    if miss > 0:
        warn(
            f"{miss} sentences not detected — VAD may be too strict or recordings too quiet"
        )
        any_rec = True

    if not any_rec:
        ok("Pipeline is well tuned. Paste numbers below to get further advice.")

    # paste block
    head("NUMBERS TO PASTE")
    print()
    print(
        f"  PAUSE_SECONDS={PAUSE_SECONDS}  SILERO_THRESHOLD={SILERO_THRESHOLD}  TRANSCRIBE_EVERY={TRANSCRIBE_EVERY}"
    )
    if wsp:
        print(
            f"  whisper_avg={sum(wsp)/len(wsp):.0f}ms  min={min(wsp):.0f}ms  max={max(wsp):.0f}ms"
        )
    if e2e:
        print(f"  pipeline_avg={sum(e2e)/len(e2e):.0f}ms  felt_e2e_est={est_e2e:.0f}ms")
    if wers:
        print(
            f"  wer_avg={sum(wers)/len(wers):.1%}  detection={len(detected)}/{len(results)}"
        )
    print()


# ── main ───────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--record",
        action="store_true",
        help="Force re-record all sentences (overwrites saved WAVs)",
    )
    parser.add_argument(
        "--replay", action="store_true", help="Force replay mode — never touch the mic"
    )
    parser.add_argument(
        "--sentence",
        type=int,
        default=0,
        help="Only run sentence N (1-based). Default: all.",
    )
    args = parser.parse_args()

    # figure out which sentences to process
    indices = [args.sentence - 1] if args.sentence else list(range(len(SENTENCES)))

    # print config header
    head("STT BENCHMARK  —  record-once, replay-forever")
    print()
    print(f"  Recordings dir : {RECORDINGS_DIR.relative_to(ROOT)}")
    print(f"  Config snapshot:")
    print(
        f"    PAUSE_SECONDS    = {c(Fore.CYAN, PAUSE_SECONDS)}   ← adds this to every utterance"
    )
    print(f"    SILERO_THRESHOLD = {c(Fore.CYAN, SILERO_THRESHOLD)}")
    print(f"    TRANSCRIBE_EVERY = {c(Fore.CYAN, TRANSCRIBE_EVERY)}")
    print(
        f"    WHISPER_MODEL    = {c(Fore.CYAN, __import__('config.whisper', fromlist=['WHISPER_MODEL_NAME']).WHISPER_MODEL_NAME)}"
    )
    rule()

    # load whisper
    print(f"\n  Loading Whisper...")
    get_model()
    ok("Whisper ready")
    # warm up scipy resampler — kills JIT hit on first sentence
    resample(
        np.zeros(int(RECORD_SAMPLE_RATE * 0.02), dtype=np.float32),
        RECORD_SAMPLE_RATE,
        WHISPER_SAMPLE_RATE,
    )
    ok("Resampler warmed up")

    results: list[dict] = [None] * len(SENTENCES)

    for idx in indices:
        sentence = SENTENCES[idx]
        path = wav_path(idx)

        # decide: record or load
        if args.replay and not path.exists():
            warn(f"[{idx+1}] No recording found at {path.name} — skipping")
            continue

        if args.record or not path.exists():
            # record mode
            if args.replay:
                warn(f"[{idx+1}] --replay set but no file — skipping")
                continue
            if not path.exists():
                info(f"[{idx+1}] No recording found — recording now")
            audio = record_sentence(idx, sentence)
        else:
            info(f"[{idx+1}] Loading saved recording: {path.name}")
            audio = load_sentence(idx)

        # benchmark
        r = benchmark_sentence(idx, audio)
        results[idx] = r
        print_result(idx, r)
        rule()

    # summary over completed results
    completed = [r for r in results if r is not None]
    if len(completed) > 1:
        print_summary(completed)
    elif len(completed) == 1:
        # single sentence — still show estimate
        r = completed[0]
        pause_ms = PAUSE_SECONDS * 1000
        est = pause_ms + r["whisper_ms"]
        print(
            f"\n  Felt latency estimate: {pause_ms:.0f}ms (pause) + {r['whisper_ms']:.0f}ms (whisper) = {c(Fore.CYAN, f'{est:.0f}ms')}"
        )


if __name__ == "__main__":
    main()
