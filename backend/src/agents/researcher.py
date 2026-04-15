"""Researcher node: Tavily search + Groq synthesis."""

import logging
from typing import Any, Dict

from langchain_core.messages import AIMessage, HumanMessage
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch

from ..logutil import preview
from ..prompts import render_prompt
from ..schemas.pipeline import ResearchBrief, normalize_state, task_from_messages
from .utils import run_tavily_for_task

logger = logging.getLogger(__name__)


def make_researcher_agent(llm: ChatGroq, tavily_search: TavilySearch):
    def researcher_agent(state: dict | object) -> Dict[str, Any]:
        s = normalize_state(state)
        task = task_from_messages(s.messages)
        logger.info("agent=researcher start task=%s", preview(task, 120))
        tavily_block = run_tavily_for_task(tavily_search, task)
        body = render_prompt(
            "researcher",
            task=task,
            tavily_results=tavily_block,
        )
        research_response = llm.invoke([HumanMessage(content=body)])
        text = research_response.content or ""

        logger.info("agent=researcher done research brief length=%d chars", len(text))

        snippet = (text[:600] + "…") if len(text) > 600 else text
        agent_message = f"Researcher: Brief ready.\n\nPreview:\n{snippet}"

        return {
            "messages": [AIMessage(content=agent_message)],
            "research": ResearchBrief(content=text),
            "next_agent": "supervisor",
        }

    return researcher_agent
