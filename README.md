# Book RAG

Ask questions across PDF books and receive grounded answers with page-level evidence.

[Live development deployment](https://d1n9699wkr1rp7.cloudfront.net) · [Complete documentation](docs/README.md) · [Getting started](docs/getting-started.md) · [AWS deployment](docs/deployment.md)

![Book RAG interface](frontend/public/og.png)

Book RAG is a full-stack retrieval-augmented generation application. Users can create an account, upload PDFs to a private library, create chat sessions, select source documents, and ask questions. The response includes citations identifying the source file, page, and chunk used for generation.

## Current status

The repository contains a working Next.js frontend, FastAPI backend, PostgreSQL persistence, ChromaDB retrieval, cross-encoder reranking, local Ollama support, Amazon Bedrock support, Docker configuration, and Terraform-managed AWS infrastructure. The development deployment and its API health endpoint returned HTTP 200 on August 20, 2026.

The public URL is a development/demo environment. Review the [security checklist](docs/security.md) and [production-hardening section](docs/deployment.md#production-hardening) before using it for sensitive or high-volume workloads.

## Main capabilities

- JWT registration and login
- Private, user-scoped PDF libraries and chat histories
- PDF extraction, cleaning, recursive chunking, embedding, and indexing
- Document-scoped semantic retrieval with BGE embeddings
- Optional cross-encoder reranking with calibrated score fusion
- Relevance gating and explicit no-context behavior
- Grounded prompts that treat uploaded text as untrusted content
- Structured source citations with file, page, chunk, and score metadata
- Local generation through Ollama and AWS generation through Amazon Bedrock
- Responsive Next.js interface with light/dark themes and mobile navigation
- Reproducible Docker images and Terraform-managed AWS deployment
- Retrieval benchmark tooling and grounded-answer evaluation coverage

## Architecture

```text
Browser
  |
  | HTTPS
  v
CloudFront
  |
  v
Application Load Balancer
  |-- /* --------> Next.js on ECS Fargate
  `-- /api/* ----> FastAPI on ECS Fargate
                         |-- RDS PostgreSQL
                         |-- EFS: uploaded PDFs + ChromaDB
                         `-- Bedrock Runtime VPC endpoint
```

For local development, Next.js calls FastAPI, PostgreSQL stores application data, ChromaDB stores vectors, and Ollama runs the configured local model. See [Architecture](docs/architecture.md) and [RAG pipeline](docs/rag-pipeline.md).

## Technology stack

| Area | Technology |
|---|---|
| Frontend | Next.js 16, React 19, TypeScript, Tailwind CSS, shadcn/ui |
| API | Python 3.12, FastAPI, Pydantic, SQLAlchemy, Alembic |
| Retrieval | BAAI BGE embeddings, ChromaDB, sentence-transformers cross-encoder |
| Generation | Ollama/Llama locally; Amazon Bedrock Nova on AWS |
| Persistence | PostgreSQL, ChromaDB, uploaded PDF storage |
| AWS | CloudFront, ALB, ECS Fargate, ECR, RDS, EFS, Secrets Manager, VPC endpoints |
| Infrastructure | Docker, Terraform |
| Quality | Ruff, strict mypy, pytest, ESLint, TypeScript, Next.js production build |

## Quick start

Requirements: Python 3.12, [uv](https://docs.astral.sh/uv/), Node.js with npm, PostgreSQL 16, and Ollama.

```bash
git clone https://github.com/UsmanAhamed12/book-rag-llama2.git
cd book-rag-llama2
cp .env.example .env
uv sync --dev
ollama pull llama3.2
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

In a second terminal:

```bash
cd frontend
npm ci
npm run dev
```

Open `http://localhost:3000`. The API runs at `http://localhost:8000`, and Swagger UI is available at `http://localhost:8000/docs`.

Follow [Getting Started](docs/getting-started.md) for database configuration, first use, and validation. For containers, see [Docker](docs/docker.md).

## Configuration

Copy `.env.example` to `.env`; never commit the resulting file. The most important settings are:

```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
OLLAMA_HOST=http://localhost:11434
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
RERANKING_ENABLED=false
RETRIEVAL_CANDIDATE_K=10
RETRIEVAL_TOP_K=5
RETRIEVAL_MINIMUM_SCORE=0.35
RERANKER_WEIGHT=0.7
```

The AWS task definition selects `LLM_PROVIDER=bedrock`, enables reranking, and supplies database/application secrets through Secrets Manager. Configuration details are documented in [Getting Started](docs/getting-started.md), [RAG pipeline](docs/rag-pipeline.md), and [Deployment](docs/deployment.md).

## Quality gates

```bash
uv run ruff check app tests scripts alembic
uv run ruff format --check app tests scripts alembic
uv run mypy app tests
uv run pytest -q

cd frontend
npm run lint
npm run build -- --webpack
```

Terraform checks:

```bash
terraform -chdir=infra/terraform/environments/dev fmt -check -recursive
terraform -chdir=infra/terraform/environments/dev init -backend=false
terraform -chdir=infra/terraform/environments/dev validate
```

See [Testing and Quality](docs/testing.md) for the full validation matrix.

## Documentation

Start with the [documentation index](docs/README.md). It links the setup, architecture, RAG, API, database, authentication, security, development, testing, Docker, AWS deployment, operations, troubleshooting, history, and roadmap guides.

## Repository layout

```text
app/                  FastAPI application and RAG services
frontend/             Next.js application
tests/                Backend unit and regression tests
data/evaluation/      Retrieval benchmark inputs and recorded results
scripts/              Database and evaluation utilities
alembic/              Active database migrations
docs/                 Project and operations documentation
docker/               Local and production container definitions
infra/terraform/      AWS environment and reusable modules
```

## Data and secret safety

Do not commit `.env`, credentials, access tokens, private PDFs, database dumps, ChromaDB data, Terraform state, or generated deployment plans. Uploaded documents are untrusted input and must remain isolated to their owning user.
