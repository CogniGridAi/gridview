"""
GridView Docker Configuration

This configuration extends the base GridView configuration with Docker-specific settings.
It inherits all settings from the base configuration and overrides container-specific values.
"""

import os

# Import base GridView configuration
from gridview.superset_integration.superset_config import *

# Override settings for Docker environment
print("🐳 Loading GridView Docker configuration...")

# Database configuration for Docker
# Use PostgreSQL in production, SQLite for development
DATABASE_DIALECT = os.environ.get("DATABASE_DIALECT", "sqlite")

if DATABASE_DIALECT == "postgresql":
    # PostgreSQL configuration for production
    DB_HOST = os.environ.get("DATABASE_HOST", "db")
    DB_PORT = os.environ.get("DATABASE_PORT", "5432")
    DB_USER = os.environ.get("DATABASE_USER", "superset")
    DB_PASS = os.environ.get("DATABASE_PASSWORD", "superset")
    DB_NAME = os.environ.get("DATABASE_DB", "superset")
    
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    print(f"🗄️ Using PostgreSQL: {DB_HOST}:{DB_PORT}/{DB_NAME}")
else:
    # SQLite for development/testing
    SQLALCHEMY_DATABASE_URI = "sqlite:////app/data/superset/superset.db"
    print("🗄️ Using SQLite database")

# Secret key from environment
SECRET_KEY = os.environ.get("SUPERSET_SECRET_KEY", "your-super-secret-key-change-this-in-production-docker")

# Redis configuration for caching and Celery (if available)
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
REDIS_CELERY_DB = os.environ.get("REDIS_CELERY_DB", "0")
REDIS_CACHE_DB = os.environ.get("REDIS_CACHE_DB", "1")

# Check if Redis is available
REDIS_AVAILABLE = os.environ.get("REDIS_AVAILABLE", "false").lower() == "true"

if REDIS_AVAILABLE:
    # Use Redis for caching and Celery
    CACHE_CONFIG = {
        'CACHE_TYPE': 'RedisCache',
        'CACHE_DEFAULT_TIMEOUT': 300,
        'CACHE_KEY_PREFIX': 'gridview_',
        'CACHE_REDIS_HOST': REDIS_HOST,
        'CACHE_REDIS_PORT': REDIS_PORT,
        'CACHE_REDIS_DB': REDIS_CACHE_DB,
    }
    
    # Redis-based Celery configuration
    class CeleryConfig:
        broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
        result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
        
        # Production Celery settings
        task_serializer = 'json'
        result_serializer = 'json'
        accept_content = ['json']
        result_expires = 3600
        
        # Task routing
        task_routes = {
            'superset.tasks.*': {'queue': 'superset'},
        }
        
        # Worker settings
        worker_prefetch_multiplier = 1
        task_acks_late = True
        
        # Set timezone
        timezone = 'UTC'
        enable_utc = True
        
    CELERY_CONFIG = CeleryConfig
    print(f"🚀 Using Redis for caching and Celery: {REDIS_HOST}:{REDIS_PORT}")
else:
    # Fallback to memory-based configuration
    print("💾 Using memory-based caching and synchronous Celery")

# Container-specific settings
ENABLE_PROXY_FIX = True
PROXY_FIX_CONFIG = {
    'x_for': 1,
    'x_proto': 1,
    'x_host': 1,
    'x_port': 1,
    'x_prefix': 1
}

# Security settings for container environment
WTF_CSRF_ENABLED = os.environ.get("WTF_CSRF_ENABLED", "true").lower() == "true"
SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "false").lower() == "true"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"

# Logging configuration for containers
ENABLE_TIME_ROTATE = True
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

# Feature flags for container deployment
FEATURE_FLAGS.update({
    # Enable production features
    "THUMBNAILS": REDIS_AVAILABLE,  # Only if Redis is available
    "ALERT_REPORTS": REDIS_AVAILABLE,  # Only if Redis is available
    "GLOBAL_ASYNC_QUERIES": REDIS_AVAILABLE,  # Only if Redis is available
})

# Data directory paths for persistent volumes
DATA_DIR = "/app/data"
UPLOAD_FOLDER = "/app/data/uploads"
IMG_UPLOAD_FOLDER = "/app/data/uploads"
IMG_UPLOAD_URL = "/static/uploads/"

# Create directories if they don't exist
import os
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# GridView Docker-specific branding
APP_NAME = "GridView"
APP_ICON = "/gridview/static/images/gridview-logo-horiz.svg"

# Override theme for container deployment
THEME_DEFAULT = {
    "token": {
        # Brand configuration
        "brandLogoUrl": "/gridview/static/images/gridview-logo-horiz.svg",
        "brandLogoAlt": "GridView",
        "brandLogoHeight": "30px",
        "brandLogoMargin": "18px",
        "brandLogoHref": "/",
        # Container-optimized colors
        "colorPrimary": "#2893B3",
        "colorSuccess": "#5ac189",
        "colorWarning": "#fcc700",
        "colorError": "#e04355",
        "fontFamily": "'Inter', Helvetica, Arial",
    }
}

print("✅ GridView Docker configuration loaded successfully")
