# LangGraph Stock Market Intelligence (backend)

Python application: **LangGraph** + **Groq** + **Tavily**, with **Pydantic** state, **Jinja** prompts, **CLI**, and **FastAPI**.

Run all commands from this directory (`backend/`) unless noted.

## Pipeline steps

1. **Supervisor** — Routes the next role (Groq).
2. **Researcher** — Tavily (finance) + Groq research brief.
3. **Analyst** — Groq analysis (scenarios, risks).
4. **Summary** — Groq executive summary.
5. **Report writer** — Full compiled report.

Checkpoint memory uses **`thread_id`** (LangGraph `InMemorySaver`).

## Prerequisites

- Python **3.14+** (see `.python-version`).
- **Groq**: `GROQ_API_KEY` (or `groqAPIKey`).
- **Tavily**: `TAVILY_API_KEY`.

## Setup

1. Open a shell in **`backend/`** (this folder).

2. Install dependencies:

   ```bash
   uv sync
   ```

   Or: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`

3. **Environment file** — copy the template and add your keys:

   ```bash
   cp .env.example .env
   ```

   Edit **`.env`** in **`backend/`** (recommended) and set at least `GROQ_API_KEY` and `TAVILY_API_KEY`.

   You can instead put a **`.env` in the repository root**; the app loads **`backend/.env` first**, then the root **`.env`** (see `src/env_bootstrap.py`).

   Optional variables: `GROQ_MODEL`, `TAVILY_MAX_RESULTS`, `LANGGRAPH_THREAD_ID`, `LOG_LEVEL`, or `groqAPIKey` instead of `GROQ_API_KEY`.

## CLI

```bash
uv run python main.py "Your market question"
```

Flags: `--thread`, `--follow-up`, `--log-level`. See `python main.py --help`.

## HTTP API

```bash
uv run uvicorn src.api_app:app --host 127.0.0.1 --port 8000 --reload
```

- `GET /health`
- `POST /report` with JSON `{"query": "...", "thread_id": null, "reset_pipeline": true}`
- Docs: `http://127.0.0.1:8000/docs`

CORS allows the Vite dev server (`localhost` / `127.0.0.1` on port **5173**); see `src/api_app.py`.

## Graph PNG export

```bash
uv run python scripts/export_graph_image.py
```

Default output: `assets/graph/langgraph_pipeline.png` (needs network for Mermaid).

## Layout

| Path | Role |
|------|------|
| `main.py` | CLI |
| `src/graph_generation.py` | Graph, `run_stock_pipeline`, `get_report_text` |
| `src/api_app.py` | FastAPI |
| `src/agents/` | Agents |
| `src/schemas/pipeline.py` | Pydantic state |
| `src/prompts/*.jinja` | Prompts |
| `src/env_bootstrap.py` | Loads `.env` from backend or repo root |
| `scripts/export_graph_image.py` | Diagram export |

## Logging

Stderr logging; use `LOG_LEVEL` or CLI `--log-level`.

Environment files are accepted in **`backend/.env`** or the **repository root** `.env` (see `src/env_bootstrap.py`).
