# PowerShell script to setup frontend Artifact Registry repository
# This is optional - Cloud Build will create it automatically if needed

$PROJECT_ID = "cloud-run-project-477318"
$LOCATION = "us-central1"
$REPOSITORY = "medscript-ai-frontend"

Write-Host "Creating Artifact Registry repository for frontend..." -ForegroundColor Green

gcloud artifacts repositories create $REPOSITORY `
  --repository-format=docker `
  --location=$LOCATION `
  --project=$PROJECT_ID `
  --description="Docker repository for MedScript AI Frontend"

Write-Host "Repository created successfully!" -ForegroundColor Green
Write-Host "You can now deploy the frontend via CI/CD." -ForegroundColor Green

