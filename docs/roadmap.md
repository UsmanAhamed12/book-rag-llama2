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
- query-aware BGE embeddings and cross-encoder score fusion
- responsive product UI and mobile chat workflows
- Terraform-managed AWS deployment on CloudFront and ECS Fargate

## Next — Measured retrieval quality

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

## Next — Product evolution

- streaming answers;
- a full-page source/citation reader;
- background ingestion progress;
- keyboard shortcuts and saved prompt templates;
- verified email and account recovery.

## Phase 4 — Production hardening

- rate limiting;
- structured observability;
- health/readiness checks;
- stronger upload validation/limits;
- dependency/security scanning;
- backup/restore plan;
- production secret management;
- authorization/security tests.

## Next — Delivery automation

- custom domain and ACM certificate;
- remote Terraform state and locking;
- CI/CD image promotion and environment approvals;
- synthetic monitoring and rollback drills.

## Optional advanced work

- hybrid lexical/vector retrieval;
- background ingestion jobs;
- streaming responses;
- model/provider abstraction;
- Kubernetes only if the operational complexity is justified;
- integration of the separate O/L paper-marking workflow as an independent bounded module rather than mixing responsibilities into the core book RAG pipeline.
