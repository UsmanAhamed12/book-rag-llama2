# Getting Started

## Requirements

Install Python 3.12, uv, PostgreSQL, Ollama, Node.js, and npm.

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

## 7. Validate the project

```bash
uv run ruff check app tests
uv run ruff format --check app tests
uv run mypy app
uv run pytest -v
```

Then validate the frontend:

```bash
cd frontend
npm run lint
npm run build
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