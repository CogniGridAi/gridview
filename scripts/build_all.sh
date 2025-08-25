#!/bin/bash

# GridView Complete Build Script
# This script builds Superset frontend and GridView together

set -e  # Exit on any error

echo "🚀 Starting GridView Complete Build..."

# Get the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SUPERSET_DIR="$PROJECT_ROOT/superset"
SUPERSET_FRONTEND_DIR="$SUPERSET_DIR/superset-frontend"

echo "📁 Project root: $PROJECT_ROOT"
echo "📁 Superset directory: $SUPERSET_DIR"

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js v20.18.3 or later."
    exit 1
fi

echo "✅ Node.js version: $(node --version)"

# Step 1: Install Superset frontend dependencies
echo "📦 Installing Superset frontend dependencies..."
cd "$SUPERSET_FRONTEND_DIR"

if [ ! -d "node_modules" ]; then
    echo "🔄 Running npm ci to install dependencies..."
    npm ci
else
    echo "✅ Dependencies already installed"
fi

# Step 2: Build Superset frontend
echo "🔨 Building Superset frontend..."
npm run build

# Step 3: Verify build output
if [ -d "$SUPERSET_DIR/superset/static/assets" ]; then
    ASSET_COUNT=$(find "$SUPERSET_DIR/superset/static/assets" -type f | wc -l)
    echo "✅ Superset frontend build completed! Generated $ASSET_COUNT assets."
else
    echo "❌ Superset frontend build failed - assets directory not found"
    exit 1
fi

# Step 4: Install GridView Python dependencies
echo "📦 Installing GridView Python dependencies..."
cd "$PROJECT_ROOT"

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "⚠️ No requirements.txt found in GridView"
fi

# Step 5: Install GridView itself
echo "🔨 Installing GridView..."
pip install -e .

echo "🎉 GridView Complete Build Successful!"
echo ""
echo "🚀 To start GridView:"
echo "   cd $PROJECT_ROOT"
echo "   python -m gridview.cli run --port 5001"
echo ""
echo "📱 Access GridView at: http://localhost:5001"
echo "📊 Superset interface will be available with full frontend assets!"
