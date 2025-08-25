#!/bin/bash

# GridView Docker Production Deployment
# Starts GridView in production mode with full stack

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}$1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Configuration
ENV_FILE=".env.prod"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

print_info "🚀 Starting GridView Production Environment"
echo "============================================="

# Create production environment file if it doesn't exist
if [ ! -f "$ENV_FILE" ]; then
    print_info "Creating production environment file..."
    cat > "$ENV_FILE" << EOF
# GridView Production Environment Variables
# IMPORTANT: Change these values for production!

# Security
SUPERSET_SECRET_KEY=CHANGE-THIS-TO-A-RANDOM-SECRET-KEY-FOR-PRODUCTION
WTF_CSRF_ENABLED=true
SESSION_COOKIE_SECURE=false  # Set to true for HTTPS

# Database
POSTGRES_DB=superset
POSTGRES_USER=superset
POSTGRES_PASSWORD=CHANGE-THIS-PASSWORD

# Application
FLASK_ENV=production
LOG_LEVEL=WARNING

# Optional: Set to your domain for HTTPS
# SERVER_NAME=gridview.yourdomain.com
EOF
    print_warning "Created $ENV_FILE - PLEASE REVIEW AND UPDATE THE SECRETS!"
    echo "Edit $ENV_FILE and update the passwords and secret keys before proceeding."
    read -p "Press Enter after updating $ENV_FILE to continue..."
fi

# Build image if it doesn't exist
if ! docker image inspect gridview:latest > /dev/null 2>&1; then
    print_info "GridView image not found. Building..."
    ./scripts/docker-build.sh
fi

# Load environment variables
if [ -f "$ENV_FILE" ]; then
    print_info "Loading environment from $ENV_FILE"
    export $(grep -v '^#' "$ENV_FILE" | xargs)
fi

# Stop any existing containers
print_info "Cleaning up existing containers..."
docker-compose -f docker/docker-compose.yml -f docker/docker-compose.prod.yml --profile full down --remove-orphans || true

# Start production environment with full stack
print_info "Starting production containers (PostgreSQL + Redis + Celery + GridView)..."
docker-compose -f docker/docker-compose.yml -f docker/docker-compose.prod.yml --profile full up -d

# Initialize database (first run only)
print_info "Initializing database (if needed)..."
docker-compose -f docker/docker-compose.yml -f docker/docker-compose.prod.yml exec -T gridview python -c "
from superset import db
from superset.app import create_app
app = create_app()
with app.app_context():
    db.create_all()
    print('Database initialized')
" || print_warning "Database initialization failed or already completed"

# Wait for services to be ready
print_info "Waiting for services to start..."
for i in {1..60}; do
    if curl -f http://localhost:8088/gridview/status > /dev/null 2>&1; then
        break
    fi
    echo -n "."
    sleep 3
done
echo ""

# Check if service is running
if curl -f http://localhost:8088/gridview/status > /dev/null 2>&1; then
    print_success "GridView production environment is ready!"
    echo ""
    echo "🌐 Access GridView at: http://localhost:8088"
    echo "🔐 Login with: admin/admin"
    echo "📊 Status endpoint: http://localhost:8088/gridview/status"
    echo ""
    echo "📋 Production services running:"
    echo "• GridView Application (Port 8088)"
    echo "• PostgreSQL Database"
    echo "• Redis Cache & Message Broker"
    echo "• Celery Workers (Background Tasks)"
    echo "• Celery Beat (Scheduled Tasks)"
    echo ""
    echo "🔧 Management commands:"
    echo "• View logs: docker-compose -f docker/docker-compose.yml -f docker/docker-compose.prod.yml --profile full logs -f"
    echo "• Stop all: docker-compose -f docker/docker-compose.yml -f docker/docker-compose.prod.yml --profile full down"
    echo "• Scale workers: docker-compose -f docker/docker-compose.yml -f docker/docker-compose.prod.yml --profile full up -d --scale celery-worker=3"
    echo ""
    echo "🔒 Security reminders:"
    echo "• Update passwords in $ENV_FILE"
    echo "• Enable HTTPS in production"
    echo "• Configure firewall rules"
    echo "• Set up SSL certificates"
    echo "• Review security headers in nginx.conf"
else
    print_warning "GridView may still be starting. Check logs with:"
    echo "docker-compose -f docker/docker-compose.yml -f docker/docker-compose.prod.yml --profile full logs -f gridview"
fi
