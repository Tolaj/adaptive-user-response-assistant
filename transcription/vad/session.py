import numpy as np

from audio.io.mic import open_mic
from audio.transform.resample import resample
from config.vad import RECORD_SAMPLE_RATE, PREROLL_SECONDS
from config.whisper import WHISPER_SAMPLE_RATE
from transcription.stream import feed
from transcription.vad.processor import process_chunk


def run_mic_session(
    transcriber: dict,
    vad_state: dict,
    on_speech_end,
    on_speech_start=None,
    should_process_chunk=None,
) -> None:
    """Run interactive mic capture loop with VAD/preroll + Whisper resampling."""
    preroll_target = int(PREROLL_SECONDS * RECORD_SAMPLE_RATE)
    preroll_chunks: list[np.ndarray] = []
    preroll_len = 0

    def on_chunk(chunk):
        nonlocal preroll_len

        if should_process_chunk is not None and not should_process_chunk():
            return

        was_in_speech = vad_state["in_speech"]
        process_chunk(
            chunk,
            vad_state,
            on_speech_start=on_speech_start,
            on_speech_end=on_speech_end,
        )
        now_in_speech = vad_state["in_speech"]

        if now_in_speech:
            if not was_in_speech and preroll_chunks:
                pad = np.concatenate(preroll_chunks).astype(np.float32)
                pad_16k = resample(pad, RECORD_SAMPLE_RATE, WHISPER_SAMPLE_RATE)
                feed(transcriber, pad_16k)
                preroll_chunks.clear()
                preroll_len = 0
            chunk_16k = resample(chunk, RECORD_SAMPLE_RATE, WHISPER_SAMPLE_RATE)
            feed(transcriber, chunk_16k)
        else:
            preroll_chunks.append(chunk.copy())
            preroll_len += len(chunk)
            while preroll_len > preroll_target and preroll_chunks:
                dropped = preroll_chunks.pop(0)
                preroll_len -= len(dropped)

    mic = open_mic(on_chunk)
    mic.start()
    print("  🔴 Listening... Press ENTER to stop.")
    input()
    mic.stop()

    if vad_state["in_speech"] and vad_state["speech_samples"] > 0:
        on_speech_end()

    mic.close()
