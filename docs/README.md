# Book RAG documentation

This directory documents the current application, local workflow, quality gates, and AWS development deployment. The checked-out code and generated FastAPI OpenAPI schema remain authoritative when behavior changes.

## Start here

| Goal | Guide |
|---|---|
| Run the project locally | [Getting Started](getting-started.md) |
| Understand the system | [Architecture](architecture.md) |
| Understand ingestion and question answering | [RAG Pipeline](rag-pipeline.md) |
| Integrate with the backend | [API Guide](api.md) |
| Work with users and tokens | [Authentication](authentication.md) |
| Understand stored data | [Database and Persistence](database.md) |
| Contribute safely | [Development Guide](development.md) |
| Run quality checks | [Testing and Quality](testing.md) |
| Use local containers | [Docker](docker.md) |
| Build, deploy, and operate AWS | [AWS Deployment](deployment.md) |
| Review security expectations | [Security](security.md) |
| Diagnose common failures | [Troubleshooting](troubleshooting.md) |
| Review project evolution | [Project History](project-history.md) |
| See completed and planned work | [Roadmap](roadmap.md) |

## System at a glance

- Next.js 16 and React 19 provide the browser application.
- FastAPI exposes versioned endpoints under `/api/v1`.
- PostgreSQL stores users, documents, sessions, messages, and citations.
- ChromaDB stores document embeddings and retrieval metadata.
- Ollama provides local generation; Amazon Bedrock provides AWS generation.
- Terraform provisions the AWS development environment.
- CloudFront is the public HTTPS entry point and forwards to an Application Load Balancer.
- ECS Fargate runs separate frontend and API services in private subnets.
- RDS stores relational data; encrypted EFS persists uploads and ChromaDB.

## Documentation conventions

- Commands are run from the repository root unless a guide explicitly changes directory.
- Replace sample account IDs, domains, ARNs, tags, and secret values before use.
- Never commit `.env`, `terraform.tfvars`, Terraform state/plans, private documents, or credentials.
- Deployment commands describe the infrastructure already represented in this repository; they do not run automatically by reading these docs.
- The development deployment is not a declaration of production readiness.

## Documentation maintenance

When behavior changes, update the closest topic guide and the root README in the same pull request. Verify relative Markdown links, copy/paste command paths, environment-variable names, API prefixes, and deployment outputs against the repository before merging.
