"""
Soprano TTS — Streaming Playback (Mac, CPU)
ekwek/Soprano-1.1-80M

Install:
    pip install soprano-tts huggingface_hub

Run:
    python soprano_stream.py                   # interactive loop
    python soprano_stream.py "Hello, world!"   # one-shot
"""

import os
import sys
import argparse
import warnings
from pathlib import Path

# MPS crashes on aten::unfold_backward (torch.istft in Vocos decoder) — force CPU
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

REPO_ID = "ekwek/Soprano-1.1-80M"
LOCAL_DIR = Path.home() / ".cache" / "soprano" / "Soprano-1.1-80M"


def download_model() -> str:
    decoder_path = LOCAL_DIR / "decoder.pth"
    if decoder_path.exists():
        print(f"[soprano] Model cached at {LOCAL_DIR}")
        return str(LOCAL_DIR)
    print(f"[soprano] Downloading {REPO_ID} → {LOCAL_DIR} …")
    from huggingface_hub import snapshot_download

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        snapshot_download(repo_id=REPO_ID, local_dir=str(LOCAL_DIR))
    print("[soprano] Download complete.\n")
    return str(LOCAL_DIR)


def load_model(model_dir: str):
    from soprano import SopranoTTS

    print("[soprano] Loading model on CPU …")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # suppress torch.load FutureWarning
        model = SopranoTTS(
            model_path=model_dir,
            device="cpu",  # MPS breaks on istft — CPU only
            backend="transformers",  # lmdeploy doesn't support CPU/MPS
            decoder_batch_size=2,
        )
    print("[soprano] Model ready.\n")
    return model


def speak(model, text: str):
    """
    On CPU, generation is ~20x real-time but sounddevice needs a steady feed.
    Strategy: collect ALL chunks first, then play the complete audio in one shot.
    This gives clean, uninterrupted playback with no buffer underruns.
    """
    import torch
    from soprano.utils.streaming import play_stream

    if not text.strip():
        return

    print(f"[soprano] Generating …")
    stream = model.infer_stream(text, chunk_size=1)

    # Collect all chunks (fast on CPU — 20x real-time means a 5s sentence takes ~0.25s)
    chunks = []
    for chunk in stream:
        chunks.append(chunk.cpu())

    if not chunks:
        return

    # Concatenate and play as a single clean audio tensor via soprano's own player
    audio = torch.cat(chunks)
    print(f"[soprano] ▶  {text!r}")
    play_stream(iter([audio]))  # wrap in iter so play_stream sees a generator
    print("[soprano] Done.\n")


def main():
    parser = argparse.ArgumentParser(description="Soprano TTS — streaming playback")
    parser.add_argument(
        "text",
        nargs="?",
        default=None,
        help="Text to speak (omit for interactive loop)",
    )
    args = parser.parse_args()

    model_dir = download_model()
    model = load_model(model_dir)

    if args.text:
        speak(model, args.text)
    else:
        print("Interactive mode — type text and press Enter.  Ctrl-C to quit.\n")
        while True:
            try:
                text = input("Text: ").strip()
                speak(model, text)
            except KeyboardInterrupt:
                print("\n[soprano] Bye!")
                sys.exit(0)


if __name__ == "__main__":
    main()
