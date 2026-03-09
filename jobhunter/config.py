# jobhunter/config.py
# ─────────────────────────────────────────────────────────────────────────────
# Job hunter runtime configuration — tweak these without touching core logic
# ─────────────────────────────────────────────────────────────────────────────

from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).parent
DATA_DIR    = BASE_DIR / "data"
DB_PATH     = DATA_DIR / "jobs.db"
CSV_PATH    = DATA_DIR / "jobs_found.csv"
LOG_PATH    = DATA_DIR / "jobhunter.log"

DATA_DIR.mkdir(parents=True, exist_ok=True)

# ── Scheduler ─────────────────────────────────────────────────────────────
RUN_EVERY_HOURS = 2       # how often the full hunt cycle runs

# ── VLM settings (mirrors your config/vlm.py style) ──────────────────────
VLM_SERVER_PORT = 8081    # must match your config/vlm.py VLM_SERVER_PORT
VLM_MAX_TOKENS  = 120     # slightly more than vision assistant — needs JSON
VLM_TEMPERATURE = 0.1     # low = consistent, deterministic action decisions

# ── Agent loop limits ──────────────────────────────────────────────────────
MAX_ACTIONS_PER_PAGE  = 40   # max VLM → click/type steps before giving up
MAX_JOBS_PER_SITE     = 20   # stop scrolling after collecting this many
ACTION_DELAY_MS       = 1500 # ms to wait after each action (human-like)
PAGE_LOAD_WAIT_MS     = 2500 # ms to wait after navigation

# ── Screenshot settings (mirrors your config/vlm.py camera settings) ──────
SCREENSHOT_WIDTH  = 1280
SCREENSHOT_HEIGHT = 800
JPEG_QUALITY      = 75    # higher than camera — need to read text clearly

# ── Scoring thresholds ─────────────────────────────────────────────────────
MIN_SCORE_TO_SAVE = 5     # VLM scores 1–10; only save jobs >= this score