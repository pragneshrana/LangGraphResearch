"""Analyst node: Groq analysis over research brief."""

import logging
from typing import Any, Dict

from langchain_core.messages import AIMessage, HumanMessage
from langchain_groq import ChatGroq

from ..logutil import preview
from ..prompts import render_prompt
from ..schemas.pipeline import AnalystOutput, normalize_state, research_text, task_from_messages

logger = logging.getLogger(__name__)


def make_analyst_agent(llm: ChatGroq):
    def analyst_agent(state: dict | object) -> Dict[str, Any]:
        s = normalize_state(state)
        task = task_from_messages(s.messages)
        rd = research_text(s)
        logger.info(
            "agent=analyst start research_in=%d chars task=%s",
            len(rd),
            preview(task, 100),
        )
        body = render_prompt(
            "analyst",
            task=task,
            research_data=rd,
        )
        analysis_response = llm.invoke([HumanMessage(content=body)])
        text = analysis_response.content or ""

        logger.info("agent=analyst done analysis length=%d chars", len(text))

        snippet = (text[:500] + "…") if len(text) > 500 else text
        agent_message = f"Analyst: Analysis complete.\n\nPreview:\n{snippet}"

        return {
            "messages": [AIMessage(content=agent_message)],
            "analysis": AnalystOutput(content=text),
            "next_agent": "supervisor",
        }

    return analyst_agent
