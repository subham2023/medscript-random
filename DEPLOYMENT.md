# Deployment Guide for MedScript AI

This guide outlines the steps to deploy the MedScript AI application, consisting of a FastAPI backend and a React frontend, to Google Cloud Platform (GCP), primarily using Google Cloud Run.

## 1. Overview

MedScript AI leverages GCP services for scalable and serverless deployment. The backend, built with FastAPI, will be deployed to Google Cloud Run. The frontend, a React application, can be deployed as static assets to Cloud Storage or Firebase Hosting, or containerized and served via Cloud Run if dynamic server-side rending becomes necessary.

## 2. Prerequisites

Before you begin, ensure you have the following:

*   **Google Cloud Project**: An active GCP project with billing enabled.
*   **gcloud CLI**: The Google Cloud SDK installed and authenticated (`gcloud auth login`, `gcloud config set project [YOUR_PROJECT_ID]`).
*   **Docker**: Docker installed on your local machine if you plan to build images locally.
*   **Node.js & npm/yarn**: For building the frontend application.
*   **Service Accounts**: Appropriate service accounts with necessary permissions (Cloud Run Admin, Storage Admin, Vision AI User, Vertex AI User, Firestore Editor).

## 3. GCP Service Setup

Ensure the following GCP APIs are enabled and services are configured in your project:

1.  **Enable APIs**:

    ```bash
    gcloud services enable run.googleapis.com
    gcloud services enable containerregistry.googleapis.com
    gcloud services enable vision.googleapis.com
    gcloud services enable aiplatform.googleapis.com # For Gemini Models
    gcloud services enable firestore.googleapis.com
    gcloud services enable cloudbuild.googleapis.com
    ```

2.  **Cloud Storage Bucket for Uploads**:

    Create a bucket for storing document uploads. The backend uses `medscript-uploads` by default.

    ```bash
    gsutil mb -p [YOUR_PROJECT_ID] gs://medscript-uploads
    ```

3.  **Firestore Database**: Initialize Firestore in Native mode.

    Go to the Google Cloud Console -> Firestore -> Create Database and select Native mode.

## 4. Backend Deployment to Cloud Run

The backend is a FastAPI application that will be containerized and deployed to Google Cloud Run.

### 4.1. Build and Push Docker Image

Navigate to the `backend` directory:

```bash
cd backend
```

Build the Docker image. Replace `[YOUR_PROJECT_ID]` with your GCP Project ID.

```bash
docker build -t gcr.io/[YOUR_PROJECT_ID]/medscript-ai-backend:latest .
```

Push the image to Google Container Registry:

```bash
docker push gcr.io/[YOUR_PROJECT_ID]/medscript-ai-backend:latest
```

### 4.2. Deploy to Cloud Run

Deploy the container image to Cloud Run. Choose a region close to your users (e.g., `us-central1`).

```bash
gcloud run deploy medscript-ai-backend \
  --image gcr.io/[YOUR_PROJECT_ID]/medscript-ai-backend:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --set-env-vars GOOGLE_CLOUD_PROJECT=[YOUR_PROJECT_ID],DOCUMENT_UPLOAD_BUCKET=medscript-uploads
```

*   `--allow-unauthenticated`: Makes the service publicly accessible. For production, consider using Identity Platform or other authentication methods.
*   `--memory` and `--cpu`: Adjust based on expected load. Refer to `target_tech_spec.md` for performance targets.
*   `--set-env-vars`: Sets environment variables required by the backend. Ensure `GOOGLE_CLOUD_PROJECT` is set correctly.

### 4.3. Service Account Permissions

Your Cloud Run service will execute with a default compute service account (`[YOUR_PROJECT_NUMBER]-compute@developer.gserviceaccount.com`). Ensure this service account has the following roles:

*   **Cloud Vision API User**
*   **Vertex AI User**
*   **Storage Object Admin** (for `medscript-uploads` bucket) or more granular permissions.
*   **Cloud Datastore User** (for Firestore access)

You can grant these permissions via the GCP IAM Console.

## 5. Frontend Deployment

The frontend is a React application.

### 5.1. Build Frontend Assets

Navigate to the `frontend` directory:

```bash
cd frontend
```

Build the production-ready assets:

```bash
npm install
npm run build
```

This will generate static files in the `build` directory.

### 5.2. Deploy to Cloud Storage (or Firebase Hosting)

Create a Google Cloud Storage bucket to host your static files. You might want to use a name matching your domain.

```bash
gsutil mb -p [YOUR_PROJECT_ID] gs://[YOUR_FRONTEND_BUCKET_NAME]
```

Configure the bucket for static website hosting:

```bash
gsutil web set -m index.html -e index.html gs://[YOUR_FRONTEND_BUCKET_NAME]
```

Upload the built frontend assets to the bucket:

```bash
gsutil -m cp -r build/* gs://[YOUR_FRONTEND_BUCKET_NAME]/
```

Finally, make the objects publicly readable (for public websites):

```bash
gsutil iam ch allUsers:objectViewer gs://[YOUR_FRONTEND_BUCKET_NAME]
```

**Important**: Update `REACT_APP_API_BASE_URL` in your frontend's `.env` file or during build to point to your deployed Cloud Run backend service URL.

## 6. CI/CD

The project includes a GitHub Actions workflow (`.github/workflows/ci-cd.yml`) that automates testing, Docker image building, and deployment to Cloud Run upon pushes to the `main` branch. Configure your GitHub project with the necessary GCP credentials (e.g., `GCP_PROJECT_ID`, `GCP_SA_KEY`) as GitHub Secrets for the workflow to function correctly.

---
