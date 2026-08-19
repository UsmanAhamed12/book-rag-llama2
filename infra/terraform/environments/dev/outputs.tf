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
