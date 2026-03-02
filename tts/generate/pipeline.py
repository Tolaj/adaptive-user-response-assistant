import numpy as np

from tts.model.singleton import get_model
from tts.text.normalise import normalise_text
from tts.generate.canvas import build_latent_canvas
from tts.generate.encode import encode_text
from tts.generate.denoise import run_denoiser
from tts.generate.decode import decode_waveform
from tts.generate.pad import apply_padding
from config.tts import (
    SUPERTONIC_VOICE,
    SUPERTONIC_LANGUAGE,
    SUPERTONIC_STEPS,
    SUPERTONIC_SPEED,
)

VALID_LANGUAGES = ["en", "ko", "es", "pt", "fr"]


def generate_speech(
    texts: list[str],
    voice: str = SUPERTONIC_VOICE,
    speed: float = SUPERTONIC_SPEED,
    steps: int = SUPERTONIC_STEPS,
    language: str = SUPERTONIC_LANGUAGE,
) -> list[np.ndarray]:
    """Generate audio for a list of texts. Returns list of float32 arrays."""
    if language not in VALID_LANGUAGES:
        raise ValueError(f"Language '{language}' not supported. Use: {VALID_LANGUAGES}")
    model = get_model()
    normalised = [normalise_text(t) for t in texts]
    hidden, durations, attn, style = encode_text(
        normalised, model, voice, speed, language
    )
    latents, lat_mask = build_latent_canvas(
        durations,
        model["latent_dim"],
        model["chunk_compress_factor"],
        model["latent_size"],
    )
    latents = run_denoiser(latents, lat_mask, style, hidden, attn, steps, model)
    waveforms = decode_waveform(latents, model)
    return [
        apply_padding(
            waveforms[i, : int(lat_mask.sum(axis=1)[i]) * model["latent_size"]],
            model["sample_rate"],
        )
        for i in range(len(texts))
    ]


def generate_one(
    text: str,
    voice: str = SUPERTONIC_VOICE,
    speed: float = SUPERTONIC_SPEED,
    steps: int = SUPERTONIC_STEPS,
    language: str = SUPERTONIC_LANGUAGE,
) -> np.ndarray:
    return generate_speech(
        [text], voice=voice, speed=speed, steps=steps, language=language
    )[0]


if __name__ == "__main__":
    audio = generate_one("Hello, world!")
    sr = get_model()["sample_rate"]
    print(f"Generated {len(audio)/sr:.2f}s at {sr} Hz")
    from tts.playback.stream import play_audio

    play_audio(audio, sr)
