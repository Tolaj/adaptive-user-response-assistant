# config/agent.py
# ─────────────────────────────────────────────────────────────────────────────
# Screen agent configuration — mirrors config/vlm.py style.
# ─────────────────────────────────────────────────────────────────────────────
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# ── OmniParser ─────────────────────────────────────────────────────────────
# Path to the OmniParser weights/ folder.
# After cloning https://github.com/microsoft/OmniParser and running
# python weights/download_weights.py, set this to that weights/ directory.
OMNIPARSER_WEIGHTS_DIR = str(BASE_DIR / "models" / "omniparser" / "weights")

# Caption model: "blip2" (lighter, faster) or "florence2" (smarter, slower)
OMNIPARSER_CAPTION_MODEL = "florence2"

# ── Agent loop ─────────────────────────────────────────────────────────────
AGENT_MAX_STEPS = 30  # hard limit — stops infinite loops
AGENT_STEP_DELAY = 1.2  # seconds between actions (let UI settle)
AGENT_SCREENSHOT_W = 1280  # VLM receives screenshot at this width
AGENT_SCREENSHOT_H = 800

# ── VLM call (reuses your existing vlm.py server) ─────────────────────────
# Inherits VLM_SERVER_PORT from config/vlm.py — no duplication needed.
AGENT_MAX_TOKENS = 256
AGENT_TEMPERATURE = 0.1  # low = deterministic action decisions

# ── Action execution ────────────────────────────────────────────────────────
AGENT_ACTION_DELAY_MS = 800  # ms pause after each click/type
AGENT_TYPE_INTERVAL = 0.05  # seconds between keystrokes (human-like)
