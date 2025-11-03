module "medscript_app_prod" {
  source = "../../modules"

  project_id   = "your-gcp-project-id" # Replace with your GCP project ID
  region       = "us-central1"
  environment  = "prod"

  cloud_run_min_instances = 1 # Keep at least one instance warm for production
  cloud_run_max_instances = 50
  cloud_run_cpu             = 2
  cloud_run_memory          = "4Gi"

  # Prod-specific variables can be added here
}