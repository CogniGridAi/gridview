#!/bin/bash

# GridView One-Click Setup and Run Script
# This script sets up the entire GridView + Superset environment and starts the server

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PYTHON_VERSION="3.11"
NODE_MIN_VERSION="18"
PORT="5001"

# Helper functions
print_step() {
    echo -e "${BLUE}======================================${NC}"
    echo -e "${BLUE}Step $1: $2${NC}"
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

check_command() {
    if command -v $1 &> /dev/null; then
        print_success "$1 is installed"
        return 0
    else
        print_error "$1 is not installed"
        return 1
    fi
}

check_python_version() {
    if command -v python3.11 &> /dev/null; then
        PYTHON_CMD="python3.11"
    elif command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        PYTHON_VER=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
        if [ "$(printf '%s\n' "3.10" "$PYTHON_VER" | sort -V | head -n1)" = "3.10" ]; then
            print_success "Python $PYTHON_VER found"
        else
            print_error "Python 3.10+ required, found $PYTHON_VER"
            exit 1
        fi
    else
        print_error "Python 3.10+ is required"
        exit 1
    fi
}

check_node_version() {
    if command -v node &> /dev/null; then
        NODE_VER=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
        if [ "$NODE_VER" -ge "$NODE_MIN_VERSION" ]; then
            print_success "Node.js v$NODE_VER found"
        else
            print_error "Node.js $NODE_MIN_VERSION+ required, found v$NODE_VER"
            exit 1
        fi
    else
        print_error "Node.js $NODE_MIN_VERSION+ is required"
        exit 1
    fi
}

# Main setup function
main() {
    echo -e "${GREEN}"
    echo "🚀 GridView + Superset One-Click Setup"
    echo "======================================"
    echo "This script will:"
    echo "1. Check system requirements"
    echo "2. Set up Python virtual environment"
    echo "3. Install Python dependencies"
    echo "4. Build Superset frontend"
    echo "5. Start GridView server"
    echo ""
    echo "After completion, visit http://localhost:$PORT"
    echo "Login with admin/admin"
    echo -e "${NC}"
    
    read -p "Continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 0
    fi

    # Step 1: Check system requirements
    print_step "1" "Checking System Requirements"
    
    check_python_version
    check_node_version
    check_command "git"
    check_command "npm"
    
    print_success "All system requirements satisfied"
    
    # Step 2: Set up Python virtual environment
    print_step "2" "Setting up Python Virtual Environment"
    
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        $PYTHON_CMD -m venv venv
        print_success "Virtual environment created"
    else
        print_warning "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    echo "Activating virtual environment..."
    source venv/bin/activate
    
    # Upgrade pip
    echo "Upgrading pip..."
    pip install --upgrade pip --quiet
    print_success "Virtual environment ready"
    
    # Step 3: Install Python dependencies
    print_step "3" "Installing Python Dependencies"
    
    echo "Installing GridView requirements..."
    pip install -r requirements.txt --quiet
    print_success "GridView dependencies installed"
    
    echo "Installing Superset dependencies..."
    cd superset
    pip install -e . --quiet
    pip install -r requirements/base.txt --quiet
    cd ..
    print_success "Superset dependencies installed"
    
    # Step 4: Build Superset frontend
    print_step "4" "Building Superset Frontend"
    
    cd superset/superset-frontend
    
    if [ ! -d "node_modules" ]; then
        echo "Installing Node.js dependencies (this may take a few minutes)..."
        npm ci --silent
        print_success "Node.js dependencies installed"
    else
        print_warning "Node.js dependencies already installed"
    fi
    
    # Check if build is needed
    if [ ! -d "../../superset/superset/static/assets" ] || [ ! "$(ls -A ../../superset/superset/static/assets 2>/dev/null)" ]; then
        echo "Building Superset frontend (this may take 10-15 minutes)..."
        echo "Please be patient, this is a one-time process..."
        npm run build
        print_success "Superset frontend built successfully"
    else
        print_warning "Frontend assets already exist, skipping build"
        echo "To force rebuild, delete superset/superset/static/assets and run again"
    fi
    
    cd ../..
    
    # Step 5: Final verification
    print_step "5" "Final Setup Verification"
    
    # Kill any existing GridView processes
    pkill -f "python.*gridview" 2>/dev/null || true
    sleep 2
    
    # Test app creation
    echo "Testing GridView app creation..."
    $PYTHON_CMD -c "
from gridview.app import GridViewApp
import sys
try:
    app = GridViewApp()
    print('✅ GridView app created successfully')
    sys.exit(0)
except Exception as e:
    print(f'❌ GridView app creation failed: {e}')
    sys.exit(1)
" || {
        print_error "GridView app creation failed"
        echo "Please check the error messages above and ensure all dependencies are installed correctly."
        exit 1
    }
    
    print_success "Setup completed successfully!"
    
    # Step 6: Start the server
    print_step "6" "Starting GridView Server"
    
    echo -e "${GREEN}"
    echo "🎉 Starting GridView + Superset..."
    echo ""
    echo "📊 Server will be available at: http://localhost:$PORT"
    echo "🔐 Login credentials: admin/admin"
    echo ""
    echo "To stop the server, press Ctrl+C"
    echo -e "${NC}"
    
    # Start the server
    echo "Starting server on port $PORT..."
    python -m gridview.cli run --port $PORT
}

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}Shutting down GridView server...${NC}"
    pkill -f "python.*gridview" 2>/dev/null || true
    echo -e "${GREEN}GridView server stopped.${NC}"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Check if we're in the right directory
if [ ! -f "gridview/app.py" ]; then
    print_error "Please run this script from the GridView project root directory"
    print_error "Current directory: $(pwd)"
    print_error "Expected files: gridview/app.py, superset/, requirements.txt"
    exit 1
fi

# Run main function
main

