variable "project_name" {
  type        = string
  description = "Project name."
}

variable "environment" {
  type        = string
  description = "Deployment environment."
}

variable "vpc_id" {
  type        = string
  description = "VPC ID."
}

variable "private_subnet_ids" {
  type        = list(string)
  description = "Private subnet IDs for RDS."
}

variable "database_name" {
  type        = string
  description = "PostgreSQL database name."
  default     = "book_rag"
}

variable "database_username" {
  type        = string
  description = "PostgreSQL master username."
  default     = "bookrag_admin"
}

variable "instance_class" {
  type        = string
  description = "RDS instance class."
  default     = "db.t4g.micro"
}
