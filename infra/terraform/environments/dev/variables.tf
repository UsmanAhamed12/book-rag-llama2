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
