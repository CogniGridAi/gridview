#!/bin/bash

# GridView Docker Development Environment
# Starts GridView in development mode with Docker

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_warning "Docker is not running. Please start Docker and try again."
    exit 1
fi

print_info "🐳 Starting GridView Development Environment"
echo "=========================================="

# Build image if it doesn't exist
if ! docker image inspect gridview:latest > /dev/null 2>&1; then
    print_info "GridView image not found. Building..."
    ./scripts/docker-build.sh
fi

# Stop any existing containers
print_info "Cleaning up existing containers..."
docker-compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml down --remove-orphans || true

# Start development environment
print_info "Starting development containers..."
docker-compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml up -d

# Wait for services to be ready
print_info "Waiting for GridView to start..."
for i in {1..30}; do
    if curl -f http://localhost:8088/gridview/status > /dev/null 2>&1; then
        break
    fi
    echo -n "."
    sleep 2
done
echo ""

# Check if service is running
if curl -f http://localhost:8088/gridview/status > /dev/null 2>&1; then
    print_success "GridView development environment is ready!"
    echo ""
    echo "🌐 Access GridView at: http://localhost:8088"
    echo "🔐 Login with: admin/admin"
    echo "📊 Status endpoint: http://localhost:8088/gridview/status"
    echo ""
    echo "📋 Useful commands:"
    echo "• View logs: docker-compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml logs -f"
    echo "• Stop: docker-compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml down"
    echo "• Restart: docker-compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml restart gridview"
    echo ""
    echo "🔧 Development features enabled:"
    echo "• Debug mode enabled"
    echo "• CSRF disabled"
    echo "• Verbose logging"
    echo "• SQLite database (persistent)"
else
    print_warning "GridView may still be starting. Check logs with:"
    echo "docker-compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml logs -f gridview"
fi
