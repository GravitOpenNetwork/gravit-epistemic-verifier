terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# VPC, Subnets, Security Groups...

module "gravit_verifier" {
  source = "./modules/verifier"

  app_name      = "gravit-epistemic-verifier"
  container_image = "ghcr.io/gravit-network/gravit-epistemic-verifier:1.0.0"
  desired_count = 2

  environment = {
    PYTHONUNBUFFERED = "1"
  }
}

output "load_balancer_dns" {
  value = module.gravit_verifier.lb_dns
}
