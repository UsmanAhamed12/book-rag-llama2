# Architecture

Book RAG separates product UI, API workflows, retrieval, generation, relational persistence, and vector storage. The same application code supports a local Ollama environment and an AWS Bedrock environment.

## Runtime topology

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
                         |-- encrypted EFS (uploads + ChromaDB)
                         `-- Bedrock Runtime VPC endpoint -> Amazon Nova
```

The load balancer accepts traffic only from the AWS-managed CloudFront origin-facing prefix list. ECS tasks, RDS, EFS mount targets, and interface endpoints live inside the VPC; application tasks do not receive public IP addresses.

## Request flow

1. CloudFront terminates viewer HTTPS and forwards dynamic requests without caching application or authorization state.
2. The load balancer routes `/api/*` requests to FastAPI and all remaining paths to Next.js.
3. The frontend stores the bearer token in the browser and calls the same public origin, avoiding cross-origin deployment complexity.
4. FastAPI validates the user and scopes documents, sessions, messages, and retrieval filters to that user.
5. PostgreSQL stores durable entities; ChromaDB stores embeddings and citation metadata on EFS.
6. The LLM service selects Ollama or Bedrock from configuration without changing the RAG pipeline.

## Backend boundaries

| Package | Responsibility |
|---|---|
| `app/api` | HTTP routing, validation, dependencies, response contracts |
| `app/services` | Document, upload, memory, and application workflows |
| `app/ingestion` | PDF extraction, cleaning, chunking, indexing |
| `app/embeddings` | Query/document embedding abstraction |
| `app/retrieval` | Vector candidates, reranking, score fusion |
| `app/rag` | Query rewrite, relevance gate, prompt, citations |
| `app/llm` | Ollama and Amazon Bedrock clients |
| `app/db` and `app/models` | Persistence infrastructure and entities |

Routes remain thin, user-owned queries must include ownership scope, and API contracts remain typed. PostgreSQL and ChromaDB have deliberately different responsibilities: relational consistency versus similarity search.

## Frontend structure

`frontend/app` contains Next.js routes and `frontend/components` contains reusable product primitives. The authenticated shell supplies responsive navigation, theme controls, identity, and session actions. The main workflows are:

- overview and recent activity;
- PDF library upload, processing, selection, and removal;
- chat session creation and switching;
- grounded answers with readable source cards and mobile-safe interaction states.

## Data and durability

- RDS PostgreSQL stores users, documents, chat sessions, messages, and citation JSON.
- EFS persists uploads and the ChromaDB directory across Fargate task replacements.
- ECR repositories are immutable and lifecycle-managed.
- Secrets Manager injects the application signing key and RDS-generated credentials at task startup.
- CloudWatch log groups retain frontend and API container logs.

## Deployment properties

Terraform owns networking, endpoints, RDS, EFS, IAM, ECR, ECS, the load balancer, and CloudFront. ECS deployment circuit breakers provide rollback behavior when a new task cannot become healthy. See [deployment.md](deployment.md) for operational commands.

## Engineering rules

- Never mix one user's document IDs or chat history into another user's query.
- Treat retrieved document content as untrusted data, not prompt instructions.
- Keep model/provider details behind the LLM service boundary.
- Persist only citations that were actually supplied to generation.
- Keep secrets, uploads, indexes, caches, and Terraform plan files out of version control.
- Validate changes with backend, frontend, container, and Terraform quality gates.
