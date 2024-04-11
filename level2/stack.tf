# MODEL TRAINING
# Cloud Functions? to build training image
# 

# Cloud Run to compile and training pipeline with training image
# python define_pipeline.py
# push .yaml to gcs

# Cloud Functions to run training pipeline
# pull .yaml from gcs
# google.loud.aiplatform.PipelineJob().submit()

# Scheduler for training pipeline
# resource "google_cloud_scheduler_job" "job" {}

# Orchestrate the above steps

locals {
  project = "simple-pipeline-415719"
}

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  project = local.project
}

# Create project bucket
resource "google_storage_bucket" "bucket" {
  name     = "${local.project}-bucket"
  location = "US"
  uniform_bucket_level_access = true
}

# Zip up test code
data "archive_file" "test" {
  type        = "zip"
  source_dir  = "test_function"
  output_path = "temp/test.zip"
}

# Push test code to bucket
resource "google_storage_bucket_object" "object" {
  name   = "temp/test.zip"
  bucket = google_storage_bucket.bucket.name
  source = "test.zip"
}

resource "google_cloudfunctions2_function" "function" {
  name = "test"
  location = "us-west1"
  description = "test function"

  build_config {
    runtime = "python310"
    entry_point = "main"  # Set the entry point 
    source {
      storage_source {
        bucket = google_storage_bucket.bucket.name
        object = google_storage_bucket_object.object.name
      }
    }
  }
}