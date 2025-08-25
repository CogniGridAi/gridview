# 🚀 GridView Quick Start Guide

## One-Click Setup

```bash
./scripts/setup_and_run.sh
```

**That's it!** Visit `http://localhost:5001` and login with `admin/admin`.

---

## What the Script Does

1. ✅ **Checks Requirements** - Python 3.10+, Node.js 18+
2. ✅ **Creates Virtual Environment** - Isolated Python environment
3. ✅ **Installs Dependencies** - GridView + Superset packages
4. ✅ **Builds Frontend** - Compiles React application (~10-15 minutes)
5. ✅ **Starts Server** - Launches on http://localhost:5001

---

## System Requirements

| Requirement | Version | Check Command |
|-------------|---------|---------------|
| Python | 3.10+ | `python3 --version` |
| Node.js | 18+ | `node --version` |
| RAM | 8GB+ | For frontend compilation |
| Disk | 5GB+ | For dependencies and build |

---

## Quick Commands

| Task | Command |
|------|---------|
| **Setup & Run** | `./scripts/setup_and_run.sh` |
| **Start Server** | `python -m gridview.cli run --port 5001` |
| **Stop Server** | `Ctrl+C` or `pkill -f "python.*gridview"` |
| **Check Status** | `curl http://localhost:5001/gridview/status` |
| **Reset Database** | `rm -rf data/superset/superset.db` |

---

## Troubleshooting

### ❌ "Port already in use"
```bash
pkill -f "python.*gridview"
# or
./scripts/setup_and_run.sh  # Will auto-kill existing processes
```

### ❌ "Frontend build fails"
```bash
cd superset/superset-frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### ❌ "Permission denied"
```bash
rm -rf data/superset/superset.db
./scripts/setup_and_run.sh  # Will recreate with proper permissions
```

### ❌ "Python/Node not found"
**macOS:**
```bash
brew install python@3.11 node
```

**Ubuntu:**
```bash
sudo apt install python3.11 nodejs npm
```

---

## Success Checklist

When everything works, you should see:

- ✅ Server starts without errors
- ✅ `http://localhost:5001` loads Superset login page
- ✅ Login with `admin/admin` succeeds
- ✅ Welcome dashboard loads with navigation menu
- ✅ No JavaScript console errors
- ✅ Can navigate between tabs (Recent, Mine, Favorites)

---

## Development Mode

For active development:

```bash
# Activate virtual environment
source venv/bin/activate

# Start with debug mode
FLASK_DEBUG=1 python -m gridview.cli run --port 5001
```

---

## Project Structure (After Setup)

```
gridview/
├── venv/                        # Python virtual environment
├── data/superset/              # Database and data files
├── superset/superset/static/   # Built frontend assets
├── gridview/                   # GridView source code
└── scripts/                    # Setup and utility scripts
```

---

## Next Steps

1. **Verify Setup**: Login and explore the interface
2. **Read Documentation**: Check `README.md` for detailed info
3. **Start Development**: Add GridView extensions in `gridview/`
4. **Team Onboarding**: Share this guide with team members

---

## Support

- **Quick Issues**: Check troubleshooting section above
- **Setup Problems**: Run `./scripts/setup_and_run.sh` again
- **Development Help**: See `README.md` for detailed documentation
- **Team Support**: Contact project maintainers

**Happy coding! 🎉**
