# jobhunter/actions.py
# ─────────────────────────────────────────────────────────────────────────────
# Executes browser actions from VLM decisions using Playwright.
# VLM says: {"action": "click", "x": 432, "y": 287}
# This module does: page.mouse.click(432, 287)
# ─────────────────────────────────────────────────────────────────────────────

import time
from jobhunter.config import ACTION_DELAY_MS, PAGE_LOAD_WAIT_MS


def execute_action(action: dict) -> str:
    """
    Execute a single action from VLM output.
    Returns the action type executed, or "unknown" if unrecognised.
    """
    from jobhunter.browser import get_browser, navigate

    page = get_browser()
    action_type = action.get("action", "unknown")

    try:
        if action_type == "click":
            x = int(action.get("x", 0))
            y = int(action.get("y", 0))
            # Human-like: move then click
            page.mouse.move(x, y)
            time.sleep(0.1)
            page.mouse.click(x, y)
            page.wait_for_timeout(ACTION_DELAY_MS)

        elif action_type == "type":
            text = action.get("text", "")
            page.keyboard.type(text, delay=50)  # 50ms between keys = human-like
            page.wait_for_timeout(500)

        elif action_type == "scroll":
            direction = action.get("direction", "down")
            delta = 600 if direction == "down" else -600
            page.mouse.wheel(0, delta)
            page.wait_for_timeout(ACTION_DELAY_MS)

        elif action_type == "wait":
            page.wait_for_timeout(PAGE_LOAD_WAIT_MS)

        elif action_type == "navigate":
            url = action.get("url", "")
            if url:
                navigate(url)

        elif action_type in ("extract", "done"):
            pass  # handled by caller

        else:
            print(f"[Actions] Unknown action type: {action_type}")

    except Exception as e:
        print(f"[Actions] Failed to execute {action_type}: {e}")

    return action_type


def press_enter():
    """Press Enter key — useful after typing search queries."""
    from jobhunter.browser import get_browser
    page = get_browser()
    page.keyboard.press("Enter")
    page.wait_for_timeout(PAGE_LOAD_WAIT_MS)


def click_at(x: int, y: int):
    """Direct click — used for known coordinates."""
    from jobhunter.browser import get_browser
    page = get_browser()
    page.mouse.move(x, y)
    time.sleep(0.15)
    page.mouse.click(x, y)
    page.wait_for_timeout(ACTION_DELAY_MS)


def type_text(text: str):
    """Type text with human-like delay."""
    from jobhunter.browser import get_browser
    page = get_browser()
    page.keyboard.type(text, delay=60)
    page.wait_for_timeout(400)