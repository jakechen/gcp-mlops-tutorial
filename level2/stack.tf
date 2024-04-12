locals {
  project = "simple-pipeline-415719"
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
  location = "us-west1"
  repository_id = "test-repo"
  format = "DOCKER"
}

# Create Cloud Function to compile pipeline
data "archive_file" "pipeline_compile_zip" {
  type        = "zip"
  source_dir  = "pipeline_compile"
  output_path = "temp/pipeline_compile.zip"
}

resource "google_storage_bucket_object" "pipeline_compile_obj" {
  name   = data.archive_file.pipeline_compile_zip.id
  bucket = google_storage_bucket.bucket.name
  source = data.archive_file.pipeline_compile_zip.output_path
}

resource "google_cloudfunctions2_function" "pipeline_compile_function" {
  name = "pipeline_compile"
  location = "us-west1"
  description = "Compile pipeline"

  build_config {
    runtime = "python310"
    entry_point = "main"  # Set the entry point 
    source {
      storage_source {
        bucket = google_storage_bucket.bucket.name
        object = google_storage_bucket_object.pipeline_compile_obj.name
      }
    }
  }
}

# Create Cloud Function to run pipeline
data "archive_file" "pipeline_run_zip" {
  type        = "zip"
  source_dir  = "pipeline_run"
  output_path = "temp/pipeline_run.zip"
}

resource "google_storage_bucket_object" "pipeline_run_obj" {
  name   = data.archive_file.pipeline_run_zip.id
  bucket = google_storage_bucket.bucket.name
  source = data.archive_file.pipeline_run_zip.output_path
}

resource "google_cloudfunctions2_function" "pipeline_run_function" {
  name = "pipeline_run"
  location = "us-west1"
  description = "Run pipeline"

  build_config {
    runtime = "python310"
    entry_point = "main"  # Set the entry point 
    source {
      storage_source {
        bucket = google_storage_bucket.bucket.name
        object = google_storage_bucket_object.pipeline_run_obj.name
      }
    }
  }
}