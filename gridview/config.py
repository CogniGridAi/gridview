"""
GridView Configuration

Configuration management for GridView application.
"""

import os
from typing import Dict, Any, Optional
from pathlib import Path

class GridViewConfig:
    """
    Configuration management for GridView application.
    """
    
    def __init__(self):
        self.app_name = "GridView Analytics Platform"
        self.version = "0.1.0"
        
        # Paths
        self.base_dir = Path(__file__).parent.parent
        self.superset_dir = self.base_dir / "superset"
        self.templates_dir = self.base_dir / "templates"
        self.static_dir = self.base_dir / "static"
        
        # Superset integration
        self.superset_route_prefix = "/gridview/superset"
        self.superset_config_path = self.superset_dir / "superset" / "config.py"
        
        # Branding
        self.branding_config_path = self.base_dir / "branding" / "config.yaml"
        
        # Database
        self.database_uri = os.environ.get('GRIDVIEW_DATABASE_URI', 'sqlite:///gridview.db')
        
        # Security
        self.secret_key = os.environ.get('GRIDVIEW_SECRET_KEY', 'dev-secret-key-change-in-production')
        
        # Features
        self.features = {
            'superset_integration': True,
            'grid_workspace': True,
            'advanced_analytics': False,  # Future feature
            'real_time_updates': False,   # Future feature
            'spark_integration': False,   # Future feature
        }
    
    def get_superset_config(self) -> Dict[str, Any]:
        """
        Get Superset configuration for GridView integration.
        
        Returns:
            Dict containing Superset configuration
        """
        return {
            'SQLALCHEMY_DATABASE_URI': self.database_uri,
            'SECRET_KEY': self.secret_key,
            'SUPERSET_WEBSERVER_PORT': 8088,
            'SUPERSET_WEBSERVER_TIMEOUT': 60,
            'SUPERSET_WEBSERVER_WORKERS': 10,
            'SUPERSET_FEATURE_FLAGS': {
                'ENABLE_TEMPLATE_PROCESSING': True,
                'DASHBOARD_NATIVE_FILTERS': True,
                'DASHBOARD_CROSS_FILTERS': True,
                'DASHBOARD_RBAC': True,
            }
        }
    
    def get_gridview_settings(self) -> Dict[str, Any]:
        """
        Get GridView-specific settings.
        
        Returns:
            Dict containing GridView settings
        """
        return {
            'app_name': self.app_name,
            'version': self.version,
            'features': self.features,
            'superset_route_prefix': self.superset_route_prefix,
        }
    
    def validate_config(self) -> bool:
        """
        Validate GridView configuration.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        # Check if Superset directory exists
        if not self.superset_dir.exists():
            print(f"Warning: Superset directory not found at {self.superset_dir}")
            return False
        
        # Check if required directories exist
        required_dirs = [self.templates_dir, self.static_dir]
        for dir_path in required_dirs:
            if not dir_path.exists():
                print(f"Creating directory: {dir_path}")
                dir_path.mkdir(parents=True, exist_ok=True)
        
        return True
