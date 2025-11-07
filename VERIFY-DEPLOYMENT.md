# Verify Deployment - MedScript AI

This guide helps you verify that both the frontend and backend are running successfully.

## Quick Verification

### 1. Check Backend Status

Your backend should be running at:
```
https://medscript-ai-backend-1074963275925.us-central1.run.app
```

**Test it:**
- Open in browser: [Backend URL](https://medscript-ai-backend-1074963275925.us-central1.run.app)
- You should see: `{"message":"Welcome to MedScript AI"}`

**Using curl (command line):**
```bash
curl https://medscript-ai-backend-1074963275925.us-central1.run.app
```

**Using PowerShell:**
```powershell
Invoke-WebRequest -Uri "https://medscript-ai-backend-1074963275925.us-central1.run.app" -UseBasicParsing
```

### 2. Find Frontend URL

The frontend URL will be displayed in the GitHub Actions workflow output.

**Steps to find it:**
1. Go to: https://github.com/subham2023/medscript-random/actions
2. Click on the latest workflow run (should show a green checkmark if successful)
3. Scroll down to find the **"deploy-frontend"** job
4. Expand the **"Show Frontend Output"** step
5. You'll see: `Frontend deployed successfully: https://medscript-ai-frontend-XXXXX-uc.a.run.app`

**Or check Cloud Run Console:**
1. Go to: https://console.cloud.google.com/run?project=cloud-run-project-477318
2. Look for service: `medscript-ai-frontend`
3. Click on it to see the URL

### 3. Test Frontend

Once you have the frontend URL:
- Open it in your browser
- You should see the MedScript AI interface
- The frontend should automatically connect to the backend

## Automated Verification

### Using PowerShell (Windows):
```powershell
cd scripts
.\verify-deployment.ps1
```

### Using Bash (Linux/Mac):
```bash
chmod +x scripts/verify-deployment.sh
./scripts/verify-deployment.sh
```

## Expected Results

### Backend:
- ✅ Status: 200 OK
- ✅ Response: `{"message":"Welcome to MedScript AI"}`
- ✅ API Endpoint: `https://medscript-ai-backend-1074963275925.us-central1.run.app/api/v1`

### Frontend:
- ✅ Status: 200 OK
- ✅ Shows MedScript AI interface
- ✅ Can connect to backend API

## Troubleshooting

### Backend not accessible:
1. Check Cloud Run console: https://console.cloud.google.com/run
2. Verify the service is running
3. Check the service logs for errors

### Frontend not accessible:
1. Check GitHub Actions workflow for errors
2. Verify the frontend Docker build succeeded
3. Check Cloud Run console for the frontend service

### Frontend can't connect to backend:
1. Verify backend URL is correct in frontend build
2. Check browser console for CORS errors
3. Verify backend allows unauthenticated requests

## Quick Links

- **Backend**: https://medscript-ai-backend-1074963275925.us-central1.run.app
- **GitHub Actions**: https://github.com/subham2023/medscript-random/actions
- **Cloud Run Console**: https://console.cloud.google.com/run?project=cloud-run-project-477318

