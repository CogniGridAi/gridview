#!/bin/bash

# GridView Docker Build Script
# Builds the GridView Docker image with optimizations

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_step() {
    echo -e "${BLUE}======================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}======================================${NC}"
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
IMAGE_NAME="gridview"
IMAGE_TAG="${1:-latest}"
FULL_IMAGE_NAME="${IMAGE_NAME}:${IMAGE_TAG}"

# Check if we're in the right directory
if [ ! -f "docker/Dockerfile" ]; then
    print_error "docker/Dockerfile not found. Please run this script from the GridView project root."
    exit 1
fi

print_step "Building GridView Docker Image"
echo "Image: ${FULL_IMAGE_NAME}"
echo ""

# Build the image
print_step "Building Docker Image"
echo "This may take 10-15 minutes for the first build..."

docker build \
    --tag "${FULL_IMAGE_NAME}" \
    --build-arg BUILDKIT_INLINE_CACHE=1 \
    --progress=plain \
    --file docker/Dockerfile \
    .

if [ $? -eq 0 ]; then
    print_success "Docker image built successfully: ${FULL_IMAGE_NAME}"
else
    print_error "Docker build failed"
    exit 1
fi

# Show image info
print_step "Image Information"
docker images "${IMAGE_NAME}" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"

# Tag as latest if building a specific version
if [ "${IMAGE_TAG}" != "latest" ]; then
    print_step "Tagging as Latest"
    docker tag "${FULL_IMAGE_NAME}" "${IMAGE_NAME}:latest"
    print_success "Tagged as ${IMAGE_NAME}:latest"
fi

print_step "Build Complete"
echo "Available commands:"
echo "• Start development: ./scripts/docker-dev.sh"
echo "• Start production: ./scripts/docker-prod.sh"
echo "• Start simple: docker run -p 8088:8088 ${FULL_IMAGE_NAME}"
echo ""
print_success "GridView Docker image ready for deployment!"
