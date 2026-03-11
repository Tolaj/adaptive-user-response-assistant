# agent/graph.py
from __future__ import annotations
import json
import re
import time
from typing import Annotated, TypedDict, Literal
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

from agent.snap import snap_screen_b64
from agent.config import VLM_SERVER_PORT, MAX_STEPS, MAX_RETRIES
import agent.logger as logger
from agent.tools import ALL_TOOLS
from agent.snap import get_cursor_in_screenshot_space

cursor_x, cursor_y = get_cursor_in_screenshot_space()
cursor_info = f"Current mouse cursor is at ({cursor_x}, {cursor_y}) in screenshot space."

TOOL_MAP = {t.name: t for t in ALL_TOOLS}

_LLM_KWARGS = dict(
    model="local-vlm",
    base_url=f"http://localhost:{VLM_SERVER_PORT}/v1",
    api_key="not-needed",
    max_tokens=300,
    temperature=0.1,
)

# ── Prompts — kept SHORT to fit in 4096 context ───────────────────────────────

_LOCATE_PROMPT = """You are analyzing a macOS screenshot to find a clickable element.

Goal: {goal}
History: {history}
Mouse cursor is currently at: {cursor}
{fail_hint}


== FEW-SHOT EXAMPLES ==

EXAMPLE 1 — Finding Finder in dock:
Screen: macOS desktop, dock visible at bottom with app icons
Target: Finder icon (blue smiley face, leftmost dock icon)
Output:
{{
  "what_i_see": "macOS desktop with dock at bottom",
  "dock_items": "Finder(x=28), Chrome(x=75), Slack(x=120), VSCode(x=165)",
  "target": "Finder icon in dock",
  "bbox": "0,920,55,980",
  "target_x": 28,
  "target_y": 392,
  "goal_already_done": false
}}

EXAMPLE 2 — Finder already open, clicking Documents in sidebar:
Screen: Finder window open, left sidebar shows Favorites with Desktop/Documents/Downloads
Target: Documents folder in Finder sidebar
Output:
{{
  "what_i_see": "Finder window open with sidebar showing folders",
  "dock_items": "Finder(x=28), Chrome(x=75)",
  "target": "Documents in Finder sidebar",
  "bbox": "5,280,150,310",
  "target_x": 77,
  "target_y": 118,
  "goal_already_done": false
}}

EXAMPLE 3 — Goal already complete:
Screen: Finder window open showing Documents folder contents
Target: Open Documents folder
Output:
{{
  "what_i_see": "Finder showing Documents folder with files listed",
  "dock_items": "Finder(x=28), Chrome(x=75)",
  "target": "Documents folder",
  "bbox": null,
  "target_x": null,
  "target_y": null,
  "goal_already_done": true
}}

EXAMPLE 4 — Chrome address bar:
Screen: Chrome browser open with some webpage
Target: Chrome address bar to type a URL
Output:
{{
  "what_i_see": "Chrome browser with webpage open",
  "dock_items": "Finder(x=28), Chrome(x=75)",
  "target": "Chrome address bar",
  "bbox": "200,45,900,75",
  "target_x": 550,
  "target_y": 18,
  "goal_already_done": false
}}

EXAMPLE 5 — Finder is active app but no window is open:
Screen: macOS desktop visible, menu bar shows "Finder" but no Finder window on screen
Target: Need to open a Finder window
Output:
{{
  "what_i_see": "macOS desktop, Finder active in menu bar but no window open",
  "dock_items": "Finder(x=28), Chrome(x=75)",
  "target": "new Finder window via cmd+n",
  "bbox": null,
  "target_x": null,
  "target_y": null,
  "goal_already_done": false
}}

== NOW ANALYZE THE ACTUAL SCREENSHOT ==

Look at the screenshot carefully. The dock is at the VERY BOTTOM of the screen.
In bbox coordinates (0-1000): dock is y between 920-990, Finder is x between 0-60.
In pixel coordinates (0-640 x, 0-400 y): dock is y between 370-400, Finder is x between 15-40.

Respond with JSON only — no explanation, no markdown:
{{
  "what_i_see": "<10 words max>",
  "dock_items": "<name(x=N) for each visible icon>",
  "target": "<exact element name>",
  "bbox": "<x1,y1,x2,y2 in 0-1000 or null>",
  "target_x": <int 0-640 or null>,
  "target_y": <int 0-400 or null>,
  "goal_already_done": <true or false>
}}"""


_DECIDE_PROMPT = """You are controlling a real macOS screen.

Goal: {goal}
What you see: {what_i_see}
Dock: {dock_items}
Target: {target} at x={target_x}, y={target_y}
{fail_hint}

APP NAME RULES — macOS app names for open_app_window:
- "iMessage" or "imessage" → use app_name="Messages"  
- "Chrome" → use app_name="Google Chrome"
- "VSCode" → use app_name="Visual Studio Code"
- All others use their exact name as shown in dock

TOOL SELECTION:
1. To OPEN AN APP → open_app_window(app_name="<correct name>")
2. To CLICK a UI element → click(x, y)
3. If goal is done → mark_done()

Call ONE tool only. ALL coordinates 0-640 x, 0-400 y.
"""

_VERIFY_PROMPT = """Look at this macOS screenshot taken AFTER an action.

Action just performed: {last_action}
Goal: {goal}
Mouse cursor is currently at: {cursor} in 0-640/0-400 space.

Use the cursor position to judge accuracy:
- Target should be at approximately what coordinates?
- Is the cursor ON the target, or offset? By how much in which direction?
- If offset, calculate: target_x - cursor_x = dx, target_y - cursor_y = dy

Respond JSON only:
{{
  "what_i_see": "<describe screen state>",
  "cursor_position": "{cursor}",
  "cursor_on_target": <true/false>,
  "offset_from_target": "<e.g. '15px right, 5px down' or 'on target'>",
  "action_worked": <true/false>,
  "goal_complete": <true/false>,
  "reason": "<cite cursor position as evidence>",
  "next_suggestion": "<if not done: include corrected coordinates based on offset>"
}}"""
# ── State — NO message accumulation ──────────────────────────────────────────
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    goal: str
    steps_taken: int
    done: bool
    last_action: str
    retry_count: int
    last_fail_hint: str
    screen_analysis: dict  # result from locate
    pending_response: dict | None


def _get_llm(with_tools: bool = True):
    llm = ChatOpenAI(**_LLM_KWARGS)
    return llm.bind_tools(ALL_TOOLS) if with_tools else llm


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


def _image_message(b64: str, text: str) -> HumanMessage:
    return HumanMessage(
        content=[
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{b64}"},
            },
            {"type": "text", "text": text},
        ]
    )


# ── Nodes ─────────────────────────────────────────────────────────────────────


def _build_text_history(messages: list) -> str:
    """
    Extract only text from message history — no images.
    Gives the model memory of what it did without re-sending screenshots.
    """
    if not messages:
        return "Nothing done yet."

    lines = []
    for msg in messages[-10:]:   # last 10 messages max
        if not hasattr(msg, "content"):
            continue
        if isinstance(msg.content, str) and msg.content.strip():
            # ToolMessage or plain assistant text
            lines.append(f"- {msg.content[:120]}")
        elif isinstance(msg.content, list):
            for part in msg.content:
                if not isinstance(part, dict):
                    continue
                if part.get("type") == "text":
                    text = part.get("text", "").strip()
                    # Skip the big locate/decide prompts, keep short summaries
                    if text and len(text) < 300 and "Respond JSON" not in text:
                        lines.append(f"- {text[:120]}")

    return "\n".join(lines) if lines else "Nothing done yet."


def _parse_bbox(bbox_val) -> tuple[int, int] | None:
    """
    Parse Qwen3-VL bbox output into (target_x, target_y) in 0-640/0-400 space.
    
    Handles these formats the model might return:
      - "250,300,450,550"          ← comma string
      - [250, 300, 450, 550]       ← list
      - "250, 300, 450, 550"       ← comma+space string
      - "<box>250,300,450,550</box>" ← grounding tag format
    
    All values are in 0-1000 normalized space from Qwen3-VL.
    """
    if not bbox_val:
        return None

    try:
        # Strip grounding tags if present
        if isinstance(bbox_val, str):
            bbox_val = re.sub(r"</?box>", "", bbox_val).strip()

        # Parse to 4 numbers
        if isinstance(bbox_val, str):
            parts = [p.strip() for p in bbox_val.split(",")]
            x1, y1, x2, y2 = map(float, parts)
        elif isinstance(bbox_val, list) and len(bbox_val) == 4:
            x1, y1, x2, y2 = map(float, bbox_val)
        else:
            return None

        # Validate: all values should be in 0-1000 range
        if not all(0 <= v <= 1000 for v in [x1, y1, x2, y2]):
            return None

        # Convert center from 0-1000 → 0-640 / 0-400
        center_x = int(((x1 + x2) / 2) / 1000 * 640)
        center_y = int(((y1 + y2) / 2) / 1000 * 400)

        # Clamp to valid range
        center_x = max(0, min(640, center_x))
        center_y = max(0, min(400, center_y))

        return center_x, center_y

    except Exception:
        return None


def screenshot_node(state: AgentState) -> AgentState:
    """
    1. Check step limit
    2. Log step start
    3. Take screenshot
    4. Build locate prompt (with history + fail hint)
    5. Call VLM — single fresh message, no accumulated images
    6. Parse response — prefer bbox over raw x/y
    7. Return updated state with screen_analysis
    """

    # ── 1. Step limit check ───────────────────────────────────────────────────
    if state["steps_taken"] >= MAX_STEPS:
        logger.log(f"[Graph] Max steps ({MAX_STEPS}) reached")
        return {**state, "done": True}

    # ── 2. Log step start ─────────────────────────────────────────────────────
    step = state["steps_taken"] + 1
    logger.log_step_start(step, state["goal"])

    if state["last_fail_hint"]:
        logger.log_retry(state["retry_count"], MAX_RETRIES, state["last_fail_hint"])

    # ── 3. Take screenshot ────────────────────────────────────────────────────
    b64 = snap_screen_b64()
    logger.log_screenshot(b64, label="before")

    # ── 4. Build locate prompt ────────────────────────────────────────────────
    history = _build_text_history(state.get("messages", []))

    fail_hint_text = ""
    if state["last_fail_hint"]:
        fail_hint_text = (
            f"\nPREVIOUS ACTION FAILED: {state['last_fail_hint']}\n"
            f"Look more carefully — focus especially on finding the correct element."
        )

    locate_prompt = _LOCATE_PROMPT.format(
        goal      = state["goal"],
        history   = history,
        fail_hint = fail_hint_text,
        cursor    = cursor_info,
    )

    # ── 5. Call VLM — single fresh message, no history images ─────────────────
    try:
        locate_llm = _get_llm(with_tools=False)
        locate_response = locate_llm.invoke([
            _image_message(b64, locate_prompt)
        ])
        raw_content = locate_response.content
        analysis    = _parse_json(raw_content)

        # Also check for grounding tags in the raw response text
        # Qwen3-VL sometimes outputs <box> tags outside the JSON
        if not analysis.get("bbox"):
            box_match = re.search(r"<box>([\d,\s]+)</box>", raw_content)
            if box_match:
                analysis["bbox"] = box_match.group(1)

    except Exception as e:
        logger.log(f"[Graph] Locate failed: {e}")
        analysis = {}

    # ── 6. Parse coordinates — prefer bbox, fall back to raw x/y ──────────────
    what_i_see = analysis.get("what_i_see", "unknown")
    dock_items = analysis.get("dock_items", "unknown")
    target     = analysis.get("target",     "unknown")
    goal_done  = analysis.get("goal_already_done", False)

    # Try bbox first
    bbox_coords = _parse_bbox(analysis.get("bbox"))

    if bbox_coords:
        target_x, target_y = bbox_coords
        coord_source = "bbox"
    else:
        # Fall back to raw coordinates the model provided
        raw_x = analysis.get("target_x", None)
        raw_y = analysis.get("target_y", None)
        if raw_x is not None and raw_y is not None:
            target_x = max(0, min(640, int(raw_x)))
            target_y = max(0, min(400, int(raw_y)))
            coord_source = "raw_xy"
        else:
            target_x = None
            target_y = None
            coord_source = "unknown"

    # ── 7. Log what we found ──────────────────────────────────────────────────
    logger.log(f"│  👁️  Sees    : {what_i_see}")
    logger.log(f"│  🗂️  Dock    : {dock_items}")
    logger.log(f"│  🎯 Target  : {target}")
    logger.log(f"│  📍 Coords  : ({target_x}, {target_y}) via {coord_source}")

    if goal_done:
        logger.log(f"│  ✅ Locate says goal is already complete")

    # ── 8. Build text summary message for history ─────────────────────────────
    # This goes into messages[] as text only — no image
    # So future steps have memory without re-sending screenshots
    summary_text = (
        f"Step {step}: Saw '{what_i_see}'. "
        f"Target: '{target}' at ({target_x}, {target_y}) [{coord_source}]."
    )
    summary_msg = HumanMessage(content=summary_text)

    return {
        **state,
        "steps_taken":    step,
        "last_fail_hint": "",
        "messages":       state.get("messages", []) + [summary_msg],
        "screen_analysis": {
            "b64":         b64,
            "what_i_see":  what_i_see,
            "dock_items":  dock_items,
            "target":      target,
            "target_x":    target_x,
            "target_y":    target_y,
            "coord_source": coord_source,
            "goal_done":   goal_done,
        },
    }


def llm_node(state: AgentState) -> AgentState:
    """Fresh single-message call — no accumulated history."""
    sa = state["screen_analysis"]

    if sa.get("goal_done"):
        logger.log(f"│  🧠 LLM skipped — locate confirmed goal done")
        return {**state, "last_action": "mark_done(goal already complete)"}

    fail_hint = ""
    if state["last_fail_hint"]:
        fail_hint = f"PREVIOUS ACTION FAILED: {state['last_fail_hint']}\nTry something different."

    decide_text = _DECIDE_PROMPT.format(
        goal=state["goal"],
        what_i_see=sa.get("what_i_see", ""),
        dock_items=sa.get("dock_items", ""),
        target=sa.get("target", ""),
        target_x=sa.get("target_x", "?"),
        target_y=sa.get("target_y", "?"),
        fail_hint=fail_hint,
    )

    try:
        # Fresh call: system + single image message
        response = _get_llm(with_tools=True).invoke(
            [
                SystemMessage(
                    content="You are a macOS automation agent. Call exactly one tool."
                ),
                _image_message(sa["b64"], decide_text),
            ]
        )
    except Exception as e:
        logger.log(f"[Graph] LLM decide failed: {e}")
        return {**state, "done": True}

    logger.log_llm_decision(response)

    # Extract last_action for verify
    tool_calls = getattr(response, "tool_calls", [])
    if tool_calls:
        tc = tool_calls[0]
        last_action = f"{tc['name']}({tc['args']})"
    else:
        last_action = state["last_action"]

    return {**state, "pending_response": response, "last_action": last_action}


def tool_node(state: AgentState) -> AgentState:
    response = state.get("pending_response")

    # Handle mark_done from locate
    if state["screen_analysis"].get("goal_done") and not response:
        logger.log(f"│  ✅ Goal confirmed complete by locate")
        return {**state, "done": True}

    if not response:
        logger.log("[Graph] No pending response")
        return {**state, "done": True}

    tool_calls = getattr(response, "tool_calls", [])
    if not tool_calls:
        logger.log("[Graph] No tool call")
        return {**state, "done": True}

    done = state["done"]

    for tc in tool_calls:
        name = tc["name"]
        args = tc["args"]

        try:
            result = TOOL_MAP[name].invoke(args)
            logger.log_tool_execution(name, args, result)
            # If tool returned an error string, treat as failure
            if isinstance(result, str) and result.startswith(("Error", "Failed", "AppleScript error")):
                logger.log(f"[Graph] Tool returned error: {result}")
                return {
                    **state,
                    "pending_response": None,
                    "last_fail_hint": f"Tool {name} failed: {result}. Try a different approach.",
                    "retry_count": state["retry_count"] + 1,
                }
        except Exception as e:

            # Clamp coordinates to valid range
            if "x" in args:
                if isinstance(args["x"], list):
                    args["y"] = args["x"][1]
                    args["x"] = args["x"][0]
                args["x"] = max(0, min(int(args["x"]), 640))
            if "y" in args:
                args["y"] = max(0, min(int(args["y"]), 400))

            if name == "mark_done":
                done = True
                result = args.get("reason", "complete")
                logger.log_tool_execution(name, args, result)
            elif name not in TOOL_MAP:
                logger.log(f"[Graph] Unknown tool: {name}")
                result = f"unknown tool: {name}"
            else:
                try:
                    result = TOOL_MAP[name].invoke(args)
                    logger.log_tool_execution(name, args, result)
                except Exception as e:
                    result = f"error: {e}"
                    logger.log(f"[Graph] Tool error: {e}")

    return {**state, "done": done, "pending_response": None}


def verify_node(state: AgentState) -> AgentState:
    if state["done"]:
        logger.log_step_end()
        return state

    time.sleep(0.8)

    b64 = snap_screen_b64()
    logger.log_screenshot(b64, label="after")

    cursor_x, cursor_y = get_cursor_in_screenshot_space()

    verify_text = _VERIFY_PROMPT.format(
        last_action=state["last_action"],
        goal=state["goal"],
        cursor      = f"({cursor_x}, {cursor_y})",
    )

    try:
        response = _get_llm(with_tools=False).invoke([_image_message(b64, verify_text)])
        result   = _parse_json(response.content)
    except Exception as e:
        logger.log(f"[Graph] Verify failed: {e}")
        result = {
            "action_worked":   True,
            "goal_complete":   False,
            "reason":          "parse error",
            "what_i_see":      "",
            "next_suggestion": "",
        }

    what_i_see    = result.get("what_i_see",    "")
    action_worked = result.get("action_worked", True)
    goal_complete = result.get("goal_complete", False)
    reason        = result.get("reason",        "")
    suggestion    = result.get("next_suggestion", "")

    # If model says goal complete, ignore any suggestion it gave
    if goal_complete:
        suggestion = ""

    logger.log(f"│  👁️  After  : {what_i_see}")
    logger.log(f"│  🔧 Action : {'✓' if action_worked else '✗'} {reason}")
    logger.log(f"│  🏁 Goal   : {'COMPLETE ✅' if goal_complete else 'not done yet'}")
    if suggestion:
        logger.log(f"│  💡 Next   : {suggestion}")

    logger.log_step_end()

    if goal_complete:
        logger.log("[Graph] ✅ Goal complete — stopping")
        return {**state, "done": True, "retry_count": 0, "last_fail_hint": ""}

    if action_worked:
        # Action worked but goal not done yet — clear fail hint, reset retries
        # DON'T pass next_suggestion as fail_hint — it's guidance, not an error
        return {**state, "retry_count": 0, "last_fail_hint": ""}
    else:
        # Action genuinely failed — pass suggestion as hint for next attempt
        retry = state["retry_count"] + 1
        return {
            **state,
            "retry_count":   retry,
            "last_fail_hint": suggestion or reason,
        }

        
# ── Routing ───────────────────────────────────────────────────────────────────
def after_verify(state: AgentState) -> Literal["screenshot", "end"]:
    if state["done"]:
        return "end"
    if state["steps_taken"] >= MAX_STEPS:
        return "end"
    if state["retry_count"] >= MAX_RETRIES:
        logger.log(f"[Graph] Max retries — moving on")
        return "screenshot"
    return "screenshot"


# ── Build ─────────────────────────────────────────────────────────────────────
def build_agent():
    graph = StateGraph(AgentState)

    graph.add_node("screenshot", screenshot_node)
    graph.add_node("llm", llm_node)
    graph.add_node("tools", tool_node)
    graph.add_node("verify", verify_node)

    graph.set_entry_point("screenshot")
    graph.add_edge("screenshot", "llm")
    graph.add_edge("llm", "tools")
    graph.add_edge("tools", "verify")
    graph.add_conditional_edges(
        "verify",
        after_verify,
        {
            "screenshot": "screenshot",
            "end": END,
        },
    )

    return graph.compile()
