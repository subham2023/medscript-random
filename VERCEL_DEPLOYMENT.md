# Deploying Frontend to Vercel

This guide explains how to deploy the MedScript AI frontend to Vercel while keeping the backend on Google Cloud Run.

## ✅ Compatibility Analysis

**Yes, it will work!** The frontend can be hosted on Vercel and communicate with your backend on Google Cloud Run. Here's what you need to know:

### Current Setup
- **Backend**: Google Cloud Run (`https://medscript-ai-backend-1074963275925.us-central1.run.app`)
- **Frontend**: React app (currently configured for Cloud Run, but compatible with Vercel)
- **Communication**: REST API via Axios

### What's Required

1. ✅ **CORS Configuration** - Added to backend to allow Vercel requests
2. ✅ **Environment Variables** - Set in Vercel dashboard
3. ✅ **Vercel Configuration** - `vercel.json` file created

## 🚀 Deployment Steps

### Step 1: Prepare Your Repository

Ensure all changes are committed and pushed to GitHub:
```bash
git add .
git commit -m "Add Vercel deployment configuration"
git push origin main
```

### Step 2: Deploy to Vercel

#### Option A: Via Vercel Dashboard (Recommended)

1. **Sign up/Login to Vercel**: Go to [vercel.com](https://vercel.com) and sign in with GitHub

2. **Import Project**:
   - Click "Add New Project"
   - Select your repository: `subham2023/medscript-random`
   - Set the **Root Directory** to: `frontend`
   - Click "Deploy"

3. **Configure Environment Variables**:
   - In project settings → Environment Variables
   - Add:
     ```
     REACT_APP_API_BASE_URL=https://medscript-ai-backend-1074963275925.us-central1.run.app/api/v1
     ```
   - Select "Production", "Preview", and "Development"
   - Click "Save"

4. **Redeploy**: After adding environment variables, trigger a new deployment

#### Option B: Via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend directory
cd frontend

# Login to Vercel
vercel login

# Deploy
vercel

# Set environment variable
vercel env add REACT_APP_API_BASE_URL
# Enter: https://medscript-ai-backend-1074963275925.us-central1.run.app/api/v1

# Deploy to production
vercel --prod
```

### Step 3: Update Backend CORS (If Needed)

After deploying to Vercel, you'll get a domain like `https://your-app.vercel.app`. 

**Update the backend CORS configuration** to include your Vercel domain:

1. Edit `backend/app/main.py`
2. Add your Vercel domain to the `allow_origins` list:
   ```python
   allow_origins=[
       "http://localhost:3000",
       "http://localhost:8080",
       "https://*.vercel.app",
       "https://your-app.vercel.app",  # Add your specific domain
   ],
   ```
3. Redeploy the backend to Cloud Run

### Step 4: Verify Deployment

1. **Check Frontend**: Visit your Vercel deployment URL
2. **Test API Connection**: 
   - Open browser DevTools → Network tab
   - Upload a test document
   - Verify API calls are successful (no CORS errors)
3. **Check Backend Logs**: Monitor Cloud Run logs for incoming requests

## 🔧 Configuration Details

### Frontend Configuration (`vercel.json`)

The `vercel.json` file configures:
- Build command: `npm run build`
- Output directory: `build` (React's default)
- SPA routing: All routes redirect to `index.html`
- Static asset caching: 1 year for `/static/*` files

### Environment Variables

| Variable | Value | Required |
|----------|-------|----------|
| `REACT_APP_API_BASE_URL` | `https://medscript-ai-backend-1074963275925.us-central1.run.app/api/v1` | Yes |

**Note**: React environment variables must start with `REACT_APP_` to be accessible in the browser.

### Backend CORS Configuration

The backend now includes CORS middleware that allows:
- ✅ All HTTP methods (GET, POST, PUT, DELETE, etc.)
- ✅ All headers
- ✅ Credentials (cookies, auth headers)
- ✅ Vercel domains (`*.vercel.app`)

## 🐛 Troubleshooting

### CORS Errors

**Symptom**: Browser console shows `CORS policy: No 'Access-Control-Allow-Origin' header`

**Solution**:
1. Verify backend CORS includes your Vercel domain
2. Check backend is deployed with latest changes
3. Verify backend URL in frontend environment variable

### API Connection Failed

**Symptom**: Network requests fail with 404 or connection refused

**Solution**:
1. Verify `REACT_APP_API_BASE_URL` is set correctly in Vercel
2. Check backend is running and accessible
3. Test backend URL directly: `https://medscript-ai-backend-1074963275925.us-central1.run.app/health`

### Build Failures

**Symptom**: Vercel build fails

**Solution**:
1. Check build logs in Vercel dashboard
2. Ensure `package.json` has all dependencies
3. Verify Node.js version (Vercel auto-detects, but you can specify in `package.json`)

### Environment Variables Not Working

**Symptom**: Frontend uses default/localhost API URL

**Solution**:
1. Environment variables must be set **before** build
2. After adding env vars, trigger a new deployment
3. Verify variable name starts with `REACT_APP_`

## 📊 Comparison: Vercel vs Cloud Run

| Feature | Vercel (Frontend) | Cloud Run (Backend) |
|---------|------------------|---------------------|
| **Best For** | Static sites, SPAs | API services, containers |
| **Deployment** | Git push → Auto deploy | Docker container |
| **Scaling** | Automatic, global CDN | Automatic, serverless |
| **Cost** | Free tier available | Pay per request |
| **Custom Domain** | Free SSL, easy setup | Requires load balancer |
| **Build Time** | Fast (optimized) | Slower (Docker build) |

## 🔄 CI/CD Integration

Vercel automatically deploys on:
- Push to `main` branch → Production
- Push to other branches → Preview deployment
- Pull requests → Preview deployment with unique URL

You can also trigger deployments via:
- Vercel Dashboard
- Vercel CLI
- GitHub Actions (if needed)

## 📝 Next Steps

1. ✅ Deploy frontend to Vercel
2. ✅ Update backend CORS with Vercel domain
3. ✅ Test end-to-end functionality
4. ✅ Set up custom domain (optional)
5. ✅ Configure monitoring and analytics

## 🔗 Useful Links

- [Vercel Documentation](https://vercel.com/docs)
- [React Environment Variables](https://create-react-app.dev/docs/adding-custom-environment-variables/)
- [FastAPI CORS](https://fastapi.tiangolo.com/tutorial/cors/)
- [Your Backend Health Check](https://medscript-ai-backend-1074963275925.us-central1.run.app/health)

---

**Note**: The backend remains on Google Cloud Run and doesn't need any changes except CORS configuration. All backend functionality (Firestore, Cloud Storage, AI analysis) continues to work as before.

