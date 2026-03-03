import threading
import numpy as np

_out_stream = None
_out_stream_lock = threading.Lock()


def play_audio(audio: np.ndarray, sample_rate: int = 44100) -> None:
    """
    Play audio through a dedicated OutputStream (blocking).
    Coexists safely with a mic InputStream — does not touch shared HAL state.
    """
    import sounddevice as sd
    from audio.transform.normalise import normalise

    global _out_stream

    audio = normalise(audio)
    done, pos = threading.Event(), [0]

    def _cb(outdata, frames, time_info, status):
        chunk = audio[pos[0] : pos[0] + frames]
        if len(chunk) < frames:
            outdata[: len(chunk), 0] = chunk
            outdata[len(chunk) :, 0] = 0.0
            pos[0] += len(chunk)
            done.set()
            raise sd.CallbackStop
        outdata[:, 0] = chunk
        pos[0] += frames

    try:
        stream = sd.OutputStream(
            samplerate=sample_rate,
            channels=1,
            dtype="float32",
            callback=_cb,
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
