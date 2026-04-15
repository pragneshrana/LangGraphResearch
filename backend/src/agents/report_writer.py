"""Report writer node: final structured report."""

import logging
from datetime import datetime, timezone
from typing import Any, Dict

from langchain_core.messages import AIMessage, HumanMessage
from langchain_groq import ChatGroq

from ..logutil import preview
from ..prompts import render_prompt
from ..schemas.pipeline import (
    FinalReport,
    analysis_text,
    normalize_state,
    research_text,
    summary_text,
    task_from_messages,
)

logger = logging.getLogger(__name__)


def make_report_writer_agent(llm: ChatGroq):
    def report_writer_agent(state: dict | object) -> Dict[str, Any]:
        s = normalize_state(state)
        task = task_from_messages(s.messages)
        logger.info(
            "agent=report_writer start task=%s summary_in=%d chars",
            preview(task, 100),
            len(summary_text(s)),
        )
        body = render_prompt(
            "report_writer",
            task=task,
            research_data=research_text(s),
            analysis=analysis_text(s),
            executive_summary=summary_text(s),
        )
        report_response = llm.invoke([HumanMessage(content=body)])
        report_body = report_response.content or ""

        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        compiled = (
            f"STOCK MARKET INTELLIGENCE REPORT\n"
            f"{'=' * 52}\n"
            f"Generated: {ts}\n"
            f"Topic: {task}\n"
            f"{'=' * 52}\n\n"
            f"{report_body}\n"
            f"{'=' * 52}\n"
            f"End of report\n"
        )
        logger.info(
            "agent=report_writer done body=%d chars compiled=%d chars",
            len(report_body),
            len(compiled),
        )

        return {
            "messages": [
                AIMessage(
                    content="Report writer: Final report generated. See `final_report` in state output."
                )
            ],
            "final_report": FinalReport(body=report_body, compiled=compiled),
            "next_agent": "supervisor",
        }

    return report_writer_agent
