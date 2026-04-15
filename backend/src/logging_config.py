"""Central logging setup (CLI entrypoints should call ``setup_logging()`` first)."""

from __future__ import annotations

import logging
import os
import sys


def setup_logging(level: str | None = None) -> None:
    """Configure root logging: level from ``level``, ``LOG_LEVEL`` env, or INFO."""
    root = logging.getLogger()
    lvl_name = (level or os.getenv("LOG_LEVEL", "INFO")).upper()
    lvl = getattr(logging, lvl_name, logging.INFO)
    root.setLevel(lvl)
    if root.handlers:
        return
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s %(levelname)s [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    root.addHandler(handler)


def ensure_logging() -> None:
    """If the root logger has no handlers yet, apply default setup."""
    if not logging.getLogger().handlers:
        setup_logging()
