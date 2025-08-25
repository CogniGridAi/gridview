"""
Superset Route Mapper

Maps Superset routes to GridView routes for seamless integration.
"""

from typing import Dict, List, Tuple
from flask import Blueprint, Flask

class SupersetRouteMapper:
    """
    Maps Superset routes to GridView routes for integration.
    """
    
    def __init__(self):
        self.route_mappings = {
            # Core Superset routes
            '/superset/dashboard/': '/gridview/superset/dashboard/',
            '/superset/chart/': '/gridview/superset/chart/',
            '/superset/sqllab/': '/gridview/superset/sqllab/',
            '/superset/explore/': '/gridview/superset/explore/',
            '/superset/datasets/': '/gridview/superset/datasets/',
            '/superset/databaseview/': '/gridview/superset/databaseview/',
            
            # API routes
            '/superset/api/': '/gridview/superset/api/',
            '/superset/chart/data': '/gridview/superset/chart/data',
            '/superset/dashboard/': '/gridview/superset/dashboard/',
            
            # Static assets
            '/superset/static/': '/gridview/superset/static/',
            '/superset/assets/': '/gridview/superset/assets/',
        }
        
        self.excluded_routes = [
            '/superset/login/',
            '/superset/logout/',
            '/superset/health/',
        ]
    
    def get_route_mappings(self) -> Dict[str, str]:
        """Get all route mappings."""
        return self.route_mappings.copy()
    
    def map_route(self, superset_route: str) -> str:
        """Map a Superset route to GridView route."""
        return self.route_mappings.get(superset_route, superset_route)
    
    def should_exclude_route(self, route: str) -> bool:
        """Check if a route should be excluded from mapping."""
        return any(route.startswith(excluded) for excluded in self.excluded_routes)
    
    def create_route_blueprint(self, superset_app: Flask, gridview_prefix: str = '/gridview/superset') -> Blueprint:
        """Create a blueprint with mapped routes."""
        blueprint = Blueprint(
            'superset_mapped',
            __name__,
            url_prefix=gridview_prefix
        )
        
        # Register mapped routes
        self._register_mapped_routes(blueprint, superset_app)
        
        return blueprint
    
    def _register_mapped_routes(self, blueprint: Blueprint, superset_app: Flask):
        """Register mapped routes in the blueprint."""
        # This is a placeholder for the actual route registration
        # In the full implementation, you would iterate through Superset routes
        # and register them with the appropriate mappings
        
        @blueprint.route('/')
        def superset_root():
            """Root of mapped Superset routes."""
            return "GridView - Superset Integration Root"
        
        @blueprint.route('/dashboard/')
        def superset_dashboards():
            """Mapped Superset dashboards route."""
            return "GridView - Superset Dashboards"
        
        @blueprint.route('/chart/')
        def superset_charts():
            """Mapped Superset charts route."""
            return "GridView - Superset Charts"
    
    def get_route_statistics(self) -> Dict[str, int]:
        """Get statistics about route mappings."""
        return {
            'total_mappings': len(self.route_mappings),
            'excluded_routes': len(self.excluded_routes),
            'mapped_prefix': '/gridview/superset'
        }
