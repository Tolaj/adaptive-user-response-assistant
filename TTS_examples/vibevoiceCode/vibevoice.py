"""
VibeVoice Realtime 0.5B — Interactive TTS
Wraps the official demo/streaming_inference_from_file.py pattern exactly.

─── ONE-TIME SETUP ──────────────────────────────────────────────
git clone https://github.com/vibevoice-community/VibeVoice.git
cd VibeVoice
pip install -e .
─────────────────────────────────────────────────────────────────

Run FROM the VibeVoice directory:
    python ../vibevoice.py                           # interactive loop
    python ../vibevoice.py "Hello, how are you?"     # one-shot
    python ../vibevoice.py "Hi" --voice Carter       # pick a voice
    python ../vibevoice.py "Hi" --steps 10           # more quality
    python ../vibevoice.py "Hi" --save output.wav    # save to file

Available voices: Carter Davis Emma Frank Grace Mike Samuel
(and multilingual ones if you downloaded them)
"""

import sys
import os
import argparse
import tempfile
import numpy as np
import soundfile as sf
import sounddevice as sd
from pathlib import Path

MODEL_ID = "microsoft/VibeVoice-Realtime-0.5B"
SAMPLE_RATE = 24_000


def find_vibevoice_root() -> Path:
    candidates = [Path.cwd()]
    d = Path(__file__).resolve().parent
    for _ in range(5):
        candidates.append(d)
        d = d.parent
    candidates.append(Path.home() / "VibeVoice")
    for p in candidates:
        if (p / "vibevoice").is_dir() and (p / "vibevoice" / "__init__.py").exists():
            return p
    return None


def ensure_importable():
    root = find_vibevoice_root()
    if root is None:
        print("[vibevoice] ERROR: VibeVoice repo not found.")
        print("  git clone https://github.com/vibevoice-community/VibeVoice.git")
        print("  cd VibeVoice && pip install -e .")
        sys.exit(1)
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    return root


def load_model(device="cpu"):
    import torch
    from vibevoice.modular.modeling_vibevoice_streaming_inference import (
        VibeVoiceStreamingForConditionalGenerationInference,
    )
    from vibevoice.processor.vibevoice_processor import VibeVoiceProcessor

    print(f"[vibevoice] Loading {MODEL_ID} …")
    processor = VibeVoiceProcessor.from_pretrained(MODEL_ID)

    model = VibeVoiceStreamingForConditionalGenerationInference.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float32,
    ).to(device)
    model.eval()

    # The tokenizer lives inside the processor — no need to load it separately.
    # AutoTokenizer fails because it tries to resolve 'vibevoice_streaming' config.
    tokenizer = processor.tokenizer

    print("[vibevoice] Ready.\n")
    return model, processor, tokenizer


def load_voices(vibevoice_root: Path, device="cpu") -> dict:
    import torch

    voices_dir = vibevoice_root / "demo" / "voices" / "streaming_model"
    voices = {}
    if voices_dir.exists():
        for pt in sorted(voices_dir.glob("*.pt")):
            voices[pt.stem] = torch.load(pt, map_location=device, weights_only=False)
        print(f"[vibevoice] Voices: {', '.join(voices.keys())}")
    else:
        print(f"[vibevoice] WARNING: no voices found at {voices_dir}")
    return voices


def generate(
    model,
    processor,
    tokenizer,
    voices,
    text,
    voice_name="Carter",
    ddpm_steps=5,
    cfg_scale=1.5,
    device="cpu",
):
    import torch

    # Resolve voice embedding
    voice_key = next((k for k in voices if k.lower() == voice_name.lower()), None)
    if voice_key is None and voices:
        voice_key = next(iter(voices))
        print(f"[vibevoice] Voice '{voice_name}' not found, using '{voice_key}'")
    speaker_emb = voices.get(voice_key)

    # Format as "Speaker 1: ..." if plain text
    script = text if text.strip().startswith("Speaker") else f"Speaker 1: {text}"
    inputs = processor(text=script, return_tensors="pt")
    print(f"[debug] processor keys: {list(inputs.keys())}")

    # Move each tensor to device individually (avoid .to() on BatchEncoding with None values)
    inputs_on_device = {
        k: v.to(device) if hasattr(v, "to") else v for k, v in inputs.items()
    }

    with torch.no_grad():
        output = model.generate(
            **inputs_on_device,
            tokenizer=tokenizer,
            speaker_embeddings=speaker_emb,
            ddpm_steps=ddpm_steps,
            cfg_scale=cfg_scale,
        )

    return output.squeeze().cpu().float().numpy()


def play(audio: np.ndarray):
    peak = np.abs(audio).max()
    if peak > 0:
        audio = audio / peak
    pad = np.zeros(int(SAMPLE_RATE * 0.5), dtype=np.float32)
    audio = np.concatenate([audio.astype(np.float32), pad])
    sd.play(audio, samplerate=SAMPLE_RATE, blocking=True)


def main():
    parser = argparse.ArgumentParser(description="VibeVoice Realtime 0.5B")
    parser.add_argument("text", nargs="?", default=None)
    parser.add_argument("--voice", "-v", default="Carter")
    parser.add_argument("--steps", "-s", type=int, default=5)
    parser.add_argument("--cfg", type=float, default=1.5)
    parser.add_argument("--device", "-d", default="cpu", choices=["cpu", "cuda", "mps"])
    parser.add_argument("--save", default=None, metavar="FILE")
    parser.add_argument("--list-voices", action="store_true")
    args = parser.parse_args()

    root = ensure_importable()
    model, processor, tokenizer = load_model(args.device)
    voices = load_voices(root, args.device)

    if args.list_voices:
        print("Voices:", ", ".join(voices.keys()) if voices else "none found")
        return

    def speak(text):
        if not text.strip():
            return
        print("[vibevoice] Generating …")
        audio = generate(
            model,
            processor,
            tokenizer,
            voices,
            text,
            voice_name=args.voice,
            ddpm_steps=args.steps,
            cfg_scale=args.cfg,
            device=args.device,
        )
        if args.save:
            sf.write(args.save, audio, SAMPLE_RATE)
            print(f"[vibevoice] Saved → {args.save}\n")
        else:
            print(f"[vibevoice] ▶  {text!r}")
            play(audio)
            print("[vibevoice] Done.\n")

    if args.text:
        speak(args.text)
    else:
        print(f"Interactive mode (voice={args.voice}  steps={args.steps})")
        print("Type text and press Enter.  Ctrl-C to quit.\n")
        while True:
            try:
                speak(input("Text: ").strip())
            except KeyboardInterrupt:
                print("\n[vibevoice] Bye!")
                sys.exit(0)


if __name__ == "__main__":
    main()
