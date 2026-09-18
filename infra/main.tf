terraform {
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


# --------------------------------------------------
# S3
# --------------------------------------------------

resource "aws_s3_bucket" "foro" {
  bucket = "foro-avance2-alexa-2026"
}

resource "aws_s3_bucket_public_access_block" "foro" {
  bucket = aws_s3_bucket.foro.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "foro" {
  bucket = aws_s3_bucket.foro.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}


# --------------------------------------------------
# RDS POSTGRESQL
# --------------------------------------------------

variable "db_password" {
  description = "Contraseña de la base de datos"
  type        = string
  sensitive   = true
}

resource "aws_db_instance" "foro" {
  identifier = "foro-db"

  engine         = "postgres"
  engine_version = "18.3"

  instance_class        = "db.t3.micro"
  allocated_storage     = 20
  storage_type          = "gp3"
  storage_encrypted     = true
  publicly_accessible   = false

  db_name  = "foro"
  username = "foro_admin"
  password = var.db_password
  port     = 5432

  backup_retention_period = 1

  multi_az            = false
  deletion_protection = false
  skip_final_snapshot = true
}