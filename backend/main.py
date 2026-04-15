"""CLI entry point for the stock-market LangGraph pipeline."""

import argparse
import logging
import os
from typing import Any

from src.logging_config import setup_logging


def _print_deliverable(out: dict[str, Any]) -> None:
    fr = out.get("final_report")
    if fr is None:
        print(out)
        return
    if isinstance(fr, dict):
        print(fr.get("compiled") or fr.get("body") or fr)
        return
    compiled = getattr(fr, "compiled", None)
    body = getattr(fr, "body", None)
    print(compiled or body or out)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Stock-market news pipeline (LangGraph + Groq + Tavily).",
    )
    parser.add_argument(
        "query",
        nargs="*",
        help="Question or topic (optional; uses a default demo query if empty)",
    )
    parser.add_argument(
        "--thread",
        default=os.getenv("LANGGRAPH_THREAD_ID", "default"),
        metavar="ID",
        help="Conversation thread id for checkpoint memory (env: LANGGRAPH_THREAD_ID)",
    )
    parser.add_argument(
        "--follow-up",
        action="store_true",
        help="Do not reset pipeline fields; continue from last state on this thread",
    )
    parser.add_argument(
        "--log-level",
        default=os.getenv("LOG_LEVEL", "INFO"),
        metavar="LEVEL",
        help="Logging level (DEBUG, INFO, WARNING, …). Env: LOG_LEVEL",
    )
    args = parser.parse_args()

    setup_logging(args.log_level)
    log = logging.getLogger(__name__)

    from src.graph_generation import run_stock_pipeline

    q = " ".join(args.query).strip() or (
        "Summarize this week's key news for large-cap US tech (e.g. NVDA, MSFT, AAPL) "
        "and main risks for the next two weeks."
    )
    log.info("Starting CLI run thread=%s follow_up=%s", args.thread, args.follow_up)
    out = run_stock_pipeline(
        q,
        thread_id=args.thread,
        reset_pipeline=not args.follow_up,
    )
    _print_deliverable(out)
    log.info("CLI run finished.")


if __name__ == "__main__":
    main()
