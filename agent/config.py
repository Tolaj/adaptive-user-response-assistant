# agent/config.py
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
LOG_PATH = DATA_DIR / "agent.log"

DATA_DIR.mkdir(parents=True, exist_ok=True)

# VLM server
VLM_SERVER_PORT = 8081
VLM_MAX_TOKENS = 256
VLM_TEMPERATURE = 0.1

# Agent loop
MAX_STEPS = 40  # total steps before giving up entirely
MAX_RETRIES = 3  # retries on a single failed action before moving on

CLICK_OFFSET_X = 10   # positive = shift right
CLICK_OFFSET_Y = 0    # positive = shift down
