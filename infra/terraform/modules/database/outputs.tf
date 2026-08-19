output "database_endpoint" {
  description = "RDS PostgreSQL endpoint."
  value       = aws_db_instance.this.address
}

output "database_port" {
  description = "RDS PostgreSQL port."
  value       = aws_db_instance.this.port
}

output "database_name" {
  description = "Database name."
  value       = aws_db_instance.this.db_name
}

output "database_username" {
  description = "Database username."
  value       = aws_db_instance.this.username
}

output "database_security_group_id" {
  description = "Database security group ID."
  value       = aws_security_group.database.id
}

output "master_user_secret_arn" {
  description = "Secrets Manager ARN containing the RDS master credentials."
  value       = try(aws_db_instance.this.master_user_secret[0].secret_arn, null)
}
