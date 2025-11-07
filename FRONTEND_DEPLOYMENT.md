# Frontend Deployment Guide

## Overview

The frontend is configured to deploy automatically to Google Cloud Run via GitHub Actions CI/CD pipeline.

## Deployment Process

### Automatic Deployment (Recommended)

1. **Commit and Push to Main Branch**
   ```bash
   git add .
   git commit -m "Add frontend deployment configuration"
   git push origin main
   ```

2. **Monitor GitHub Actions**
   - Go to your GitHub repository
   - Click on "Actions" tab
   - Watch the workflow run
   - The workflow will:
     - Deploy backend first
     - Get the backend URL
     - Build frontend with backend URL configured
     - Deploy frontend to Cloud Run

3. **Get Frontend URL**
   - After deployment completes, check the workflow output
   - The frontend URL will be displayed: `🚀 Frontend deployed successfully: https://medscript-ai-frontend-XXXXX-uc.a.run.app`

### Manual Setup (If Needed)

If the Artifact Registry repository doesn't exist, Cloud Build will create it automatically. However, you can create it manually:

**Using gcloud CLI:**
```bash
gcloud artifacts repositories create medscript-ai-frontend \
  --repository-format=docker \
  --location=us-central1 \
  --project=cloud-run-project-477318 \
  --description="Docker repository for MedScript AI Frontend"
```

**Or use the provided scripts:**
- Linux/Mac: `./scripts/setup-frontend-repo.sh`
- Windows: `.\scripts\setup-frontend-repo.ps1`

## Configuration

### Backend URL Configuration

The frontend automatically gets the backend URL from the backend deployment. The backend URL is passed as a build argument:
- `REACT_APP_API_BASE_URL` - Set automatically from backend deployment URL

### Frontend Resources

- **Memory**: 512Mi (suitable for static file serving)
- **CPU**: 1 core
- **Timeout**: 60 seconds
- **Max Instances**: 10
- **Concurrency**: 80 requests per instance

## Troubleshooting

### Repository Doesn't Exist Error

If you see an error about the repository not existing:
1. Cloud Build should create it automatically
2. If not, manually create it using the command above
3. Ensure the service account has Artifact Registry Admin permissions

### Build Fails

1. Check that `nginx.conf.template` exists in `frontend/` directory
2. Verify `package.json` has all required dependencies
3. Check GitHub Actions logs for specific error messages

### Frontend Can't Connect to Backend

1. Verify backend is deployed and accessible
2. Check the backend URL in the frontend build logs
3. Ensure CORS is configured on the backend if needed
4. Verify the backend URL format: `https://backend-url/api/v1`

## Local Testing

Before deploying, you can test the Docker build locally:

```bash
cd frontend
docker build -t medscript-frontend:local \
  --build-arg REACT_APP_API_BASE_URL=https://medscript-ai-backend-gzux6ei4ta-uc.a.run.app/api/v1 .

docker run -p 8080:8080 medscript-frontend:local
```

Visit `http://localhost:8080` to test the frontend.

## Environment Variables

The frontend uses the following environment variable (set at build time):
- `REACT_APP_API_BASE_URL` - Backend API base URL

This is automatically configured during CI/CD deployment.

