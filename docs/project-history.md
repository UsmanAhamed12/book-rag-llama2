# Project History

## Origin

The project began as a local question-answering application over books/PDFs, with the goal of learning and demonstrating an end-to-end production-style RAG architecture rather than building only a notebook prototype.

## Foundation

The repository was structured around FastAPI and Python with configuration, logging, API routing, PDF loading, text cleaning, recursive chunking, typed document/chunk models, and automated tests.

## Embeddings and retrieval

The next stage added local sentence-transformer embeddings, ChromaDB vector storage, semantic similarity retrieval, metadata preservation, and retrieval tests.

## RAG and local LLM

A grounded prompt/pipeline was introduced and connected to a local Ollama model. The pipeline evolved to include relevance filtering, source metadata/citations, fallback behavior when context is absent, and graceful behavior when local generation is unavailable.

## Persistence and product behavior

PostgreSQL/SQLAlchemy/Alembic were added for application metadata. The application expanded to user authentication, PDF uploads, document records, document summaries/topics, chat sessions, message history, document-scoped retrieval, and multi-document behavior.

## Frontend

The project moved beyond the initial lightweight UI direction to a dedicated Next.js/React/TypeScript frontend while retaining the FastAPI backend as the application API.

## Engineering hardening

The backend was progressively moved to strict typing. Ruff, strict mypy, pytest, frontend checks, Docker build checks, and GitHub Actions became the quality gate.

An important CI portability issue was discovered when PDF tests relied on a local `data/uploads/Data_Engineering.pdf`. The tests were made self-contained so they could pass on a clean Linux CI runner rather than only on the developer machine.

## v0.1.0 foundation

The `v0.1.0` milestone represents the stable engineering foundation of the project. The focus after this milestone shifts from adding basic components to evaluating retrieval/RAG quality, improving UX, hardening security/operations, and preparing a credible deployment.