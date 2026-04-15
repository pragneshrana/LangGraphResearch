"""Executive summary node: Groq short-form synthesis."""

import logging
from typing import Any, Dict

from langchain_core.messages import AIMessage, HumanMessage
from langchain_groq import ChatGroq

from ..logutil import preview
from ..prompts import render_prompt
from ..schemas.pipeline import (
    ExecutiveSummary,
    analysis_text,
    normalize_state,
    research_text,
    task_from_messages,
)

logger = logging.getLogger(__name__)


def make_summary_agent(llm: ChatGroq):
    def summary_agent(state: dict | object) -> Dict[str, Any]:
        s = normalize_state(state)
        task = task_from_messages(s.messages)
        logger.info(
            "agent=summary start task=%s research_in=%d analysis_in=%d",
            preview(task, 100),
            len(research_text(s)),
            len(analysis_text(s)),
        )
        body = render_prompt(
            "summary",
            task=task,
            research_data=research_text(s),
            analysis=analysis_text(s),
        )
        out = llm.invoke([HumanMessage(content=body)])
        text = out.content or ""

        logger.info("agent=summary done executive summary length=%d chars", len(text))

        snippet = (text[:500] + "…") if len(text) > 500 else text
        agent_message = f"Summary: Executive summary drafted.\n\nPreview:\n{snippet}"

        return {
            "messages": [AIMessage(content=agent_message)],
            "executive_summary": ExecutiveSummary(content=text),
            "next_agent": "supervisor",
        }

    return summary_agent
