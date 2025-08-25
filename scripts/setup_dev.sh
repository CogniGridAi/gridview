#!/bin/bash

# GridView Development Environment Setup
# This script sets up a development environment with additional tools

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

main() {
    echo -e "${GREEN}"
    echo "🛠 GridView Development Environment Setup"
    echo "========================================"
    echo "This will set up:"
    echo "• Python virtual environment"
    echo "• Development dependencies"
    echo "• Pre-commit hooks"
    echo "• Testing tools"
    echo "• Development server with hot reload"
    echo -e "${NC}"

    # Run basic setup first
    print_step "Running Basic Setup"
    source scripts/setup_and_run.sh --dev-mode &
    PID=$!
    
    # Wait for basic setup to complete, then kill the server
    sleep 30
    kill $PID 2>/dev/null || true
    
    print_step "Setting up Development Tools"
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install development dependencies
    echo "Installing development dependencies..."
    pip install -r requirements/development.txt 2>/dev/null || {
        # If dev requirements don't exist, install common dev tools
        pip install pytest black flake8 pre-commit jupyter notebook --quiet
    }
    
    # Set up pre-commit hooks
    echo "Setting up pre-commit hooks..."
    if command -v pre-commit &> /dev/null; then
        pre-commit install
        print_success "Pre-commit hooks installed"
    else
        print_warning "Pre-commit not available, skipping hooks"
    fi
    
    # Create development configuration
    print_step "Creating Development Configuration"
    
    cat > .env.development << EOF
# GridView Development Configuration
FLASK_DEBUG=1
FLASK_ENV=development
SUPERSET_LOAD_EXAMPLES=yes
GRIDVIEW_LOG_LEVEL=DEBUG
EOF
    
    print_success "Development environment file created (.env.development)"
    
    print_step "Development Setup Complete!"
    
    echo -e "${GREEN}"
    echo "🎉 Development environment ready!"
    echo ""
    echo "Common development commands:"
    echo "• Start dev server: python -m gridview.cli run --port 5001 --debug"
    echo "• Run tests: python -m pytest"
    echo "• Code formatting: black ."
    echo "• Linting: flake8 gridview/"
    echo "• Pre-commit check: pre-commit run --all-files"
    echo ""
    echo "Files created:"
    echo "• .env.development - Development environment variables"
    echo "• venv/ - Python virtual environment"
    echo ""
    echo "Next steps:"
    echo "1. Activate environment: source venv/bin/activate"
    echo "2. Start development server with auto-reload"
    echo "3. Begin extending GridView!"
    echo -e "${NC}"
}

# Check if we're in the right directory
if [ ! -f "gridview/app.py" ]; then
    print_error "Please run this script from the GridView project root directory"
    exit 1
fi

main
