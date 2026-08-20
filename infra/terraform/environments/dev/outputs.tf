output "aws_region" {
  description = "AWS region configured for this environment."
  value       = var.aws_region
}

output "project_name" {
  description = "Project name."
  value       = var.project_name
}

output "environment" {
  description = "Deployment environment."
  value       = var.environment
}

output "vpc_id" {
  description = "Development VPC ID."
  value       = module.networking.vpc_id
}

output "public_subnet_ids" {
  description = "Development public subnet IDs."
  value       = module.networking.public_subnet_ids
}

output "private_subnet_ids" {
  description = "Development private subnet IDs."
  value       = module.networking.private_subnet_ids
}

output "backend_ecr_repository_name" {
  description = "Backend ECR repository name."
  value       = module.ecr.backend_repository_name
}

output "backend_ecr_repository_url" {
  description = "Backend ECR repository URL."
  value       = module.ecr.backend_repository_url
}

output "database_endpoint" {
  description = "RDS PostgreSQL endpoint."
  value       = module.database.database_endpoint
}

output "database_port" {
  description = "RDS PostgreSQL port."
  value       = module.database.database_port
}

output "database_security_group_id" {
  description = "RDS security group ID."
  value       = module.database.database_security_group_id
}

output "database_master_secret_arn" {
  description = "Secrets Manager ARN for RDS master credentials."
  value       = module.database.master_user_secret_arn
}


output "vpc_endpoint_security_group_id" {
  description = "Security group used by interface VPC endpoints."
  value       = module.vpc_endpoints.security_group_id
}

output "vpc_interface_endpoint_ids" {
  description = "Interface VPC endpoint IDs."
  value       = module.vpc_endpoints.interface_endpoint_ids
}

output "s3_vpc_endpoint_id" {
  description = "S3 gateway VPC endpoint ID."
  value       = module.vpc_endpoints.s3_endpoint_id
}