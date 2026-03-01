"""
client/native_player.py

Client-side TTS player using macOS `say` command.

Implements the same interface as SupertonicPlayer:
    .feed_token(token)
    .flush()
    .interrupt()
    .resume()
    .is_speaking() → bool
    .shutdown()
"""

import re
import queue
import threading
import subprocess
import time

from config import TTS_RATE, TTS_VOICE_INDEX

# ── Sentence / clause splitter ────────────────────────────────────────────────

_SENTENCE_END = re.compile(r"(?<![A-Z][a-z])(?<!\d)([.?!])(\s+|$)")
_CLAUSE_BREAK = re.compile(r"[,;:]\s+")

MIN_CHUNK_CHARS = 6
MERGE_WINDOW_SEC = 0.05


def _split_sentence(buf: str) -> tuple[str, str]:
    m = _SENTENCE_END.search(buf)
    if m:
        return buf[: m.end()].strip(), buf[m.end() :]
    m = _CLAUSE_BREAK.search(buf)
    if m and m.start() >= MIN_CHUNK_CHARS:
        return buf[: m.start()].strip(), buf[m.end() :]
    return "", buf


def _clean_text(text: str) -> str:
    text = re.sub(r"\*+", "", text)
    text = re.sub(r"_+", "", text)
    text = re.sub(r"`+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ── Player ────────────────────────────────────────────────────────────────────


class NativeTTSPlayer:
    def __init__(self, rate: int = TTS_RATE, voice_index: int = TTS_VOICE_INDEX):
        self._rate = rate
        self._voice_name = "Samantha"
        self._proc = None
        self._proc_lock = threading.Lock()

        self._token_buf = ""
        self._queue: queue.Queue = queue.Queue()
        self._interrupted = threading.Event()
        self._speaking = threading.Event()

        self._resolve_voice(voice_index)

        self._worker = threading.Thread(target=self._loop, daemon=True)
        self._worker.start()

    # ── Public interface ──────────────────────────────────────────────────────

    def feed_token(self, token: str) -> None:
        if self._interrupted.is_set():
            return
        self._token_buf += token
        while True:
            sentence, remainder = _split_sentence(self._token_buf)
            if sentence and len(sentence) >= MIN_CHUNK_CHARS:
                self._token_buf = remainder
                self._queue.put(sentence)
            else:
                break
        if len(self._token_buf.split()) >= 8:
            text = self._token_buf.strip()
            self._token_buf = ""
            if text:
                self._queue.put(text)

    def flush(self) -> None:
        text = self._token_buf.strip()
        self._token_buf = ""
        if text and len(text) >= 2:
            self._queue.put(text)

    def interrupt(self) -> None:
        self._interrupted.set()
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except queue.Empty:
                break
        with self._proc_lock:
            if self._proc and self._proc.poll() is None:
                self._proc.terminate()
                try:
                    self._proc.wait(timeout=0.5)
                except Exception:
                    pass

    def resume(self) -> None:
        self._token_buf = ""
        self._interrupted.clear()

    def is_speaking(self) -> bool:
        return self._speaking.is_set()

    def shutdown(self) -> None:
        self.interrupt()
        self._queue.put(None)
        self._worker.join(timeout=3)

    # ── Internals ─────────────────────────────────────────────────────────────

    def _resolve_voice(self, voice_index: int) -> None:
        try:
            out = subprocess.check_output(["say", "-v", "?"], text=True, timeout=5)
            voices = [
                line.split()[0] for line in out.strip().splitlines() if line.strip()
            ]
            self._voice_name = (
                voices[voice_index] if voice_index < len(voices) else "Samantha"
            )
        except Exception:
            self._voice_name = "Samantha"
        print(f"[NativeTTS] Ready — voice={self._voice_name}, rate={self._rate} wpm")

    def _say(self, text: str) -> None:
        cmd = ["say", "-v", self._voice_name, "-r", str(self._rate), text]
        with self._proc_lock:
            if self._interrupted.is_set():
                return
            self._proc = subprocess.Popen(cmd)
        self._proc.wait()
        with self._proc_lock:
            self._proc = None

    def _loop(self) -> None:
        while True:
            item = self._queue.get()
            if item is None:
                break
            if self._interrupted.is_set():
                continue

            # Merge window — batch same-burst chunks into one `say` call
            collected = [item]
            deadline = time.time() + MERGE_WINDOW_SEC
            while time.time() < deadline:
                try:
                    nxt = self._queue.get_nowait()
                    if nxt is None:
                        self._queue.put(None)
                        break
                    collected.append(nxt)
                except queue.Empty:
                    time.sleep(0.005)

            if self._interrupted.is_set():
                continue

            merged = " ".join(_clean_text(c) for c in collected if c and c.strip())
            if not merged:
                continue

            self._speaking.set()
            try:
                self._say(merged)
            except Exception as e:
                print(f"[NativeTTS] Error: {e}")
            finally:
                self._speaking.clear()
