"""
tests/benchmark_runtime.py — Runtime STT benchmark for AURA

Tests the FULL real pipeline exactly as it runs in production:
  Mic → Silero VAD → Preroll → Buffer → Whisper → Transcript

Scenarios:
  1. Single clean utterance
  2. Interrupting yourself mid-sentence
  3. Long pause mid-sentence then continuing
  4. Multiple sentences back to back
  5. Loud then quiet speech
  6. Speech with background music

Metrics per scenario:
  - EOS latency (stop speaking → transcript appears)
  - Sentence capture (was full sentence transcribed)
  - VAD accuracy (triggered correctly, no false starts)
  - Partial appearances (did partials show during speech)
  - False triggers on silence between sentences

Usage:
    python tests/benchmark_runtime.py
    python tests/benchmark_runtime.py --scenario 1   # run single test
"""

import sys
import time
import argparse
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import jiwer
from colorama import Fore, Style, init as colorama_init

colorama_init()

from config.vad import (
    RECORD_SAMPLE_RATE,
    ENERGY_THRESHOLD,
    PAUSE_SECONDS,
    MIN_SPEECH_SEC,
    PREROLL_SECONDS,
)
from transcription.model.singleton import get_model
from transcription.vad.state import create_vad_state, reset_vad_state
from transcription.stream import (
    create_stream,
    start_stream,
    stop_stream,
    feed,
    end_of_speech,
    clear_stream,
)
from transcription.vad.session import run_mic_session


# ── Colours ───────────────────────────────────────────────────
def ok(msg):
    print(f"  {Fore.GREEN}✓{Style.RESET_ALL}  {msg}")


def fail(msg):
    print(f"  {Fore.RED}✗{Style.RESET_ALL}  {msg}")


def info(msg):
    print(f"  {Fore.CYAN}→{Style.RESET_ALL}  {msg}")


def warn(msg):
    print(f"  {Fore.YELLOW}!{Style.RESET_ALL}  {msg}")


def head(msg):
    print(f"\n  {Fore.YELLOW}{msg}{Style.RESET_ALL}")


def normalise(text: str) -> str:
    import re

    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    text = text.replace("i'll", "i will").replace("i'm", "i am")
    text = text.replace("9am", "nine am").replace("9 am", "nine am")
    return text


def wer_score(ref: str, hyp: str) -> float:
    if not hyp:
        return 1.0
    return jiwer.wer(normalise(ref), normalise(hyp))


def countdown(n: int, msg: str = "") -> None:
    if msg:
        print(f"  {msg}")
    for i in range(n, 0, -1):
        print(f"\r  {Fore.RED}Starting in {i}...{Style.RESET_ALL}", end="", flush=True)
        time.sleep(1)
    print("\r" + " " * 30 + "\r", end="")


# ── Runtime session runner ────────────────────────────────────


class RuntimeSession:
    """
    Runs the real AURA pipeline for a fixed duration.
    Collects all events: partials, finals, VAD triggers, latencies.
    """

    def __init__(self, duration: float):
        self.duration = duration
        self.partials: list[tuple[float, str]] = []  # (time, text)
        self.finals: list[tuple[float, str]] = []  # (time, text)
        self.speech_starts: list[float] = []
        self.speech_ends: list[float] = []
        self.eos_latencies: list[float] = []
        self._t0 = None
        self._speech_end_time = None
        self._stream = None
        self._vad_state = None
        self._done = threading.Event()

    def _t(self) -> float:
        return time.time() - self._t0

    def run(self) -> None:
        self._t0 = time.time()

        def on_partial(text: str) -> None:
            self.partials.append((self._t(), text))

        def on_final(text: str) -> None:
            self.finals.append((self._t(), text))

        self._stream = create_stream(on_partial=on_partial, on_final=on_final)
        start_stream(self._stream)
        self._vad_state = create_vad_state(RECORD_SAMPLE_RATE)

        def on_speech_start() -> None:
            self.speech_starts.append(self._t())

        def on_speech_end() -> None:
            self.speech_ends.append(self._t())
            self._speech_end_time = time.time()
            t_start = time.time()
            text = end_of_speech(self._stream)
            latency = time.time() - t_start
            if text:
                self.eos_latencies.append(latency)

            reset_vad_state(self._vad_state)

        # run session in thread, stop after duration
        session_thread = threading.Thread(
            target=run_mic_session,
            kwargs=dict(
                transcriber=self._stream,
                vad_state=self._vad_state,
                on_speech_start=on_speech_start,
                on_speech_end=on_speech_end,
            ),
            daemon=True,
        )

        # patch input() so it returns after duration
        import builtins

        original_input = builtins.input

        def timed_input(prompt=""):
            print(prompt, end="", flush=True)
            self._done.wait(timeout=self.duration)
            print()
            return ""

        builtins.input = timed_input
        session_thread.start()
        session_thread.join(timeout=self.duration + 5)
        builtins.input = original_input
        stop_stream(self._stream)

    def stop(self) -> None:
        self._done.set()

    def summary(self) -> dict:
        return {
            "partials": self.partials,
            "finals": self.finals,
            "speech_starts": self.speech_starts,
            "speech_ends": self.speech_ends,
            "eos_latencies": self.eos_latencies,
        }


def run_scenario(
    name: str,
    instructions: list[str],
    duration: float,
    ref_sentences: list[str],
    expect_finals: int,
    expect_partials: bool,
    expect_no_false_triggers: bool,
    auto: bool = False,
) -> dict:
    head(name)
    print()
    for line in instructions:
        print(f"  {line}")
    print()

    if not auto:
        input(f"  Press ENTER when ready...")

    countdown(3)
    print(f"  {Fore.RED}● RECORDING ({duration}s){Style.RESET_ALL}", flush=True)

    session = RuntimeSession(duration)

    # auto-stop after duration
    def auto_stop():
        time.sleep(duration)
        session.stop()

    threading.Thread(target=auto_stop, daemon=True).start()
    session.run()

    s = session.summary()
    results = {}

    print()
    info(f"Finals received:  {len(s['finals'])}")
    info(f"Partials received: {len(s['partials'])}")
    info(f"Speech starts:    {len(s['speech_starts'])}")
    info(f"Speech ends:      {len(s['speech_ends'])}")
    if s["eos_latencies"]:
        avg_lat = sum(s["eos_latencies"]) / len(s["eos_latencies"])
        info(f"Avg EOS latency:  {avg_lat:.2f}s")
        results["avg_eos_latency"] = avg_lat
        if avg_lat < 1.5:
            ok(f"EOS latency acceptable ({avg_lat:.2f}s)")
            results["latency_ok"] = True
        else:
            fail(f"EOS latency too high ({avg_lat:.2f}s)")
            results["latency_ok"] = False
    else:
        warn("No EOS latency measured — no speech detected")
        results["avg_eos_latency"] = None
        results["latency_ok"] = False

    # finals check
    final_texts = [t for _, t in s["finals"]]
    info(f"Transcriptions:   {final_texts}")

    if len(final_texts) >= expect_finals:
        ok(f"Expected {expect_finals} final(s), got {len(final_texts)}")
        results["finals_ok"] = True
    else:
        fail(f"Expected {expect_finals} final(s), got {len(final_texts)}")
        results["finals_ok"] = False

    seen = set()
    final_texts = [t for t in final_texts if not (t in seen or seen.add(t))]

    # WER against reference sentences
    if ref_sentences and final_texts:
        combined_ref = " ".join(ref_sentences)
        combined_hyp = " ".join(final_texts)
        score = wer_score(combined_ref, combined_hyp)
        info(f"WER: {score:.1%}")
        results["wer"] = score
        if score <= 0.15:
            ok(f"WER acceptable ({score:.1%})")
            results["wer_ok"] = True
        else:
            fail(f"WER too high ({score:.1%})")
            results["wer_ok"] = False
    else:
        results["wer"] = None
        results["wer_ok"] = False

    # partials check
    if expect_partials:
        if s["partials"]:
            ok(f"Partials appeared during speech ({len(s['partials'])} updates)")
            results["partials_ok"] = True
        else:
            fail("No partials appeared during speech")
            results["partials_ok"] = False
    else:
        results["partials_ok"] = True

    # false trigger check
    if expect_no_false_triggers:
        # false trigger = speech_start with no following speech_end or final
        false_count = max(0, len(s["speech_starts"]) - len(s["speech_ends"]))
        if false_count == 0:
            ok("No false VAD triggers detected")
            results["vad_ok"] = True
        else:
            fail(f"{false_count} false VAD trigger(s) detected")
            results["vad_ok"] = False
    else:
        results["vad_ok"] = True

    results["passed"] = all(
        [
            results.get("finals_ok", True),
            results.get("wer_ok", True),
            results.get("latency_ok", True),
            results.get("vad_ok", True),
        ]
    )

    status = Fore.GREEN + "PASS" if results["passed"] else Fore.RED + "FAIL"
    print(f"\n  Result: {status}{Style.RESET_ALL}")
    return results


# ── Scenarios ─────────────────────────────────────────────────


def scenario_single_utterance(auto=False):
    return run_scenario(
        name="SCENARIO 1: Single clean utterance",
        instructions=[
            "Say clearly: 'open the calendar and show me this week'",
            "Then stay silent until recording ends.",
        ],
        duration=8.0,
        ref_sentences=["open the calendar and show me this week"],
        expect_finals=1,
        expect_partials=True,
        expect_no_false_triggers=True,
        auto=auto,
    )


def scenario_self_interrupt(auto=False):
    return run_scenario(
        name="SCENARIO 2: Interrupting yourself mid-sentence",
        instructions=[
            "Start saying: 'send a message to...'",
            "Stop after 2 words, pause 0.5s, then say the full sentence:",
            "'send a message to John saying I will be late'",
        ],
        duration=10.0,
        ref_sentences=["send a message to John saying I will be late"],
        expect_finals=1,
        expect_partials=True,
        expect_no_false_triggers=False,
        auto=auto,
    )


def scenario_long_pause(auto=False):
    return run_scenario(
        name="SCENARIO 3: Long pause mid-sentence then continuing",
        instructions=[
            "Say: 'search the web for'",
            "Pause for 2 seconds",
            "Then say: 'latest AI news'",
            "(Tests whether VAD cuts you off during thinking pauses)",
        ],
        duration=12.0,
        ref_sentences=["search the web for latest AI news"],
        expect_finals=1,
        expect_partials=True,
        expect_no_false_triggers=True,
        auto=auto,
    )


def scenario_multiple_sentences(auto=False):
    return run_scenario(
        name="SCENARIO 4: Multiple sentences back to back",
        instructions=[
            "Say each sentence clearly, pausing 2s between them:",
            "  1. 'what is the weather like today'",
            "  2. 'set a reminder for tomorrow at nine am'",
            "  3. 'turn off the lights in the living room'",
        ],
        duration=20.0,
        ref_sentences=[
            "what is the weather like today",
            "set a reminder for tomorrow at nine am",
            "turn off the lights in the living room",
        ],
        expect_finals=3,
        expect_partials=True,
        expect_no_false_triggers=True,
        auto=auto,
    )


def scenario_loud_quiet(auto=False):
    return run_scenario(
        name="SCENARIO 5: Loud then quiet speech",
        instructions=[
            "Say LOUDLY: 'CALL MOM WHEN YOU GET A CHANCE'",
            "Pause 2s",
            "Say quietly (near whisper): 'how long does it take to drive to the airport'",
        ],
        duration=15.0,
        ref_sentences=[
            "call mom when you get a chance",
            "how long does it take to drive to the airport",
        ],
        expect_finals=2,
        expect_partials=True,
        expect_no_false_triggers=True,
        auto=auto,
    )


def scenario_background_music(auto=False):
    return run_scenario(
        name="SCENARIO 6: Speech with background music",
        instructions=[
            "⚠  Play some music on your speakers first (medium volume)",
            "Then say: 'play some music on spotify'",
            "Then stay silent for 5 seconds",
            "Then say: 'the quick brown fox jumps over the lazy dog'",
        ],
        duration=20.0,
        ref_sentences=[
            "play some music on spotify",
            "the quick brown fox jumps over the lazy dog",
        ],
        expect_finals=2,
        expect_partials=True,
        expect_no_false_triggers=True,
        auto=auto,
    )


SCENARIOS = [
    scenario_single_utterance,
    scenario_self_interrupt,
    scenario_long_pause,
    scenario_multiple_sentences,
    scenario_loud_quiet,
    scenario_background_music,
]

SCENARIO_NAMES = [
    "Single clean utterance",
    "Self-interrupt",
    "Long pause mid-sentence",
    "Multiple sentences back to back",
    "Loud then quiet",
    "Background music",
]


# ── Main ──────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scenario",
        type=int,
        default=0,
        help="Run single scenario by number (1-6). Default: all.",
    )
    parser.add_argument(
        "--auto", action="store_true", help="Skip ENTER prompts between scenarios."
    )
    args = parser.parse_args()

    print(f"\n  Loading Whisper...")
    get_model()
    print(f"  Ready.\n")
    print(f"  Pipeline config:")
    print(f"    PAUSE_SECONDS    = {PAUSE_SECONDS}")
    print(f"    MIN_SPEECH_SEC   = {MIN_SPEECH_SEC}")
    print(f"    PREROLL_SECONDS  = {PREROLL_SECONDS}")
    print(f"    ENERGY_THRESHOLD = {ENERGY_THRESHOLD}")

    if args.scenario:
        idx = args.scenario - 1
        if not 0 <= idx < len(SCENARIOS):
            print(f"  Invalid scenario {args.scenario}. Choose 1-{len(SCENARIOS)}.")
            return
        SCENARIOS[idx](auto=args.auto)
        return

    # run all
    all_results = {}
    for i, (fn, name) in enumerate(zip(SCENARIOS, SCENARIO_NAMES)):
        if not args.auto:
            print(f"\n  ── Scenario {i+1}/{len(SCENARIOS)}: {name} ──")
            ans = input("  Run this scenario? [Y/n]: ").strip().lower()
            if ans == "n":
                print("  Skipped.")
                continue
        all_results[name] = fn(auto=args.auto)

    # summary
    print(f"\n  {'═'*52}")
    print(f"  RUNTIME STT BENCHMARK SUMMARY")
    print(f"  {'═'*52}")
    passed_total = 0
    for name, r in all_results.items():
        status = Fore.GREEN + "PASS" if r["passed"] else Fore.RED + "FAIL"
        wer_str = f"  WER={r['wer']:.1%}" if r.get("wer") is not None else ""
        lat_str = (
            f"  EOS={r['avg_eos_latency']:.2f}s" if r.get("avg_eos_latency") else ""
        )
        print(f"  {status}{Style.RESET_ALL}  {name}{wer_str}{lat_str}")
        if r["passed"]:
            passed_total += 1

    print(f"\n  {passed_total}/{len(all_results)} scenarios passed")

    # recommendations
    print(f"\n  {'─'*52}")
    any_rec = False
    for name, r in all_results.items():
        if not r.get("latency_ok") and r.get("avg_eos_latency"):
            warn(f"High latency in '{name}': consider lowering PAUSE_SECONDS")
            any_rec = True
        if not r.get("vad_ok"):
            warn(f"False VAD triggers in '{name}': consider raising SILERO_THRESHOLD")
            any_rec = True
        if not r.get("finals_ok"):
            warn(f"Missing finals in '{name}': check MIN_SPEECH_SEC or PREROLL_SECONDS")
            any_rec = True
    if not any_rec:
        ok("No configuration changes recommended")
    print()


if __name__ == "__main__":
    main()
