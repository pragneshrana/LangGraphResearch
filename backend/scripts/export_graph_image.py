#!/usr/bin/env python3
"""Render the LangGraph structure to a PNG (Mermaid) and save under assets/graph/."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# Project root = parent of scripts/
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.env_bootstrap import load_env

load_env()

logger = logging.getLogger(__name__)


def main() -> None:
    from src.logging_config import setup_logging

    parser = argparse.ArgumentParser(description="Export LangGraph diagram to PNG.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=ROOT / "assets" / "graph" / "langgraph_pipeline.png",
        help="Output PNG path",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        metavar="LEVEL",
        help="Logging level (default INFO)",
    )
    args = parser.parse_args()
    setup_logging(args.log_level)

    logger.info("Loading graph and rendering Mermaid PNG -> %s", args.output)

    from src.graph_generation import graph

    args.output.parent.mkdir(parents=True, exist_ok=True)
    png = graph.get_graph().draw_mermaid_png()
    args.output.write_bytes(png)
    logger.info("Wrote %s (%d bytes)", args.output, len(png))


if __name__ == "__main__":
    main()
