#!/bin/sh
set -e

# Default to port 8080 if not provided
PORT=${PORT:-8080}

# Replace $PORT placeholder in nginx config
envsubst '$PORT' < /tmp/nginx.conf.template > /etc/nginx/conf.d/default.conf

echo "✅ Nginx configuration generated with PORT=$PORT"
echo "🚀 Starting Nginx..."
exec nginx -g "daemon off;"
