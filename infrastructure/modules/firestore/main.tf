resource "google_firestore_database" "database" {
  project    = var.project_id
  name       = "(default)"
  location_id = var.location
  type       = "FIRESTORE_NATIVE"
}