"""
GridView Superset Integration Configuration

This module provides configuration for integrating Superset within GridView.
"""

import os
from pathlib import Path

class GridViewSupersetConfig:
    """Configuration for GridView's Superset integration."""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.parent
        self.superset_dir = self.base_dir / "superset"
        
        # Superset configuration
        self.SECRET_KEY = "gridview-superset-secret-key-change-in-production"
        self.DATA_DIR = str(self.base_dir / "data" / "superset")
        self.CACHE_CONFIG = {
            'CACHE_TYPE': 'SimpleCache',
            'CACHE_DEFAULT_TIMEOUT': 300
        }
        self.SQLALCHEMY_DATABASE_URI = f"sqlite:///{self.base_dir}/data/superset/superset.db"
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        
        # Ensure data directory exists
        os.makedirs(self.DATA_DIR, exist_ok=True)
        os.makedirs(self.base_dir / "data" / "superset", exist_ok=True)
    
    def get_config_dict(self):
        """Get configuration as a dictionary."""
        return {
            'SECRET_KEY': self.SECRET_KEY,
            'DATA_DIR': self.DATA_DIR,
            'CACHE_CONFIG': self.CACHE_CONFIG,
            'SQLALCHEMY_DATABASE_URI': self.SQLALCHEMY_DATABASE_URI,
            'SQLALCHEMY_TRACK_MODIFICATIONS': self.SQLALCHEMY_TRACK_MODIFICATIONS,
            'DEBUG': True,
            'TESTING': False,
            'WTF_CSRF_ENABLED': False,
            'ENABLE_PROXY_FIX': True,
            'ENABLE_CORS': True,
            'CORS_OPTIONS': {
                'supports_credentials': True,
                'allow_headers': ['*'],
                'resources': ['*'],
                'origins': ['*']
            }
        }
