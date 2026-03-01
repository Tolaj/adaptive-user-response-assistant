"""
tts/supertonic_model.py

Shared, lazily-loaded Supertonic 2 ONNX model wrapper.
Used by both server_tts/supertonic_backend.py and client/supertonic_player.py
so the model is only downloaded / loaded once per process.
"""

import warnings
import numpy as np
from pathlib import Path

MODEL_ID = "onnx-community/Supertonic-TTS-2-ONNX"
LOCAL_DIR = Path.home() / ".cache" / "supertonic2"

VOICES = ["M1", "M2", "M3", "M4", "M5", "F1", "F2", "F3", "F4", "F5"]
LANGUAGES = ["en", "ko", "es", "pt", "fr"]

# ── Module-level singleton ────────────────────────────────────────────────────
_model_instance: "SupertonicModel | None" = None


def get_model() -> "SupertonicModel":
    global _model_instance
    if _model_instance is None:
        _model_instance = SupertonicModel(_ensure_downloaded())
    return _model_instance


# ── Download helper ───────────────────────────────────────────────────────────


def _ensure_downloaded() -> str:
    marker = LOCAL_DIR / "onnx" / "text_encoder.onnx"
    if marker.exists():
        print(f"[Supertonic] Model cached at {LOCAL_DIR}")
        return str(LOCAL_DIR)

    print(f"[Supertonic] Downloading {MODEL_ID} → {LOCAL_DIR} …")
    print("[Supertonic] (one-time download, ~200 MB)")
    from huggingface_hub import snapshot_download

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        snapshot_download(repo_id=MODEL_ID, local_dir=str(LOCAL_DIR))
    print("[Supertonic] Download complete.\n")
    return str(LOCAL_DIR)


# ── Model ─────────────────────────────────────────────────────────────────────


class SupertonicModel:
    SAMPLE_RATE = 44100
    CHUNK_COMPRESS_FACTOR = 6
    BASE_CHUNK_SIZE = 512
    LATENT_DIM = 24
    STYLE_DIM = 128
    LATENT_SIZE = BASE_CHUNK_SIZE * 6  # 3072

    def __init__(self, model_path: str):
        import os
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
        print(f"[Supertonic] Model loaded from {model_path}")

    def _load_style(self, voice: str) -> np.ndarray:
        import os

        path = os.path.join(self.model_path, "voices", f"{voice}.bin")
        if not os.path.exists(path):
            raise ValueError(f"Voice '{voice}' not found. Choose from: {VOICES}")
        return np.fromfile(path, dtype=np.float32).reshape(1, -1, self.STYLE_DIM)

    def generate(
        self,
        texts: list[str],
        *,
        voice: str = "M1",
        speed: float = 1.0,
        steps: int = 5,
        language: str = "en",
    ) -> list[np.ndarray]:
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

    def generate_one(
        self,
        text: str,
        *,
        voice: str = "M1",
        speed: float = 1.0,
        steps: int = 5,
        language: str = "en",
    ) -> np.ndarray:
        """Convenience wrapper for single-text generation."""
        return self.generate(
            [text], voice=voice, speed=speed, steps=steps, language=language
        )[0]


# ── Playback helper ───────────────────────────────────────────────────────────


def play_audio(
    audio: np.ndarray, sample_rate: int = SupertonicModel.SAMPLE_RATE
) -> None:
    """
    Play a float32 numpy audio array through speakers (blocking).
    Pads 0.4 s of silence so the DAC finishes before the call returns.
    Supports interruption: if sounddevice raises an exception mid-play
    (e.g. from sd.stop()), it is silently absorbed.
    """
    import sounddevice as sd

    peak = np.abs(audio).max()
    if peak > 0:
        audio = audio / peak

    pad = np.zeros(int(sample_rate * 0.4), dtype=np.float32)
    audio = np.concatenate([audio.astype(np.float32), pad])

    try:
        sd.play(audio, samplerate=sample_rate, blocking=True)
    except Exception:
        pass


def stop_audio() -> None:
    """Immediately stop sounddevice playback (interrupt)."""
    try:
        import sounddevice as sd

        sd.stop()
    except Exception:
        pass
