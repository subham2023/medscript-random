# This file will now act as the entrypoint for the combined modules.
# Enable necessary Google Cloud APIs
resource "google_project_service" "apis" {
  for_each = toset([
    "run.googleapis.com",
    "iam.googleapis.com",
    "cloudbuild.googleapis.com",
    "artifactregistry.googleapis.com",
    "firestore.googleapis.com",
    "storage.googleapis.com",
    "vision.googleapis.com",
    "aiplatform.googleapis.com"
  ])

  project = var.project_id
  service = each.key
  disable_on_destroy = false
}

# Cloud Storage Buckets
resource "google_storage_bucket" "uploads" {
  name     = "${var.project_id}-medscript-uploads-${var.environment}"
  location = var.region
  project  = var.project_id
  uniform_bucket_level_access = true

  # Lifecycle rule to delete old files
  lifecycle_rule {
    condition {
      age = 7 # Delete files older than 7 days
    }
    action {
      type = "Delete"
    }
  }
}

# Firestore Database
module "firestore" {
  source     = "./firestore"
  project_id = var.project_id
  location   = "nam5" # Multi-region for Firestore
  depends_on = [google_project_service.apis]
}

# Cloud Run Service
module "cloud_run" {
  source              = "./cloud_run"
  service_name        = "medscript-ai-backend-${var.environment}"
  project_id          = var.project_id
  region              = var.region
  image_url           = "gcr.io/${var.project_id}/medscript-ai-backend" # This will be populated by CI/CD
  min_instances       = var.cloud_run_min_instances
  max_instances       = var.cloud_run_max_instances
  cpu                 = var.cloud_run_cpu
  memory              = var.cloud_run_memory
  upload_bucket_name  = google_storage_bucket.uploads.name
  depends_on          = [google_project_service.apis]
}