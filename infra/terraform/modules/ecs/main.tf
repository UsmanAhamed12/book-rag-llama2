data "aws_iam_policy_document" "ecs_task_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

data "aws_ec2_managed_prefix_list" "cloudfront" {
  name = "com.amazonaws.global.cloudfront.origin-facing"
}

resource "aws_ecs_cluster" "this" {
  name = "${var.project_name}-${var.environment}"
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
  tags = { Name = "${var.project_name}-${var.environment}" }
}

resource "aws_cloudwatch_log_group" "api" {
  name              = "/ecs/${var.project_name}-${var.environment}-api"
  retention_in_days = 14
}

resource "aws_cloudwatch_log_group" "frontend" {
  name              = "/ecs/${var.project_name}-${var.environment}-frontend"
  retention_in_days = 14
}

resource "aws_iam_role" "execution" {
  name               = "${var.project_name}-${var.environment}-ecs-execution"
  assume_role_policy = data.aws_iam_policy_document.ecs_task_assume_role.json
}

resource "aws_iam_role_policy_attachment" "execution" {
  role       = aws_iam_role.execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

data "aws_iam_policy_document" "execution_secrets" {
  statement {
    actions   = ["secretsmanager:GetSecretValue"]
    resources = [var.database_secret_arn, var.app_secret_arn]
  }
}

resource "aws_iam_role_policy" "execution_secrets" {
  name   = "${var.project_name}-${var.environment}-ecs-secrets"
  role   = aws_iam_role.execution.id
  policy = data.aws_iam_policy_document.execution_secrets.json
}

resource "aws_iam_role" "task" {
  name               = "${var.project_name}-${var.environment}-ecs-task"
  assume_role_policy = data.aws_iam_policy_document.ecs_task_assume_role.json
}

data "aws_iam_policy_document" "task_bedrock" {
  statement {
    actions   = ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"]
    resources = ["*"]
  }
}

resource "aws_iam_role_policy" "task_bedrock" {
  name   = "${var.project_name}-${var.environment}-bedrock"
  role   = aws_iam_role.task.id
  policy = data.aws_iam_policy_document.task_bedrock.json
}

resource "aws_security_group" "load_balancer" {
  name_prefix = "${var.project_name}-${var.environment}-alb-"
  description = "CloudFront access to the Book RAG load balancer"
  vpc_id      = var.vpc_id

  ingress {
    description     = "HTTP from CloudFront origin-facing network"
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    prefix_list_ids = [data.aws_ec2_managed_prefix_list.cloudfront.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "${var.project_name}-${var.environment}-alb-sg" }
  lifecycle { create_before_destroy = true }
}

resource "aws_security_group" "api" {
  name_prefix = "${var.project_name}-${var.environment}-api-"
  description = "Security group for Book RAG API ECS tasks"
  vpc_id      = var.vpc_id

  ingress {
    description     = "API traffic from the load balancer"
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [aws_security_group.load_balancer.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "${var.project_name}-${var.environment}-api-sg" }
  lifecycle { create_before_destroy = true }
}

resource "aws_security_group" "frontend" {
  name_prefix = "${var.project_name}-${var.environment}-frontend-"
  description = "Security group for Book RAG frontend ECS tasks"
  vpc_id      = var.vpc_id

  ingress {
    description     = "Frontend traffic from the load balancer"
    from_port       = 3000
    to_port         = 3000
    protocol        = "tcp"
    security_groups = [aws_security_group.load_balancer.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "${var.project_name}-${var.environment}-frontend-sg" }
  lifecycle { create_before_destroy = true }
}

resource "aws_vpc_security_group_ingress_rule" "database_from_api" {
  security_group_id            = var.database_security_group_id
  referenced_security_group_id = aws_security_group.api.id
  from_port                    = 5432
  to_port                      = 5432
  ip_protocol                  = "tcp"
  description                  = "PostgreSQL access from ECS API tasks"
}

resource "aws_lb" "this" {
  name                       = "${var.project_name}-${var.environment}"
  internal                   = false
  load_balancer_type         = "application"
  security_groups            = [aws_security_group.load_balancer.id]
  subnets                    = var.public_subnet_ids
  enable_deletion_protection = false
  drop_invalid_header_fields = true
  tags                       = { Name = "${var.project_name}-${var.environment}-alb" }
}

resource "aws_lb_target_group" "frontend" {
  name                 = "${var.project_name}-${var.environment}-web"
  port                 = 3000
  protocol             = "HTTP"
  target_type          = "ip"
  vpc_id               = var.vpc_id
  deregistration_delay = 30
  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 3
    interval            = 30
    path                = "/login"
    matcher             = "200-399"
    timeout             = 5
  }
}

resource "aws_lb_target_group" "api" {
  name                 = "${var.project_name}-${var.environment}-api"
  port                 = 8000
  protocol             = "HTTP"
  target_type          = "ip"
  vpc_id               = var.vpc_id
  deregistration_delay = 30
  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 3
    interval            = 30
    path                = "/"
    matcher             = "200"
    timeout             = 5
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.this.arn
  port              = 80
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.frontend.arn
  }
}

resource "aws_lb_listener_rule" "api" {
  listener_arn = aws_lb_listener.http.arn
  priority     = 10
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api.arn
  }
  condition {
    path_pattern { values = ["/api/*"] }
  }
}

resource "aws_ecs_task_definition" "api" {
  family                   = "${var.project_name}-${var.environment}-api"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "1024"
  memory                   = "4096"
  execution_role_arn       = aws_iam_role.execution.arn
  task_role_arn            = aws_iam_role.task.arn

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "ARM64"
  }

  volume {
    name = "app-data"
    efs_volume_configuration {
      file_system_id     = var.efs_file_system_id
      transit_encryption = "ENABLED"
      authorization_config {
        access_point_id = var.efs_access_point_id
        iam             = "DISABLED"
      }
    }
  }

  container_definitions = jsonencode([
    {
      name         = "api"
      image        = var.api_image_uri
      essential    = true
      portMappings = [{ containerPort = 8000, hostPort = 8000, protocol = "tcp" }]
      mountPoints  = [{ sourceVolume = "app-data", containerPath = "/app/data", readOnly = false }]
      environment = [
        { name = "ENVIRONMENT", value = var.environment },
        { name = "POSTGRES_HOST", value = var.database_host },
        { name = "POSTGRES_PORT", value = tostring(var.database_port) },
        { name = "POSTGRES_DB", value = var.database_name },
        { name = "ALGORITHM", value = "HS256" },
        { name = "ACCESS_TOKEN_EXPIRE_MINUTES", value = "60" },
        { name = "LLM_PROVIDER", value = "bedrock" },
        { name = "BEDROCK_MODEL", value = var.bedrock_model },
        { name = "BEDROCK_REGION", value = var.aws_region },
        { name = "CHROMA_DB_PATH", value = "/app/data/chroma" },
        { name = "CHROMA_PATH", value = "/app/data/chroma" },
        { name = "UPLOAD_DIR", value = "/app/data/uploads" },
        { name = "EMBEDDING_MODEL", value = "BAAI/bge-small-en-v1.5" },
        { name = "RERANKING_ENABLED", value = "true" },
        { name = "RERANKER_MODEL", value = "cross-encoder/ms-marco-MiniLM-L6-v2" },
        { name = "RETRIEVAL_CANDIDATE_K", value = "20" },
        { name = "RETRIEVAL_TOP_K", value = "5" },
        { name = "RETRIEVAL_MINIMUM_SCORE", value = "0.35" },
        { name = "RERANKER_WEIGHT", value = "0.7" },
      ]
      secrets = [
        { name = "POSTGRES_USER", valueFrom = "${var.database_secret_arn}:username::" },
        { name = "POSTGRES_PASSWORD", valueFrom = "${var.database_secret_arn}:password::" },
        { name = "SECRET_KEY", valueFrom = "${var.app_secret_arn}:SECRET_KEY::" },
      ]
      healthCheck = {
        command     = ["CMD-SHELL", "python -c \"import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/', timeout=2).read()\" || exit 1"]
        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 90
      }
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.api.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "api"
        }
      }
    }
  ])
}

resource "aws_ecs_task_definition" "frontend" {
  family                   = "${var.project_name}-${var.environment}-frontend"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.execution.arn
  task_role_arn            = aws_iam_role.task.arn

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "ARM64"
  }

  container_definitions = jsonencode([
    {
      name      = "frontend"
      image     = var.frontend_image_uri
      essential = true
      environment = [
        { name = "HOSTNAME", value = "0.0.0.0" },
        { name = "PORT", value = "3000" },
      ]
      portMappings = [{ containerPort = 3000, hostPort = 3000, protocol = "tcp" }]
      healthCheck = {
        command     = ["CMD-SHELL", "wget -q -O /dev/null http://$HOSTNAME:3000/login || exit 1"]
        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 30
      }
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.frontend.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "frontend"
        }
      }
    }
  ])
}

resource "aws_ecs_service" "api" {
  name            = "${var.project_name}-${var.environment}-api"
  cluster         = aws_ecs_cluster.this.id
  task_definition = aws_ecs_task_definition.api.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }
  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.api.id]
    assign_public_ip = false
  }
  load_balancer {
    target_group_arn = aws_lb_target_group.api.arn
    container_name   = "api"
    container_port   = 8000
  }
  depends_on = [aws_lb_listener_rule.api]
}

resource "aws_ecs_service" "frontend" {
  name            = "${var.project_name}-${var.environment}-frontend"
  cluster         = aws_ecs_cluster.this.id
  task_definition = aws_ecs_task_definition.frontend.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }
  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.frontend.id]
    assign_public_ip = false
  }
  load_balancer {
    target_group_arn = aws_lb_target_group.frontend.arn
    container_name   = "frontend"
    container_port   = 3000
  }
  depends_on = [aws_lb_listener.http]
}

resource "aws_cloudfront_cache_policy" "dynamic" {
  name        = "${var.project_name}-${var.environment}-dynamic"
  default_ttl = 0
  max_ttl     = 0
  min_ttl     = 0
  parameters_in_cache_key_and_forwarded_to_origin {
    cookies_config { cookie_behavior = "none" }
    headers_config { header_behavior = "none" }
    query_strings_config { query_string_behavior = "none" }
    enable_accept_encoding_brotli = false
    enable_accept_encoding_gzip   = false
  }
}

resource "aws_cloudfront_origin_request_policy" "all_viewer_except_host" {
  name = "${var.project_name}-${var.environment}-viewer-headers"
  cookies_config { cookie_behavior = "all" }
  query_strings_config { query_string_behavior = "all" }
  headers_config {
    header_behavior = "allExcept"
    headers { items = ["Host"] }
  }
}

resource "aws_cloudfront_distribution" "this" {
  enabled         = true
  is_ipv6_enabled = true
  comment         = "${var.project_name}-${var.environment} application"
  price_class     = "PriceClass_200"

  origin {
    domain_name = aws_lb.this.dns_name
    origin_id   = "application-load-balancer"
    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  default_cache_behavior {
    target_origin_id         = "application-load-balancer"
    viewer_protocol_policy   = "redirect-to-https"
    allowed_methods          = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods           = ["GET", "HEAD"]
    compress                 = true
    cache_policy_id          = aws_cloudfront_cache_policy.dynamic.id
    origin_request_policy_id = aws_cloudfront_origin_request_policy.all_viewer_except_host.id
  }

  restrictions {
    geo_restriction { restriction_type = "none" }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
    minimum_protocol_version       = "TLSv1.2_2021"
  }

  tags = { Name = "${var.project_name}-${var.environment}" }
}
