# Frontend — Stock Market Intelligence

React **19** + **TypeScript** + **Vite** + **Tailwind CSS v4** + **HeroUI** (`@heroui/react`). The UI calls the FastAPI backend (`POST /report`, `GET /health`) and renders the pipeline output as a styled report (including markdown via `react-markdown`).

## Prerequisites

- **Node.js** 20+ (recommended)
- Backend running on the URL you configure (default **http://127.0.0.1:8000**). See the repository **[README.md](../README.md)** and **[backend/README.md](../backend/README.md)**.

## Setup

```bash
cd frontend
npm install
```

Optional: copy environment defaults and adjust the API URL if needed:

```bash
cp .env.example .env
```

| Variable        | Purpose |
|----------------|---------|
| `VITE_API_URL` | Backend origin with **no** trailing slash (e.g. `http://127.0.0.1:8000`). Embedded at **build** time. |

## Scripts

| Command        | Description |
|----------------|-------------|
| `npm run dev`    | Start Vite dev server (default **http://localhost:5173**). |
| `npm run build`  | Typecheck and production build to `dist/`. |
| `npm run preview`| Serve the production build locally. |
| `npm run lint`   | Run ESLint. |

## Development flow

1. Start the API from **`backend/`** (e.g. `uv run uvicorn src.api_app:app --host 127.0.0.1 --port 8000 --reload`).
2. In **`frontend/`**, run `npm run dev`.
3. Open the app in the browser; CORS on the API allows the Vite origin (`localhost` / `127.0.0.1` on port **5173**).

If requests fail with a network or CORS error, confirm `VITE_API_URL` matches where the API is listening and that the backend is up.
