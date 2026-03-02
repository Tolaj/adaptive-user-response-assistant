import threading
import time
from datetime import datetime
from config.paths import LOGS_DIR


def create_logger() -> dict:
    LOGS_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = LOGS_DIR / f"conversation_{ts}.log"
    with open(path, "w") as f:
        f.write("╔══════════════════════════════════════════════════════╗\n")
        f.write(f"  Session started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("╚══════════════════════════════════════════════════════╝\n\n")
    print(f"[LOG] {path}")
    return {
        "path": path,
        "req_num": 0,
        "session_start": time.time(),
        "lock": threading.Lock(),
    }


def log_request(
    logger: dict,
    user_text: str,
    ai_response: str,
    whisper_latency: float,
    llm_first_token: float,
    llm_total: float,
    end_to_end: float,
) -> None:
    with logger["lock"]:
        logger["req_num"] += 1
        n = logger["req_num"]
        ts = datetime.now().strftime("%H:%M:%S")
        st = time.time() - logger["session_start"]
        sep = "─" * 54
        print(f"\n  {sep}\n  Request #{n:02d}  [{ts}]  (+{st:.0f}s)\n  {sep}")
        print(f"  YOU : {user_text}\n  AI  : {ai_response}\n  {sep}")
        print(
            f"  ⏱  Whisper:{whisper_latency:.3f}s  FirstToken:{llm_first_token:.3f}s  LLM:{llm_total:.3f}s  E2E:{end_to_end:.3f}s\n  {sep}\n"
        )
        with open(logger["path"], "a") as f:
            f.write(
                f"[{ts}] #{n:02d}  YOU:{user_text}  AI:{ai_response}  "
                f"whisper:{whisper_latency:.3f}s  ft:{llm_first_token:.3f}s  "
                f"llm:{llm_total:.3f}s  e2e:{end_to_end:.3f}s\n\n"
            )


def log_event(logger: dict, event: str) -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    with logger["lock"]:
        print(f"  [LOG] {event}")
        with open(logger["path"], "a") as f:
            f.write(f"[{ts}] EVENT: {event}\n\n")


def close_logger(logger: dict) -> None:
    dur = time.time() - logger["session_start"]
    with open(logger["path"], "a") as f:
        f.write(f"  Session ended — {logger['req_num']} requests in {dur:.0f}s\n")
    print(f"[LOG] Closed — {logger['req_num']} requests in {dur:.0f}s")
