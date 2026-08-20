resource "aws_security_group" "efs" {
  name_prefix = "${var.project_name}-${var.environment}-efs-"
  description = "NFS access for Book RAG application storage"
  vpc_id      = var.vpc_id

  ingress {
    description = "NFS from application resources in the VPC"
    from_port   = 2049
    to_port     = 2049
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-efs-sg"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_efs_file_system" "this" {
  encrypted        = true
  performance_mode = "generalPurpose"
  throughput_mode  = "bursting"

  lifecycle_policy {
    transition_to_ia = "AFTER_30_DAYS"
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-data"
  }
}

resource "aws_efs_mount_target" "this" {
  for_each = toset(var.private_subnet_ids)

  file_system_id  = aws_efs_file_system.this.id
  subnet_id       = each.value
  security_groups = [aws_security_group.efs.id]
}

resource "aws_efs_access_point" "app" {
  file_system_id = aws_efs_file_system.this.id

  posix_user {
    gid = 0
    uid = 0
  }

  root_directory {
    path = "/book-rag"

    creation_info {
      owner_gid   = 0
      owner_uid   = 0
      permissions = "0755"
    }
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-app-data"
  }
}
