#!/usr/bin/env python3
"""
Voice Clone TTS — powered by mlx-audio + Qwen3-TTS
----------------------------------------------------
Runs natively on Apple Silicon GPU/Neural Engine via MLX.

Setup:
    pip install mlx-audio sounddevice numpy

Usage:
    python voice_clone_tts.py --voice my_voice.wav
    python voice_clone_tts.py --voice my_voice.wav --out output.wav
"""

import argparse
import sys
import os
import threading
import tempfile
from pathlib import Path


def require(pkg, install_name=None):
    import importlib

    try:
        return importlib.import_module(pkg)
    except ImportError:
        name = install_name or pkg
        print(f"[!] Missing package '{name}'. Run:  pip install {name}")
        sys.exit(1)


def load_model():
    from mlx_audio.tts.utils import load_model as mlx_load

    print("[*] Loading Qwen3-TTS via MLX (first run downloads model)…")
    # 0.6B = fast, 1.7B = higher quality — swap if you want more quality
    model = mlx_load("mlx-community/Qwen3-TTS-12Hz-0.6B-Base-bf16")
    print("[*] Model ready — running on Apple Silicon GPU via MLX\n")
    return model


def print_hw_info():
    import subprocess, platform

    if platform.system() == "Darwin":
        try:
            chip = (
                subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"])
                .decode()
                .strip()
            )
            print(f"[*] Chip : {chip}")
            print(f"[*] Backend: MLX (Metal GPU + Neural Engine)")
        except Exception:
            pass


def speak(model, text: str, voice_wav: str, out_path: str | None):
    """Generate audio with voice cloning and either play or save it."""
    import numpy as np

    sd = require("sounddevice")

    print("[…] Generating", end="", flush=True)

    chunks = []
    done = threading.Event()
    error_holder = []

    def producer():
        try:
            import mlx.core as mx

            results = list(
                model.generate(
                    text=text,
                    voice=voice_wav,  # reference wav for cloning
                    language="English",
                )
            )
            for r in results:
                # r.audio is an mx.array — convert to numpy
                audio = np.array(r.audio).astype("float32").ravel()
                peak = np.abs(audio).max()
                if peak > 1.0:
                    audio /= peak
                chunks.append(audio)
        except Exception as e:
            error_holder.append(e)
        finally:
            done.set()

    t = threading.Thread(target=producer, daemon=True)
    t.start()

    while not done.wait(timeout=0.3):
        print(".", end="", flush=True)
    print()

    if error_holder:
        raise error_holder[0]

    if not chunks:
        print("[!] No audio generated.")
        return

    audio = np.concatenate(chunks)

    if out_path:
        import scipy.io.wavfile as wav

        # Qwen3-TTS outputs at 24000 Hz
        wav.write(out_path, 24000, audio)
        print(f"[✓] Saved → {out_path}")
    else:
        print("[✓] Playing…")
        sd.play(audio, samplerate=24000)
        sd.wait()
        print("[✓] Done")


def main():
    parser = argparse.ArgumentParser(
        description="Voice Clone TTS (MLX / Apple Silicon GPU)"
    )
    parser.add_argument(
        "--voice",
        default="my_voice.wav",
        help="Reference voice WAV for cloning (6–30 s)",
    )
    parser.add_argument(
        "--out", default=None, help="Save output here instead of playing"
    )
    args = parser.parse_args()

    voice_path = Path(args.voice)
    if not voice_path.exists():
        print(f"[!] Voice file not found: {voice_path}")
        sys.exit(1)

    require("mlx_audio", "mlx-audio")
    model = load_model()
    print_hw_info()

    print("=" * 50)
    print("  Voice Clone TTS  |  backend=MLX (Apple GPU)")
    print("  type 'quit' to exit")
    print("=" * 50)

    while True:
        try:
            text = input("\n> Enter text: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not text:
            continue
        if text.lower() in ("quit", "exit", "q"):
            print("Bye!")
            break

        try:
            out = args.out
            if out and Path(out).exists():
                import time

                out = f"{Path(out).stem}_{int(time.time())}{Path(out).suffix}"
            speak(model, text, str(voice_path), out)
        except Exception as e:
            print(f"[!] Error: {e}")


if __name__ == "__main__":
    main()
