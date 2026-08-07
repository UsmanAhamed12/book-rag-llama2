# Project Architecture

This project uses a layered FastAPI RAG architecture. Runtime application code
lives in `app/`; development utilities, deployment files, tests, and runtime
data remain outside that package.

```text
book-rag-llama2/
├── app/                         # Backend application package
│   ├── api/                     # HTTP API and authentication dependencies
│   │   └── v1/routes/           # Active, versioned FastAPI endpoints
│   ├── core/                    # Settings, security, logging, DI container
│   ├── db/                      # PostgreSQL and ChromaDB connections
│   ├── embeddings/              # Embedding provider abstraction and service
│   ├── ingestion/               # PDF loading, cleaning, and chunking
│   ├── llm/                     # Ollama client and LLM service
│   ├── models/                  # Domain and SQLAlchemy database models
│   │   └── database/            # Persistent database entities
│   ├── rag/                     # Prompt and answer-generation pipeline
│   ├── retrieval/               # Vector search and retrieval result models
│   ├── schemas/                 # FastAPI request/response schemas
│   ├── services/                # Application use-case services
│   └── vectorstores/            # ChromaDB storage adapter
├── data/                        # Local runtime data; not application code
│   ├── chroma/                  # Chroma persistent index (git-ignored)
│   ├── processed/               # Reserved for derived document data
│   └── uploads/                 # Uploaded source PDFs
├── docker/                      # API, frontend, and Compose deployment files
├── docs/                        # Project documentation
├── frontend/                    # Streamlit user interface
├── scripts/                     # Manual maintenance and smoke-test commands
├── tests/                       # Automated pytest test suite
├── pyproject.toml               # Dependencies, Ruff, pytest, and mypy config
└── uv.lock                      # Locked Python dependencies
```

## Ownership Rules

- Add new HTTP endpoints only under `app/api/v1/routes/`.
- Keep business workflows in `app/services/`; route handlers should stay thin.
- Put database connection code in `app/db/`, SQLAlchemy entities in
  `app/models/database/`, and API schemas in `app/schemas/`.
- Put reusable ingestion steps under `app/ingestion/` and retrieval logic under
  `app/retrieval/`.
- Keep one-off developer commands in `scripts/`; automated tests belong only in
  `tests/`.
- Never commit Chroma indexes, virtual environments, logs, secrets, or Python
  cache files. The existing `.gitignore` covers these runtime artifacts.

## Current Compatibility Note

`app/api/routes/` contains older placeholder routes while the running API uses
`app/api/v1/routes/`. The placeholders are intentionally retained for backwards
compatibility and are not part of the active router configuration. Removing or
moving them would require a separate, explicit compatibility change.
