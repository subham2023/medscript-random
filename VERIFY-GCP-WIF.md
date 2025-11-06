# Verify GCP Workload Identity Federation Configuration

## The Error

The error "Invalid value for 'audience'" means the Workload Identity Provider resource doesn't exist in GCP or the values don't match.

## Step 1: Verify Your GCP Configuration

Run these commands to verify your Workload Identity Provider exists:

```bash
# Set your project
export PROJECT_ID="cloud-run-project-477318"
export PROJECT_NUMBER="1074963275925"
export POOL_ID="github-random-medscript"
export PROVIDER_ID="github"

# 1. Check if the pool exists
echo "Checking Workload Identity Pool..."
gcloud iam workload-identity-pools describe $POOL_ID \
  --project=$PROJECT_ID \
  --location=global

# 2. Check if the provider exists
echo "Checking Workload Identity Provider..."
gcloud iam workload-identity-pools providers describe $PROVIDER_ID \
  --project=$PROJECT_ID \
  --location=global \
  --workload-identity-pool=$POOL_ID

# 3. Get the full resource name (this is what should match)
echo "Full resource name:"
gcloud iam workload-identity-pools providers describe $PROVIDER_ID \
  --project=$PROJECT_ID \
  --location=global \
  --workload-identity-pool=$POOL_ID \
  --format="value(name)"
```

## Step 2: Expected Output

The last command should output something like:
```
projects/1074963275925/locations/global/workloadIdentityPools/github-random-medscript/providers/github
```

**This MUST exactly match what's in your GitHub secrets!**

## Step 3: Common Issues

### Issue 1: Pool or Provider Doesn't Exist

If you get an error like "NOT_FOUND", the pool or provider doesn't exist. Create them:

```bash
# Create the pool (if it doesn't exist)
gcloud iam workload-identity-pools create github-random-medscript \
  --project=$PROJECT_ID \
  --location=global \
  --display-name="GitHub Actions Pool"

# Create the provider (if it doesn't exist)
gcloud iam workload-identity-pools providers create-oidc github \
  --project=$PROJECT_ID \
  --location=global \
  --workload-identity-pool=github-random-medscript \
  --display-name="GitHub Provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
  --attribute-condition="assertion.repository=='subham2023/medscript-random'" \
  --issuer-uri="https://token.actions.githubusercontent.com"
```

**Important**: Replace `subham2023/medscript-random` with your actual GitHub username and repository name!

### Issue 2: Wrong Pool/Provider Names

If the names don't match, you have two options:

**Option A**: Update GitHub secrets to match GCP
- Run the commands above to get the actual names from GCP
- Update your GitHub secrets with the correct names

**Option B**: Update GCP to match GitHub secrets
- Delete the existing pool/provider
- Recreate with the names from your GitHub secrets

### Issue 3: Service Account Not Configured

Verify the service account exists and has the right permissions:

```bash
# Check if service account exists
gcloud iam service-accounts describe github-wif@cloud-run-project-477318.iam.gserviceaccount.com \
  --project=$PROJECT_ID

# Check IAM binding (service account should allow GitHub to impersonate it)
gcloud iam service-accounts get-iam-policy github-wif@cloud-run-project-477318.iam.gserviceaccount.com \
  --project=$PROJECT_ID
```

The service account should have a binding like:
```
- members:
  - principalSet://iam.googleapis.com/projects/1074963275925/locations/global/workloadIdentityPools/github-random-medscript/attribute.repository/subham2023/medscript-random
  role: roles/iam.workloadIdentityUser
```

## Step 4: Fix the IAM Binding (if needed)

If the service account doesn't have the right binding:

```bash
gcloud iam service-accounts add-iam-policy-binding \
  github-wif@cloud-run-project-477318.iam.gserviceaccount.com \
  --project=$PROJECT_ID \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/1074963275925/locations/global/workloadIdentityPools/github-random-medscript/attribute.repository/subham2023/medscript-random"
```

**Important**: Replace `subham2023/medscript-random` with your actual GitHub username and repository name!

## Step 5: Verify Everything Matches

After fixing, verify:

1. **Pool name in GCP** = `WIF_POOL_ID` in GitHub secrets
2. **Provider name in GCP** = `WIF_PROVIDER_ID` in GitHub secrets  
3. **Project number in GCP** = `GCP_PROJECT_NUMBER` in GitHub secrets
4. **Service account email** = `GCP_SERVICE_ACCOUNT` in GitHub secrets
5. **IAM binding** allows your GitHub repo to impersonate the service account

## Quick Checklist

- [ ] Pool exists: `github-random-medscript`
- [ ] Provider exists: `github`
- [ ] Provider is OIDC type (not AWS or other)
- [ ] Provider issuer URI: `https://token.actions.githubusercontent.com`
- [ ] Provider attribute condition matches your repo: `subham2023/medscript-random`
- [ ] Service account exists: `github-wif@cloud-run-project-477318.iam.gserviceaccount.com`
- [ ] Service account has `roles/iam.workloadIdentityUser` binding
- [ ] GitHub secrets match GCP resource names exactly

