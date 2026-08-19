# Book RAG Assistant

A full-stack, local-first Retrieval-Augmented Generation (RAG) application for uploading PDF books, indexing their content, and asking grounded questions with source citations.

The project combines a FastAPI backend, PostgreSQL metadata and chat persistence, ChromaDB vector search, sentence-transformer embeddings, Ollama/Llama 3.2 generation, and a Next.js frontend. It is designed as a production-style portfolio project with strict typing, automated tests, Docker support, and GitHub Actions CI.

## Features

- PDF upload, validation, parsing, cleaning, chunking, and indexing
- Semantic retrieval with ChromaDB
- Local embeddings with `BAAI/bge-small-en-v1.5`
- Local LLM inference through Ollama using `llama3.2`
- Grounded RAG answers with file/page/chunk citations
- Multi-document selection and document summaries
- JWT authentication
- PostgreSQL document, user, chat-session, and message persistence
- Chat history and session management
- Next.js frontend
- FastAPI OpenAPI/Swagger API documentation
- Ruff formatting/linting, strict mypy, pytest
- Docker and GitHub Actions CI

## Architecture

```text
User
  |
  v
Next.js Frontend
  |
  | HTTP / JSON + JWT
  v
FastAPI API
  |
  +--> Authentication --------> PostgreSQL
  |
  +--> PDF Upload / Ingestion
  |       |
  |       +--> PDF Loader -> Cleaner -> Recursive Chunker
  |       |                              |
  |       |                              v
  |       +------------------------> Embedding Service
  |                                      |
  |                                      v
  |                                   ChromaDB
  |
  +--> Chat / RAG Pipeline
          |
          +--> Query Rewrite / Chat History
          +--> Retriever ------------> ChromaDB
          +--> Prompt Builder
          +--> Ollama / Llama 3.2
          +--> Answer + Citations ----> PostgreSQL
```

See [docs/architecture.md](docs/architecture.md) for the detailed architecture.

## Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, FastAPI, Pydantic |
| Package management | uv |
| Relational database | PostgreSQL, SQLAlchemy, Alembic |
| Vector database | ChromaDB |
| Embeddings | Sentence Transformers / BAAI bge-small-en-v1.5 |
| LLM | Ollama / Llama 3.2 |
| PDF processing | PyPDF, PyMuPDF |
| Authentication | JWT, python-jose, password hashing |
| Frontend | Next.js, React, TypeScript |
| Testing | pytest |
| Quality | Ruff, mypy strict mode |
| DevOps | Docker, GitHub Actions |

## Repository Structure

```text
book-rag-llama2/
├── app/                    # FastAPI backend
│   ├── api/                # Routes and dependencies
│   ├── core/               # Settings, security, DI/container
│   ├── db/                 # PostgreSQL and Chroma infrastructure
│   ├── ingestion/          # PDF ingestion pipeline
│   ├── llm/                # LLM client/service
│   ├── models/             # Domain/database models
│   ├── rag/                # RAG prompt and pipeline
│   ├── retrieval/          # Semantic retrieval
│   ├── schemas/            # Pydantic request/response models
│   └── services/           # Application services
├── alembic/                # Database migrations
├── data/                   # Local uploads/vector data (runtime)
├── docker/                 # Docker configuration
├── docs/                   # Project documentation
├── frontend/               # Next.js application
├── tests/                  # Backend automated tests
├── .github/workflows/      # CI workflows
├── .env.example            # Environment template
├── pyproject.toml          # Python project/tool configuration
└── README.md
```

## Prerequisites

Install:

- Python 3.12
- uv
- PostgreSQL
- Ollama
- Node.js/npm

Pull the local model:

```bash
ollama pull llama3.2
```

## Backend Setup

```bash
git clone https://github.com/UsmanAhamed12/book-rag-llama2.git
cd book-rag-llama2
uv sync --dev
cp .env.example .env
```

Create a PostgreSQL database named `book_rag`, then update `POSTGRES_URL` and `SECRET_KEY` in `.env`.

Run migrations when required:

```bash
uv run alembic upgrade head
```

Start the API:

```bash
uv run uvicorn app.main:app --reload
```

The API runs locally on port `8000`. Interactive API documentation is available at `/docs`.

## Frontend Setup

```bash
cd frontend
npm ci
npm run dev
```

The frontend runs locally on port `3000`.

## Environment Configuration

Important variables are documented in `.env.example`:

```env
SECRET_KEY=replace_with_a_secure_random_secret
POSTGRES_URL=postgresql+psycopg://postgres:your_password@localhost:5432/book_rag
OLLAMA_MODEL=llama3.2
OLLAMA_HOST=http://localhost:11434
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
CHROMA_DB_PATH=data/chroma
UPLOAD_DIR=data/uploads
```

Generate a strong development secret with:

```bash
openssl rand -hex 32
```

Never commit the real `.env` file, passwords, tokens, uploaded private documents, or runtime database data.

## RAG Flow

### Ingestion

```text
PDF -> Loader -> Text Cleaning -> Chunking -> Embeddings -> ChromaDB
                                      |
                                      +--> PostgreSQL metadata
```

### Question Answering

```text
Question
  -> recent chat context
  -> query rewrite
  -> semantic retrieval
  -> relevance filtering
  -> grounded prompt
  -> Llama 3.2 through Ollama
  -> answer + source citations
  -> chat persistence
```

The pipeline returns a fallback response instead of inventing an answer when sufficiently relevant context cannot be found.

## Quality Checks

Run the complete backend quality gate:

```bash
uv run ruff check app tests
uv run ruff format --check app tests
uv run mypy app
uv run pytest -v
```

To automatically apply Ruff-safe fixes and formatting:

```bash
uv run ruff check app tests --fix
uv run ruff format app tests
```

For the frontend:

```bash
cd frontend
npm ci
npm run lint
npm run build
```

The repository CI validates backend checks, frontend checks, and Docker build checks before changes are considered stable.

## API Areas

The application exposes versioned `/api/v1` routes covering authentication, document upload/management, chat, and chat sessions. FastAPI's generated `/docs` page is the canonical interactive endpoint reference for the running version.

See [docs/api.md](docs/api.md) for the API overview.

## Security

The project uses JWT-based authentication and user-scoped resources. Production deployments should additionally use HTTPS, strong secrets, restricted CORS origins, database least privilege, upload limits, secure secret management, and appropriate observability/rate limiting.

See [docs/security.md](docs/security.md).

## Documentation

- [Architecture](docs/architecture.md)
- [Getting Started](docs/getting-started.md)
- [Development Guide](docs/development.md)
- [API Guide](docs/api.md)
- [RAG Pipeline](docs/rag-pipeline.md)
- [Database](docs/database.md)
- [Authentication](docs/authentication.md)
- [Testing](docs/testing.md)
- [Docker](docs/docker.md)
- [Security](docs/security.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Roadmap](docs/roadmap.md)
- [Project History](docs/project-history.md)

## Project Status

Version `0.1.0` establishes the stable project foundation: ingestion, embeddings, vector retrieval, RAG, authentication, persistence, chat sessions, frontend integration, strict backend typing, tests, Docker checks, and CI foundations.

The next engineering phase focuses on retrieval quality, evaluation, observability, deployment hardening, and portfolio-grade production polish.

## License

No license is currently declared in the repository. Add a license before treating the project as generally reusable open-source software.
