# jobhunter/logger.py
# ─────────────────────────────────────────────────────────────────────────────
# Simple file + console logger. Mirrors server/logger.py style.
# ─────────────────────────────────────────────────────────────────────────────

from datetime import datetime
from jobhunter.config import LOG_PATH


def log(message: str) -> None:
    """Print to console and append to log file."""
    ts  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {message}"
    print(line, flush=True)
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass  # never crash because of logging