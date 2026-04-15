"""FastAPI HTTP API for the stock-market LangGraph pipeline."""

from __future__ import annotations

import logging
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .env_bootstrap import load_env

load_env()

from .logging_config import setup_logging

setup_logging(os.getenv("LOG_LEVEL", "INFO"))

from .graph_generation import get_report_text, run_stock_pipeline

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Stock Market Intelligence",
    description="Multi-agent pipeline (supervisor → research → analysis → summary → report).",
    version="0.1.0",
)

# Browsers calling the Vite dev server need CORS when the API is on another origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ReportRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        description="Question or topic for the market intelligence report.",
    )
    thread_id: str | None = Field(
        default=None,
        description="Optional LangGraph checkpoint thread id (conversation memory).",
    )
    reset_pipeline: bool = Field(
        default=True,
        description="If true, clear prior pipeline artifacts for this thread before running.",
    )


class ReportResponse(BaseModel):
    report: str = Field(description="Full compiled report text.")
    success: bool = True


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/report", response_model=ReportResponse)
def create_report(body: ReportRequest) -> ReportResponse:
    """Run the full pipeline and return the final report text."""
    logger.info(
        "POST /report query_len=%d thread_id=%s reset=%s",
        len(body.query),
        body.thread_id or "(default)",
        body.reset_pipeline,
    )
    try:
        state = run_stock_pipeline(
            body.query,
            thread_id=body.thread_id,
            reset_pipeline=body.reset_pipeline,
        )
    except Exception as exc:
        logger.exception("Pipeline failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    report = get_report_text(state)
    if not report.strip():
        logger.error("Pipeline returned empty final_report")
        raise HTTPException(
            status_code=500,
            detail="Pipeline completed but produced no final report.",
        )
    return ReportResponse(report=report)
