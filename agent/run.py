# agent/run.py
import agent.logger as logger
from agent.graph import build_agent, AgentState


def run(goal: str) -> dict:
    session = logger.start_session(goal)
    agent = build_agent()

    initial: AgentState = {
        "goal": goal,
        "steps_taken": 0,
        "done": False,
        "last_action": "",
        "retry_count": 0,
        "last_fail_hint": "",
        "screen_analysis": {},
        "pending_response": None,  # ← add this
    }

    final = agent.invoke(initial)
    logger.end_session(final)
    return final
