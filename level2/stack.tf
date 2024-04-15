# Project configurations
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

# Create GCS Bucket for project
resource "google_storage_bucket" "bucket" {
  name     = "${local.project}-bucket"
  location = "us-west1"
  uniform_bucket_level_access = true
}

# Create Artifact Registry repository for Docker images
resource "google_artifact_registry_repository" "iris_docker_repo" {
  project = local.project
  location = local.location
  repository_id = "iris-docker-repo"
  format = "DOCKER"
}

# Create Artifact Registry repository for KFP images
resource "google_artifact_registry_repository" "iris_kfp_repo" {
  project = local.project
  location = local.location
  repository_id = "iris-kfp-repo"
  format = "KFP"
}

# Create Cloud Run to run pipeline
resource "google_cloud_run_v2_job" "kfp_run_job" {
  name     = "kfp-run-job"
  location = local.location

  template {
    template {
      service_account = google_service_account.account.email
      containers {
        image = "${local.location}-docker.pkg.dev/${local.project}/${google_artifact_registry_repository.iris_docker_repo.repository_id}/kfp_run_container"
      }
    }
  }
}

# Create service account
resource "google_service_account" "account" {
  account_id = "iris-sa"
}

# The binding to grant necessary roles 
resource "google_project_iam_member" "grant_editor_permissions" {
  project = local.project
  role    = "roles/editor"
  member  = "serviceAccount:${google_service_account.account.email}"
}