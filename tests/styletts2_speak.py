"""
StyleTTS2 — Fast Voice Cloning TTS for Apple M3
- Multi-sample voice cloning with averaged ref_s embeddings
- Pre-computed embeddings saved to disk
- Text chunking + streaming playback
- Sensual/intimate text auto-formatter

Install:
    pip install styletts2 sounddevice scipy numpy torch librosa

Usage:
    # First run — compute & save embedding from wav samples
    python styletts2_speak.py --speaker_wavs v1.wav v2.wav v3.wav v4.wav

    # Or point to a folder
    python styletts2_speak.py --speaker_dir ./my_samples/

    # After first run — embedding saved, just run:
    python styletts2_speak.py

    # Single line
    python styletts2_speak.py --text "Hey, I missed you today"
"""

import argparse
import glob
import os
import queue
import re
import sys
import tempfile
import threading
import time
import numpy as np
import torch

# ── Dependency checks ─────────────────────────────────────────────────────────
try:
    from styletts2 import tts as styletts2_tts
except ImportError:
    sys.exit("Run: pip install styletts2")

try:
    import sounddevice as sd
    import scipy.io.wavfile as wavfile
except ImportError:
    sys.exit("Run: pip install sounddevice scipy")

try:
    import librosa
    import soundfile as sf
except ImportError:
    sys.exit("Run: pip install librosa soundfile")

# ── Constants ─────────────────────────────────────────────────────────────────
MODEL_DIR      = "./models/styletts2"
EMBEDDING_FILE = "voice_embedding.pt"
SAMPLE_RATE    = 24000
DEVICE         = (
    "mps"  if torch.backends.mps.is_available()
    else "cuda" if torch.cuda.is_available()
    else "cpu"
)

# ── Audio preprocessing ───────────────────────────────────────────────────────
def preprocess_wav(wav_path: str) -> str:
    """
    Resample and convert wav to 24kHz mono — required by StyleTTS2.
    Returns path to a temp file if conversion needed, else original path.
    """
    audio, sr = librosa.load(wav_path, sr=SAMPLE_RATE, mono=True)
    # Write to temp file
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(tmp.name, audio, SAMPLE_RATE)
    return tmp.name

# ── Sensual text formatter ────────────────────────────────────────────────────
def format_sensual(text: str) -> str:
    text = text.strip()
    sentences = re.split(r'(?<=[.!?…])\s+', text)
    result = []
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        s = s.replace('!', '.')
        if s[-1] not in '.?…,':
            s += '...'
        elif s[-1] == '.':
            s = s[:-1] + '...'
        result.append(s)
    return '\n\n'.join(result)

# ── Text chunker ──────────────────────────────────────────────────────────────
def chunk_text(text: str, max_chars: int = 120) -> list[str]:
    raw = re.split(r'(?<=[.!?…,])\s+|\n+', text)
    chunks, current = [], ""
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

# ── Load model ────────────────────────────────────────────────────────────────
def load_model():
    os.makedirs(MODEL_DIR, exist_ok=True)
    print(f"[…] Loading StyleTTS2 on {DEVICE.upper()} ...")
    t0 = time.time()
    tts = styletts2_tts.StyleTTS2()
    print(f"[✓] Model loaded in {time.time()-t0:.1f}s")
    return tts

# ── Voice embedding ───────────────────────────────────────────────────────────
def compute_embedding(tts, wav_paths: list[str]):
    print(f"[🎙] Computing embedding from {len(wav_paths)} sample(s)...")
    all_refs = []
    tmp_files = []

    for p in wav_paths:
        print(f"     • {os.path.basename(p)} (resampling to 24kHz mono...)")
        tmp_path = preprocess_wav(p)
        tmp_files.append(tmp_path)
        try:
            ref = tts.compute_style(tmp_path)
            all_refs.append(ref.clone().detach())
            print(f"     ✓ embedding extracted")
        except Exception as e:
            print(f"     [!] Error: {e}")

    for f in tmp_files:
        try:
            os.unlink(f)
        except:
            pass

    if not all_refs:
        print("[!] Could not extract embeddings — using fallback.")
        torch.save({"ref_s": None, "fallback": wav_paths[0], "sources": wav_paths}, EMBEDDING_FILE)
        return None, wav_paths[0]

    avg_ref = torch.stack(all_refs).mean(dim=0)
    torch.save({"ref_s": avg_ref, "fallback": None, "sources": wav_paths}, EMBEDDING_FILE)
    print(f"[✓] Averaged embedding from {len(all_refs)} sample(s) → {EMBEDDING_FILE}")
    return avg_ref, None

def load_embedding():
    data = torch.load(EMBEDDING_FILE, weights_only=False)
    print(f"[✓] Loaded saved embedding ({len(data['sources'])} source(s))")
    return data["ref_s"], data.get("fallback")

def get_embedding(tts, wav_paths):
    if not wav_paths and os.path.isfile(EMBEDDING_FILE):
        return load_embedding()
    if not wav_paths:
        sys.exit("[✗] No embedding found. Provide --speaker_wavs or --speaker_dir on first run.")
    return compute_embedding(tts, wav_paths)

# ── Synthesise one chunk ──────────────────────────────────────────────────────
def synthesize_chunk(tts, ref_s, fallback_wav, text: str,
                     diffusion_steps: int = 5,
                     alpha: float = 0.3,
                     beta: float = 0.7,
                     embedding_scale: float = 1.5):
    kwargs = dict(
        diffusion_steps=diffusion_steps,
        alpha=alpha,
        beta=beta,
        embedding_scale=embedding_scale,
        output_sample_rate=SAMPLE_RATE,
    )
    if ref_s is not None:
        kwargs["ref_s"] = ref_s
    elif fallback_wav:
        tmp_path = preprocess_wav(fallback_wav)
        kwargs["target_voice_path"] = tmp_path

    audio = tts.inference(text, **kwargs)

    if fallback_wav and "target_voice_path" in kwargs:
        try:
            os.unlink(kwargs["target_voice_path"])
        except:
            pass

    audio = np.array(audio, dtype=np.float32)
    if audio.max() > 0:
        audio = audio / audio.max() * 0.95
    # Pad to prevent cutoff
    padding = np.zeros(int(SAMPLE_RATE * 0.3), dtype=np.float32)
    return np.concatenate([audio, padding])

# ── Streaming speak ───────────────────────────────────────────────────────────
def speak(tts, ref_s, fallback_wav, text: str,
          do_format: bool = True,
          diffusion_steps: int = 5,
          alpha: float = 0.3,
          beta: float = 0.7,
          embedding_scale: float = 1.5,
          chunk_size: int = 120):

    if do_format:
        text = format_sensual(text)
        print(f"\n── Formatted ──────────────────────────────────\n{text}\n───────────────────────────────────────────────\n")

    chunks = chunk_text(text, max_chars=chunk_size)
    print(f"[i] {len(chunks)} chunk(s) → streaming playback")

    audio_queue = queue.Queue()
    t_start = time.time()

    def producer():
        for i, chunk in enumerate(chunks):
            t0 = time.time()
            audio = synthesize_chunk(tts, ref_s, fallback_wav, chunk,
                                     diffusion_steps, alpha, beta, embedding_scale)
            elapsed = time.time() - t0
            label = f"'{chunk[:50]}...'" if len(chunk) > 50 else f"'{chunk}'"
            print(f"[{i+1}/{len(chunks)}] {elapsed:.2f}s — {label}")
            audio_queue.put(audio)
        audio_queue.put(None)

    def consumer():
        while True:
            audio = audio_queue.get()
            if audio is None:
                break
            sd.play(audio, samplerate=SAMPLE_RATE)
            sd.wait()

    prod = threading.Thread(target=producer, daemon=True)
    prod.start()
    consumer()
    prod.join()
    print(f"[✓] Done  |  total: {time.time()-t_start:.1f}s")

# ── Resolve wav list ──────────────────────────────────────────────────────────
def resolve_wavs(speaker_wavs, speaker_wav, speaker_dir):
    wavs = []
    if speaker_wavs:
        wavs = list(speaker_wavs)
    elif speaker_dir:
        wavs = sorted(glob.glob(os.path.join(speaker_dir, "*.wav")))
        if not wavs:
            sys.exit(f"[✗] No .wav files in {speaker_dir}")
    elif speaker_wav:
        wavs = [speaker_wav]
    for w in wavs:
        if not os.path.isfile(w):
            sys.exit(f"[✗] File not found: {w}")
    if wavs:
        if len(wavs) < 4:
            print(f"[!] {len(wavs)} sample(s) — 4+ recommended for best quality.")
        else:
            print(f"[✓] {len(wavs)} voice samples loaded.")
    return wavs

# ── Interactive loop ──────────────────────────────────────────────────────────
def interactive_loop(tts, ref_s, fallback_wav, args):
    print("\n── StyleTTS2 Interactive Mode ────────────────────────────────")
    print(f"Device: {DEVICE.upper()} | steps={args.steps} | alpha={args.alpha} | beta={args.beta} | scale={args.scale}")
    print("Commands: 'raw' = toggle formatting | 'quit' = exit\n")

    do_format = not args.no_format
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
        speak(tts, ref_s, fallback_wav, text,
              do_format=do_format,
              diffusion_steps=args.steps,
              alpha=args.alpha,
              beta=args.beta,
              embedding_scale=args.scale,
              chunk_size=args.chunk_size)

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="StyleTTS2 Fast Voice Cloning TTS")
    parser.add_argument("--speaker_wavs", nargs="+", default=None)
    parser.add_argument("--speaker_dir",  type=str,  default=None)
    parser.add_argument("--speaker_wav",  type=str,  default=None)
    parser.add_argument("--text",         type=str,  default=None)
    parser.add_argument("--no-format",    action="store_true")
    parser.add_argument("--steps",        type=int,   default=5,
                        help="Diffusion steps: 3=fastest, 10=best (default: 5)")
    parser.add_argument("--alpha",        type=float, default=0.3,
                        help="Timbre: 0=clone voice, 1=model default (default: 0.3)")
    parser.add_argument("--beta",         type=float, default=0.7,
                        help="Prosody: 0=clone voice, 1=model default (default: 0.7)")
    parser.add_argument("--scale",        type=float, default=1.5,
                        help="Expressiveness scale (default: 1.5)")
    parser.add_argument("--chunk-size",   type=int,   default=120)
    args = parser.parse_args()

    tts = load_model()
    wavs = resolve_wavs(args.speaker_wavs, args.speaker_wav, args.speaker_dir)
    ref_s, fallback_wav = get_embedding(tts, wavs)

    if args.text:
        speak(tts, ref_s, fallback_wav, args.text,
              do_format=not args.no_format,
              diffusion_steps=args.steps,
              alpha=args.alpha,
              beta=args.beta,
              embedding_scale=args.scale,
              chunk_size=args.chunk_size)
    else:
        interactive_loop(tts, ref_s, fallback_wav, args)

if __name__ == "__main__":
    main()