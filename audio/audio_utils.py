"""
audio/audio_utils.py
Helpers for loading and converting audio files.
No ffmpeg required — uses soundfile + resampy.
"""

import numpy as np
import soundfile as sf
import resampy

from config import WHISPER_SAMPLE_RATE


def load_audio_as_array(path: str) -> np.ndarray:
    """
    Load a WAV file and return a 16 kHz float32 mono numpy array
    ready for Whisper.
    """
    audio, sr = sf.read(path)

    # Stereo → mono
    if len(audio.shape) > 1:
        audio = audio.mean(axis=1)

    audio = audio.astype(np.float32)

    # Resample to Whisper's expected sample rate
    if sr != WHISPER_SAMPLE_RATE:
        audio = resampy.resample(audio, sr, WHISPER_SAMPLE_RATE)

    return audio


def numpy_to_wav(audio: np.ndarray, path: str, sample_rate: int = WHISPER_SAMPLE_RATE) -> str:
    """Write a float32 numpy array to a WAV file. Returns the path."""
    sf.write(path, audio, sample_rate)
    return path