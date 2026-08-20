# AWS deployment and operations

The Terraform environment under `infra/terraform/environments/dev` describes the current AWS development deployment. Its public CloudFront URL is [https://d1n9699wkr1rp7.cloudfront.net](https://d1n9699wkr1rp7.cloudfront.net). The login page and API health endpoint returned HTTP 200 on August 20, 2026.

This guide documents the deployment; none of its commands run automatically. Plan and review every infrastructure change before applying it.

## Runtime topology

```text
Internet
  |
  | HTTPS (CloudFront certificate)
  v
CloudFront
  |
  | HTTP to origin; ALB ingress restricted to CloudFront prefix list
  v
Public Application Load Balancer
  |-- /* --------> Next.js ECS service :3000
  `-- /api/* ----> FastAPI ECS service :8000
                         |-- RDS PostgreSQL :5432
                         |-- encrypted EFS mounted at /app/data
                         `-- private Bedrock Runtime endpoint
```

The ECS tasks have no public IP addresses. Public subnets host the load balancer; application tasks, RDS, EFS mount targets, and interface endpoints use private subnets.

## Provisioned services

Terraform manages:

- a two-Availability-Zone VPC with public and private subnets;
- an internet gateway and separate public/private route tables;
- immutable ECR repositories with lifecycle policies for backend and frontend images;
- an ECS cluster with Container Insights;
- ARM64 FastAPI and Next.js Fargate task definitions and services;
- deployment circuit breakers with automatic rollback;
- an internet-facing Application Load Balancer and two target groups;
- a no-cache CloudFront distribution that redirects viewers to HTTPS;
- RDS PostgreSQL with AWS-managed master credentials in Secrets Manager;
- encrypted EFS storage for uploads and ChromaDB;
- interface endpoints for ECR API/DKR, CloudWatch Logs, Secrets Manager, and Bedrock Runtime;
- an S3 gateway endpoint;
- CloudWatch log groups with 14-day retention;
- separate ECS execution and task roles.

## Deployment defaults

| Setting | Current Terraform behavior |
|---|---|
| AWS Region | `ap-south-1` by default |
| Environment | `dev` |
| Compute architecture | Linux ARM64 |
| API task | 1 vCPU, 4 GiB, desired count 1 |
| Frontend task | 0.25 vCPU, 512 MiB, desired count 1 |
| Generation | Amazon Bedrock, configured Nova inference profile |
| Retrieval | BGE embeddings, candidate pool 20, top 5, reranking enabled |
| Persistent mount | EFS at `/app/data` |
| API health | `/` for ECS/ALB; `/api/v1/health/` for readiness checks |
| Frontend health | `/login` |

## Prerequisites

- AWS CLI authenticated to the intended account
- Terraform `>= 1.6`
- Docker with Linux ARM64 build support
- permission to use ECR, ECS, EC2/VPC, ELB, CloudFront, RDS, EFS, IAM, Logs, Secrets Manager, and Bedrock
- an application secret stored as a JSON object in Secrets Manager with a `SECRET_KEY` field
- Bedrock model access for the configured inference profile and region

Do not deploy with AWS root credentials. Prefer a reviewed deployment role and, for shared environments, encrypted remote Terraform state with locking and versioning.

## 1. Inspect and configure Terraform

```bash
cd infra/terraform/environments/dev
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform fmt -check -recursive
terraform validate
terraform plan
```

Set `app_secret_arn` to the base ARN of the JSON secret. Terraform appends the `SECRET_KEY` selector when injecting it into the API task. Keep `terraform.tfvars`, state, and saved plan files out of Git.

## 2. Build and publish images

Run from the repository root:

```bash
REGION=ap-south-1
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
TAG=$(git rev-parse --short HEAD)

BACKEND_REPO="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/book-rag-dev-backend"
FRONTEND_REPO="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/book-rag-dev-frontend"

aws ecr get-login-password --region "$REGION" \
  | docker login --username AWS --password-stdin \
    "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com"

docker build --platform linux/arm64 \
  -f docker/Dockerfile.api \
  -t "$BACKEND_REPO:$TAG" .

docker build --platform linux/arm64 \
  -f docker/Dockerfile.frontend \
  --build-arg NEXT_PUBLIC_API_URL=/api/v1 \
  --build-arg NEXT_PUBLIC_APP_URL=https://your-domain.example \
  -t "$FRONTEND_REPO:$TAG" .

docker push "$BACKEND_REPO:$TAG"
docker push "$FRONTEND_REPO:$TAG"
```

Use immutable commit-derived tags. Confirm both tags exist in ECR before applying Terraform.

## 3. Plan and apply the release

```bash
cd infra/terraform/environments/dev
terraform plan \
  -var="backend_image_tag=$TAG" \
  -var="frontend_image_tag=$TAG" \
  -out=deployment.tfplan
terraform show deployment.tfplan
terraform apply deployment.tfplan
terraform output -raw live_app_url
```

Review replacements, security-group changes, database changes, and any destructive action before approval. Never apply a plan created from a different source revision or environment.

## 4. Verify the release

Start with infrastructure stability:

```bash
aws ecs wait services-stable \
  --region ap-south-1 \
  --cluster book-rag-dev \
  --services book-rag-dev-api book-rag-dev-frontend

aws ecs describe-services \
  --region ap-south-1 \
  --cluster book-rag-dev \
  --services book-rag-dev-api book-rag-dev-frontend
```

Check logs and public endpoints:

```bash
aws logs tail /ecs/book-rag-dev-api --region ap-south-1 --since 15m
aws logs tail /ecs/book-rag-dev-frontend --region ap-south-1 --since 15m

LIVE_URL=$(terraform output -raw live_app_url)
curl -I "$LIVE_URL/login"
curl "$LIVE_URL/api/v1/health/"
```

Expected readiness response:

```json
{"status":"healthy","service":"book-rag-api"}
```

Complete a smoke test through the UI:

1. Register a test account and sign in.
2. Upload a small, non-sensitive PDF.
3. Wait until document processing reaches `completed`.
4. Create a chat and select the document.
5. Ask a question whose answer is present in the PDF.
6. Confirm the answer is grounded and source cards identify the correct page.
7. Confirm another user cannot access the document or chat.

## Rollback

ECS deployment circuit breakers roll back tasks that fail to become healthy. For an application rollback, redeploy previously known-good immutable image tags through a reviewed Terraform plan. Check ECS service events and both CloudWatch log groups before retrying a failed release.

Do not roll back database migrations blindly. Confirm schema compatibility with the target application version and restore from a tested backup when necessary.

## Operational checks

Review these routinely:

- ECS desired/running task counts and recent service events;
- ALB target health for the API and frontend target groups;
- API/frontend CloudWatch errors and latency;
- RDS connections, free storage, CPU, and backup status;
- EFS storage growth and mount health;
- CloudFront error rate;
- Bedrock errors, throttling, latency, and spend;
- ECR image retention and vulnerability findings;
- AWS Budgets alerts.

## Data, backup, and teardown safety

RDS contains users, document records, sessions, messages, and citations. EFS contains uploaded PDFs and ChromaDB data. Before any teardown, export required relational data and preserve required EFS content. Review a destroy plan line by line; deleting RDS or EFS can permanently remove user data.

If the vector index is considered rebuildable, test the rebuild process from retained source PDFs and PostgreSQL metadata before relying on that assumption.

## Cost awareness

Continuous costs include RDS, ALB, EFS, interface VPC endpoints, Fargate, CloudFront traffic, CloudWatch Logs, ECR storage, and Bedrock usage. Configure AWS Budgets alerts and remove unused development resources only through a reviewed plan.

## Production hardening

Before public production use:

- add a custom domain and ACM certificate;
- move Terraform state to an encrypted remote backend with locking and versioning;
- deploy through CI with a non-root IAM role and environment approvals;
- add WAF/rate limiting, CloudWatch alarms, tracing, dashboards, and incident alerts;
- restrict registration or add verified email and account recovery;
- add upload-size quotas, content validation, and malware scanning;
- define retention/deletion behavior for PDFs, relational records, and vector indexes;
- test RDS/EFS backup and restore procedures;
- narrow Bedrock IAM resources where supported by the chosen model/inference profile;
- run dependency, container, IaC, and secret scanning;
- run retrieval and grounded-answer evaluation for each release;
- document incident response and disaster recovery objectives.
