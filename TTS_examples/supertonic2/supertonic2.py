"""
Supertonic 2 — CPU Streaming Playback
onnx-community/Supertonic-TTS-2-ONNX

No PyTorch needed — runs entirely on ONNX Runtime (CPU-native, no MPS issues).

Install:
    pip install onnxruntime transformers huggingface_hub sounddevice soundfile numpy

Run:
    python supertonic2.py                                    # interactive loop
    python supertonic2.py "Hello, world!"                    # one-shot
    python supertonic2.py "Hello!" --voice F1 --lang en      # female voice
    python supertonic2.py "Hola!" --voice M2 --lang es       # Spanish
    python supertonic2.py --list-voices                      # show all voices
    python supertonic2.py "Hi" --steps 15                    # higher quality
    python supertonic2.py "Hi" --save output.wav             # save to file

Voices:   M1 M2 M3 M4 M5  F1 F2 F3 F4 F5
Languages: en ko es pt fr
"""

import os
import sys
import argparse
import warnings
import numpy as np
from pathlib import Path

MODEL_ID = "onnx-community/Supertonic-TTS-2-ONNX"
LOCAL_DIR = Path.home() / ".cache" / "supertonic2"
VOICES = ["M1", "M2", "M3", "M4", "M5", "F1", "F2", "F3", "F4", "F5"]
LANGUAGES = ["en", "ko", "es", "pt", "fr"]


# ─────────────────────────────────────────────────────────
# Download
# ─────────────────────────────────────────────────────────


def download_model() -> str:
    marker = LOCAL_DIR / "onnx" / "text_encoder.onnx"
    if marker.exists():
        print(f"[supertonic2] Model cached at {LOCAL_DIR}")
        return str(LOCAL_DIR)

    print(f"[supertonic2] Downloading {MODEL_ID} → {LOCAL_DIR} …")
    print("[supertonic2] (one-time download, ~200 MB)")
    from huggingface_hub import snapshot_download

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        snapshot_download(repo_id=MODEL_ID, local_dir=str(LOCAL_DIR))
    print("[supertonic2] Download complete.\n")
    return str(LOCAL_DIR)


# ─────────────────────────────────────────────────────────
# Model class (from official docs)
# ─────────────────────────────────────────────────────────


class SupertonicTTS:
    SAMPLE_RATE = 44100
    CHUNK_COMPRESS_FACTOR = 6
    BASE_CHUNK_SIZE = 512
    LATENT_DIM = 24
    STYLE_DIM = 128
    LATENT_SIZE = BASE_CHUNK_SIZE * 6  # 3072

    def __init__(self, model_path: str):
        import onnxruntime as ort
        from transformers import AutoTokenizer

        self.model_path = model_path
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)

        opts = ort.SessionOptions()
        opts.log_severity_level = 3  # suppress verbose ONNX logs

        onnx_dir = os.path.join(model_path, "onnx")
        self.text_encoder = ort.InferenceSession(
            os.path.join(onnx_dir, "text_encoder.onnx"), opts
        )
        self.latent_denoiser = ort.InferenceSession(
            os.path.join(onnx_dir, "latent_denoiser.onnx"), opts
        )
        self.voice_decoder = ort.InferenceSession(
            os.path.join(onnx_dir, "voice_decoder.onnx"), opts
        )

    def _load_style(self, voice: str) -> np.ndarray:
        path = os.path.join(self.model_path, "voices", f"{voice}.bin")
        if not os.path.exists(path):
            raise ValueError(f"Voice '{voice}' not found. Choose from: {VOICES}")
        return np.fromfile(path, dtype=np.float32).reshape(1, -1, self.STYLE_DIM)

    def generate(
        self, texts: list, *, voice="M1", speed=1.0, steps=5, language="en"
    ) -> list:
        if language not in LANGUAGES:
            raise ValueError(
                f"Language '{language}' not supported. Choose from: {LANGUAGES}"
            )

        tagged = [f"<{language}>{t}</{language}>" for t in texts]
        inputs = self.tokenizer(
            tagged, return_tensors="np", padding=True, truncation=True
        )
        ids = inputs["input_ids"]
        attn = inputs["attention_mask"]
        batch = ids.shape[0]
        style = self._load_style(voice).repeat(batch, axis=0)

        # Text → hidden states + durations
        hidden, raw_dur = self.text_encoder.run(
            None, {"input_ids": ids, "attention_mask": attn, "style": style}
        )
        durations = (raw_dur / speed * self.SAMPLE_RATE).astype(np.int64)

        # Build latent canvas
        lat_lens = (durations + self.LATENT_SIZE - 1) // self.LATENT_SIZE
        max_len = lat_lens.max()
        lat_mask = (np.arange(max_len) < lat_lens[:, None]).astype(np.int64)
        latents = np.random.randn(
            batch, self.LATENT_DIM * self.CHUNK_COMPRESS_FACTOR, max_len
        ).astype(np.float32)
        latents *= lat_mask[:, None, :]

        # Denoising loop
        n_steps = np.full(batch, steps, dtype=np.float32)
        for step in range(steps):
            ts = np.full(batch, step, dtype=np.float32)
            latents = self.latent_denoiser.run(
                None,
                {
                    "noisy_latents": latents,
                    "latent_mask": lat_mask,
                    "style": style,
                    "encoder_outputs": hidden,
                    "attention_mask": attn,
                    "timestep": ts,
                    "num_inference_steps": n_steps,
                },
            )[0]

        # Decode to waveform
        waveforms = self.voice_decoder.run(None, {"latents": latents})[0]

        results = []
        for i, length in enumerate(lat_mask.sum(axis=1) * self.LATENT_SIZE):
            results.append(waveforms[i, :length])
        return results


# ─────────────────────────────────────────────────────────
# Playback / save helpers
# ─────────────────────────────────────────────────────────


def play_audio(audio: np.ndarray, sample_rate: int = 44100):
    """Play a float32 numpy audio array through speakers."""
    import sounddevice as sd

    # Normalise to [-1, 1]
    peak = np.abs(audio).max()
    if peak > 0:
        audio = audio / peak

    # Pad 0.4s of silence at the end.
    # sd.wait() / blocking=True returns when the last buffer is *sent* to the OS,
    # not when the DAC finishes playing — short clips get cut off without this.
    pad = np.zeros(int(sample_rate * 0.4), dtype=np.float32)
    audio = np.concatenate([audio.astype(np.float32), pad])

    sd.play(audio, samplerate=sample_rate, blocking=True)


def save_audio(audio: np.ndarray, path: str, sample_rate: int = 44100):
    import soundfile as sf

    sf.write(path, audio, sample_rate)
    print(f"[supertonic2] Saved → {path}")


def speak(
    model: SupertonicTTS,
    text: str,
    *,
    voice="M1",
    speed=1.0,
    steps=5,
    language="en",
    save_path=None,
):
    if not text.strip():
        return
    print(f"[supertonic2] Generating ({steps} steps, voice={voice}, lang={language}) …")
    results = model.generate(
        [text], voice=voice, speed=speed, steps=steps, language=language
    )
    audio = results[0]

    if save_path:
        save_audio(audio, save_path)
    else:
        print(f"[supertonic2] ▶  {text!r}")
        play_audio(audio, model.SAMPLE_RATE)
        print("[supertonic2] Done.\n")


# ─────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Supertonic 2 TTS — CPU playback",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "text",
        nargs="?",
        default=None,
        help="Text to speak (omit for interactive loop)",
    )
    parser.add_argument(
        "--voice", "-v", default="M1", choices=VOICES, help="Voice preset (default: M1)"
    )
    parser.add_argument(
        "--lang", "-l", default="en", choices=LANGUAGES, help="Language (default: en)"
    )
    parser.add_argument(
        "--steps",
        "-s",
        type=int,
        default=5,
        help="Denoising steps — more = higher quality (default: 5, max: 50)",
    )
    parser.add_argument(
        "--speed",
        type=float,
        default=1.0,
        help="Speech speed multiplier (default: 1.0)",
    )
    parser.add_argument(
        "--save",
        default=None,
        metavar="FILE",
        help="Save to WAV file instead of playing",
    )
    parser.add_argument(
        "--list-voices", action="store_true", help="List available voices and exit"
    )
    args = parser.parse_args()

    if args.list_voices:
        print("Available voices:")
        print("  Male  :", " ".join(v for v in VOICES if v.startswith("M")))
        print("  Female:", " ".join(v for v in VOICES if v.startswith("F")))
        print("\nLanguages:", " ".join(LANGUAGES))
        return

    model_dir = download_model()
    print("[supertonic2] Loading ONNX model …")
    model = SupertonicTTS(model_dir)
    print("[supertonic2] Ready.\n")

    kwargs = dict(
        voice=args.voice,
        speed=args.speed,
        steps=args.steps,
        language=args.lang,
        save_path=args.save,
    )

    if args.text:
        speak(model, args.text, **kwargs)
    else:
        print("Interactive mode — type text and press Enter.  Ctrl-C to quit.")
        print(f"(voice={args.voice}  lang={args.lang}  steps={args.steps})\n")
        while True:
            try:
                text = input("Text: ").strip()
                speak(model, text, **kwargs)
            except KeyboardInterrupt:
                print("\n[supertonic2] Bye!")
                sys.exit(0)


if __name__ == "__main__":
    main()
