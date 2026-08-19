# Testing and Quality

## Backend quality gate

Run:

```bash
uv run ruff check app tests
uv run ruff format --check app tests
uv run mypy app
uv run pytest -v
```

The project uses strict mypy configuration for Python 3.12 and Ruff for linting/import ordering/formatting.

## Current core test areas

The backend suite covers core behaviors including:

- Chroma store creation
- embedding generation
- PDF loading
- ingestion pipeline execution
- RAG prompt/answer behavior
- Ollama-unavailable fallback behavior
- no-answer behavior when relevant context is absent
- recursive chunking
- retrieval ordering
- text cleaning

## CI-safe fixtures

Tests must not depend on a developer's private `data/uploads/Data_Engineering.pdf` or another untracked local document. File-processing tests should create temporary PDF fixtures so the same tests pass on a clean GitHub Actions Linux runner.

## Frontend checks

```bash
cd frontend
npm ci
npm run lint
npm run build
```

## Docker check

The CI pipeline also validates that the configured Docker image can be built successfully.

## Regression testing

When a bug is found:

1. reproduce it with a failing test where practical;
2. implement the smallest correct fix;
3. run the full quality gate;
4. keep the regression test permanently.

## CI expectation

A stable change should finish with all configured backend, frontend, and Docker checks green. Local success alone is insufficient because CI also verifies clean-environment portability.