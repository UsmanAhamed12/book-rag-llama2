# Project Architecture

Book RAG Assistant uses a layered full-stack architecture that separates HTTP/API concerns, application services, relational persistence, vector retrieval, local LLM inference, and the web UI.

## System view

```text
+-----------------------+
|      End User         |
+-----------+-----------+
            |
            v
+-----------------------+
| Next.js / React UI    |
| TypeScript            |
+-----------+-----------+
            |
            | HTTP JSON + JWT
            v
+-----------------------+
| FastAPI API (/api/v1) |
+----+-------------+----+
     |             |
     |             +--------------------------+
     v                                        v
+-------------------+               +---------------------+
| App Services      |               | Authentication      |
| Documents / Chat  |               | JWT / password hash |
+---------+---------+               +----------+----------+
          |                                    |
          v                                    v
+-------------------+                 +-------------------+
| Ingestion / RAG   |<--------------->| PostgreSQL        |
+----+----------+---+                 | users/docs/chats  |
     |          |                     +-------------------+
     |          |
     v          v
+---------+  +------------------+
| Chroma  |  | Ollama           |
| vectors |  | Llama 3.2        |
+---------+  +------------------+
```

## Repository layout

```text
book-rag-llama2/
├── app/
│   ├── api/                     # FastAPI routing and dependencies
│   │   └── v1/routes/           # Active versioned endpoints
│   ├── core/                    # Settings, security, logging, DI/container
│   ├── db/                      # PostgreSQL/Chroma infrastructure
│   ├── embeddings/              # Embedding provider/service
│   ├── ingestion/               # PDF loader, cleaning, chunking, pipeline
│   ├── llm/                     # Ollama client and LLM service
│   ├── models/                  # Domain and SQLAlchemy models
│   ├── rag/                     # Prompt and RAG pipeline
│   ├── retrieval/               # Retriever and retrieval models
│   ├── schemas/                 # Pydantic API contracts
│   ├── services/                # Application use cases
│   └── vectorstores/            # Vector-store adapter(s)
├── alembic/                     # Relational DB migrations
├── data/                        # Local runtime storage
├── docker/                      # Container configuration
├── docs/                        # Engineering documentation
├── frontend/                    # Next.js/React/TypeScript frontend
├── frontend_streamlit_backup/   # Historical Streamlit UI backup
├── tests/                       # pytest suite
├── .github/workflows/           # CI
├── pyproject.toml               # Python dependencies/tooling
└── uv.lock                      # Locked Python dependency graph
```

## Backend layers

### API

`app/api/v1/routes/` exposes the active HTTP interface. Routes should handle request validation, authentication dependencies, response construction, and HTTP-specific errors while delegating reusable business behavior.

### Services

`app/services/` contains use-case logic such as document management, chat memory, upload behavior, and document-profile workflows.

### Ingestion

The ingestion layer converts PDFs into searchable chunks:

```text
PDF -> page extraction -> cleaning -> recursive chunking -> embeddings -> ChromaDB
```

Relational metadata is persisted separately in PostgreSQL.

### Retrieval

The retrieval layer performs semantic search against ChromaDB and returns typed retrieval results containing text, similarity score, and citation metadata.

### RAG

The RAG layer combines bounded conversation context, query rewriting, document-scoped retrieval, relevance filtering, prompt construction, local generation, citation creation, and chat persistence.

### LLM

The LLM service abstracts calls to Ollama. The default configured model is `llama3.2`, allowing the core generation workflow to run locally.

### Persistence

PostgreSQL stores durable application entities and ownership relationships. ChromaDB stores embeddings/vector-search metadata. These systems have different responsibilities and should not be conflated.

## Frontend

`frontend/` is the active Next.js application. It communicates with FastAPI over HTTP, sends bearer authentication for protected requests, and provides document/chat workflows. The older Streamlit implementation is retained only as a backup/history artifact.

## Design rules

- New active endpoints belong under `app/api/v1/routes/`.
- Route handlers should remain thin.
- Reusable workflows belong in services/pipelines.
- SQLAlchemy entities belong in `app/models/database/`.
- API contracts belong in `app/schemas/`.
- Retrieval and ingestion should remain independently testable.
- User-owned resources must be scoped by authenticated user ID.
- Runtime data, secrets, uploaded private PDFs, logs, caches, and vector indexes must not be committed.
- Tests must be self-contained and CI-portable.

## Quality boundary

Changes are validated through Ruff, strict mypy, pytest, frontend checks, Docker build validation, and GitHub Actions. This quality gate is part of the architecture because it protects contracts between layers as the project grows.