"""
Superset Configuration for GridView Integration

This module extends Superset's default configuration with GridView-specific settings.
"""

import os
from pathlib import Path

# Import Superset's default configuration
from superset.config import *

# Base directory for GridView
BASE_DIR = Path(__file__).parent.parent.parent

# Override specific settings for GridView
DATA_DIR = str(BASE_DIR / "data" / "superset")
os.makedirs(DATA_DIR, exist_ok=True)

# Database configuration
SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR}/data/superset/superset.db"

# Secret key - use a strong key for development
SECRET_KEY = "your-super-secret-key-change-this-in-production-12345"

# Debug mode
DEBUG = True
TESTING = False

# Basic settings
ENABLE_PROXY_FIX = True
ENABLE_CORS = True
WTF_CSRF_ENABLED = False

# URL prefixing for GridView integration
PREFERRED_URL_SCHEME = 'http'
PROXY_FIX_CONFIG = {
    'x_for': 1,
    'x_proto': 1,
    'x_host': 1,
    'x_port': 1,
    'x_prefix': 1
}

# Basic configuration for direct Superset operation
SUPERSET_WEBSERVER_PROTOCOL = 'http'
SUPERSET_WEBSERVER_ADDRESS = 'localhost'
SUPERSET_WEBSERVER_PORT = 5001

# Security configuration - disable CSRF for easier development
WTF_CSRF_ENABLED = False
WTF_CSRF_EXEMPT_LIST = []

# Authentication configuration  
AUTH_TYPE = 1  # Database authentication
AUTH_ROLE_ADMIN = 'Admin'
AUTH_ROLE_PUBLIC = 'Public'
AUTH_USER_REGISTRATION = False

# Session configuration for better compatibility
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
PERMANENT_SESSION_LIFETIME = 3600 * 24 * 31  # 31 days in seconds

# CORS configuration
ENABLE_CORS = True
CORS_OPTIONS = {
    'supports_credentials': True,
    'allow_headers': ['*'],
    'resources': ['*'],
    'origins': ['*']
}

# Session settings
SESSION_SERVER_SIDE = False
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Celery configuration for lightweight embedded use
class CeleryConfig:
    """
    Minimal Celery configuration for GridView embedded use.
    
    This configuration runs Celery in synchronous mode (task_always_eager=True)
    which means tasks execute immediately in the same process, eliminating the
    need for separate worker processes or Redis broker for basic functionality.
    """
    # Use memory broker for lightweight operation
    broker_url = 'memory://'
    result_backend = 'cache+memory://'
    
    # Execute tasks synchronously (no separate workers needed)
    task_always_eager = True
    task_eager_propagates = True
    
    # Disable periodic tasks and beat scheduler
    beat_schedule = {}
    
    # Minimal task configuration
    task_serializer = 'json'
    result_serializer = 'json'
    accept_content = ['json']
    
    # Disable worker features not needed for embedded use
    worker_hijack_root_logger = False
    worker_log_format = None
    worker_task_log_format = None
    
    # Set timezone
    timezone = 'UTC'
    enable_utc = True

CELERY_CONFIG = CeleryConfig

# Basic feature flags for direct Superset operation
FEATURE_FLAGS = {
    # Keep essential features enabled
    'DASHBOARD_NATIVE_FILTERS': True,
    'DASHBOARD_CROSS_FILTERS': True,
    'HORIZONTAL_FILTER_BAR': True,
    # Disable features that require complex async setup for now
    'GLOBAL_ASYNC_QUERIES': False,
    'THUMBNAILS': False,
    'ALERT_REPORTS': False,
    # Enable permissions that might help with 403 errors
    'EMBEDDED_SUPERSET': False,
    'ENABLE_BROAD_ACTIVITY_ACCESS': True,
}

# Permission configurations to help with API access
PUBLIC_ROLE_LIKE_GAMMA = True
ENABLE_ACCESS_REQUEST = False

# Additional security configurations
FAB_ADD_SECURITY_PERMISSION_VIEW = False
FAB_ADD_SECURITY_PERMISSION_VIEWS_VIEW = False
FAB_ADD_SECURITY_PERMISSION_MENU_VIEW = False

# Results backend configuration for sync operation
RESULTS_BACKEND_USE_MSGPACK = False
RESULTS_BACKEND = None  # Use default cache backend

# Logging - use default Superset logging configuration
# LOGGING_CONFIGURATOR = DefaultLoggingConfigurator  # Commented out to use default
