terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  # Configure remote state to be stored in a GCS bucket for collaboration
  backend "gcs" {
    bucket = "medscript-ai-tf-state" # IMPORTANT: Create this GCS bucket manually first!
    prefix = "terraform/state"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

variable "project_id" {
  description = "The GCP project ID."
  type        = string
}

variable "region" {
  description = "The GCP region for resources."
  type        = string
  default     = "us-central1"
}```

### **`infrastructure/environments/dev/main.tf`**

```terraform
module "medscript_app_dev" {
  source = "../../modules"

  project_id   = "your-gcp-project-id" # Replace with your GCP project ID
  region       = "us-central1"
  environment  = "dev"
  
  cloud_run_min_instances = 0
  cloud_run_max_instances = 5
  cloud_run_cpu             = 1
  cloud_run_memory          = "2Gi"

  # Dev-specific variables can be added here
}