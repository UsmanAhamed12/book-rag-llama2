module "networking" {
  source = "../../modules/networking"

  project_name = var.project_name
  environment  = var.environment

  vpc_cidr = var.vpc_cidr

  availability_zones = var.availability_zones

  public_subnet_cidrs = var.public_subnet_cidrs

  private_subnet_cidrs = var.private_subnet_cidrs
}

module "ecr" {
  source = "../../modules/ecr"

  project_name = var.project_name
  environment  = var.environment
}

module "database" {
  source = "../../modules/database"

  project_name = var.project_name
  environment  = var.environment

  vpc_id             = module.networking.vpc_id
  private_subnet_ids = module.networking.private_subnet_ids

  database_name     = var.database_name
  database_username = var.database_username
  instance_class    = var.database_instance_class
}


module "vpc_endpoints" {
  source = "../../modules/vpc_endpoints"

  project_name = var.project_name
  environment  = var.environment
  aws_region   = var.aws_region

  vpc_id   = module.networking.vpc_id
  vpc_cidr = var.vpc_cidr

  private_subnet_ids = module.networking.private_subnet_ids

  private_route_table_id = module.networking.private_route_table_id
}

module "storage" {
  source = "../../modules/storage"

  project_name = var.project_name
  environment  = var.environment
  vpc_id       = module.networking.vpc_id
  vpc_cidr     = var.vpc_cidr

  private_subnet_ids = module.networking.private_subnet_ids
}

module "ecs" {
  source = "../../modules/ecs"

  project_name = var.project_name
  environment  = var.environment
  aws_region   = var.aws_region

  vpc_id             = module.networking.vpc_id
  public_subnet_ids  = module.networking.public_subnet_ids
  private_subnet_ids = module.networking.private_subnet_ids

  api_image_uri      = "${module.ecr.backend_repository_url}:${var.backend_image_tag}"
  frontend_image_uri = "${module.ecr.frontend_repository_url}:${var.frontend_image_tag}"

  database_host              = module.database.database_endpoint
  database_port              = module.database.database_port
  database_name              = var.database_name
  database_secret_arn        = module.database.master_user_secret_arn
  database_security_group_id = module.database.database_security_group_id

  app_secret_arn = var.app_secret_arn

  efs_file_system_id  = module.storage.file_system_id
  efs_access_point_id = module.storage.access_point_id
  bedrock_model       = var.bedrock_model
}
