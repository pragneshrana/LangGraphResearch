"""Conditional routing for the stock-market multi-agent graph."""

import logging
from typing import Any

from langgraph.graph import END

from .schemas.pipeline import normalize_state

logger = logging.getLogger(__name__)


def route(state: dict[str, Any] | object):
    s = normalize_state(state)
    if s.next_agent == "end":
        logger.debug("route: -> END")
        return END
    n = s.next_agent or "supervisor"
    if n in ("supervisor", "researcher", "analyst", "summary", "report_writer"):
        logger.debug("route: -> %s", n)
        return n
    logger.warning("route: unknown next_agent=%r, defaulting to supervisor", n)
    return "supervisor"
