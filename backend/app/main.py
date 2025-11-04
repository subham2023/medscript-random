import time

import structlog
from app.api.endpoints import analysis, documents
from app.core.config import settings
from fastapi import FastAPI, Request
from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import Response

# Configure logging
logger = structlog.get_logger()

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Prometheus Metrics
REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "endpoint", "http_status"]
)
REQUEST_DURATION = Histogram(
    "http_request_duration_seconds", "HTTP request duration", ["method", "endpoint"]
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Middleware to add a process time header and log requests.
    Also captures Prometheus metrics.
    """
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    endpoint = request.url.path
    method = request.method
    status_code = response.status_code

    REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(process_time)
    REQUEST_COUNT.labels(
        method=method, endpoint=endpoint, http_status=status_code
    ).inc()

    logger.info(
        "http_request",
        method=method,
        endpoint=endpoint,
        status_code=status_code,
        process_time=process_time,
    )

    return response


@app.get("/", tags=["Root"])
async def read_root():
    """
    Root endpoint for the application.
    """
    return {"message": "Welcome to MedScript AI"}


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}


@app.get("/metrics", tags=["Metrics"])
async def metrics():
    """
    Prometheus metrics endpoint.
    """
    return Response(media_type="text/plain", content=generate_latest())


# Include API routers
app.include_router(documents.router, prefix=settings.API_V1_STR, tags=["Documents"])
app.include_router(analysis.router, prefix=settings.API_V1_STR, tags=["Analysis"])
