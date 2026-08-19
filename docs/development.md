# Development Guide

## Development philosophy

Keep the application modular: API routes coordinate HTTP concerns, services own application behavior, database models own persistence structure, ingestion/retrieval/RAG modules own AI pipeline behavior, and Pydantic schemas define API contracts.

## Backend workflow

Install dependencies:

```bash
uv sync --dev
```

Run locally:

```bash
uv run uvicorn app.main:app --reload
```

Before committing backend changes:

```bash
uv run ruff check app tests --fix
uv run ruff format app tests
uv run mypy app
uv run pytest -v
```

Strict mypy is enabled. Avoid untyped `dict` values where a concrete schema, TypedDict, or parameterized mapping can express the contract.

## Frontend workflow

```bash
cd frontend
npm ci
npm run dev
```

Before committing frontend changes:

```bash
npm run lint
npm run build
```

## Database changes

Use SQLAlchemy models and Alembic migrations. Schema changes should be represented by a migration rather than manual production database edits.

Typical commands:

```bash
uv run alembic revision --autogenerate -m "describe change"
uv run alembic upgrade head
```

Review generated migrations before applying them.

## Branch workflow

Use small branches such as:

```text
feature/<name>
fix/<name>
docs/<name>
refactor/<name>
```

Recommended lifecycle:

```text
branch -> implementation -> local quality gate -> push -> PR -> CI -> review -> merge
```

Keep `main` stable.

## Testing principles

- Unit-test deterministic services and transformations.
- Do not make unit tests depend on private local PDFs.
- Use temporary/generated fixtures for file-processing tests.
- Mock external/local runtime dependencies where appropriate.
- Add regression tests when fixing defects.
- Keep tests deterministic across macOS and Linux CI.

## Configuration

Use `.env.example` as the documented configuration contract. Real secrets belong in `.env` locally or in a deployment secret manager.

## Definition of done

A change is complete when its behavior is implemented, types are correct, tests cover important behavior, Ruff/mypy/pytest pass, frontend lint/build pass when affected, documentation is updated when behavior changes, and CI is green.