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