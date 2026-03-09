# jobhunter/vlm_query.py
# ─────────────────────────────────────────────────────────────────────────────
# Sends browser screenshots to your VLM server and gets back structured actions.
# Mirrors vision/inference/query.py — same HTTP call to your llama-server.
# ─────────────────────────────────────────────────────────────────────────────

import json
import re
import requests

from jobhunter.snap import snap_browser_b64
from jobhunter.config import VLM_SERVER_PORT, VLM_MAX_TOKENS, VLM_TEMPERATURE


# ── System prompt for navigation decisions ─────────────────────────────────
_NAV_SYSTEM = """You are a browser automation agent controlling a web browser to find job listings.
You see a screenshot of the current browser page.
Your job is to take ONE action to make progress toward the goal.

You MUST respond with ONLY a JSON object — no explanation, no markdown, no extra text.

JSON format:
{
  "action": "click" | "type" | "scroll" | "wait" | "extract" | "done" | "navigate",
  "x": <pixel x, only for click>,
  "y": <pixel y, only for click>,
  "text": "<text to type, only for type action>",
  "url": "<url, only for navigate action>",
  "direction": "down" | "up",
  "reason": "<one short sentence why>"
}

Rules:
- click: click at pixel coordinates (x, y)
- type: type text (assumes an input is already focused)
- scroll: scroll the page
- wait: wait for page to load (use after clicks that trigger navigation)
- extract: the page now shows job listings you can read — extract them now
- navigate: go directly to a URL
- done: no more jobs to find on this page
"""

# ── System prompt for job data extraction ──────────────────────────────────
_EXTRACT_SYSTEM = """You are a job listing extractor. You see a screenshot of a job search results page.
Extract ALL visible job listings into a JSON array.

Respond with ONLY a JSON array — no markdown, no explanation.

Each item format:
{
  "title": "<job title>",
  "company": "<company name>",
  "location": "<location or Remote>",
  "salary": "<salary if shown, else null>",
  "posted": "<time posted if shown, else null>",
  "url": "<job URL if visible in browser address or links, else null>",
  "snippet": "<brief description if visible, else null>"
}

If you cannot see any job listings, return an empty array: []
"""

# ── System prompt for VLM job scoring ──────────────────────────────────────
_SCORE_SYSTEM = """You are a job relevance scorer for a junior software developer.
Given a job listing and a candidate profile, score the job from 1-10.

Respond with ONLY a JSON object:
{
  "score": <1-10>,
  "reason": "<one sentence why>",
  "good_match": true | false
}

Score guide:
10 = perfect match (title, skills, level all match)
7-9 = strong match (most criteria match)
5-6 = partial match (some skills missing but worth applying)
1-4 = poor match (wrong level, wrong skills, or flagged keywords)
"""


def _call_vlm(screenshot_b64: str, system_prompt: str, user_prompt: str) -> str:
    """
    Single HTTP call to your llama-server.
    Mirrors _query_server() in vision/inference/query.py — same endpoint.
    """
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
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{screenshot_b64}"
                                },
                            },
                            {"type": "text", "text": user_prompt},
                        ],
                    },
                ],
                "max_tokens": VLM_MAX_TOKENS,
                "temperature": VLM_TEMPERATURE,
                "stream": False,
            },
            timeout=30,
        )
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[VLM] Call failed: {e}")
        return "{}"


def _parse_json(raw: str) -> dict | list:
    """Robustly extract JSON from VLM response — handles stray markdown."""
    raw = raw.strip()
    # Strip markdown code fences if present
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    try:
        return json.loads(raw)
    except Exception:
        # Try to find JSON object/array inside the text
        match = re.search(r"(\{.*\}|\[.*\])", raw, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except Exception:
                pass
    return {}


def decide_action(goal: str) -> dict:
    """
    Take a screenshot of the current page and ask the VLM what to do next.
    Returns a parsed action dict.
    """
    screenshot = snap_browser_b64()
    prompt = f"Goal: {goal}\n\nWhat is the single next action to take? Respond in JSON only."
    raw = _call_vlm(screenshot, _NAV_SYSTEM, prompt)
    action = _parse_json(raw)
    print(f"[VLM→Action] {action.get('action','?')} — {action.get('reason','')}")
    return action if isinstance(action, dict) else {}


def extract_jobs_from_page() -> list[dict]:
    """
    Take a screenshot and ask the VLM to extract all visible job listings.
    Returns a list of job dicts.
    """
    screenshot = snap_browser_b64()
    prompt = "Extract all visible job listings from this screenshot as a JSON array."
    raw = _call_vlm(screenshot, _EXTRACT_SYSTEM, prompt)
    result = _parse_json(raw)
    jobs = result if isinstance(result, list) else []
    print(f"[VLM→Extract] Found {len(jobs)} jobs on this page")
    return jobs


def score_job(job: dict, profile: dict) -> dict:
    """
    Ask VLM to score a single job against the candidate profile.
    Returns {score, reason, good_match}.
    """
    screenshot = snap_browser_b64()
    prompt = (
        f"Job listing:\n{json.dumps(job, indent=2)}\n\n"
        f"Candidate profile:\n"
        f"- Titles looking for: {', '.join(profile.get('job_titles', []))}\n"
        f"- Skills: {', '.join(profile.get('skills', []))}\n"
        f"- Experience: {profile.get('years_experience', 1)} year(s)\n"
        f"- Prefers: {profile.get('remote_preference', 'any')}\n"
        f"- Avoid keywords: {', '.join(profile.get('avoid_keywords', []))}\n\n"
        f"Score this job 1–10. Respond in JSON only."
    )
    raw = _call_vlm(screenshot, _SCORE_SYSTEM, prompt)
    result = _parse_json(raw)
    return result if isinstance(result, dict) else {"score": 5, "reason": "unknown", "good_match": True}