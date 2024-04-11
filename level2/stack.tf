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

terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  project = "<PROJECT_ID>"
}

resource "google_compute_network" "vpc_network" {
  name = "terraform-network"
}