# RAG Document Assistant

Ask questions about PDF documents and get answers with page-level citations, backed by an
evaluation harness that measures retrieval and answer quality.

**Status:** M0 (project setup). See [docs/PLAN.md](docs/PLAN.md) for scope and milestones.

## Stack
Python 3.12 · uv · FastAPI + Pydantic v2 · LiteLLM · Postgres 16 + pgvector · SQLAlchemy 2 ·
pytest · ruff · mypy · Docker · GitHub Actions.

## Getting started

Prerequisites: [uv](https://docs.astral.sh/uv/) and Docker.

```bash
uv sync                           # install dependencies
docker compose up -d --wait db    # Postgres + pgvector on localhost:5432
uv run uvicorn app.main:app --reload
```

- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health → `{"db": "ok"}` (503 if Postgres is unreachable)

Defaults work without a `.env`. To override settings, copy `.env.example` to `.env` and fill in
only the values you need (empty values override defaults).

## Checks

```bash
uv run ruff check . && uv run ruff format --check .
uv run mypy
uv run pytest -m "not integration"   # unit tests, no database
uv run pytest                         # all tests (needs docker compose up)
uv run pre-commit install             # optional: run the checks before each commit
```

CI runs all of these on every push and pull request, with Postgres as a service container.

## Project layout

```
app/
  api/        HTTP routes, Pydantic schemas, error handlers
  services/   business logic
  db/         engine, sessions (models + migrations from M1)
  config.py   settings from environment
tests/
docs/PLAN.md
```

## Data
Only public, openly licensed documents are used (see PLAN §3).
