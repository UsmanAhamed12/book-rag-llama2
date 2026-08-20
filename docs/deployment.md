# AWS deployment

The live development environment is available at [https://d1n9699wkr1rp7.cloudfront.net](https://d1n9699wkr1rp7.cloudfront.net).

## Provisioned services

Terraform under `infra/terraform` manages:

- a two-AZ VPC with public and private subnets;
- ECR repositories for immutable backend and frontend images;
- ECS Fargate services and deployment circuit breakers;
- an Application Load Balancer with separate API/frontend target groups;
- CloudFront with viewer HTTPS and dynamic request forwarding;
- RDS PostgreSQL with generated credentials in Secrets Manager;
- encrypted EFS storage for uploads and ChromaDB;
- private endpoints for ECR, CloudWatch Logs, Secrets Manager, S3, and Bedrock Runtime;
- least-purpose ECS execution and Bedrock task roles.

## Prerequisites

- AWS CLI authenticated to the intended account
- Terraform `>= 1.6`
- Docker with ARM64 build support
- an application secret stored as JSON in Secrets Manager with a `SECRET_KEY` field

Do not deploy from an AWS root credential. Use a dedicated deployment role with reviewed permissions and remote Terraform state/locking for shared or production environments.

## Build and publish images

```bash
REGION=ap-south-1
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
TAG=$(git rev-parse --short HEAD)

aws ecr get-login-password --region "$REGION" \
  | docker login --username AWS --password-stdin \
    "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com"

docker build --platform linux/arm64 \
  -f docker/Dockerfile.api \
  -t "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/book-rag-dev-backend:$TAG" .

docker build --platform linux/arm64 \
  -f docker/Dockerfile.frontend \
  --build-arg NEXT_PUBLIC_API_URL=/api/v1 \
  --build-arg NEXT_PUBLIC_APP_URL=https://your-domain.example \
  -t "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/book-rag-dev-frontend:$TAG" .

docker push "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/book-rag-dev-backend:$TAG"
docker push "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/book-rag-dev-frontend:$TAG"
```

## Plan and apply

```bash
cd infra/terraform/environments/dev
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform fmt -check -recursive
terraform validate
terraform plan \
  -var="backend_image_tag=$TAG" \
  -var="frontend_image_tag=$TAG" \
  -out=deployment.tfplan
terraform apply deployment.tfplan
terraform output -raw live_app_url
```

Supply the base Secrets Manager ARN in `app_secret_arn`; Terraform appends the `SECRET_KEY` JSON-key selector for the ECS task definition.

## Verify a release

```bash
aws ecs wait services-stable \
  --region ap-south-1 \
  --cluster book-rag-dev \
  --services book-rag-dev-api book-rag-dev-frontend

aws logs tail /ecs/book-rag-dev-api --region ap-south-1 --since 15m
curl -I "$(terraform output -raw live_app_url)/login"
curl "$(terraform output -raw live_app_url)/api/v1/health/"
```

Also verify both target groups report `healthy`, registration/login succeeds, a PDF reaches `completed`, and a cited question reaches Bedrock successfully.

## Operations and cost

The main continuous costs are RDS, the load balancer, EFS, interface VPC endpoints, Fargate, CloudFront transfer, logs, and Bedrock usage. Set AWS Budgets alerts before leaving a development stack running. ECR lifecycle rules limit old images, but database backups, log retention, and document-retention policy still require an explicit production decision.

Before destroying an environment, export any required relational data and EFS content. Then review a destroy plan carefully; RDS and EFS contain durable user data.

## Production hardening

- Use a custom domain and ACM certificate.
- Move Terraform state to an encrypted remote backend with locking and versioning.
- Deploy through a non-root IAM role and CI environment approvals.
- Add WAF/rate limiting, alarms, tracing, dashboards, and backup-restore drills.
- Restrict registration or add verified email before public promotion.
- Define retention and deletion behavior for uploaded books and vector indexes.
- Run security scanning and a retrieval evaluation suite for every release.
