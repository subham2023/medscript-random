resource "google_cloud_run_v2_service" "default" {
  name     = var.service_name
  location = var.region
  project  = var.project_id

  template {
    scaling {
      min_instance_count = var.min_instances
      max_instance_count = var.max_instances
    }

    containers {
      image = var.image_url
      ports {
        container_port = 8000
      }
      resources {
        limits = {
          cpu    = var.cpu
          memory = var.memory
        }
      }
      env {
        name  = "GOOGLE_CLOUD_PROJECT"
        value = var.project_id
      }
      env {
        name = "DOCUMENT_UPLOAD_BUCKET"
        value = var.upload_bucket_name
      }
    }
  }
}

# IAM policy to allow unauthenticated access to the service
resource "google_cloud_run_v2_service_iam_binding" "noauth" {
  project  = google_cloud_run_v2_service.default.project
  location = google_cloud_run_v2_service.default.location
  name     = google_cloud_run_v2_service.default.name
  role     = "roles/run.invoker"
  members = [
    "allUsers",
  ]
}

# Grant the default Cloud Run service account permissions
resource "google_project_iam_member" "vision_user" {
  project = var.project_id
  role    = "roles/vision.user"
  member  = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
}

resource "google_project_iam_member" "vertex_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
}

resource "google_project_iam_member" "firestore_user" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
}

resource "google_storage_bucket_iam_member" "storage_admin" {
  bucket = var.upload_bucket_name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
}

data "google_project" "project" {
  project_id = var.project_id
}```

### **`infrastructure/modules/cloud_run/variables.tf`**

```terraform
variable "service_name" {
  description = "The name of the Cloud Run service."
  type        = string
}

variable "project_id" {
  description = "The GCP project ID."
  type        = string
}

variable "region" {
  description = "The GCP region."
  type        = string
}

variable "image_url" {
  description = "The URL of the container image to deploy."
  type        = string
}

variable "min_instances" {
  description = "Minimum number of instances."
  type        = number
}

variable "max_instances" {
  description = "Maximum number of instances."
  type        = number
}

variable "cpu" {
  description = "CPU allocation."
  type        = number
}

variable "memory" {
  description = "Memory allocation."
  type        = string
}

variable "upload_bucket_name" {
  description = "The name of the GCS bucket for uploads."
  type        = string
}