variable "aws_region" {
  description = "AWS region used for the deployment."
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Name of the application."
  type        = string
  default     = "book-rag"
}

variable "environment" {
  description = "Deployment environment."
  type        = string
  default     = "dev"
}

variable "vpc_cidr" {
  description = "CIDR block for the development VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Availability zones used by the development environment."
  type        = list(string)
  default = [
    "ap-south-1a",
    "ap-south-1b",
  ]
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets."
  type        = list(string)
  default = [
    "10.0.1.0/24",
    "10.0.2.0/24",
  ]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets."
  type        = list(string)
  default = [
    "10.0.11.0/24",
    "10.0.12.0/24",
  ]
}

variable "database_name" {
  description = "PostgreSQL database name."
  type        = string
  default     = "book_rag"
}

variable "database_username" {
  description = "PostgreSQL master username."
  type        = string
  default     = "bookrag_admin"
}

variable "database_instance_class" {
  description = "RDS instance class for development."
  type        = string
  default     = "db.t4g.micro"
}

variable "backend_image_tag" {
  description = "Immutable ECR image tag deployed to ECS."
  type        = string
  default     = "production"
}

variable "frontend_image_tag" {
  description = "Immutable frontend ECR image tag deployed to ECS."
  type        = string
  default     = "production"
}

variable "app_secret_arn" {
  description = "Secrets Manager ARN containing application secrets."
  type        = string
}

variable "bedrock_model" {
  description = "Amazon Bedrock inference profile for generation."
  type        = string
  default     = "apac.amazon.nova-lite-v1:0"
}
