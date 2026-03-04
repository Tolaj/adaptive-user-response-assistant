"""
tests/benchmark_vad.py — VAD accuracy benchmark for AURA

Tests:
  1. First-word capture    — speaks immediately, checks first word not clipped
  2. Mid-sentence pause    — 1s pause mid-sentence, checks not cut off early
  3. Silence rejection     — 5s silence, checks no false triggers
  4. End-of-speech latency — measures time from stop speaking to final result

Usage:
    python tests/benchmark_vad.py
"""

import sys
import time
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import sounddevice as sd
from colorama import Fore, Style, init as colorama_init

from config.vad import (
    RECORD_SAMPLE_RATE,
    ENERGY_THRESHOLD,
    PAUSE_SECONDS,
    MIN_SPEECH_SEC,
    PREROLL_SECONDS,
)
from config.whisper import WHISPER_SAMPLE_RATE
from audio.transform.resample import resample
from audio.transform.normalise import normalise
from transcription.model.singleton import get_model
from transcription.vad.state import create_vad_state, reset_vad_state
from transcription.vad.processor import process_chunk
from transcription.vad.energy import is_speech_energy
from transcription.stream import create_stream, start_stream, end_of_speech, feed
from transcription.stream.buffer import clear_buffer

colorama_init()

BLOCK = int(RECORD_SAMPLE_RATE * 0.02)  # 20ms chunks — same as mic.py


# ── Recording helpers ─────────────────────────────────────────


def record(seconds: float, label: str) -> np.ndarray:
    print(f"  {Fore.RED}● REC{Style.RESET_ALL}  {label} ({seconds}s)", flush=True)
    audio = sd.rec(
        int(seconds * RECORD_SAMPLE_RATE),
        samplerate=RECORD_SAMPLE_RATE,
        channels=1,
        dtype="float32",
        device=0,
    )
    sd.wait()
    return audio[:, 0]


def countdown(n: int) -> None:
    for i in range(n, 0, -1):
        print(f"\r  Starting in {i}...", end="", flush=True)
        time.sleep(1)
    print("\r" + " " * 25 + "\r", end="")


def split_into_chunks(audio: np.ndarray) -> list[np.ndarray]:
    return [
        audio[i : i + BLOCK]
        for i in range(0, len(audio), BLOCK)
        if len(audio[i : i + BLOCK]) == BLOCK
    ]


# ── Test helpers ──────────────────────────────────────────────


def run_vad_on_audio(
    audio: np.ndarray,
    on_speech_start=None,
    on_speech_end=None,
) -> dict:
    """Feed raw audio through VAD chunk by chunk. Returns event log."""
    state = create_vad_state(RECORD_SAMPLE_RATE)
    events = []
    t0 = time.time()

    for chunk in split_into_chunks(audio):
        t = time.time() - t0
        process_chunk(
            chunk,
            state,
            on_speech_start=lambda: events.append(("start", t)),
            on_speech_end=lambda: events.append(("end", t)),
        )

    return {"events": events, "final_state": state}


def transcribe_audio(audio: np.ndarray) -> tuple[str, float]:
    """Run through real pipeline. Returns (text, latency_seconds)."""
    partials = []
    finals = []

    stream = create_stream(
        on_partial=lambda t: partials.append(t),
        on_final=lambda t: finals.append(t),
    )
    start_stream(stream)

    # feed resampled chunks
    audio_16k = resample(audio, RECORD_SAMPLE_RATE, WHISPER_SAMPLE_RATE)
    audio_16k = normalise(audio_16k)
    feed(stream, audio_16k)

    t0 = time.time()
    text = end_of_speech(stream)
    latency = time.time() - t0

    return text.strip(), latency


def ok(msg):
    print(f"  {Fore.GREEN}✓{Style.RESET_ALL}  {msg}")


def fail(msg):
    print(f"  {Fore.RED}✗{Style.RESET_ALL}  {msg}")


def info(msg):
    print(f"  {Fore.CYAN}→{Style.RESET_ALL}  {msg}")


# ── Tests ─────────────────────────────────────────────────────


def test_first_word_capture() -> dict:
    print(f"\n  {Fore.YELLOW}TEST 1: First-word capture{Style.RESET_ALL}")
    print(f"  Say 'the quick brown fox' IMMEDIATELY when recording starts.")
    countdown(3)
    audio = record(4.0, "speak immediately")

    result = run_vad_on_audio(audio)
    events = result["events"]

    chunks = split_into_chunks(audio)
    first_speech_chunk = next(
        (i for i, c in enumerate(chunks) if is_speech_energy(c)), None
    )
    first_vad_start = next((e[1] for e in events if e[0] == "start"), None)

    first_speech_t = (
        (first_speech_chunk * 0.02) if first_speech_chunk is not None else None
    )
    preroll_t = PREROLL_SECONDS

    text, latency = transcribe_audio(audio)
    info(f"Transcription: '{text}'")
    info(
        f"First energy detected at: {first_speech_t:.3f}s"
        if first_speech_t
        else "No speech energy detected"
    )
    info(
        f"VAD speech_start fired at: {first_vad_start:.3f}s"
        if first_vad_start
        else "VAD never triggered"
    )
    info(f"Preroll buffer: {preroll_t}s")

    passed = text.lower().startswith("the")
    if passed:
        ok("First word captured correctly")
    else:
        fail(f"First word likely clipped — got: '{text}'")

    words = text.lower().split()
    expected = ["the", "quick", "brown", "fox"]
    missing = [w for w in expected if w not in words]
    if missing:
        fail(f"Missing words: {missing}")
    else:
        ok("All expected words present")

    return {"passed": passed, "text": text, "latency": latency}


def test_mid_sentence_pause() -> dict:
    print(f"\n  {Fore.YELLOW}TEST 2: Mid-sentence pause tolerance{Style.RESET_ALL}")
    print(
        f"  Say 'send a message to John'... pause 1 second... then say 'saying I will be late'"
    )
    countdown(3)
    audio = record(7.0, "speak with 1s pause in middle")

    result = run_vad_on_audio(audio)
    events = result["events"]
    end_events = [e for e in events if e[0] == "end"]

    text, latency = transcribe_audio(audio)
    info(f"Transcription: '{text}'")
    info(f"VAD end events fired: {len(end_events)}")
    info(f"PAUSE_SECONDS threshold: {PAUSE_SECONDS}s")

    if len(end_events) == 0:
        ok("VAD did not cut off mid-sentence")
        passed = True
    elif len(end_events) == 1:
        fail(f"VAD cut off at {end_events[0][1]:.2f}s — may have split sentence")
        passed = False
    else:
        fail(f"VAD fired {len(end_events)} end events — too sensitive")
        passed = False

    words = text.lower().split()
    has_both = "message" in words and "late" in words
    if has_both:
        ok("Both halves of sentence captured")
    else:
        fail(f"Sentence appears split — got: '{text}'")

    return {"passed": passed, "text": text, "end_events": len(end_events)}


def test_silence_rejection() -> dict:
    print(f"\n  {Fore.YELLOW}TEST 3: Silence rejection{Style.RESET_ALL}")
    print(f"  Stay COMPLETELY SILENT for 5 seconds.")
    countdown(3)
    audio = record(5.0, "stay silent")

    result = run_vad_on_audio(audio)
    events = result["events"]
    start_events = [e for e in events if e[0] == "start"]

    chunks = split_into_chunks(audio)
    energy_chunks = sum(1 for c in chunks if is_speech_energy(c))
    avg_rms = float(np.mean([np.sqrt(np.mean(c**2)) for c in chunks]))

    text, _ = transcribe_audio(audio)

    info(f"Average RMS: {avg_rms:.5f}  (threshold: {ENERGY_THRESHOLD})")
    info(f"Chunks above energy threshold: {energy_chunks}/{len(chunks)}")
    info(f"VAD start events: {len(start_events)}")
    info(f"Transcription: '{text or '(empty)'}'")

    passed = len(start_events) == 0 and not text
    if passed:
        ok("No false triggers on silence")
    else:
        if start_events:
            fail(
                f"VAD triggered {len(start_events)} times on silence — ENERGY_THRESHOLD too low"
            )
        if text:
            fail(f"Whisper hallucinated on silence: '{text}'")

    return {
        "passed": passed,
        "false_triggers": len(start_events),
        "hallucination": text,
    }


def test_eos_latency() -> dict:
    print(f"\n  {Fore.YELLOW}TEST 4: End-of-speech latency{Style.RESET_ALL}")
    print(f"  Say 'open the calendar and show me this week' then stop speaking.")
    countdown(3)
    audio = record(6.0, "speak then stop")

    result = run_vad_on_audio(audio)
    events = result["events"]

    chunks = split_into_chunks(audio)
    last_speech_chunk = max(
        (i for i, c in enumerate(chunks) if is_speech_energy(c)), default=None
    )
    first_end_event = next((e[1] for e in events if e[0] == "end"), None)

    last_speech_t = (
        (last_speech_chunk * 0.02) if last_speech_chunk is not None else None
    )

    _, transcribe_latency = transcribe_audio(audio)

    if last_speech_t and first_end_event:
        vad_reaction = first_end_event - last_speech_t
        info(f"Last speech energy at: {last_speech_t:.2f}s")
        info(f"VAD end fired at:      {first_end_event:.2f}s")
        info(
            f"VAD reaction time:     {vad_reaction:.2f}s  (PAUSE_SECONDS={PAUSE_SECONDS})"
        )
    else:
        info("Could not compute VAD reaction time")

    info(f"Whisper transcription latency: {transcribe_latency:.2f}s")
    info(f"Total perceived latency: ~{(PAUSE_SECONDS + transcribe_latency):.2f}s")

    passed = transcribe_latency < 2.0
    if passed:
        ok(f"Transcription latency acceptable ({transcribe_latency:.2f}s)")
    else:
        fail(f"Transcription latency too high ({transcribe_latency:.2f}s)")

    return {
        "passed": passed,
        "transcribe_latency": transcribe_latency,
        "vad_reaction": (
            first_end_event - last_speech_t
            if (last_speech_t and first_end_event)
            else None
        ),
    }


# ── Main ──────────────────────────────────────────────────────


def main() -> None:
    print(f"\n  Loading Whisper...")
    get_model()
    print(f"  Ready.\n")
    print(f"  Current VAD config:")
    print(f"    ENERGY_THRESHOLD = {ENERGY_THRESHOLD}")
    print(f"    PAUSE_SECONDS    = {PAUSE_SECONDS}")
    print(f"    MIN_SPEECH_SEC   = {MIN_SPEECH_SEC}")
    print(f"    PREROLL_SECONDS  = {PREROLL_SECONDS}")

    results = {
        "first_word": test_first_word_capture(),
        "mid_pause": test_mid_sentence_pause(),
        "silence": test_silence_rejection(),
        "eos_latency": test_eos_latency(),
    }

    print(f"\n  {'═'*50}")
    print(f"  VAD BENCHMARK SUMMARY")
    print(f"  {'═'*50}")
    for name, r in results.items():
        status = Fore.GREEN + "PASS" if r["passed"] else Fore.RED + "FAIL"
        print(f"  {status}{Style.RESET_ALL}  {name}")

    passed = sum(1 for r in results.values() if r["passed"])
    print(f"\n  {passed}/4 tests passed")

    if results["silence"]["false_triggers"] > 0:
        print(
            f"\n  {Fore.YELLOW}Recommendation:{Style.RESET_ALL} Increase ENERGY_THRESHOLD (currently {ENERGY_THRESHOLD})"
        )
    if (
        results["eos_latency"].get("vad_reaction")
        and results["eos_latency"]["vad_reaction"] > PAUSE_SECONDS + 0.2
    ):
        print(
            f"\n  {Fore.YELLOW}Recommendation:{Style.RESET_ALL} Decrease PAUSE_SECONDS (currently {PAUSE_SECONDS})"
        )
    if not results["first_word"]["passed"]:
        print(
            f"\n  {Fore.YELLOW}Recommendation:{Style.RESET_ALL} Increase PREROLL_SECONDS (currently {PREROLL_SECONDS})"
        )
    print()


if __name__ == "__main__":
    main()
