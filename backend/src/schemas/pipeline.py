"""Pydantic models for agent-to-agent handoffs and graph state."""

from __future__ import annotations

from typing import Annotated, Any

from langchain_core.messages import AnyMessage, HumanMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, ConfigDict, Field


class ResearchBrief(BaseModel):
    """Researcher → analyst."""

    content: str = Field(default="", description="Structured research brief text")


class AnalystOutput(BaseModel):
    """Analyst → summary."""

    content: str = Field(default="", description="Analysis and scenarios")


class ExecutiveSummary(BaseModel):
    """Summary agent → report writer."""

    content: str = Field(default="", description="Executive summary / bullets")


class FinalReport(BaseModel):
    """Report writer deliverable."""

    body: str = Field(default="", description="LLM-generated report body (markdown)")
    compiled: str = Field(
        default="",
        description="Full document including title block and footer",
    )


class StockMarketState(BaseModel):
    """Graph state: messages plus validated handoff artifacts."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    messages: Annotated[list[AnyMessage], add_messages]
    next_agent: str = ""
    research: ResearchBrief | None = None
    analysis: AnalystOutput | None = None
    executive_summary: ExecutiveSummary | None = None
    final_report: FinalReport | None = None
    task_complete: bool = False
    current_task: str = ""


def normalize_state(state: StockMarketState | dict[str, Any]) -> StockMarketState:
    """Coerce LangGraph state (dict after invoke) to ``StockMarketState``."""
    if isinstance(state, StockMarketState):
        return state
    return StockMarketState.model_validate(state)


def task_from_messages(messages: list[AnyMessage] | None) -> str:
    for m in messages or []:
        if isinstance(m, HumanMessage):
            c = m.content
            return c if isinstance(c, str) else str(c)
    return "Stock market overview"


def research_text(state: StockMarketState | dict[str, Any]) -> str:
    s = normalize_state(state)
    return s.research.content if s.research else ""


def analysis_text(state: StockMarketState | dict[str, Any]) -> str:
    s = normalize_state(state)
    return s.analysis.content if s.analysis else ""


def summary_text(state: StockMarketState | dict[str, Any]) -> str:
    s = normalize_state(state)
    return s.executive_summary.content if s.executive_summary else ""


def report_compiled(state: StockMarketState | dict[str, Any]) -> str:
    s = normalize_state(state)
    if s.final_report and s.final_report.compiled:
        return s.final_report.compiled
    if s.final_report and s.final_report.body:
        return s.final_report.body
    return ""
