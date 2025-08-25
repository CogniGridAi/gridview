# GridView Dockerfile
# Multi-stage build for optimized production image

# Stage 1: Frontend Build
FROM node:18-alpine AS frontend-builder

WORKDIR /app

# Copy Superset frontend source
COPY superset/superset-frontend ./superset-frontend

# Install frontend dependencies and build
WORKDIR /app/superset-frontend
RUN npm ci --only=production
RUN npm run build

# Stage 2: Python Dependencies
FROM python:3.11-slim AS python-builder

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    libssl-dev \
    libffi-dev \
    libsasl2-dev \
    libldap2-dev \
    libxi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install Superset dependencies
COPY superset/requirements/base.txt ./superset-requirements.txt
RUN pip install -r superset-requirements.txt

# Install Superset in development mode
COPY superset ./superset
RUN cd superset && pip install -e .

# Stage 3: Production Image
FROM python:3.11-slim AS production

# Install runtime system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    libsasl2-modules \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r gridview && useradd -r -g gridview gridview

# Copy virtual environment from builder
COPY --from=python-builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy built frontend assets
COPY --from=frontend-builder /app/superset-frontend/dist /app/superset/superset/static/assets

# Set working directory
WORKDIR /app

# Copy GridView application code
COPY gridview ./gridview
COPY scripts ./scripts

# Copy Superset code (needed for imports and templates)
COPY superset ./superset

# Create data directory for SQLite database
RUN mkdir -p /app/data/superset && chown -R gridview:gridview /app/data

# Create logs directory
RUN mkdir -p /app/logs && chown -R gridview:gridview /app/logs

# Copy Docker-specific configuration
COPY docker/superset_config_docker.py ./gridview/superset_integration/superset_config_docker.py

# Set environment variables
ENV PYTHONPATH="/app:/app/superset:$PYTHONPATH"
ENV FLASK_APP="gridview.app:create_app"
ENV SUPERSET_CONFIG_PATH="/app/gridview/superset_integration/superset_config_docker.py"

# Expose port
EXPOSE 8088

# Switch to non-root user
USER gridview

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8088/gridview/status || exit 1

# Default command
CMD ["python", "-m", "gridview.cli", "run", "--host", "0.0.0.0", "--port", "8088"]
