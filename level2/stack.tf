locals {
  project = "simple-pipeline-415719"
  location = "us-west1"
}

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.24.0"
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

# Create Artifact Registry Repository
resource "google_artifact_registry_repository" "repo" {
  project = local.project
  location = local.location
  repository_id = local.project
  format = "DOCKER"
}

# Create Cloud Function to compile and run pipeline
data "archive_file" "pipeline_zip" {
  type        = "zip"
  source_dir  = "pipeline_function"
  output_path = "temp/pipeline_function.zip"
}

resource "google_storage_bucket_object" "pipeline_obj" {
  name   = data.archive_file.pipeline_zip.id
  bucket = google_storage_bucket.bucket.name
  source = data.archive_file.pipeline_zip.output_path
}

resource "google_cloudfunctions2_function" "pipeline_function" {
  name = "pipeline_function"
  location = local.location
  description = "Compile and run pipeline"

  build_config {
    runtime = "python310"
    entry_point = "main"  # Set the entry point 
    source {
      storage_source {
        bucket = google_storage_bucket.bucket.name
        object = google_storage_bucket_object.pipeline_obj.name
      }
    }
  }

  lifecycle {ignore_changes = [service_config]}
}