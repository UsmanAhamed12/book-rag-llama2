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

For local development, `NEXT_PUBLIC_API_URL` should normally be `http://localhost:8000/api/v1`. The AWS frontend image is built with `/api/v1` so browser requests stay on the CloudFront origin.

## AWS service does not stabilize

Inspect ECS service events, stopped-task reasons, target-group health, and both log groups:

```bash
aws ecs describe-services --region ap-south-1 \
  --cluster book-rag-dev \
  --services book-rag-dev-api book-rag-dev-frontend
aws logs tail /ecs/book-rag-dev-api --region ap-south-1 --since 15m
aws logs tail /ecs/book-rag-dev-frontend --region ap-south-1 --since 15m
```

Common causes include a missing ECR tag, secret JSON without `SECRET_KEY`, unavailable Bedrock model access, unhealthy database credentials, EFS mount failure, or insufficient startup time while embedding/reranker models load.

## CloudFront returns 5xx

Check the ALB target groups before changing CloudFront. The API target must answer `/` with HTTP 200 and the frontend target must answer `/login` with HTTP 200-399. Confirm ECS tasks are running and security groups still allow ALB-to-task traffic.

## Bedrock generation fails

Confirm `LLM_PROVIDER=bedrock`, the configured inference profile is available in `BEDROCK_REGION`, the ECS task role can call Bedrock, and the Bedrock Runtime VPC endpoint is healthy. Review API logs without exposing document content or credentials.

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
uv run ruff check app tests scripts alembic
uv run ruff format --check app tests scripts alembic
uv run mypy app tests
uv run pytest -q
```

Then run frontend lint/build and confirm GitHub Actions is green.
