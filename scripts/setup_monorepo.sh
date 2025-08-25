#!/bin/bash

echo "Setting up GridView Monorepo Structure..."
echo "========================================"

# Check if we're in the right directory
if [ ! -f "setup.py" ]; then
    echo "Error: setup.py not found. Please run this script from the GridView project root."
    exit 1
fi

# Check if Superset is already embedded
if [ -d "superset" ]; then
    echo "✅ Superset directory found"
else
    echo "❌ Superset directory not found. Please copy the Superset codebase first."
    exit 1
fi

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p gridview/templates
mkdir -p gridview/static
mkdir -p logs

# Remove Superset .git directory if it exists (we want one repo)
if [ -d "superset/.git" ]; then
    echo "Removing Superset .git directory (monorepo structure)..."
    rm -rf superset/.git
fi

# Create .gitignore for the monorepo
echo "Creating .gitignore for monorepo..."
cat > .gitignore << 'GITIGNORE_EOF'
# GridView specific
*.pyc
__pycache__/
*.pyo
*.pyd
.Python
env/
venv/
.env
*.log
logs/
*.db
*.sqlite

# Superset specific (embedded)
superset/.env
superset/superset.db
superset/superset.cache
superset/superset.pid
superset/superset.log
superset/superset-error.log

# Frontend build artifacts
superset/superset-frontend/dist/
superset/superset-frontend/build/
superset/superset-frontend/node_modules/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Docker
.dockerignore
docker-compose.override.yml
GITIGNORE_EOF

echo ""
echo "🎉 Monorepo structure setup complete!"
echo ""
echo "Next steps:"
echo "1. Install GridView: pip install -e ."
echo "2. Install Superset dependencies: cd superset && pip install -r requirements/development.txt"
echo "3. Test the integration: gridview run"
echo ""
echo "Git ignore file created: .gitignore"
