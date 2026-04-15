"""Small helpers for log-safe string previews."""

from __future__ import annotations


def preview(text: str | None, max_len: int = 160) -> str:
    if not text:
        return ""
    one_line = " ".join(text.split())
    if len(one_line) <= max_len:
        return one_line
    return one_line[: max_len - 1] + "…"
