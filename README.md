# GridView - Enhanced Superset Analytics Platform

GridView is an extension platform built on top of Apache Superset, providing enhanced analytics capabilities while keeping the core Superset codebase untouched.

## 🚀 Quick Start

### Option 1: Docker (Recommended for Production)
```bash
# Simple single-container deployment
./scripts/docker-simple.sh

# OR development environment with hot reload
./scripts/docker-dev.sh

# OR full production stack (PostgreSQL + Redis + Celery)
./scripts/docker-prod.sh
```

### Option 2: Local Development (Native)
```bash
# Check if your system meets requirements
./scripts/check_requirements.sh

# One-click setup and run
./scripts/setup_and_run.sh
```

### Option 3: Manual Setup (Advanced)
```bash
# Check requirements first
./scripts/check_requirements.sh

# Set up environment and dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd superset && pip install -e . && pip install -r requirements/base.txt && cd ..

# Build frontend
./scripts/build.sh

# Start server
python -m gridview.cli run --port 5001
```

**Access GridView:**
- **Docker**: `http://localhost:8088`  
- **Local**: `http://localhost:5001`
- **Login**: `admin/admin`

## 📋 Requirements

### Local Development
- **Python 3.10+** (3.11 recommended)
- **Node.js 18+** and npm
- **Git**
- **8GB+ RAM** (for Superset frontend compilation)

### Docker Deployment (Recommended)
- **Docker 20.10+**
- **Docker Compose 2.0+**
- **4GB+ RAM** (for containers)
- **10GB+ Disk** (for images and data)

### System Dependencies

**macOS:**
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and Node.js
brew install python@3.11 node
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip nodejs npm build-essential
```

**Windows (WSL recommended):**
```bash
# Use WSL2 with Ubuntu, then follow Ubuntu instructions above
```

## 🛠 Manual Setup (Step by Step)

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd gridview
```

### 2. Set up Python Environment
```bash
# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

### 3. Install GridView Dependencies
```bash
# Install GridView requirements
pip install -r requirements.txt
```

### 4. Install Superset Dependencies
```bash
# Navigate to Superset directory and install
cd superset
pip install -e .
pip install -r requirements/base.txt
cd ..
```

### 5. Build Superset Frontend
```bash
# Navigate to Superset frontend and build
cd superset/superset-frontend
npm ci
npm run build
cd ../..
```

### 6. Run GridView
```bash
# Start the server
python -m gridview.cli run --port 5001
```

### 7. Access the Application
- **URL**: `http://localhost:5001`
- **Username**: `admin`
- **Password**: `admin`

## 🐳 Docker Deployment

GridView provides multiple Docker deployment options for different use cases:

### Quick Start (Single Container)
```bash
# Build and run in one command
./scripts/docker-simple.sh

# Access at http://localhost:8088
```

### Development Environment
```bash
# Start development environment with debug features
./scripts/docker-dev.sh

# Features enabled:
# • Debug mode with verbose logging
# • CSRF disabled for easier testing
# • Code hot-reloading (if mounted)
# • SQLite database (persistent)
```

### Production Deployment
```bash
# Full production stack with PostgreSQL + Redis + Celery
./scripts/docker-prod.sh

# Includes:
# • PostgreSQL database
# • Redis for caching and message queuing
# • Celery workers for background tasks
# • Celery beat for scheduled tasks
# • Production security settings
```

### Manual Docker Commands

**Build Image:**
```bash
./scripts/docker-build.sh [tag]
```

**Docker Compose Profiles:**
```bash
# Development (SQLite + single container)
docker-compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml up

# Production (PostgreSQL + Redis + Celery)
docker-compose -f docker/docker-compose.yml -f docker/docker-compose.prod.yml --profile full up

# With specific services (from docker directory)
cd docker && docker-compose up gridview db redis
```

### Environment Configuration

Create environment file for production:
```bash
cp docker/environment.template .env.prod
# Edit .env.prod with your settings
```

**Key Environment Variables:**
```bash
# Security (REQUIRED for production)
SUPERSET_SECRET_KEY=your-random-secret-key
POSTGRES_PASSWORD=your-database-password

# Database
DATABASE_DIALECT=postgresql  # or sqlite
POSTGRES_DB=superset
POSTGRES_USER=superset

# Features
REDIS_AVAILABLE=true  # Enables caching and async tasks
WTF_CSRF_ENABLED=true  # CSRF protection
SESSION_COOKIE_SECURE=true  # HTTPS only

# Application
FLASK_ENV=production
LOG_LEVEL=WARNING
```

### Docker Architecture

```
GridView Docker Stack
├── gridview (Main application)
├── db (PostgreSQL database)
├── redis (Cache & message broker)
├── celery-worker (Background tasks)
├── celery-beat (Scheduled tasks)
└── nginx (Reverse proxy - optional)
```

### Persistent Data

Docker volumes for data persistence:
- `gridview_data` - Application data, uploads, SQLite DB
- `postgres_data` - PostgreSQL database files  
- `redis_data` - Redis persistence
- `gridview_logs` - Application logs

### Container Management

**View Logs:**
```bash
# From project root
docker-compose -f docker/docker-compose.yml logs -f gridview
docker-compose -f docker/docker-compose.yml logs -f db redis

# Or from docker directory
cd docker && docker-compose logs -f gridview
```

**Scale Services:**
```bash
# Scale Celery workers (from project root)
docker-compose -f docker/docker-compose.yml -f docker/docker-compose.prod.yml up -d --scale celery-worker=3
```

**Database Backup:**
```bash
# PostgreSQL backup
docker-compose -f docker/docker-compose.yml exec db pg_dump -U superset superset > backup.sql

# SQLite backup (development)
docker cp gridview-simple:/app/data/superset/superset.db ./backup.db
```

### Production Considerations

1. **Security:**
   - Change default passwords in `.env.prod`
   - Enable HTTPS with SSL certificates
   - Use Docker secrets for sensitive data
   - Configure firewall rules

2. **Performance:**
   - Scale Celery workers based on load
   - Configure PostgreSQL for your workload
   - Set up Redis persistence and optimization
   - Use external load balancer if needed

3. **Monitoring:**
   - Set up health checks and alerts
   - Monitor container resource usage
   - Configure log aggregation
   - Set up backup strategies

### Troubleshooting Docker

**Container Won't Start:**
```bash
# Check logs
docker-compose -f docker/docker-compose.yml logs gridview

# Check container status  
docker-compose -f docker/docker-compose.yml ps

# Rebuild if needed
docker-compose -f docker/docker-compose.yml build --no-cache gridview
```

**Database Connection Issues:**
```bash
# Check database connectivity
docker-compose -f docker/docker-compose.yml exec gridview python -c "
from superset import app, db
with app.app_context():
    print('Database connection:', db.engine.url)
"
```

**Permission Errors:**
```bash
# Fix data directory permissions
docker-compose -f docker/docker-compose.yml exec gridview chown -R gridview:gridview /app/data
```

## 🎯 What You Should See

1. **Home Page**: Automatically redirects to Superset interface
2. **Login Page**: Clean Superset login form
3. **Welcome Dashboard**: Full Superset interface with:
   - Navigation menu
   - Welcome tabs (Recent, Mine, Favorites, Created by me)
   - Fully functional React SPA
   - No JavaScript errors in console

## 🏗 Architecture

GridView runs Superset directly (not as a proxy) with the following approach:

```
GridView (localhost:5001)
├── Pure Superset Core (unmodified)
├── GridView Configuration Layer
├── Enhanced Permission System
└── Extension Framework (for future features)
```

**Key Features:**
- ✅ **Direct Integration**: GridView IS Superset with extensions
- ✅ **Clean Routing**: No URL prefixes or proxying complexity
- ✅ **Full Compatibility**: Standard Superset features work as expected
- ✅ **Extension Ready**: Framework for adding custom features
- ✅ **Update Safe**: Core Superset remains untouched

## 🔧 Development

### Project Structure
```
gridview/
├── gridview/                     # GridView core application
│   ├── app.py                   # Main application factory
│   ├── cli.py                   # Command-line interface
│   ├── config.py                # GridView configuration
│   └── superset_integration/    # Superset integration layer
│       ├── integrator.py        # Integration management
│       ├── superset_config.py   # Custom Superset configuration
│       └── route_mapper.py      # Route mapping utilities
├── superset/                    # Apache Superset (git submodule)
├── data/                        # Database and data storage
├── scripts/                     # Build and utility scripts
└── requirements.txt             # Python dependencies
```

### Key Configuration Files

**GridView Config** (`gridview/superset_integration/superset_config.py`):
- Custom Superset configuration
- Security settings
- Feature flags
- Database configuration

**Main App** (`gridview/app.py`):
- Application factory
- Superset integration
- Permission initialization

### Adding GridView Extensions

```python
# Example: Add custom routes to GridView
@app.route('/gridview/custom-feature')
def custom_feature():
    return render_template('custom_feature.html')
```

## 🐛 Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Kill existing processes
pkill -f "python.*gridview"
# Or use a different port
python -m gridview.cli run --port 5002
```

**2. Frontend Build Fails**
```bash
# Clear node_modules and rebuild
cd superset/superset-frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

**3. Permission Errors**
```bash
# Reset database permissions
rm -rf data/superset/superset.db
python -m gridview.cli run --port 5001
# This will recreate the database with proper permissions
```

**4. Python Import Errors**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
cd superset && pip install -e . && cd ..
```

### Debug Mode

Run with debug logging:
```bash
FLASK_DEBUG=1 python -m gridview.cli run --port 5001
```

### Check Status
```bash
curl http://localhost:5001/gridview/status
```

## 📦 Deployment

### Production Setup

1. **Use Production WSGI Server**:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 "gridview.app:create_app()"
```

2. **Environment Variables**:
```bash
export SUPERSET_SECRET_KEY="your-production-secret-key"
export SUPERSET_DATABASE_URI="postgresql://user:pass@localhost/superset"
```

3. **Static File Serving**:
Configure nginx or similar to serve static files directly.

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Development Workflow

```bash
# Set up development environment
./scripts/setup_dev.sh

# Run tests
python -m pytest

# Run linting
pre-commit run --all-files

# Start development server
python -m gridview.cli run --port 5001 --debug
```

## 📄 License

This project extends Apache Superset and maintains compatibility with the Apache 2.0 License.

## 🆘 Support

- **GitHub Issues**: Report bugs and feature requests
- **Team Slack**: Internal team support channel
- **Documentation**: Check `docs/` directory for detailed guides

---

## 🎉 Success Criteria

When everything is working correctly, you should be able to:

1. ✅ Visit `http://localhost:5001`
2. ✅ Login with `admin/admin`
3. ✅ See full Superset interface load without errors
4. ✅ Navigate through dashboards, charts, SQL Lab
5. ✅ No JavaScript console errors
6. ✅ All API endpoints return proper data
7. ✅ Ready to add GridView extensions

**Welcome to GridView! 🚀**