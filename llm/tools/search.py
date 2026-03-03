# llm/tools/search.py


# ─────────────────────────────────────────────
# NEW: llm/tools/search.py
# Plain Python DuckDuckGo search — no MCP needed.
# ─────────────────────────────────────────────
def web_search(query: str, max_results: int = 3) -> str:
    try:
        from ddgs import DDGS

        results = DDGS().text(query, max_results=max_results)
        if not results:
            return "No results found."
        lines = [f"{r['title']}: {r['body']}" for r in results]
        return "\n".join(lines)
    except Exception as e:
        return f"[Search error] {e}"
