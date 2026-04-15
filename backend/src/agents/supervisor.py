"""Supervisor node: routes the pipeline with Groq."""

import logging
from typing import Any, Dict

from langchain_core.messages import AIMessage, HumanMessage
from langchain_groq import ChatGroq

from ..logutil import preview
from ..prompts import render_prompt
from ..schemas.pipeline import normalize_state, task_from_messages

logger = logging.getLogger(__name__)


def make_supervisor_agent(llm: ChatGroq):
    def supervisor_agent(state: dict | object) -> Dict[str, Any]:
        s = normalize_state(state)
        messages = s.messages or []
        task = task_from_messages(messages)
        logger.info(
            "agent=supervisor task=%s",
            preview(task, 120),
        )

        has_research = bool(s.research and s.research.content.strip())
        has_analysis = bool(s.analysis and s.analysis.content.strip())
        has_summary = bool(s.executive_summary and s.executive_summary.content.strip())
        has_report = bool(
            s.final_report
            and (s.final_report.compiled or s.final_report.body).strip()
        )

        if has_report:
            logger.info("agent=supervisor pipeline already has final_report -> end")
            return {
                "messages": [
                    AIMessage(
                        content="Supervisor: Report already generated. Pipeline complete."
                    )
                ],
                "next_agent": "end",
                "task_complete": True,
                "current_task": str(task),
            }

        prompt = render_prompt(
            "supervisor",
            task=task,
            has_research=has_research,
            has_analysis=has_analysis,
            has_summary=has_summary,
            has_report=has_report,
        )
        decision = llm.invoke([HumanMessage(content=prompt)])
        decision_text = (decision.content or "").strip().lower()

        if "done" in decision_text and has_report:
            msg = "Supervisor: All stages complete."
            next_agent = "end"
        elif "report_writer" in decision_text and has_summary:
            next_agent = "report_writer"
            msg = "Supervisor: Proceeding to final report."
        elif "summary" in decision_text and has_analysis:
            next_agent = "summary"
            msg = "Supervisor: Proceeding to executive summary."
        elif "analyst" in decision_text and has_research:
            next_agent = "analyst"
            msg = "Supervisor: Proceeding to analysis."
        elif "researcher" in decision_text or not has_research:
            next_agent = "researcher"
            msg = "Supervisor: Starting research with live search."
        elif has_research and not has_analysis:
            next_agent = "analyst"
            msg = "Supervisor: Research ready — assigning analyst."
        elif has_analysis and not has_summary:
            next_agent = "summary"
            msg = "Supervisor: Analysis ready — assigning summary."
        elif has_summary and not has_report:
            next_agent = "report_writer"
            msg = "Supervisor: Summary ready — assigning report writer."
        else:
            next_agent = "end"
            msg = "Supervisor: Pipeline complete."

        logger.info(
            "agent=supervisor next_agent=%s flags=%s",
            next_agent,
            {
                "research": has_research,
                "analysis": has_analysis,
                "summary": has_summary,
                "report": has_report,
            },
        )
        return {
            "messages": [AIMessage(content=msg)],
            "next_agent": next_agent,
            "current_task": str(task),
            "task_complete": next_agent == "end",
        }

    return supervisor_agent
