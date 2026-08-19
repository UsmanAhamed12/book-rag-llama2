# Roadmap

## Completed foundation

- FastAPI backend architecture
- environment/settings management
- PDF loading and text cleaning
- recursive chunking
- embedding service
- ChromaDB vector storage/retrieval
- RAG prompt/pipeline
- local Ollama integration
- PostgreSQL persistence
- JWT authentication
- document management
- chat sessions and memory
- multi-document/document-profile behavior
- Next.js frontend foundation
- strict mypy typing
- Ruff lint/format checks
- pytest suite
- Docker build validation
- GitHub Actions CI

## Phase 1 — Retrieval quality

- create a fixed evaluation question set;
- measure retrieval relevance/recall;
- tune chunk size/overlap and relevance threshold;
- evaluate query rewriting;
- improve multi-document retrieval;
- verify citation correctness.

## Phase 2 — RAG evaluation

- answer faithfulness tests;
- answer relevance tests;
- citation-grounding tests;
- latency measurements;
- failure/no-context evaluation;
- regression benchmark stored in CI-friendly fixtures.

## Phase 3 — Product polish

- improved upload/processing UX;
- richer document library;
- source/citation viewer;
- loading/error/empty states;
- responsive frontend;
- chat/session UX improvements.

## Phase 4 — Production hardening

- rate limiting;
- structured observability;
- health/readiness checks;
- stronger upload validation/limits;
- dependency/security scanning;
- backup/restore plan;
- production secret management;
- authorization/security tests.

## Phase 5 — Deployment

- finalize container/service topology;
- deploy backend/database/vector persistence;
- deploy frontend;
- configure HTTPS/domain;
- CI/CD deployment workflow;
- monitoring and rollback strategy.

## Optional advanced work

- reranking/hybrid retrieval;
- background ingestion jobs;
- streaming responses;
- model/provider abstraction;
- Kubernetes only if the operational complexity is justified;
- integration of the separate O/L paper-marking workflow as an independent bounded module rather than mixing responsibilities into the core book RAG pipeline.