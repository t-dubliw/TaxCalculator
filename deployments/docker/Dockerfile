# # Dockerfile
# FROM python:3.11-slim
# WORKDIR /app

# RUN apt-get update && apt-get install -y \
#     gcc \
#     && rm -rf /var/lib/apt/lists/*

# COPY ../../requirements.txt ./requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# COPY ../../src ./src

# RUN useradd --create-home --shell /bin/bash appuser && chown -R appuser:appuser /app
# USER appuser

# EXPOSE 8000

# HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
#     CMD curl -f http://localhost:8000/health || exit 1

# # Run the FastAPI app using uvicorn
# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]





FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -r taxcalc && useradd -r -g taxcalc taxcalc

# Set work directory
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Development stage
FROM base as development

# Install development dependencies
RUN pip install pytest pytest-cov black flake8 mypy pre-commit

# Copy source code
COPY --chown=taxcalc:taxcalc src/ ./src/
COPY --chown=taxcalc:taxcalc config/ ./config/

# Create necessary directories
RUN mkdir -p logs data && \
    chown -R taxcalc:taxcalc /app

# Switch to non-root user
USER taxcalc

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Development command with hot reload
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Production stage
FROM base as production

# Copy only necessary files for production
COPY --chown=taxcalc:taxcalc src/ ./src/
COPY --chown=taxcalc:taxcalc config/ ./config/


# Create necessary directories with proper permissions
RUN mkdir -p logs data tmp && \
    chown -R taxcalc:taxcalc /app && \
    chmod -R 755 /app

# Switch to non-root user
USER taxcalc

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Production command with gunicorn for better performance
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--access-logfile", "-", "--error-logfile", "-", "src.main:app"]

# Default to production stage
FROM production









