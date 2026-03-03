# transcription/model/lock.py
import threading

# Single lock shared by all Whisper callers — GPU is not re-entrant
infer_lock = threading.Lock()
