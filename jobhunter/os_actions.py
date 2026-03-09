# jobhunter/os_actions.py
# ─────────────────────────────────────────────────────────────────────────────
# VLM-guided OS automation actions.
# Replaces jobhunter/actions.py (which used Playwright).
# Takes a real screenshot → asks your VLM → executes via pyautogui.
#
# Usage:
#   from jobhunter.os_actions import decide_and_execute, os_navigate
# ─────────────────────────────────────────────────────────────────────────────

import json
import re
import time
import requests

from jobhunter.os_snap import snap_screen_b64
from jobhunter.os_browser import (
    click, double_click, scroll, type_text,
    press_enter, press_escape, navigate,
    bring_chrome_to_front,
)
from jobhunter.config import VLM_SERVER_PORT, VLM_MAX_TOKENS, VLM_TEMPERATURE
from jobhunter.logger import log


# ── VLM system prompts ──────────────────────────────────────────────────────
_NAV_SYSTEM = """You are a browser automation agent controlling a REAL macOS Chrome browser via mouse and keyboard.
You see a screenshot of the current screen.
Your job is to take ONE action to make progress toward the goal.

You MUST respond with ONLY a JSON object — no explanation, no markdown.

JSON format:
{
  "action": "click" | "type" | "scroll" | "wait" | "extract" | "done" | "navigate" | "already_open" | "press_enter" | "hotkey",
  "x": <pixel x in 1280x800 space, only for click>,
  "y": <pixel y in 1280x800 space, only for click>,
  "text": "<text to type, only for type action>",
  "url": "<url, only for navigate action>",
  "keys": "<hotkey combo like 'command+l', only for hotkey action>",
  "direction": "down" | "up",
  "reason": "<one short sentence why>"
}

IMPORTANT coordinate rules:
- The screenshot is 1280x800 pixels
- x=0 is LEFT edge, x=1280 is RIGHT edge
- y=0 is TOP edge, y=800 is BOTTOM edge
- Be precise — click the CENTER of buttons/links/input fields
"""

_EXTRACT_SYSTEM = """You are a job listing extractor. You see a screenshot of a job search results page.
Extract ALL visible job listings into a JSON array.
Respond with ONLY a JSON array — no markdown, no explanation.

Each item:
{
  "title": "<job title>",
  "company": "<company name>",
  "location": "<location or Remote>",
  "salary": "<salary if shown, else null>",
  "posted": "<time posted if shown, else null>",
  "url": "<job URL if visible, else null>",
  "snippet": "<brief description if visible, else null>"
}

If no job listings visible, return: []
"""

_LOGIN_SYSTEM = """You are helping automate a browser login flow on macOS Chrome.
You see a screenshot. Identify what login step is currently visible and what to click/type next.

Respond with ONLY a JSON object:
{
  "action": "click" | "type" | "press_enter" | "done" | "wait",
  "x": <x in 1280x800 space>,
  "y": <y in 1280x800 space>,
  "text": "<text to type if action=type>",
  "step": "<what step you see: profile_picker | email_input | password_input | signed_in | captcha | 2fa | other>",
  "reason": "<one sentence>"
}
"""


# ── Core VLM call ───────────────────────────────────────────────────────────
def _call_vlm(screenshot_b64: str, system_prompt: str, user_prompt: str, max_tokens: int = None) -> str:
    """Single HTTP call to llama-server."""
    try:
        response = requests.post(
            f"http://localhost:{VLM_SERVER_PORT}/v1/chat/completions",
            json={
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{screenshot_b64}"},
                            },
                            {"type": "text", "text": user_prompt},
                        ],
                    },
                ],
                "max_tokens": max_tokens or VLM_MAX_TOKENS,
                "temperature": VLM_TEMPERATURE,
                "stream": False,
            },
            timeout=30,
        )
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        log(f"[VLM] Call failed: {e}")
        try:
            log(f"[VLM] Raw response: {response.json()}")
        except:
            pass
        return "{}"


def _parse_json(raw: str) -> dict | list:
    """Robustly extract JSON from VLM response."""
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    try:
        return json.loads(raw)
    except Exception:
        match = re.search(r"(\{.*\}|\[.*\])", raw, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except Exception:
                pass
    return {}


# ── Action execution ────────────────────────────────────────────────────────
def execute_action(action: dict) -> str:
    """Execute a VLM action dict using real OS controls."""
    action_type = action.get("action", "unknown")

    try:
        if action_type == "click":
            vx = action.get("x", 0)
            vy = action.get("y", 0)
            # VLM sometimes returns x as [x, y] list — handle it
            if isinstance(vx, list):
                vx, vy = vx[0], vx[1]
            click(int(vx), int(vy))
            time.sleep(0.8)

        elif action_type == "double_click":
            vx = int(action.get("x", 0))
            vy = int(action.get("y", 0))
            double_click(vx, vy)
            time.sleep(0.8)

        elif action_type == "type":
            text = action.get("text", "")
            if text:
                type_text(text)
                time.sleep(0.4)

        elif action_type == "press_enter":
            press_enter()

        elif action_type == "hotkey":
            import pyautogui
            keys = action.get("keys", "").replace("+", " ").split()
            if keys:
                pyautogui.hotkey(*keys)
                time.sleep(0.5)

        elif action_type == "scroll":
            direction = action.get("direction", "down")
            scroll(direction, amount=3)

        elif action_type == "navigate":
            url = action.get("url", "")
            if url:
                navigate(url)

        elif action_type == "wait":
            time.sleep(2.0)

        elif action_type in ("extract", "done", "already_open"):
            pass  # handled by caller

        else:
            log(f"[OS Actions] Unknown action: {action_type}")

    except Exception as e:
        log(f"[OS Actions] Failed to execute {action_type}: {e}")

    return action_type


# ── High-level helpers ──────────────────────────────────────────────────────
def decide_action(goal: str) -> dict:
    from jobhunter.os_browser import bring_chrome_to_front
    bring_chrome_to_front()
    time.sleep(0.4)
    screenshot = snap_screen_b64()
    prompt = f"Goal: {goal}\n\nWhat is the single next action? Respond in JSON only."
    raw = _call_vlm(screenshot, _NAV_SYSTEM, prompt)
    action = _parse_json(raw)
    log(f"[VLM→Action] {action.get('action','?')} — {action.get('reason','')}")
    return action if isinstance(action, dict) else {}


def decide_login_step() -> dict:
    """Screenshot → VLM → login step dict."""
    screenshot = snap_screen_b64()
    prompt = "What login step is currently visible? What should I do next?"
    raw = _call_vlm(screenshot, _LOGIN_SYSTEM, prompt, max_tokens=150)
    result = _parse_json(raw)
    log(f"[VLM→Login] step={result.get('step','?')} action={result.get('action','?')}")
    return result if isinstance(result, dict) else {}


def extract_jobs_from_screen() -> list[dict]:
    """Screenshot → VLM → list of job dicts."""
    screenshot = snap_screen_b64()
    prompt = "Extract all visible job listings from this screenshot as a JSON array."
    raw = _call_vlm(screenshot, _EXTRACT_SYSTEM, prompt, max_tokens=500)
    result = _parse_json(raw)
    jobs = result if isinstance(result, list) else []
    log(f"[VLM→Extract] Found {len(jobs)} jobs on screen")
    return jobs


def os_navigate(url: str) -> None:
    """Navigate Chrome to URL using keyboard (no Playwright)."""
    navigate(url)