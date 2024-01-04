variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "aws_region" {}

provider "aws" {
    access_key = var.aws_access_key
    secret_key = var.aws_secret_key
    region = var.aws_region
}

# Create ECR
resource "aws_ecr_repository" "translation_app_ecr_repo" {
  name = "translation-app-repo"
}
