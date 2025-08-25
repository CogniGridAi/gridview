#!/bin/bash

# GridView Requirements Checker
# Verifies that all system requirements are met

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔍 GridView System Requirements Check${NC}"
echo "===================================="

# Check functions
check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✅ $1 is available${NC}"
        return 0
    else
        echo -e "${RED}❌ $1 is not installed${NC}"
        return 1
    fi
}

check_python() {
    if command -v python3.11 &> /dev/null; then
        VERSION=$(python3.11 --version | cut -d' ' -f2)
        echo -e "${GREEN}✅ Python $VERSION (python3.11)${NC}"
        return 0
    elif command -v python3 &> /dev/null; then
        VERSION=$(python3 --version | cut -d' ' -f2)
        MAJOR=$(echo $VERSION | cut -d'.' -f1)
        MINOR=$(echo $VERSION | cut -d'.' -f2)
        if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 10 ]; then
            echo -e "${GREEN}✅ Python $VERSION${NC}"
            return 0
        else
            echo -e "${RED}❌ Python $VERSION (need 3.10+)${NC}"
            return 1
        fi
    else
        echo -e "${RED}❌ Python 3.10+ not found${NC}"
        return 1
    fi
}

check_node() {
    if command -v node &> /dev/null; then
        VERSION=$(node --version)
        MAJOR=$(echo $VERSION | cut -d'v' -f2 | cut -d'.' -f1)
        if [ "$MAJOR" -ge 18 ]; then
            echo -e "${GREEN}✅ Node.js $VERSION${NC}"
            return 0
        else
            echo -e "${RED}❌ Node.js $VERSION (need v18+)${NC}"
            return 1
        fi
    else
        echo -e "${RED}❌ Node.js not found${NC}"
        return 1
    fi
}

check_memory() {
    if command -v free &> /dev/null; then
        # Linux
        MEM_GB=$(free -g | awk '/^Mem:/{print $2}')
    elif command -v vm_stat &> /dev/null; then
        # macOS
        MEM_BYTES=$(sysctl -n hw.memsize)
        MEM_GB=$((MEM_BYTES / 1024 / 1024 / 1024))
    else
        echo -e "${YELLOW}⚠️ Memory check not available${NC}"
        return 0
    fi
    
    if [ "$MEM_GB" -ge 8 ]; then
        echo -e "${GREEN}✅ Memory: ${MEM_GB}GB${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️ Memory: ${MEM_GB}GB (recommended: 8GB+)${NC}"
        return 0
    fi
}

check_disk() {
    if command -v df &> /dev/null; then
        # Try different df options for different systems
        if df -BG . &> /dev/null; then
            # GNU df (Linux)
            AVAIL_GB=$(df -BG . | tail -1 | awk '{print $4}' | tr -d 'G')
        else
            # macOS/BSD df
            AVAIL_GB=$(df -g . | tail -1 | awk '{print $4}')
        fi
        
        if [ -n "$AVAIL_GB" ] && [ "$AVAIL_GB" -ge 5 ]; then
            echo -e "${GREEN}✅ Disk space: ${AVAIL_GB}GB available${NC}"
            return 0
        elif [ -n "$AVAIL_GB" ]; then
            echo -e "${YELLOW}⚠️ Disk space: ${AVAIL_GB}GB (recommended: 5GB+)${NC}"
            return 0
        else
            echo -e "${YELLOW}⚠️ Disk space check failed${NC}"
            return 0
        fi
    else
        echo -e "${YELLOW}⚠️ Disk space check not available${NC}"
        return 0
    fi
}

# Run checks
ERRORS=0

echo "Checking core requirements..."
check_python || ERRORS=$((ERRORS + 1))
check_node || ERRORS=$((ERRORS + 1))
check_command "git" || ERRORS=$((ERRORS + 1))
check_command "npm" || ERRORS=$((ERRORS + 1))

echo ""
echo "Checking system resources..."
check_memory
check_disk

echo ""
echo "Checking project structure..."
if [ -f "gridview/app.py" ]; then
    echo -e "${GREEN}✅ GridView source code found${NC}"
else
    echo -e "${RED}❌ GridView source code not found${NC}"
    ERRORS=$((ERRORS + 1))
fi

if [ -d "superset" ]; then
    echo -e "${GREEN}✅ Superset directory found${NC}"
else
    echo -e "${RED}❌ Superset directory not found${NC}"
    ERRORS=$((ERRORS + 1))
fi

if [ -f "requirements.txt" ]; then
    echo -e "${GREEN}✅ Requirements file found${NC}"
else
    echo -e "${RED}❌ Requirements file not found${NC}"
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo "====================================="

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}🎉 All requirements satisfied!${NC}"
    echo ""
    echo "You can now run:"
    echo "  ./scripts/setup_and_run.sh"
    exit 0
else
    echo -e "${RED}❌ $ERRORS requirement(s) not met${NC}"
    echo ""
    echo "Please install missing requirements:"
    echo ""
    echo "macOS:"
    echo "  brew install python@3.11 node"
    echo ""
    echo "Ubuntu/Debian:"
    echo "  sudo apt install python3.11 nodejs npm"
    echo ""
    echo "Then run this check again:"
    echo "  ./scripts/check_requirements.sh"
    exit 1
fi
