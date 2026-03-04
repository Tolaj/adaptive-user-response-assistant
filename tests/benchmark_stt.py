"""
benchmark_stt.py — STT accuracy benchmark for AURA
Records each sentence through the real pipeline (VAD, resample, hallucination
filters) then measures WER with jiwer.

Usage:
    python benchmark_stt.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import time
import numpy as np
import sounddevice as sd
import jiwer
from jiwer import wer, mer, wil
from colorama import Fore, Style, init as colorama_init

from config.vad import RECORD_SAMPLE_RATE
from config.whisper import WHISPER_SAMPLE_RATE
from audio.transform.resample import resample
from audio.transform.normalise import normalise
from transcription.model.singleton import get_model
from transcription.stream.final import run_final_pass
from transcription.stream.buffer import create_buffer, append, clear_buffer

colorama_init()

# ── Sentences ─────────────────────────────────────────────────
SENTENCES = [
    "the quick brown fox jumps over the lazy dog",
    "send a message to John saying I will be late",
    "what is the weather like today",
    "set a reminder for tomorrow at nine am",
    "search the web for latest AI news",
    "open the calendar and show me this week",
    "play some music on spotify",
    "how long does it take to drive to the airport",
    "turn off the lights in the living room",
    "call mom when you get a chance",
]

RECORD_SECONDS = 5  # recording window per sentence
COUNTDOWN_SEC = 3  # countdown before each recording


# ── Helpers ───────────────────────────────────────────────────
def countdown(n: int) -> None:
    for i in range(n, 0, -1):
        print(f"\r  Starting in {i}...", end="", flush=True)
        time.sleep(1)
    print("\r" + " " * 20 + "\r", end="")


def record(seconds: int, sr: int) -> np.ndarray:
    print(f"  {Fore.RED}● REC{Style.RESET_ALL}  speak now ({seconds}s)", flush=True)
    audio = sd.rec(
        int(seconds * sr),
        samplerate=sr,
        channels=1,
        dtype="float32",
        device=0,  # add this — MacBook Air Microphone
    )
    sd.wait()
    return audio[:, 0]


def transcribe_chunk(audio: np.ndarray) -> str:
    """Run through the real pipeline: resample → normalise → buffer → final pass."""
    audio_16k = resample(audio, RECORD_SAMPLE_RATE, WHISPER_SAMPLE_RATE)
    audio_16k = normalise(audio_16k)
    buf = create_buffer(WHISPER_SAMPLE_RATE)
    append(buf, audio_16k)
    return run_final_pass(buf).strip().lower()


def normalise_for_wer(text: str) -> str:
    import re

    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    text = text.replace("i'll", "i will")
    text = text.replace("i'm", "i am")
    text = text.replace("it's", "it is")
    text = text.replace("9am", "nine am")
    text = text.replace("9 am", "nine am")
    return text


def diff_line(ref: str, hyp: str) -> str:
    """Colour-coded word diff: green=correct, red=wrong/missing."""
    r = ref.split()
    h = hyp.split() if hyp else []
    out = []
    for i, rw in enumerate(r):
        if i < len(h) and h[i] == rw:
            out.append(Fore.GREEN + rw + Style.RESET_ALL)
        else:
            hw = h[i] if i < len(h) else "_"
            out.append(Fore.RED + f"{rw}→{hw}" + Style.RESET_ALL)
    if len(h) > len(r):
        for extra in h[len(r) :]:
            out.append(Fore.YELLOW + f"+{extra}" + Style.RESET_ALL)
    return " ".join(out)


# ── Main ──────────────────────────────────────────────────────
def main() -> None:
    print(f"\n  Loading Whisper...")
    get_model()
    print(
        f"  Ready. Recording at {RECORD_SAMPLE_RATE} Hz → transcribing at {WHISPER_SAMPLE_RATE} Hz\n"
    )
    print(f"  You will see each sentence. Say it clearly after the beep.\n")

    refs, hyps = [], []
    results = []

    for i, sentence in enumerate(SENTENCES):
        print(f"  ── [{i+1}/{len(SENTENCES)}] ──────────────────────────────")
        print(f"  Say: {Fore.CYAN}{sentence}{Style.RESET_ALL}")
        countdown(COUNTDOWN_SEC)

        audio = record(RECORD_SECONDS, RECORD_SAMPLE_RATE)
        hyp = transcribe_chunk(audio)

        ref_n = normalise_for_wer(sentence)
        hyp_n = normalise_for_wer(hyp) if hyp else ""
        score = wer(ref_n, hyp_n) if hyp_n else 1.0
        refs.append(ref_n)
        hyps.append(hyp_n)

        status = Fore.GREEN + "✓" if score == 0 else Fore.RED + "✗"
        print(f"  Got:  {Fore.YELLOW}{hyp or '(nothing)'}{Style.RESET_ALL}")
        print(f"  WER:  {status}  {score:.0%}{Style.RESET_ALL}")
        print(f"  Diff: {diff_line(sentence, hyp)}")
        results.append((sentence, hyp, score))
        print()

    # ── Summary ───────────────────────────────────────────────
    overall_wer = wer(refs, hyps)
    overall_mer = mer(refs, hyps)
    overall_wil = wil(refs, hyps)

    measures = jiwer.process_words(refs, hyps)

    print("  ══ RESULTS ══════════════════════════════════════")
    print(f"  WER  (Word Error Rate)       {overall_wer:.1%}")
    print(f"  MER  (Match Error Rate)      {overall_mer:.1%}")
    print(f"  WIL  (Word Info Lost)        {overall_wil:.1%}")
    print(f"  Substitutions                {measures.substitutions}")
    print(f"  Deletions                    {measures.deletions}")
    print(f"  Insertions                   {measures.insertions}")

    # worst sentences
    ranked = sorted(results, key=lambda x: x[2], reverse=True)
    print("  ── Worst sentences ──────────────────────────────")
    for ref, hyp, score in ranked[:3]:
        print(f"  {score:.0%}  ref: {ref}")
        print(f"       hyp: {hyp or '(empty)'}")
    print("  ═════════════════════════════════════════════════\n")


if __name__ == "__main__":
    main()
