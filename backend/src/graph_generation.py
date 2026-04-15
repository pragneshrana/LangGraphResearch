"""Multi-agent stock market news pipeline: supervisor → research → analysis → summary → report."""

from __future__ import annotations

import logging
import os
import time
from typing import Any

from .env_bootstrap import load_env
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from .agents import (
    make_analyst_agent,
    make_researcher_agent,
    make_report_writer_agent,
    make_summary_agent,
    make_supervisor_agent,
)
from .logging_config import ensure_logging
from .router import route
from .schemas.pipeline import StockMarketState
from .logutil import preview

load_env()

logger = logging.getLogger(__name__)
ensure_logging()

# In-process checkpoint store (conversation + state per thread_id). For production,
# swap for PostgresSaver / RedisSaver from langgraph-checkpoint-* packages.
checkpointer = InMemorySaver()


def _groq_api_key() -> str | None:
    return os.getenv("GROQ_API_KEY") or os.getenv("groqAPIKey")


def _tavily_api_key() -> str | None:
    return os.getenv("TAVILY_API_KEY")


def build_llm() -> ChatGroq:
    key = _groq_api_key()
    if not key:
        raise ValueError("Set GROQ_API_KEY (or groqAPIKey) in the environment.")
    model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    return ChatGroq(model=model, api_key=key)


def build_tavily_search() -> TavilySearch:
    key = _tavily_api_key()
    if not key:
        raise ValueError("Set TAVILY_API_KEY in the environment.")
    return TavilySearch(
        max_results=int(os.getenv("TAVILY_MAX_RESULTS", "5")),
        topic="finance",
        search_depth="advanced",
        tavily_api_key=key,
    )


llm = build_llm()
tavily_search = build_tavily_search()


def build_graph():
    workflow = StateGraph(StockMarketState)
    workflow.add_node("supervisor", make_supervisor_agent(llm))
    workflow.add_node("researcher", make_researcher_agent(llm, tavily_search))
    workflow.add_node("analyst", make_analyst_agent(llm))
    workflow.add_node("summary", make_summary_agent(llm))
    workflow.add_node("report_writer", make_report_writer_agent(llm))

    workflow.add_edge(START, "supervisor")

    mapping = {
        "supervisor": "supervisor",
        "researcher": "researcher",
        "analyst": "analyst",
        "summary": "summary",
        "report_writer": "report_writer",
        END: END,
    }
    for node in (
        "supervisor",
        "researcher",
        "analyst",
        "summary",
        "report_writer",
    ):
        workflow.add_conditional_edges(node, route, mapping)

    return workflow.compile(checkpointer=checkpointer)


graph = build_graph()
logger.info("LangGraph compiled with checkpointer; graph ready.")


def run_stock_pipeline(
    user_message: str,
    *,
    thread_id: str | None = None,
    reset_pipeline: bool = True,
) -> dict[str, Any]:
    """Run the compiled graph and return final state.

    Uses LangGraph checkpointing: each ``thread_id`` keeps its own conversation and
    artifacts. By default ``reset_pipeline`` clears research/analysis/report fields so
    each run starts a fresh pipeline while still appending to ``messages`` for that
    thread.

    Set ``reset_pipeline=False`` to continue from the last checkpoint without clearing
    (e.g. follow-up in the same analysis); note a completed ``final_report`` may cause
    the supervisor to short-circuit until you use a new ``thread_id`` or reset.
    """
    tid = thread_id or os.getenv("LANGGRAPH_THREAD_ID", "default")
    logger.info(
        "Pipeline invoke thread_id=%s reset_pipeline=%s query=%s",
        tid,
        reset_pipeline,
        preview(user_message, 200),
    )
    t0 = time.perf_counter()
    config: dict[str, Any] = {
        "configurable": {"thread_id": tid},
        "recursion_limit": 40,
    }

    patch: dict[str, Any] = {
        "messages": [HumanMessage(content=user_message)],
    }
    if reset_pipeline:
        patch.update(
            {
                "next_agent": "",
                "research": None,
                "analysis": None,
                "executive_summary": None,
                "final_report": None,
                "task_complete": False,
                "current_task": "",
            }
        )

    try:
        out = graph.invoke(patch, config)
    except Exception:
        logger.exception("Pipeline invoke failed")
        raise
    elapsed = time.perf_counter() - t0
    fr = out.get("final_report")
    has_report = False
    if fr is not None:
        if isinstance(fr, dict):
            has_report = bool(fr.get("compiled") or fr.get("body"))
        else:
            has_report = bool(
                getattr(fr, "compiled", None) or getattr(fr, "body", None)
            )
    logger.info(
        "Pipeline finished in %.2fs final_report=%s",
        elapsed,
        has_report,
    )
    return out


def get_report_text(state: dict[str, Any]) -> str:
    """Extract the user-facing report string from a pipeline ``invoke`` result."""
    fr = state.get("final_report")
    if fr is None:
        return ""
    if isinstance(fr, dict):
        return str(fr.get("compiled") or fr.get("body") or "")
    return str(
        getattr(fr, "compiled", None) or getattr(fr, "body", None) or ""
    )
