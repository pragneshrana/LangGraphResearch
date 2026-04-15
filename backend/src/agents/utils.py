"""Tavily formatting and search helpers."""

import logging
from typing import Any, Dict

from langchain_tavily import TavilySearch

from ..logutil import preview

logger = logging.getLogger(__name__)


def format_tavily_results(raw: Dict[str, Any]) -> str:
    if raw.get("error"):
        logger.warning("Tavily API returned error in payload: %s", raw["error"])
        return f"Search error: {raw['error']}"
    lines: list[str] = []
    if raw.get("answer"):
        lines.append(f"Answer (API): {raw['answer']}\n")
    for i, r in enumerate(raw.get("results") or [], 1):
        title = r.get("title") or ""
        url = r.get("url") or ""
        content = (r.get("content") or "")[:1200]
        lines.append(f"{i}. {title}\n   URL: {url}\n   Excerpt: {content}\n")
    return "\n".join(lines) if lines else "No search results returned."


def run_tavily_for_task(tavily_search: TavilySearch, task: str) -> str:
    query = (
        f"{task} stock market equities latest news earnings macro "
        "Wall Street analyst sentiment"
    ).strip()
    logger.info("Tavily query: %s", preview(query, 300))
    try:
        raw = tavily_search.invoke({"query": query})
        out = format_tavily_results(
            raw if isinstance(raw, dict) else {"error": str(raw)}
        )
        logger.debug("Tavily result length=%d chars", len(out))
        return out
    except Exception as exc:
        logger.warning("Tavily search failed: %s", exc)
        return f"Tavily search failed: {exc}"
