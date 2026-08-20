variable "project_name" { type = string }
variable "environment" { type = string }
variable "aws_region" { type = string }
variable "vpc_id" { type = string }
variable "public_subnet_ids" { type = list(string) }
variable "private_subnet_ids" { type = list(string) }
variable "api_image_uri" { type = string }
variable "frontend_image_uri" { type = string }
variable "database_host" { type = string }
variable "database_port" { type = number }
variable "database_name" { type = string }
variable "database_secret_arn" { type = string }
variable "app_secret_arn" { type = string }
variable "database_security_group_id" { type = string }
variable "efs_file_system_id" { type = string }
variable "efs_access_point_id" { type = string }

variable "bedrock_model" {
  description = "Bedrock inference profile used for grounded answer generation."
  type        = string
  default     = "apac.amazon.nova-lite-v1:0"
}
