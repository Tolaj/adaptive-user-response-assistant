# jobhunter/__init__.py

from jobhunter.config import (
    VLM_SERVER_PORT,
    MAX_ACTIONS_PER_PAGE,
    MAX_JOBS_PER_SITE,
    MIN_SCORE_TO_SAVE,
)
from jobhunter.logger import log
from jobhunter.storage import save_job, is_seen, get_stats
from jobhunter.os_snap import snap_screen_b64
from jobhunter.os_browser import (
    launch_chrome,
    bring_chrome_to_front,
    navigate,
    click,
    type_text,
    scroll,
    press_enter,
    find_text_on_screen,
)
from jobhunter.os_actions import decide_action, execute_action
from jobhunter.lg_agent import hunt_site, run_full_hunt