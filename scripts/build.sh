#!/bin/bash

# GridView Build Script
# Builds the Superset frontend and prepares the application for running

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🔨 Building GridView + Superset Frontend${NC}"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "gridview/app.py" ]; then
    echo -e "${YELLOW}❌ Please run this script from the GridView project root${NC}"
    exit 1
fi

# Check if virtual environment exists and is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}⚠️ Virtual environment not activated${NC}"
    if [ -d "venv" ]; then
        echo "Activating virtual environment..."
        source venv/bin/activate
    else
        echo -e "${YELLOW}❌ Virtual environment not found. Run ./scripts/setup_and_run.sh first${NC}"
        exit 1
    fi
fi

echo "📦 Building Superset frontend..."
cd superset/superset-frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm ci
fi

# Build the frontend
echo "Building frontend assets (this may take 10-15 minutes)..."
npm run build

cd ../..

echo -e "${GREEN}✅ Build completed successfully!${NC}"
echo ""
echo "Frontend assets are now available in: superset/superset/static/"
echo ""
echo "To start the server:"
echo "  python -m gridview.cli run --port 5001"
