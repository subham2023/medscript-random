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

# Build the production app
RUN npm run build


# ===============================
# Stage 2 — Serve with Nginx
# ===============================
FROM nginx:alpine

# Install gettext for envsubst (used in start script)
RUN apk add --no-cache gettext

# Copy nginx configuration template
COPY nginx.conf.template /tmp/nginx.conf.template

# Copy startup script
COPY start-nginx.sh /start-nginx.sh
RUN chmod +x /start-nginx.sh

# Copy the built React app from the build stage
COPY --from=build /app/build /usr/share/nginx/html

# Expose the default Cloud Run port
EXPOSE 8080

# Set default PORT environment variable (Cloud Run overrides it)
ENV PORT=8080

# Start Nginx using our startup script
CMD ["/start-nginx.sh"]
