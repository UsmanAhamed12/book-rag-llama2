output "file_system_id" {
  description = "EFS file system ID."
  value       = aws_efs_file_system.this.id
}

output "access_point_id" {
  description = "EFS access point used by the API task."
  value       = aws_efs_access_point.app.id
}
