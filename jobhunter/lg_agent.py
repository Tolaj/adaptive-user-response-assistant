# jobhunter/lg_agent.py
# ─────────────────────────────────────────────────────────────────────────────
# LangGraph-based job hunter agent.
# Replaces: agent.py + os_actions.py + vlm_query.py
#
# Architecture:
#   LangGraph state machine with nodes:
#     screenshot → llm_decide → execute_tool → screenshot (loop)
#                                    ↓
#                               extract / score / done
#
# Tools the LLM can call:
#   click(x, y)           - click at screen coordinates
#   type_text(text)        - type text
#   scroll(direction)      - scroll page
#   navigate(url)          - go to URL
#   press_enter()          - press enter key
#   extract_jobs()         - extract job listings from current screen
#   mark_done()            - signal agent to stop
# ─────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

import json
import base64
import time
from typing import Annotated, TypedDict, Literal

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

from jobhunter.os_snap import snap_screen_b64
from jobhunter.os_browser import (
    click as _click,
    type_text as _type_text,
    scroll as _scroll,
    navigate as _navigate,
    press_enter as _press_enter,
    bring_chrome_to_front,
)
from jobhunter.storage import save_job, is_seen
from jobhunter.logger import log
from jobhunter.config import (
    VLM_SERVER_PORT,
    MAX_ACTIONS_PER_PAGE,
    MAX_JOBS_PER_SITE,
    MIN_SCORE_TO_SAVE,
)


# ── LangChain-compatible local VLM client ──────────────────────────────────
def get_vlm() -> ChatOpenAI:
    """
    Point LangChain at your local llama-server.
    Uses ChatOpenAI because llama-server exposes an OpenAI-compatible API.
    """
    return ChatOpenAI(
        model="local-vlm",                               # name doesn't matter
        base_url=f"http://localhost:{VLM_SERVER_PORT}/v1",
        api_key="not-needed",                            # llama-server ignores this
        max_tokens=256,
        temperature=0.1,
    )


# ── Agent state ────────────────────────────────────────────────────────────
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]   # full conversation history
    goal: str                                  # current high-level goal
    jobs_found: list[dict]                     # extracted jobs so far
    steps_taken: int                           # loop counter
    done: bool                                 # stop signal


# ── Tool definitions ────────────────────────────────────────────────────────
# Each @tool is a real OS action the LLM can call by name.
# LangChain handles argument parsing and dispatch automatically.

@tool
def click(
    x: Annotated[int, Field(description="X coordinate in 640x400 screenshot space")],
    y: Annotated[int, Field(description="Y coordinate in 640x400 screenshot space")],
) -> str:
    """Click at the given screen coordinates."""
    _click(x, y)
    time.sleep(0.8)
    return f"Clicked at ({x}, {y})"


@tool
def type_text(
    text: Annotated[str, Field(description="Text to type into the focused element")],
) -> str:
    """Type text using the keyboard."""
    _type_text(text)
    time.sleep(0.4)
    return f"Typed: {text}"


@tool
def scroll(
    direction: Annotated[Literal["down", "up"], Field(description="Scroll direction")] = "down",
) -> str:
    """Scroll the page up or down."""
    _scroll(direction)
    return f"Scrolled {direction}"


@tool
def navigate_to(
    url: Annotated[str, Field(description="Full URL to navigate to")],
) -> str:
    """Navigate Chrome to a URL using the address bar."""
    _navigate(url)
    return f"Navigated to {url}"


@tool
def press_enter() -> str:
    """Press the Enter key."""
    _press_enter()
    return "Pressed Enter"


@tool
def extract_jobs() -> str:
    """
    Extract all visible job listings from the current screen.
    Call this when you can see a list of job postings.
    Returns JSON array of jobs found.
    """
    from langchain_core.messages import HumanMessage
    from langchain_openai import ChatOpenAI

    screenshot_b64 = snap_screen_b64()

    extraction_llm = ChatOpenAI(
        model="local-vlm",
        base_url=f"http://localhost:{VLM_SERVER_PORT}/v1",
        api_key="not-needed",
        max_tokens=600,
        temperature=0.0,
    )

    system = (
        "You are a job listing extractor. Extract ALL visible job listings from the screenshot. "
        "Respond with ONLY a JSON array, no markdown, no explanation.\n"
        'Each item: {"title":"...","company":"...","location":"...","salary":null,"posted":null,"url":null,"snippet":null}'
    )

    msg = HumanMessage(content=[
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{screenshot_b64}"}},
        {"type": "text", "text": "Extract all visible job listings as a JSON array."},
    ])

    try:
        response = extraction_llm.invoke([SystemMessage(content=system), msg])
        raw = response.content.strip().lstrip("```json").lstrip("```").rstrip("```")
        jobs = json.loads(raw)
        if isinstance(jobs, list):
            log(f"[Extract] Found {len(jobs)} jobs")
            return json.dumps(jobs)
    except Exception as e:
        log(f"[Extract] Failed: {e}")

    return "[]"


@tool
def score_job_against_profile(
    job_json: Annotated[str, Field(description="JSON string of a single job dict")],
    profile_json: Annotated[str, Field(description="JSON string of the candidate profile")],
) -> str:
    """
    Score a job listing against a candidate profile.
    Returns JSON: {"score": 1-10, "reason": "...", "good_match": true/false}
    """
    from langchain_openai import ChatOpenAI

    scoring_llm = ChatOpenAI(
        model="local-vlm",
        base_url=f"http://localhost:{VLM_SERVER_PORT}/v1",
        api_key="not-needed",
        max_tokens=100,
        temperature=0.0,
    )

    system = (
        "You are a job relevance scorer for a junior software developer. "
        "Score the job 1-10. Respond ONLY with JSON: "
        '{"score": N, "reason": "one sentence", "good_match": true/false}'
    )

    try:
        job = json.loads(job_json)
        profile = json.loads(profile_json)
        prompt = (
            f"Job: {json.dumps(job)}\n"
            f"Profile titles: {profile.get('job_titles', [])}\n"
            f"Skills: {profile.get('skills', [])}\n"
            f"Experience: {profile.get('years_experience', 1)} year(s)\n"
            f"Avoid keywords: {profile.get('avoid_keywords', [])}\n"
            f"Score this job."
        )
        response = scoring_llm.invoke([SystemMessage(content=system), HumanMessage(content=prompt)])
        return response.content.strip()
    except Exception as e:
        return json.dumps({"score": 5, "reason": str(e), "good_match": True})


@tool
def mark_done(reason: Annotated[str, Field(description="Why you are done")] = "") -> str:
    """Signal that you have finished the current goal."""
    return f"Done: {reason}"


# All tools the agent can use
TOOLS = [click, type_text, scroll, navigate_to, press_enter, extract_jobs, mark_done]
TOOL_MAP = {t.name: t for t in TOOLS}


# ── Graph nodes ────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are a browser automation agent controlling a real macOS Chrome browser.
You see a screenshot of the current screen after every action.

You have these tools:
- click(x, y): click at coordinates in 640x400 screenshot space
- type_text(text): type text
- scroll(direction): scroll up or down  
- navigate_to(url): go to a URL
- press_enter(): press Enter
- extract_jobs(): extract job listings from the current screen
- mark_done(reason): signal you are finished

Rules:
- Take ONE action at a time
- After typing in a search box, call press_enter()
- When you can see job listings on screen, call extract_jobs()
- When there are no more jobs to find, call mark_done()
- The screenshot is 640x400 pixels. x=0 is LEFT, x=640 is RIGHT, y=0 is TOP, y=400 is BOTTOM
- Be precise — click the CENTER of buttons and input fields
- NEVER return x or y as a list. Always return a single integer for x and a single integer for y.

"""


def screenshot_node(state: AgentState) -> AgentState:
    if state["steps_taken"] >= MAX_ACTIONS_PER_PAGE:
        log(f"[Agent] Max steps reached ({MAX_ACTIONS_PER_PAGE})")
        return {**state, "done": True}

    log(f"[Agent] Step {state['steps_taken'] + 1} — taking screenshot")
    bring_chrome_to_front()   # ← add this
    time.sleep(0.5)           # ← give Chrome time to come to foreground
    b64 = snap_screen_b64()

    msg = HumanMessage(content=[
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
        {"type": "text", "text": f"Goal: {state['goal']}\n\nWhat is the next action?"},
    ])

    return {
        **state,
        "messages": state["messages"] + [msg],
        "steps_taken": state["steps_taken"] + 1,
    }


def llm_node(state: AgentState) -> AgentState:
    """Ask the LLM what to do next, with tool calling enabled."""
    vlm = get_vlm().bind_tools(TOOLS)

    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"][-2:]

    try:
        response = vlm.invoke(messages)
    except Exception as e:
        log(f"[Agent] LLM call failed: {e}")
        return {**state, "done": True}

    return {**state, "messages": state["messages"] + [response]}


def tool_node(state: AgentState) -> AgentState:
    """Execute whatever tool the LLM called."""
    last_msg = state["messages"][-1]

    if not hasattr(last_msg, "tool_calls") or not last_msg.tool_calls:
        log("[Agent] No tool call in LLM response — ending.")
        return {**state, "done": True}

    tool_results = []
    new_jobs = list(state["jobs_found"])
    done = state["done"]

    for tool_call in last_msg.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        # Fix: VLM sometimes returns x as [x, y] list
        if "x" in tool_args and isinstance(tool_args["x"], list):
            tool_args["y"] = tool_args["x"][1]
            tool_args["x"] = tool_args["x"][0]

        log(f"[Agent] Tool: {tool_name}({tool_args})")

        if tool_name not in TOOL_MAP:
            result = f"Unknown tool: {tool_name}"
        else:
            try:
                result = TOOL_MAP[tool_name].invoke(tool_args)
            except Exception as e:
                result = f"Error: {e}"

        # Handle extract_jobs result — parse and store jobs
        if tool_name == "extract_jobs":
            try:
                jobs = json.loads(result)
                for job in jobs:
                    if job.get("title") and job.get("company"):
                        new_jobs.append(job)
                log(f"[Agent] Total jobs collected: {len(new_jobs)}")
            except Exception:
                pass

        # Handle mark_done
        if tool_name == "mark_done":
            done = True

        tool_results.append(
            ToolMessage(content=str(result), tool_call_id=tool_call["id"])
        )

    return {
        **state,
        "messages": state["messages"] + tool_results,
        "jobs_found": new_jobs,
        "done": done,
    }


def should_continue(state: AgentState) -> Literal["screenshot", "end"]:
    """Decide whether to take another screenshot or stop."""
    if state["done"]:
        return "end"
    if state["steps_taken"] >= MAX_ACTIONS_PER_PAGE:
        return "end"
    if len(state["jobs_found"]) >= MAX_JOBS_PER_SITE:
        return "end"
    return "screenshot"


# ── Build the graph ────────────────────────────────────────────────────────
def build_agent() -> any:
    graph = StateGraph(AgentState)

    graph.add_node("screenshot", screenshot_node)
    graph.add_node("llm",        llm_node)
    graph.add_node("tools",      tool_node)

    graph.set_entry_point("screenshot")
    graph.add_edge("screenshot", "llm")
    graph.add_edge("llm",        "tools")
    graph.add_conditional_edges("tools", should_continue, {
        "screenshot": "screenshot",
        "end":        END,
    })

    return graph.compile()

def _handle_login_if_needed(site: str) -> None:
    from jobhunter.os_actions import decide_action, execute_action
    from jobhunter.os_browser import find_text_on_screen
    import pyautogui

    for attempt in range(10):
        bring_chrome_to_front()
        time.sleep(0.5)

        # Try OCR first — find exact coordinates of known elements
        for search_text in ["swapnilhgf@gmail.com", "Sign in", "Sign In"]:
            coords = find_text_on_screen(search_text)
            if coords:
                lx, ly = coords
                log(f"[Login] OCR found '{search_text}' at ({lx},{ly}) — clicking")
                pyautogui.click(lx, ly)
                time.sleep(2.5)
                # Check if now logged in
                if find_text_on_screen("Search") or find_text_on_screen("Jobs"):
                    log(f"[Login] Logged in to {site}")
                    return
                break
        else:
            # OCR found nothing — fall back to VLM
            action = decide_action(
                f"Look at the screen. What login step is visible? "
                f"Click the appropriate element. Coordinates are 640x400 max."
            )
            atype = action.get("action", "unknown")
            if atype == "already_open":
                return
            if atype in ("click", "type", "press_enter"):
                execute_action(action)
                time.sleep(2.5)

# ── High-level hunt function ───────────────────────────────────────────────
def hunt_site(site: str, query: str, profile: dict) -> int:
    """
    Run the LangGraph agent on one site with one search query.
    Returns the number of new jobs saved.
    """
    SITE_URLS = {
        "linkedin":  "https://www.linkedin.com/jobs",
        "indeed":    "https://www.indeed.com",
        "naukri":    "https://www.naukri.com",
        "wellfound": "https://wellfound.com/jobs",
    }

    url = SITE_URLS.get(site, "https://www.google.com")
    log(f"[{site.upper()}] Navigating to {url}")
    bring_chrome_to_front()
    _navigate(url)
    _handle_login_if_needed(site)

    goal = (
        f"Search for '{query}' jobs on this site. "
        f"Type the query in the search box, press enter, scroll through results. "
        f"When you see job listings call extract_jobs(). "
        f"After extracting, scroll down and extract again. "
        f"Call mark_done() when finished."
    )

    agent = build_agent()

    initial_state: AgentState = {
        "messages":    [],
        "goal":        goal,
        "jobs_found":  [],
        "steps_taken": 0,
        "done":        False,
    }

    log(f"[{site.upper()}] Starting LangGraph agent for: '{query}'")
    final_state = agent.invoke(initial_state)

    # Score and save collected jobs
    jobs_saved = 0
    profile_json = json.dumps(profile)

    for job in final_state["jobs_found"]:
        title   = job.get("title", "")
        company = job.get("company", "")

        if not title or not company:
            continue
        if is_seen(title, company, site):
            log(f"  [SKIP] Already seen: {title} @ {company}")
            continue

        avoid = profile.get("avoid_keywords", [])
        combined = f"{title} {job.get('snippet', '')}".lower()
        if any(kw.lower() in combined for kw in avoid):
            log(f"  [SKIP] Avoided keyword in: {title}")
            continue

        # Score the job
        try:
            raw_score = score_job_against_profile.invoke({
                "job_json": json.dumps(job),
                "profile_json": profile_json,
            })
            score_data = json.loads(raw_score)
        except Exception:
            score_data = {"score": 5, "reason": "parse error", "good_match": True}

        score  = int(score_data.get("score", 5))
        reason = score_data.get("reason", "")

        if score >= MIN_SCORE_TO_SAVE:
            saved = save_job(job, site, score, reason)
            if saved:
                jobs_saved += 1
                log(f"  [SAVED ★{score}] {title} @ {company} — {reason}")
        else:
            log(f"  [LOW ★{score}] {title} @ {company} — {reason}")

    log(f"[{site.upper()}] Done. Saved {jobs_saved} new jobs from '{query}'.")
    return jobs_saved


def run_full_hunt(profile: dict, search_queries: dict) -> dict:
    """Run the full job hunt across all sites and queries."""
    from jobhunter.storage import get_stats

    summary = {}
    total_new = 0

    for site, queries in search_queries.items():
        site_new = 0
        for query in queries:
            try:
                new = hunt_site(site, query, profile)
                site_new += new
                total_new += new
                time.sleep(3)
            except Exception as e:
                log(f"[ERROR] {site} / '{query}': {e}")
                import traceback
                log(traceback.format_exc())
        summary[site] = site_new

    stats = get_stats()
    log(
        f"\n{'='*50}\n"
        f"HUNT COMPLETE — {total_new} new jobs\n"
        f"Total in DB: {stats['total']}\n"
        f"{'='*50}\n"
    )
    return {"new_this_run": total_new, "stats": stats, "by_site": summary}