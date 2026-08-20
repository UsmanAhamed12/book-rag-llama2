# Getting Started

## Requirements

Install Python 3.12, uv, PostgreSQL 16, Ollama, Node.js, and npm. Docker is optional.

## 1. Clone and install

```bash
git clone https://github.com/UsmanAhamed12/book-rag-llama2.git
cd book-rag-llama2
uv sync --dev
```

## 2. Configure environment

```bash
cp .env.example .env
openssl rand -hex 32
```

Put the generated value into `SECRET_KEY`. Configure `POSTGRES_URL` for your local PostgreSQL instance.

The minimum local configuration is:

```env
SECRET_KEY=<generated-value>
POSTGRES_URL=postgresql+psycopg://postgres:<password>@localhost:5432/book_rag
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
OLLAMA_HOST=http://localhost:11434
CHROMA_DB_PATH=data/chroma
UPLOAD_DIR=data/uploads
```

Leave `RERANKING_ENABLED=false` for the lightest first run. Enabling it downloads and loads the configured cross-encoder model and uses `RETRIEVAL_CANDIDATE_K`, `RETRIEVAL_TOP_K`, and `RERANKER_WEIGHT`.

## 3. Prepare PostgreSQL

Create a database named `book_rag`, then apply migrations where required:

```bash
uv run alembic upgrade head
```

## 4. Prepare Ollama

```bash
ollama pull llama3.2
ollama list
```

Ollama should be reachable at the host configured by `OLLAMA_HOST`, normally `http://localhost:11434`.

## 5. Start backend

```bash
uv run uvicorn app.main:app --reload
```

Open the FastAPI Swagger interface at `http://127.0.0.1:8000/docs`.

## 6. Start frontend

In another terminal:

```bash
cd frontend
npm ci
npm run dev
```

Open `http://localhost:3000`.

The browser app expects the API base URL from `frontend/.env.local` or its build environment. For local development, use:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## 7. Validate the project

```bash
uv run ruff check app tests scripts alembic
uv run ruff format --check app tests scripts alembic
uv run mypy app tests
uv run pytest -q
```

Then validate the frontend:

```bash
cd frontend
npm run lint
npm run build -- --webpack
```

## Typical first-use flow

1. Register/login.
2. Upload a PDF.
3. Allow ingestion to extract, clean, chunk, embed, and index the document.
4. Create a chat session.
5. Select the relevant document(s).
6. Ask a question.
7. Review the generated answer and returned citations.

Do not commit `.env`, private PDFs, local Chroma data, database credentials, or access tokens.
