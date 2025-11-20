terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# -------------------------
# VPC Module
# -------------------------
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "tf-eks-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true
}

# -------------------------
# EKS Module
# -------------------------
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "20.17.0" # MUST match this version for aws_auth support

  cluster_name    = "tf-eks-cluster"
  cluster_version = "1.29"

  cluster_endpoint_public_access = true

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  eks_managed_node_groups = {
    default = {
      desired_size   = 1
      max_size       = 2
      min_size       = 1
      instance_types = ["t3.medium"]
    }
  }

  # Automatically map your AWS IAM user into Kubernetes RBAC
  # NOTE: The top-level EKS module no longer supports managing the aws-auth
  # configmap directly. The module provides the rendered ConfigMap YAML via
  # the output `aws_auth_configmap_yaml` which you can apply with kubectl
  # after the cluster is created. Example:
  #
  #   terraform apply
  #   terraform output -raw module.eks.aws_auth_configmap_yaml > aws-auth.yaml
  #   kubectl apply -f aws-auth.yaml

}

output "cluster_name" {
  value = module.eks.cluster_name
}

output "cluster_endpoint" {
  value = module.eks.cluster_endpoint
}
