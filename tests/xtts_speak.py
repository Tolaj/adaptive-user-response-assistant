"""
XTTS v2 — Optimized for speed on Apple M3
- Pre-computed voice embeddings (saved to disk)
- Text chunking + streaming playback
- Shorter first chunk for faster first audio
- Multi-sample voice cloning

Install:
    pip install TTS huggingface_hub sounddevice scipy numpy torch torchaudio==2.3.0

Usage:
    # First run — computes & saves embedding
    python xtts_speak.py --speaker_wavs v1.wav v2.wav v3.wav v4.wav

    # After first run — loads saved embedding instantly
    python xtts_speak.py

    # Single text
    python xtts_speak.py --text "Hey, I missed you today"
"""

import argparse
import glob
import os
import queue
import re
import sys
import threading
import time
import numpy as np
import torch

# ── Dependency checks ─────────────────────────────────────────────────────────
try:
    from huggingface_hub import snapshot_download
except ImportError:
    sys.exit("Run: pip install huggingface_hub")

try:
    from TTS.tts.configs.xtts_config import XttsConfig
    from TTS.tts.models.xtts import Xtts
except ImportError:
    sys.exit("Run: pip install TTS")

try:
    import sounddevice as sd
    import scipy.io.wavfile as wavfile
except ImportError:
    sys.exit("Run: pip install sounddevice scipy")

# ── Constants ─────────────────────────────────────────────────────────────────
HF_REPO_ID = "coqui/XTTS-v2"
MODEL_DIR = os.path.expanduser("./models/xtts/XTTS-v2")
EMBEDDING_FILE = "voice_embedding.pt"
OUTPUT_FILE = "output.wav"
SAMPLE_RATE = 24000
DEFAULT_LANG = "en"
DEVICE = "cpu"  # MPS too buggy for XTTS; CPU is stable on M3


# ── Sensual text formatter ────────────────────────────────────────────────────
def format_sensual(text: str) -> str:
    text = text.strip()
    sentences = re.split(r"(?<=[.!?…])\s+", text)
    result = []
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        s = s.replace("!", ".")
        if s[-1] not in ".?…,":
            s += "..."
        elif s[-1] == ".":
            s = s[:-1] + "..."
        result.append(s)
    return "\n\n".join(result)


# ── Text chunker ──────────────────────────────────────────────────────────────
def chunk_text(text: str, max_chars: int = 120) -> list[str]:
    """
    Split text into short chunks at sentence boundaries.
    Shorter chunks = faster first audio output.
    """
    # Split on sentence endings
    raw = re.split(r"(?<=[.!?…,])\s+", text)
    chunks = []
    current = ""
    for part in raw:
        part = part.strip()
        if not part:
            continue
        if len(current) + len(part) <= max_chars:
            current = (current + " " + part).strip()
        else:
            if current:
                chunks.append(current)
            current = part
    if current:
        chunks.append(current)
    return chunks if chunks else [text]


# ── Download ──────────────────────────────────────────────────────────────────
def download_model():
    if os.path.isfile(os.path.join(MODEL_DIR, "config.json")):
        print(f"[✓] Using cached model at {MODEL_DIR}")
        return
    print(f"[↓] Downloading {HF_REPO_ID} to {MODEL_DIR} ...")
    snapshot_download(
        repo_id=HF_REPO_ID, local_dir=MODEL_DIR, local_dir_use_symlinks=False
    )
    print("[✓] Download complete.")


# ── Load model ────────────────────────────────────────────────────────────────
def load_model():
    config_path = os.path.join(MODEL_DIR, "config.json")
    if not os.path.isfile(config_path):
        sys.exit(f"[✗] config.json not found in {MODEL_DIR}")

    print("[…] Loading XTTS-v2 model ...")
    t0 = time.time()
    config = XttsConfig()
    config.load_json(config_path)
    model = Xtts.init_from_config(config)

    # PyTorch 2.6 weights_only fix
    _orig = torch.load
    torch.load = lambda *a, **kw: _orig(*a, **{**kw, "weights_only": False})
    model.load_checkpoint(config, checkpoint_dir=MODEL_DIR, eval=True)
    torch.load = _orig

    model.to(DEVICE)
    print(f"[✓] Model loaded in {time.time()-t0:.1f}s on {DEVICE.upper()}.")
    return model, config


# ── Voice embedding ───────────────────────────────────────────────────────────
def compute_embedding(model, wav_paths: list[str]):
    print(f"[🎙] Computing embedding from {len(wav_paths)} sample(s)...")
    all_gpt, all_spk = [], []
    for p in wav_paths:
        print(f"     • {os.path.basename(p)}")
        gpt, spk = model.get_conditioning_latents(
            audio_path=p,
            gpt_cond_len=10,
            gpt_cond_chunk_len=4,
            max_ref_length=60,
        )
        all_gpt.append(gpt)
        all_spk.append(spk)

    avg_gpt = torch.stack(all_gpt).mean(dim=0)
    avg_spk = torch.stack(all_spk).mean(dim=0)
    avg_spk = avg_spk / avg_spk.norm()

    torch.save({"gpt": avg_gpt, "spk": avg_spk, "sources": wav_paths}, EMBEDDING_FILE)
    print(f"[✓] Embedding saved → {EMBEDDING_FILE}")
    return avg_gpt, avg_spk


def load_embedding():
    data = torch.load(EMBEDDING_FILE, weights_only=False)
    print(f"[✓] Loaded saved embedding ({len(data['sources'])} source(s))")
    return data["gpt"], data["spk"]


def get_embedding(model, wav_paths):
    if not wav_paths and os.path.isfile(EMBEDDING_FILE):
        return load_embedding()
    if not wav_paths:
        sys.exit(
            "[✗] No embedding found. Provide --speaker_wavs or --speaker_dir on first run."
        )
    return compute_embedding(model, wav_paths)


# ── Synthesise one chunk ──────────────────────────────────────────────────────
def synthesize_chunk(model, gpt_cond_latent, speaker_embedding, text: str, lang: str):
    out = model.inference(
        text,
        lang,
        gpt_cond_latent,
        speaker_embedding,
        temperature=0.85,
        length_penalty=1.0,
        repetition_penalty=2.0,
        top_k=50,
        top_p=0.85,
        enable_text_splitting=False,  # we handle splitting ourselves
    )
    audio = np.array(out["wav"], dtype=np.float32)
    # Pad end to prevent cutoff
    padding = np.zeros(int(SAMPLE_RATE * 0.3), dtype=np.float32)
    return np.concatenate([audio, padding])


# ── Streaming speak ───────────────────────────────────────────────────────────
def speak(
    model,
    gpt_cond_latent,
    speaker_embedding,
    text: str,
    lang: str,
    do_format: bool = True,
):
    if do_format:
        text = format_sensual(text)
        print(
            f"\n── Formatted ──────────────────────────────────\n{text}\n───────────────────────────────────────────────\n"
        )

    chunks = chunk_text(text)
    print(f"[i] {len(chunks)} chunk(s) → streaming playback")

    audio_queue = queue.Queue()
    all_audio = []

    # ── Producer: generate chunks in background ───────────────────────────────
    def producer():
        for i, chunk in enumerate(chunks):
            t0 = time.time()
            audio = synthesize_chunk(
                model, gpt_cond_latent, speaker_embedding, chunk, lang
            )
            elapsed = time.time() - t0
            print(
                f"[{i+1}/{len(chunks)}] generated in {elapsed:.1f}s — '{chunk[:50]}...' "
                if len(chunk) > 50
                else f"[{i+1}/{len(chunks)}] generated in {elapsed:.1f}s — '{chunk}'"
            )
            audio_queue.put(audio)
        audio_queue.put(None)  # sentinel

    # ── Consumer: play chunks as they arrive ──────────────────────────────────
    def consumer():
        while True:
            audio = audio_queue.get()
            if audio is None:
                break
            all_audio.append(audio)
            sd.play(audio, samplerate=SAMPLE_RATE)
            sd.wait()

    t_start = time.time()
    prod = threading.Thread(target=producer, daemon=True)
    prod.start()
    consumer()
    prod.join()

    # Save full audio
    print(f"[✓] Done  |  total time: {time.time()-t_start:.1f}s")


# ── Interactive loop ──────────────────────────────────────────────────────────
def interactive_loop(model, gpt_cond_latent, speaker_embedding, lang):
    print("\n── XTTS-v2 Interactive Mode ──────────────────────────────────")
    print("Streaming enabled. First audio plays as soon as first chunk is ready.")
    print("Commands: 'raw' = toggle formatting | 'quit' = exit\n")

    do_format = True
    while True:
        try:
            text = input("▶ ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break
        if not text:
            continue
        if text.lower() in ("quit", "exit", "q"):
            print("Bye!")
            break
        if text.lower() == "raw":
            do_format = not do_format
            print(f"[i] Auto-formatting {'ON' if do_format else 'OFF'}")
            continue
        speak(model, gpt_cond_latent, speaker_embedding, text, lang, do_format)


# ── Resolve wav list ──────────────────────────────────────────────────────────
def resolve_wavs(speaker_wavs, speaker_wav, speaker_dir):
    wavs = []
    if speaker_wavs:
        wavs = list(speaker_wavs)
    elif speaker_dir:
        wavs = sorted(glob.glob(os.path.join(speaker_dir, "*.wav")))
        if not wavs:
            sys.exit(f"[✗] No .wav files found in {speaker_dir}")
    elif speaker_wav:
        wavs = [speaker_wav]
    for w in wavs:
        if not os.path.isfile(w):
            sys.exit(f"[✗] File not found: {w}")
    if wavs:
        print(f"[✓] {len(wavs)} voice sample(s) provided — will recompute embedding.")
    return wavs


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="XTTS-v2 Optimized TTS")
    parser.add_argument("--speaker_wavs", nargs="+", default=None)
    parser.add_argument("--speaker_dir", type=str, default=None)
    parser.add_argument("--speaker_wav", type=str, default=None)
    parser.add_argument("--text", type=str, default=None)
    parser.add_argument("--lang", type=str, default=DEFAULT_LANG)
    parser.add_argument("--no-format", action="store_true")
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=120,
        help="Max chars per chunk (smaller = faster first audio, default 120)",
    )
    args = parser.parse_args()

    download_model()
    model, config = load_model()

    wavs = resolve_wavs(args.speaker_wavs, args.speaker_wav, args.speaker_dir)
    gpt_cond_latent, speaker_embedding = get_embedding(model, wavs)

    do_format = not args.no_format

    if args.text:
        speak(
            model, gpt_cond_latent, speaker_embedding, args.text, args.lang, do_format
        )
    else:
        interactive_loop(model, gpt_cond_latent, speaker_embedding, args.lang)


if __name__ == "__main__":
    main()
