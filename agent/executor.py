# agent/executor.py
import json
import re
import time
import requests

from agent.snap import snap_screen_b64
from agent.controls import (
    click,
    double_click,
    scroll,
    type_text,
    press_enter,
    press_escape,
    hotkey,
    navigate,
    bring_chrome_to_front,
)
from agent.config import VLM_SERVER_PORT, VLM_MAX_TOKENS, VLM_TEMPERATURE
from agent.logger import log

# ── Generic system prompt ────────────────────────────────────────────────────
_SYSTEM = """You are a macOS desktop automation agent controlling the REAL screen via mouse and keyboard.
You see a screenshot of the current screen.
Take ONE action to make progress toward the goal.

Respond with ONLY a JSON object — no explanation, no markdown.

{
  "action": "click" | "double_click" | "type" | "scroll" | "press_enter" | "hotkey" | "navigate" | "wait" | "done",
  "x":         <int, pixel x in 640x400 screenshot space — only for click/double_click>,
  "y":         <int, pixel y in 640x400 screenshot space — only for click/double_click>,
  "text":      "<string — only for type>",
  "url":       "<string — only for navigate>",
  "keys":      "<string like 'command+c' — only for hotkey>",
  "direction": "down" | "up",
  "reason":    "<one sentence why>"
}

Coordinate rules:
- x=0 LEFT, x=640 RIGHT, y=0 TOP, y=400 BOTTOM
- Click the CENTER of the target element
"""


# ── VLM helpers ──────────────────────────────────────────────────────────────
def _call_vlm(screenshot_b64: str, prompt: str, max_tokens: int = None) -> str:
    try:
        response = requests.post(
            f"http://localhost:{VLM_SERVER_PORT}/v1/chat/completions",
            json={
                "messages": [
                    {"role": "system", "content": _SYSTEM},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{screenshot_b64}"
                                },
                            },
                            {"type": "text", "text": prompt},
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
        return "{}"


def _parse_json(raw: str) -> dict:
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    try:
        return json.loads(raw)
    except Exception:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except Exception:
                pass
    return {}


# ── Public API ───────────────────────────────────────────────────────────────
def decide_action(goal: str) -> dict:
    """Screenshot → VLM → action dict."""
    bring_chrome_to_front()
    time.sleep(0.4)
    screenshot = snap_screen_b64()
    prompt = f"Goal: {goal}\n\nWhat is the single next action? Respond in JSON only."
    raw = _call_vlm(screenshot, prompt)
    action = _parse_json(raw)
    log(f"[VLM] {action.get('action','?')} — {action.get('reason','')}")
    return action if isinstance(action, dict) else {}


def execute_action(action: dict) -> str:
    """Execute an action dict. Returns the action type string."""
    action_type = action.get("action", "unknown")
    try:
        if action_type in ("click", "double_click"):
            vx = action.get("x", 0)
            vy = action.get("y", 0)
            if isinstance(vx, list):  # VLM sometimes returns [x, y]
                vx, vy = vx[0], vx[1]
            if action_type == "click":
                click(int(vx), int(vy))
            else:
                double_click(int(vx), int(vy))
            time.sleep(0.8)

        elif action_type == "type":
            text = action.get("text", "")
            if text:
                type_text(text)
                time.sleep(0.4)

        elif action_type == "press_enter":
            press_enter()

        elif action_type == "hotkey":
            keys = action.get("keys", "").replace("+", " ").split()
            if keys:
                hotkey(*keys)

        elif action_type == "scroll":
            scroll(action.get("direction", "down"))

        elif action_type == "navigate":
            url = action.get("url", "")
            if url:
                navigate(url)

        elif action_type == "wait":
            time.sleep(2.0)

        elif action_type == "done":
            pass

        else:
            log(f"[Executor] Unknown action: {action_type}")

    except Exception as e:
        log(f"[Executor] Failed '{action_type}': {e}")

    return action_type
