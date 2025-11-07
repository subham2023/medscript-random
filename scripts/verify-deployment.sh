#!/bin/bash
# Bash script to verify both frontend and backend are running

BACKEND_URL="https://medscript-ai-backend-1074963275925.us-central1.run.app"
FRONTEND_URL=""  # Will be retrieved from workflow or you can set it manually

echo "=== Verifying MedScript AI Deployment ==="
echo ""

# Test Backend
echo "Testing Backend..."
if curl -s -f -o /dev/null -w "%{http_code}" "$BACKEND_URL" | grep -q "200"; then
    echo "✓ Backend is running!"
    echo "  URL: $BACKEND_URL"
    echo "  Response: $(curl -s $BACKEND_URL)"
else
    echo "✗ Backend is not accessible"
fi

echo ""

# Test Backend API
echo "Testing Backend API..."
if curl -s -f -o /dev/null -w "%{http_code}" "$BACKEND_URL/api/v1/health" | grep -q "200"; then
    echo "✓ Backend API is responding!"
    echo "  Response: $(curl -s $BACKEND_URL/api/v1/health)"
else
    echo "⚠ Backend API endpoint may not be available (this is okay if health endpoint doesn't exist)"
fi

echo ""

# Instructions for Frontend
echo "To find your Frontend URL:"
echo "1. Go to: https://github.com/subham2023/medscript-random/actions"
echo "2. Click on the latest workflow run"
echo "3. Look for 'Show Frontend Output' step"
echo "4. The URL will be displayed in the logs"
echo ""

if [ -n "$FRONTEND_URL" ]; then
    echo "Testing Frontend..."
    if curl -s -f -o /dev/null -w "%{http_code}" "$FRONTEND_URL" | grep -q "200"; then
        echo "✓ Frontend is running!"
        echo "  URL: $FRONTEND_URL"
    else
        echo "✗ Frontend is not accessible"
    fi
else
    echo "Set FRONTEND_URL variable in this script to test frontend automatically"
fi

echo ""
echo "=== Deployment Verification Complete ==="

