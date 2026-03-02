def stop_audio() -> None:
    """Abort current OutputStream mid-playback."""
    import tts.playback.stream as _m

    with _m._out_stream_lock:
        stream = _m._out_stream
    if stream is not None:
        try:
            stream.abort()
        except Exception:
            pass
