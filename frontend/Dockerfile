# Multi-stage build for React app
# Stage 1: Build the React application
FROM node:18-alpine AS build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build argument for API URL (defaults to backend URL)
ARG REACT_APP_API_BASE_URL=https://medscript-ai-backend-1074963275925.us-central1.run.app/api/v1
ENV REACT_APP_API_BASE_URL=$REACT_APP_API_BASE_URL

# Build the React app
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:alpine

# Copy custom nginx configuration template
# nginx:alpine automatically processes .template files in /etc/nginx/templates/
COPY nginx.conf.template /etc/nginx/templates/default.conf.template

# Copy built app from build stage
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 8080 (Cloud Run default)
EXPOSE 8080

# Set default PORT for Cloud Run (Cloud Run will override this)
ENV PORT=8080

# nginx:alpine automatically processes template files and starts nginx
# The PORT environment variable will be substituted in the template

