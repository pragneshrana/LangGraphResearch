"""Jinja2-rendered prompt templates (`.jinja` files in this directory)."""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

_PROMPTS_DIR = Path(__file__).parent
_env = Environment(
    loader=FileSystemLoader(_PROMPTS_DIR),
    autoescape=False,
    trim_blocks=True,
    lstrip_blocks=True,
)


def render_prompt(name: str, **kwargs: object) -> str:
    """Render `name.jinja` with the given context variables."""
    template_name = name if name.endswith(".jinja") else f"{name}.jinja"
    return _env.get_template(template_name).render(**kwargs)
