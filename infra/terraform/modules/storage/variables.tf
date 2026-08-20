variable "project_name" {
  description = "Project name."
  type        = string
}

variable "environment" {
  description = "Deployment environment."
  type        = string
}

variable "vpc_id" {
  description = "VPC ID."
  type        = string
}

variable "vpc_cidr" {
  description = "VPC CIDR allowed to mount the file system."
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnets for EFS mount targets."
  type        = list(string)
}
