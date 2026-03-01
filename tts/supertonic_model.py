"""
tts/supertonic_model.py

Shared, lazily-loaded Supertonic 2 ONNX model wrapper.
Used by both server_tts/tts_engine.py and client/supertonic_player.py
so the model is only downloaded / loaded once per process.

Fixes for clipped / dropped words
───────────────────────────────────
1. LATENT CANVAS MARGIN — lat_lens is padded by +LATENT_MARGIN chunks so the
   waveform is never cut short by an undersized canvas.
2. AUDIO PRE/POST PADDING — 30 ms of silence prepended and 80 ms appended to
   the raw waveform so the DAC and the prosody model both get clean boundaries.
3. TEXT NORMALISATION — text is wrapped in a comma-space prefix and a period
   suffix so the prosody encoder sees clean sentence context at both edges.
   Single-word or very short inputs get extra protection.
"""

import warnings
import threading as _threading
import numpy as np
from pathlib import Path

MODEL_ID = "onnx-community/Supertonic-TTS-2-ONNX"
LOCAL_DIR = Path.home() / ".cache" / "supertonic2"

VOICES = ["M1", "M2", "M3", "M4", "M5", "F1", "F2", "F3", "F4", "F5"]
LANGUAGES = ["en", "ko", "es", "pt", "fr"]

# Extra latent chunks added to the canvas to prevent end-clipping
LATENT_MARGIN = 3

# Silence padding added around the raw waveform (in seconds)
PRE_PAD_SEC = 0.03  # 30 ms before — prevents first-phoneme clip
POST_PAD_SEC = 0.08  # 80 ms after  — lets the last phoneme ring out

# ── Module-level singleton ────────────────────────────────────────────────────
_model_instance = None


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


# ── Text normalisation ────────────────────────────────────────────────────────


def _normalise_text(text: str) -> str:
    """
    Ensure the text has clean prosody context at both edges.

    - Strip whitespace
    - Guarantee it ends with sentence-final punctuation so the model
      knows the utterance is complete (prevents trailing word dropout)
    - Very short inputs (≤ 3 words) get a silent lead-in comma so the
      prosody encoder doesn't clip the first phoneme
    """
    text = text.strip()
    if not text:
        return text

    # Ensure terminal punctuation
    if text[-1] not in ".!?,;:":
        text = text + "."

    # Short utterances need a prosody lead-in
    if len(text.split()) <= 3:
        text = ", " + text

    return text


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
        opts.log_severity_level = 3

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
        texts,
        *,
        voice="M1",
        speed=1.0,
        steps=5,
        language="en",
    ):
        if language not in LANGUAGES:
            raise ValueError(
                f"Language '{language}' not supported. Choose from: {LANGUAGES}"
            )

        # Normalise each text for clean prosody boundaries
        texts = [_normalise_text(t) for t in texts]

        tagged = [f"<{language}>{t}</{language}>" for t in texts]
        inputs = self.tokenizer(
            tagged, return_tensors="np", padding=True, truncation=True
        )
        ids = inputs["input_ids"]
        attn = inputs["attention_mask"]
        batch = ids.shape[0]
        style = self._load_style(voice).repeat(batch, axis=0)

        hidden, raw_dur = self.text_encoder.run(
            None, {"input_ids": ids, "attention_mask": attn, "style": style}
        )
        durations = (raw_dur / speed * self.SAMPLE_RATE).astype(np.int64)

        # ── LATENT CANVAS with margin ─────────────────────────────────────
        # Without LATENT_MARGIN the canvas is sized exactly to the predicted
        # duration. Any prediction underflow clips the tail. The margin adds
        # extra chunks so there is always room for the full waveform.
        lat_lens = (
            durations + self.LATENT_SIZE - 1
        ) // self.LATENT_SIZE + LATENT_MARGIN
        max_len = lat_lens.max()
        lat_mask = (np.arange(max_len) < lat_lens[:, None]).astype(np.int64)
        latents = np.random.randn(
            batch, self.LATENT_DIM * self.CHUNK_COMPRESS_FACTOR, max_len
        ).astype(np.float32)
        latents *= lat_mask[:, None, :]

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

        waveforms = self.voice_decoder.run(None, {"latents": latents})[0]

        pre_pad = int(self.SAMPLE_RATE * PRE_PAD_SEC)
        post_pad = int(self.SAMPLE_RATE * POST_PAD_SEC)

        results = []
        for i, length in enumerate(lat_mask.sum(axis=1) * self.LATENT_SIZE):
            raw = waveforms[i, :length]
            # ── AUDIO PADDING ─────────────────────────────────────────────
            # Prepend silence so the DAC/speaker is already open when the
            # first phoneme hits. Append silence so the last phoneme fully
            # decays before playback stops.
            padded = np.concatenate(
                [
                    np.zeros(pre_pad, dtype=np.float32),
                    raw.astype(np.float32),
                    np.zeros(post_pad, dtype=np.float32),
                ]
            )
            results.append(padded)
        return results

    def generate_one(self, text, *, voice="M1", speed=1.0, steps=5, language="en"):
        return self.generate(
            [text], voice=voice, speed=speed, steps=steps, language=language
        )[0]


# ── Playback ──────────────────────────────────────────────────────────────────
#
# WHY a dedicated OutputStream instead of sd.play():
#   sd.play() reconfigures sounddevice's global default stream. When a mic
#   InputStream is already open (client TTS mode), macOS CoreAudio raises
#   err=-50 (kAudio_ParamError). An explicit OutputStream coexists with the
#   mic stream without touching shared HAL state.

_out_stream = None
_out_stream_lock = _threading.Lock()


def play_audio(
    audio: np.ndarray, sample_rate: int = SupertonicModel.SAMPLE_RATE
) -> None:
    """
    Play audio through a dedicated OutputStream (blocking).
    Safe to call while a sounddevice InputStream (mic) is open.
    Audio padding is already baked in by generate() — no extra padding here.
    """
    import sounddevice as sd

    global _out_stream

    # Normalise to [-1, 1]
    peak = np.abs(audio).max()
    if peak > 0:
        audio = audio / peak
    audio = audio.astype(np.float32)

    done = _threading.Event()
    pos = [0]

    def _callback(outdata, frames, time_info, status):
        chunk = audio[pos[0] : pos[0] + frames]
        if len(chunk) < frames:
            outdata[: len(chunk), 0] = chunk
            outdata[len(chunk) :, 0] = 0.0
            pos[0] += len(chunk)
            done.set()
            raise sd.CallbackStop
        else:
            outdata[:, 0] = chunk
            pos[0] += frames

    try:
        stream = sd.OutputStream(
            samplerate=sample_rate,
            channels=1,
            dtype="float32",
            callback=_callback,
            finished_callback=done.set,
        )
        with _out_stream_lock:
            _out_stream = stream

        with stream:
            stream.start()
            done.wait()

    except Exception:
        pass
    finally:
        with _out_stream_lock:
            _out_stream = None


def stop_audio() -> None:
    """Abort current OutputStream immediately (interrupt mid-playback)."""
    with _out_stream_lock:
        stream = _out_stream
    if stream is not None:
        try:
            stream.abort()
        except Exception:
            pass
