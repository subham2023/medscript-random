# PowerShell script to verify both frontend and backend are running

$BACKEND_URL = "https://medscript-ai-backend-1074963275925.us-central1.run.app"
$FRONTEND_URL = ""  # Will be retrieved from workflow or you can set it manually

Write-Host "=== Verifying MedScript AI Deployment ===" -ForegroundColor Green
Write-Host ""

# Test Backend
Write-Host "Testing Backend..." -ForegroundColor Yellow
try {
    $backendResponse = Invoke-WebRequest -Uri $BACKEND_URL -Method GET -UseBasicParsing -TimeoutSec 10
    if ($backendResponse.StatusCode -eq 200) {
        Write-Host "✓ Backend is running!" -ForegroundColor Green
        Write-Host "  URL: $BACKEND_URL" -ForegroundColor Cyan
        Write-Host "  Response: $($backendResponse.Content)" -ForegroundColor Gray
    }
} catch {
    Write-Host "✗ Backend is not accessible" -ForegroundColor Red
    Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test Backend API
Write-Host "Testing Backend API..." -ForegroundColor Yellow
try {
    $apiResponse = Invoke-WebRequest -Uri "$BACKEND_URL/api/v1/health" -Method GET -UseBasicParsing -TimeoutSec 10
    if ($apiResponse.StatusCode -eq 200) {
        Write-Host "✓ Backend API is responding!" -ForegroundColor Green
        Write-Host "  Response: $($apiResponse.Content)" -ForegroundColor Gray
    }
} catch {
    Write-Host "⚠ Backend API endpoint may not be available (this is okay if health endpoint doesn't exist)" -ForegroundColor Yellow
}

Write-Host ""

# Instructions for Frontend
Write-Host "To find your Frontend URL:" -ForegroundColor Yellow
Write-Host "1. Go to: https://github.com/subham2023/medscript-random/actions" -ForegroundColor Cyan
Write-Host "2. Click on the latest workflow run" -ForegroundColor Cyan
Write-Host "3. Look for 'Show Frontend Output' step" -ForegroundColor Cyan
Write-Host "4. The URL will be displayed in the logs" -ForegroundColor Cyan
Write-Host ""

if ($FRONTEND_URL -ne "") {
    Write-Host "Testing Frontend..." -ForegroundColor Yellow
    try {
        $frontendResponse = Invoke-WebRequest -Uri $FRONTEND_URL -Method GET -UseBasicParsing -TimeoutSec 10
        if ($frontendResponse.StatusCode -eq 200) {
            Write-Host "✓ Frontend is running!" -ForegroundColor Green
            Write-Host "  URL: $FRONTEND_URL" -ForegroundColor Cyan
        }
    } catch {
        Write-Host "✗ Frontend is not accessible" -ForegroundColor Red
        Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "Set FRONTEND_URL variable in this script to test frontend automatically" -ForegroundColor Gray
}

Write-Host ""
Write-Host "=== Deployment Verification Complete ===" -ForegroundColor Green

