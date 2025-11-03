variable "project_id" {
  description = "The GCP project ID."
  type        = string
}

variable "location" {
  description = "The location for the Firestore database (e.g., nam5 for multi-region US)."
  type        = string
}