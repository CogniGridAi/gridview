"""
GridView Main Application

Main Flask application that directly runs Superset with GridView extensions.
"""

import os
import sys
from typing import Optional
from pathlib import Path
from flask import Flask


def create_gridview_superset_app():
    """
    Create GridView app that directly runs Superset (no proxying).
    
    This approach makes GridView the main app that IS Superset, rather than
    embedding or proxying Superset.
    """
    # Add Superset to Python path
    project_root = Path(__file__).parent.parent
    superset_dir = project_root / "superset"
    
    if not superset_dir.exists():
        raise RuntimeError(f"Superset directory not found at {superset_dir}")
    
    sys.path.insert(0, str(superset_dir))
    
    try:
        # Import Superset's create_app function
        from superset.app import create_app as create_superset_app
        
        # Create Superset app with GridView configuration
        config_module = 'gridview.superset_integration.superset_config'
        print(f"🚀 Creating Superset app with GridView config: {config_module}")
        
        # This creates a pure Superset app with our config
        app = create_superset_app(superset_config_module=config_module)
        
        # CRITICAL: Initialize permissions (equivalent of 'superset init')
        # This is what was missing and causing 403 errors on all APIs
        print("🔧 Initializing Superset permissions and roles...")
        with app.app_context():
            try:
                # Step 1: Create all permissions for registered views/APIs
                print("   📋 Adding permissions for all API endpoints...")
                app.appbuilder.add_permissions(update_perms=True)
                
                # Step 2: Sync role definitions (assign permissions to Admin/Alpha/Gamma roles)
                print("   👥 Syncing role definitions...")
                app.appbuilder.sm.sync_role_definitions()
                
                print("✅ Permission initialization completed successfully")
                
            except Exception as init_error:
                print(f"⚠️  Warning: Permission initialization failed: {init_error}")
                # Don't fail app creation, but log the issue
                import traceback
                traceback.print_exc()
        
        # Later: This is where we'll add GridView extensions
        # For now: Just return the pure Superset app with proper permissions
        
        print("✅ GridView-enhanced Superset app created successfully")
        return app
        
    except Exception as e:
        print(f"❌ Failed to create GridView Superset app: {e}")
        import traceback
        traceback.print_exc()
        raise


class GridViewApp:
    """
    GridView application that directly runs Superset.
    
    This is a simplified wrapper that will later be extended with
    GridView-specific features.
    """
    
    def __init__(self):
        # Create the Superset app directly
        self.app = create_gridview_superset_app()
        self._add_gridview_status_routes()
    
    def _add_gridview_status_routes(self):
        """Add basic GridView status routes."""
        
        @self.app.route('/gridview/status')
        def gridview_status():
            """GridView status endpoint."""
            return {
                'gridview': 'running',
                'version': '0.1.0',
                'mode': 'direct_superset',
                'status': 'operational'
            }
    
    def run(self, host: str = '0.0.0.0', port: int = 8088, debug: bool = False):
        """Run the GridView application."""
        print(f"🚀 Starting GridView (Superset) on http://{host}:{port}")
        print(f"📊 Superset interface available at http://{host}:{port}/")
        print(f"🔧 GridView status available at http://{host}:{port}/gridview/status")
        self.app.run(host=host, port=port, debug=debug)


def create_app() -> Flask:
    """
    Factory function to create GridView Flask application.
    
    Returns:
        Flask: Configured GridView application (which is Superset)
    """
    gridview_app = GridViewApp()
    return gridview_app.app


if __name__ == '__main__':
    app = GridViewApp()
    app.run(debug=True)
