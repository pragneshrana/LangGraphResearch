"""Load ``.env`` from the backend package dir or the repository root."""

from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv


def load_env() -> None:
    """Load first existing file: ``backend/.env``, then repo root ``.env``."""
    _src = Path(__file__).resolve().parent
    backend = _src.parent
    repo = backend.parent
    for path in (backend / ".env", repo / ".env"):
        if path.is_file():
            load_dotenv(path)
