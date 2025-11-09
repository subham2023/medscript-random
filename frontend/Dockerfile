# ===============================
# Stage 1 — Build the React App
# ===============================
FROM node:18-alpine AS build

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm ci

# Copy all source files
COPY . .

# Build-time argument for backend API URL
ARG REACT_APP_API_BASE_URL=https://medscript-ai-backend-1074963275925.us-central1.run.app/api/v1
ENV REACT_APP_API_BASE_URL=$REACT_APP_API_BASE_URL

# Build the React app
RUN npm run build || (echo "Build failed!" && exit 1)

# Verify build output exists
RUN test -d build || (echo "Build directory not found!" && exit 1)


# ===============================
# Stage 2 — Serve with Nginx
# ===============================
FROM nginx:alpine

# Install gettext for envsubst (used in start script)
RUN apk add --no-cache gettext

# Copy nginx configuration template
COPY nginx.conf.template /tmp/nginx.conf.template

# Copy startup script and make it executable
COPY start-nginx.sh /start-nginx.sh
RUN chmod +x /start-nginx.sh && \
    test -f /start-nginx.sh || (echo "Startup script not found!" && exit 1)

# Copy the built React app from the build stage
COPY --from=build /app/build /usr/share/nginx/html

# Verify files were copied
RUN test -f /usr/share/nginx/html/index.html || (echo "index.html not found!" && exit 1)

# Expose port 8080 (Cloud Run default)
EXPOSE 8080

# Set default PORT environment variable (Cloud Run overrides it)
ENV PORT=8080

# Make sure permissions are correct even if repo didn’t track exec bit
RUN chmod 755 /start-nginx.sh

# Start Nginx using our startup script
CMD ["/start-nginx.sh"]
