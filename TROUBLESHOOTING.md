# Troubleshooting Guide - Backend Not Working

## 🔍 Quick Diagnosis

If the frontend shows "An error occurred during upload" or connection errors, follow these steps:

### 1. Check Backend is Running

Test the backend health endpoint:
```bash
curl https://medscript-ai-backend-1074963275925.us-central1.run.app/health
```

Expected response:
```json
{"status": "healthy"}
```

### 2. Check Frontend API Configuration

**In Vercel Dashboard:**
1. Go to your project → Settings → Environment Variables
2. Verify `REACT_APP_API_BASE_URL` is set to:
   ```
   https://medscript-ai-backend-1074963275925.us-central1.run.app/api/v1
   ```
3. Make sure it's enabled for **Production**, **Preview**, and **Development**
4. **Redeploy** after adding/changing environment variables

### 3. Check Browser Console

Open browser DevTools (F12) → Console tab:
- Look for CORS errors
- Look for connection refused errors
- Check Network tab to see actual API calls

### 4. Verify Backend Endpoints

Test each endpoint directly:

```bash
# Health check
curl https://medscript-ai-backend-1074963275925.us-central1.run.app/health

# Root endpoint
curl https://medscript-ai-backend-1074963275925.us-central1.run.app/

# Test upload endpoint (should return 400 without file, but confirms endpoint exists)
curl -X POST https://medscript-ai-backend-1074963275925.us-central1.run.app/api/v1/documents/upload
```

## 🐛 Common Issues & Fixes

### Issue 1: "ERR_CONNECTION_REFUSED" or "localhost:8000"

**Cause:** Frontend is using localhost instead of production backend

**Fix:**
1. Set `REACT_APP_API_BASE_URL` in Vercel environment variables
2. Redeploy frontend
3. Or wait for the code update (now defaults to production URL)

### Issue 2: CORS Errors

**Error:** `Access to XMLHttpRequest has been blocked by CORS policy`

**Fix:**
1. Backend CORS is configured for `*.vercel.app` domains
2. If using a custom domain, add it to `backend/app/main.py`:
   ```python
   allow_origins=[
       "http://localhost:3000",
       "http://localhost:8080",
       "https://your-custom-domain.com",  # Add here
   ],
   ```
3. Redeploy backend

### Issue 3: "Document not found" or 404 errors

**Cause:** Backend endpoints might not be registered correctly

**Fix:**
1. Check backend logs in Cloud Run console
2. Verify endpoints are registered in `main.py`:
   ```python
   app.include_router(documents.router, prefix=settings.API_V1_STR, tags=["Documents"])
   app.include_router(analysis.router, prefix=settings.API_V1_STR, tags=["Analysis"])
   ```

### Issue 4: Upload works but analysis fails

**Cause:** Background task or AI agent issues

**Check:**
1. Cloud Run logs for errors
2. Firestore permissions
3. Vertex AI/Gemini API credentials
4. Google Cloud Storage bucket permissions

### Issue 5: Environment Variables Not Working

**Cause:** React environment variables must be set at build time

**Fix:**
1. Environment variables must start with `REACT_APP_`
2. Must be set **before** building
3. After adding env vars in Vercel, **trigger a new deployment**

## 🔧 Quick Fixes

### Fix 1: Update Frontend API URL (Already Done)

The frontend now defaults to production backend URL when `NODE_ENV=production`.

### Fix 2: Verify Vercel Environment Variables

1. Go to Vercel Dashboard
2. Your Project → Settings → Environment Variables
3. Add/Verify:
   ```
   REACT_APP_API_BASE_URL = https://medscript-ai-backend-1074963275925.us-central1.run.app/api/v1
   ```
4. Select: Production, Preview, Development
5. Save and Redeploy

### Fix 3: Test Backend Directly

```bash
# Test health
curl https://medscript-ai-backend-1074963275925.us-central1.run.app/health

# Test upload (will fail without file, but confirms endpoint exists)
curl -X POST https://medscript-ai-backend-1074963275925.us-central1.run.app/api/v1/documents/upload \
  -H "Content-Type: multipart/form-data"
```

### Fix 4: Check Backend Logs

1. Go to Google Cloud Console
2. Cloud Run → medscript-ai-backend → Logs
3. Look for errors during request processing

## ✅ Verification Steps

After fixes, verify:

1. **Backend Health:**
   ```bash
   curl https://medscript-ai-backend-1074963275925.us-central1.run.app/health
   ```
   Should return: `{"status": "healthy"}`

2. **Frontend Console:**
   - Open browser DevTools
   - Check Network tab
   - Upload a document
   - Verify requests go to Cloud Run URL, not localhost

3. **Full Flow Test:**
   - Upload a document
   - Check status endpoint returns "processing"
   - Wait for analysis
   - Check results endpoint returns complete analysis

## 📞 Still Not Working?

1. Check Cloud Run service is running
2. Verify backend has proper IAM permissions
3. Check Firestore database exists and is accessible
4. Verify Google Cloud Storage bucket exists
5. Check Vertex AI API is enabled
6. Review Cloud Run logs for specific errors

## 🔗 Useful Links

- Backend URL: https://medscript-ai-backend-1074963275925.us-central1.run.app
- Health Check: https://medscript-ai-backend-1074963275925.us-central1.run.app/health
- Cloud Run Console: https://console.cloud.google.com/run
- Vercel Dashboard: https://vercel.com/dashboard

