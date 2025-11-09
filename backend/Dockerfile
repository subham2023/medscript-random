# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

# Install system dependencies in one layer and clean up
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements file first for better layer caching
COPY requirements.txt .

# Install Python dependencies with optimizations
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip cache purge || true

# Copy application code
COPY app/ ./app/

# Expose port 8080 (Cloud Run default)
EXPOSE 8080

# Use PORT environment variable if provided (Cloud Run requirement), default to 8080
ENV PORT=8080

# Set the command to run the application
# Use shell form to allow environment variable expansion for Cloud Run
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}

