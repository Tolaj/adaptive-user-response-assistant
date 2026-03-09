# jobhunter/scheduler.py
# ─────────────────────────────────────────────────────────────────────────────
# Keeps the job hunt running all day.
# Runs immediately on start, then every RUN_EVERY_HOURS hours.
# ─────────────────────────────────────────────────────────────────────────────

import time
import schedule
from datetime import datetime

from jobhunter.config import RUN_EVERY_HOURS
from jobhunter.logger import log


def _run_hunt():
    """Single hunt cycle — called by scheduler."""
    from jobhunter.profile import PROFILE, SEARCH_QUERIES
    from jobhunter.lg_agent import run_full_hunt

    log(f"\n{'='*50}")
    log(f"HUNT CYCLE STARTING — {datetime.now().strftime('%A %d %b %Y, %H:%M')}")
    log(f"{'='*50}")

    try:
        result = run_full_hunt(PROFILE, SEARCH_QUERIES)
        log(f"Cycle complete. {result['new_this_run']} new jobs saved.")
    except Exception as e:
        log(f"[ERROR] Hunt cycle crashed: {e}")
        import traceback
        log(traceback.format_exc())


def start_scheduler():
    """
    Run immediately, then repeat every RUN_EVERY_HOURS hours.
    Blocks forever — call from main_jobhunter.py.
    """
    log(f"Job hunter scheduler starting.")
    log(f"Will run every {RUN_EVERY_HOURS} hour(s). Press Ctrl+C to stop.\n")

    # Run once immediately
    _run_hunt()

    # Then schedule repeating runs
    schedule.every(RUN_EVERY_HOURS).hours.do(_run_hunt)

    while True:
        schedule.run_pending()
        time.sleep(60)  # check every minute