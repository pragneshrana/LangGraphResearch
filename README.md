# LangGraphResearch

Stock market intelligence pipeline (**LangGraph**, **Groq**, **Tavily**) with a **FastAPI** service and CLI.

## Where the code lives

All application code is under **`backend/`** (Python package `src`, `main.py`, `pyproject.toml`, `scripts/`, `assets/`).

## Quick start

```bash
cd backend
uv sync
cp .env.example .env   # then edit .env with GROQ_API_KEY and TAVILY_API_KEY
uv run python main.py "Your question about markets"
uv run uvicorn src.api_app:app --host 127.0.0.1 --port 8000 --reload
```

Full documentation: **[backend/README.md](backend/README.md)**.

## Web frontend (React + Tailwind + HeroUI)

From **`frontend/`**:

```bash
cd frontend
npm install
cp .env.example .env   # optional: set VITE_API_URL if the API is not at http://127.0.0.1:8000
npm run dev
```

Open the printed local URL (typically `http://localhost:5173`). Start the API from **`backend/`** on port **8000** so the UI can call `POST /report`.
