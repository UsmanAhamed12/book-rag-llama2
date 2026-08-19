# Troubleshooting

## `FileNotFoundError` during CI tests

Do not make tests depend on a private/untracked PDF in `data/uploads`. Generate a temporary PDF fixture during the test so a clean GitHub Actions runner has everything it needs.

## mypy: `Missing type arguments for generic type dict`

Strict mypy requires parameterized mappings such as `dict[str, Any]`, a TypedDict, or a concrete Pydantic model. Prefer a real domain/API type instead of weakening mypy.

## mypy: `str | None` used as `str`

Values such as `UploadFile.filename` may be optional. Validate them before use or derive a safe required value after validation.

## Ollama unavailable

Check:

```bash
ollama list
```

Verify the configured model exists and `OLLAMA_HOST` points to the running Ollama server. The RAG layer includes fallback behavior for unavailable generation, but normal local Q&A requires Ollama.

## PostgreSQL connection failure

Confirm PostgreSQL is running, the `book_rag` database exists, credentials match `.env`, and `POSTGRES_URL` uses the expected psycopg SQLAlchemy URL.

## Frontend cannot reach backend

Confirm the backend is running on port 8000, the frontend is using the correct API base URL, and CORS allows the frontend's actual origin. Do not accidentally use Markdown-formatted URLs in CORS configuration; origins must be plain URL strings.

## Chroma/retrieval returns no useful context

Confirm the PDF completed ingestion, chunks were indexed, document IDs match the user's selected documents, embeddings use a consistent model, and the relevance threshold is not excluding all results.

## Ruff import/format errors

```bash
uv run ruff check app tests --fix
uv run ruff format app tests
```

Then rerun mypy and pytest.

## Clean final validation

```bash
uv run ruff check app tests
uv run ruff format --check app tests
uv run mypy app
uv run pytest -v
```

Then run frontend lint/build and confirm GitHub Actions is green.