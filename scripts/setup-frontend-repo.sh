#!/bin/bash
# Setup script for frontend Artifact Registry repository
# This is optional - Cloud Build will create it automatically if needed

PROJECT_ID="cloud-run-project-477318"
LOCATION="us-central1"
REPOSITORY="medscript-ai-frontend"

echo "Creating Artifact Registry repository for frontend..."

gcloud artifacts repositories create $REPOSITORY \
  --repository-format=docker \
  --location=$LOCATION \
  --project=$PROJECT_ID \
  --description="Docker repository for MedScript AI Frontend"

echo "Repository created successfully!"
echo "You can now deploy the frontend via CI/CD."

