"""Agent factories for the stock-market LangGraph."""

from ..schemas.pipeline import StockMarketState, normalize_state, task_from_messages
from .analyst import make_analyst_agent
from .report_writer import make_report_writer_agent
from .researcher import make_researcher_agent
from .summary import make_summary_agent
from .supervisor import make_supervisor_agent

__all__ = [
    "StockMarketState",
    "make_analyst_agent",
    "make_researcher_agent",
    "make_report_writer_agent",
    "make_summary_agent",
    "make_supervisor_agent",
    "normalize_state",
    "task_from_messages",
]
