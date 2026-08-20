variable "project_name" {
  description = "Project name used for resource naming."
  type        = string
}

variable "environment" {
  description = "Deployment environment."
  type        = string
}

variable "aws_region" {
  description = "AWS region containing the VPC."
  type        = string
}

variable "vpc_id" {
  description = "ID of the VPC."
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block of the VPC."
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnet IDs used by interface endpoints."
  type        = list(string)
}

variable "private_route_table_id" {
  description = "Private route table ID used by the S3 gateway endpoint."
  type        = string
}