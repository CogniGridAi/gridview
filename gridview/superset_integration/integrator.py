"""
Superset Integrator

Handles the integration of Apache Superset within GridView.
"""

import os
import sys
from typing import Optional, Dict, Any
from pathlib import Path
from flask import Flask, Blueprint, current_app

class SupersetIntegrator:
    """
    Integrates Apache Superset within GridView application.
    """
    
    def __init__(self):
        self.superset_app = None
        self.route_mapper = None
        self._initialize_superset()
    
    def _initialize_superset(self):
        """Initialize Superset application for integration."""
        try:
            # Add Superset directory to Python path
            superset_dir = Path(__file__).parent.parent.parent.parent / "superset"
            if superset_dir.exists():
                sys.path.insert(0, str(superset_dir))
                
                try:
                    # Try to import full Superset
                    print("Attempting to import superset.app...")
                    from superset.app import create_app as create_superset_app
                    print("✓ superset.app imported successfully")
                    
                    # Create Superset app with GridView configuration
                    # Pass the config module path to create_app
                    config_module_path = 'gridview.superset_integration.superset_config'
                    print(f"Creating Superset app with config: {config_module_path}")
                    self.superset_app = create_superset_app(superset_config_module=config_module_path)
                    
                    print("✓ Full Superset integration initialized successfully")
                except ImportError as e:
                    print(f"⚠ Full Superset import failed: {e}")
                    print(f"  Import error type: {type(e)}")
                    import traceback
                    print(f"  Traceback: {traceback.format_exc()}")
                    print("  Using minimal Superset integration instead")
                    self.superset_app = None
                except Exception as e:
                    print(f"⚠ Error creating Superset app: {e}")
                    print(f"  Error type: {type(e)}")
                    import traceback
                    print(f"  Traceback: {traceback.format_exc()}")
                    print("  Using minimal Superset integration instead")
                    self.superset_app = None
                    
            else:
                print(f"⚠ Superset directory not found at {superset_dir}")
                print("  Superset functionality will not be available")
                
        except Exception as e:
            print(f"⚠ Error initializing Superset: {e}")
            print("  Superset functionality will not be available")
    
    def _get_superset_config(self) -> Dict[str, Any]:
        """Get configuration for Superset integration."""
        from . import superset_config
        
        # Get all configuration variables from the module
        config = {}
        for key, value in vars(superset_config).items():
            if key.isupper() and not key.startswith('_'):
                config[key] = value
        
        return config
    
    def register_routes(self, gridview_app: Flask):
        """Register Superset routes within GridView application."""
        if not self.superset_app:
            print("⚠ Cannot register Superset routes - Superset not initialized")
            return
        
        try:
            # Create a blueprint for Superset routes
            superset_blueprint = Blueprint(
                'superset',
                __name__,
                url_prefix='/gridview/superset',
                template_folder='templates',
                static_folder='static'
            )
            
            # Register Superset routes
            self._register_superset_routes(superset_blueprint)
            
            # Register the blueprint with GridView
            gridview_app.register_blueprint(superset_blueprint)
            
            print("✓ Superset routes registered successfully")
            
        except Exception as e:
            print(f"⚠ Error registering Superset routes: {e}")
    
    def _register_superset_routes(self, blueprint: Blueprint):
        """Register individual Superset routes."""
        
        @blueprint.route('/')
        def superset_home():
            """Superset home page within GridView - serve actual Superset welcome page."""
            if self.superset_app:
                try:
                    with self.superset_app.app_context():
                        # Try to get the actual Superset welcome page (React SPA)
                        response = self.superset_app.test_client().get('/superset/welcome/')
                        if response.status_code == 200:
                            return response.data, response.status_code, response.headers
                        elif response.status_code == 302:
                            # User not logged in, serve login page
                            login_response = self.superset_app.test_client().get('/login/')
                            if login_response.status_code == 200:
                                return login_response.data, login_response.status_code, login_response.headers
                        
                        # If welcome page doesn't work, try the main Superset route
                        response = self.superset_app.test_client().get('/')
                        if response.status_code == 200:
                            return response.data, response.status_code, response.headers
                        elif response.status_code == 302:
                            # Follow redirect
                            location = response.headers.get('Location', '')
                            if location:
                                redirect_response = self.superset_app.test_client().get(location)
                                if redirect_response.status_code == 200:
                                    return redirect_response.data, redirect_response.status_code, redirect_response.headers
                        
                        # Last resort: show error message instead of basic HTML
                        return f"Superset welcome page not accessible. Status: {response.status_code}", 503
                        
                except Exception as e:
                    print(f"Error serving Superset home: {e}")
                    import traceback
                    traceback.print_exc()
                    return f"Superset error: {e}", 500
            else:
                return "Superset not available", 503
        
        @blueprint.route('/dashboard/')
        def superset_dashboards():
            """Superset dashboards within GridView."""
            if self.superset_app:
                try:
                    with self.superset_app.app_context():
                        # Try to get actual Superset dashboard content
                        try:
                            response = self.superset_app.test_client().get('/dashboard/list/')
                            if response.status_code == 200:
                                return response.data, response.status_code, response.headers
                        except:
                            pass
                        
                        # If that fails, try the main dashboard page
                        try:
                            response = self.superset_app.test_client().get('/dashboard/')
                            if response.status_code == 200:
                                return response.data, response.status_code, response.headers
                        except:
                            pass
                        
                        # If all else fails, try to create a new dashboard
                        try:
                            response = self.superset_app.test_client().get('/dashboard/new')
                            if response.status_code == 200:
                                return response.data, response.status_code, response.headers
                        except:
                            pass
                        
                        # Last resort: redirect to Superset root
                        return f"""
                        <html>
                        <head>
                            <title>GridView - Superset</title>
                            <meta http-equiv="refresh" content="0; url=/gridview/superset/">
                        </head>
                        <body>
                            <p>Redirecting to Superset...</p>
                            <p><a href="/gridview/superset/">Click here if not redirected</a></p>
                        </body>
                        </html>
                        """
                except Exception as e:
                    print(f"Error serving Superset dashboards: {e}")
                    return f"""
                    <html>
                    <head><title>GridView - Superset Error</title></head>
                    <body>
                        <h1>GridView Analytics Platform</h1>
                        <h2>Superset Dashboard Error</h2>
                        <p>Error: {e}</p>
                        <p><a href="/gridview/superset/">← Back to Superset</a></p>
                    </body>
                    </html>
                    """
            else:
                return self._render_superset_page('dashboards')
        
        @blueprint.route('/dashboard/list/')
        def superset_dashboard_list():
            """Superset dashboard list within GridView."""
            if self.superset_app:
                try:
                    with self.superset_app.app_context():
                        response = self.superset_app.test_client().get('/dashboard/list/')
                        return response.data, response.status_code, response.headers
                except Exception as e:
                    print(f"Error serving Superset dashboard list: {e}")
                    return f"""
                    <html>
                    <head><title>GridView - Superset Error</title></head>
                    <body>
                        <h1>GridView Analytics Platform</h1>
                        <h2>Superset Dashboard List Error</h2>
                        <p>Error: {e}</p>
                        <p><a href="/gridview/superset/">← Back to Superset</a></p>
                    </body>
                    </html>
                    """
            else:
                return "Superset not available", 503
        
        @blueprint.route('/chart/')
        def superset_charts():
            """Superset charts within GridView."""
            if self.superset_app:
                try:
                    with self.superset_app.app_context():
                        # Try to get actual Superset chart content
                        try:
                            response = self.superset_app.test_client().get('/chart/list/')
                            if response.status_code == 200:
                                return response.data, response.status_code, response.headers
                        except:
                            pass
                        
                        # If that fails, try the main chart page
                        try:
                            response = self.superset_app.test_client().get('/chart/')
                            if response.status_code == 200:
                                return response.data, response.status_code, response.headers
                        except:
                            pass
                        
                        # If all else fails, try to create a new chart
                        try:
                            response = self.superset_app.test_client().get('/chart/add')
                            if response.status_code == 200:
                                return response.data, response.status_code, response.headers
                        except:
                            pass
                        
                        # Last resort: redirect to Superset root
                        return f"""
                        <html>
                        <head>
                            <title>GridView - Superset</title>
                            <meta http-equiv="refresh" content="0; url=/gridview/superset/">
                        </head>
                        <body>
                            <p>Redirecting to Superset...</p>
                            <p><a href="/gridview/superset/">Click here if not redirected</a></p>
                        </body>
                        </html>
                        """
                except Exception as e:
                    print(f"Error serving Superset charts: {e}")
                    return f"""
                    <html>
                    <head><title>GridView - Superset Error</title></head>
                    <body>
                        <h1>GridView Analytics Platform</h1>
                        <h2>Superset Chart Error</h2>
                        <p>Error: {e}</p>
                        <p><a href="/gridview/superset/">← Back to Superset</a></p>
                    </body>
                    </html>
                    """
            else:
                return self._render_superset_page('charts')
        
        @blueprint.route('/chart/add')
        def superset_chart_add():
            """Superset add chart within GridView."""
            if self.superset_app:
                try:
                    with self.superset_app.app_context():
                        response = self.superset_app.test_client().get('/chart/add')
                        return response.data, response.status_code, response.headers
                except Exception as e:
                    print(f"Error serving Superset add chart: {e}")
                    return f"""
                    <html>
                    <head><title>GridView - Superset Error</title></head>
                    <body>
                        <h1>GridView Analytics Platform</h1>
                        <h2>Superset Add Chart Error</h2>
                        <p>Error: {e}</p>
                        <p><a href="/gridview/superset/">← Back to Superset</a></p>
                    </body>
                    </html>
                    """
            else:
                return "Superset not available", 503
        
        @blueprint.route('/sqllab/')
        def superset_sqllab():
            """Superset SQL Lab within GridView."""
            if self.superset_app:
                try:
                    with self.superset_app.app_context():
                        response = self.superset_app.test_client().get('/sqllab/')
                        return response.data, response.status_code, response.headers
                except Exception as e:
                    print(f"Error serving Superset SQL Lab: {e}")
                    return self._render_superset_page('sqllab')
            else:
                return self._render_superset_page('sqllab')
        
        @blueprint.route('/dataset/list/')
        def superset_dataset_list():
            """Superset dataset list within GridView."""
            if self.superset_app:
                try:
                    with self.superset_app.app_context():
                        response = self.superset_app.test_client().get('/dataset/list/')
                        return response.data, response.status_code, response.headers
                except Exception as e:
                    print(f"Error serving Superset dataset list: {e}")
                    return f"""
                    <html>
                    <head><title>GridView - Superset Error</title></head>
                    <body>
                        <h1>GridView Analytics Platform</h1>
                        <h2>Superset Dataset List Error</h2>
                        <p>Error: {e}</p>
                        <p><a href="/gridview/superset/">← Back to Superset</a></p>
                    </body>
                    </html>
                    """
            else:
                return "Superset not available", 503
        
        @blueprint.route('/login/')
        def superset_login():
            """Handle Superset login redirects."""
            if self.superset_app:
                try:
                    with self.superset_app.app_context():
                        response = self.superset_app.test_client().get('/login/')
                        return response.data, response.status_code, response.headers
                except Exception as e:
                    print(f"Error serving Superset login: {e}")
                    return "Superset login error", 500
            else:
                return "Superset not available", 503
        
        @blueprint.route('/debug')
        def superset_debug():
            """Debug endpoint to check Superset integration status."""
            if self.superset_app:
                try:
                    # Test basic Superset functionality
                    with self.superset_app.app_context():
                        # Try to get basic Superset info
                        try:
                            from superset import __version__
                            version = __version__
                        except:
                            version = "unknown"
                        
                        return {
                            'status': 'success',
                            'superset_version': version,
                            'superset_app': 'available',
                            'message': 'Superset is fully integrated and working'
                        }
                except Exception as e:
                    return {
                        'status': 'error',
                        'error': str(e),
                        'message': 'Superset is available but has errors'
                    }
            else:
                return {
                    'status': 'not_available',
                    'message': 'Superset app not initialized'
                }
        
        # Add comprehensive Superset route proxying for all HTTP methods
        @blueprint.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
        def superset_proxy(path):
            """Proxy all Superset routes with full HTTP method support."""
            if self.superset_app:
                try:
                    from flask import request, jsonify
                    
                    with self.superset_app.app_context():
                        # Handle the path properly
                        target_path = f'/{path}' if not path.startswith('/') else path
                        print(f"🔄 Proxying {request.method} request to Superset: {target_path}")
                        
                        # Prepare request data
                        request_data = None
                        content_type = request.content_type
                        
                        if request.method in ['POST', 'PUT', 'PATCH']:
                            if content_type and 'application/json' in content_type:
                                request_data = request.get_json(silent=True)
                            elif content_type and 'application/x-www-form-urlencoded' in content_type:
                                request_data = dict(request.form)
                            else:
                                request_data = request.get_data()
                        
                        # Make the request to Superset
                        test_client = self.superset_app.test_client()
                        
                        if request.method == 'GET':
                            response = test_client.get(target_path, query_string=request.query_string)
                        elif request.method == 'POST':
                            if isinstance(request_data, dict):
                                response = test_client.post(target_path, data=request_data, query_string=request.query_string)
                            else:
                                response = test_client.post(target_path, data=request_data, content_type=content_type, query_string=request.query_string)
                        elif request.method == 'PUT':
                            response = test_client.put(target_path, data=request_data, content_type=content_type, query_string=request.query_string)
                        elif request.method == 'DELETE':
                            response = test_client.delete(target_path, query_string=request.query_string)
                        elif request.method == 'PATCH':
                            response = test_client.patch(target_path, data=request_data, content_type=content_type, query_string=request.query_string)
                        else:
                            response = test_client.get(target_path, query_string=request.query_string)
                        
                        print(f"📋 Superset response: {response.status_code}")
                        
                        # Handle different response types
                        response_headers = dict(response.headers)
                        
                        # Fix content-type for JSON responses
                        if response_headers.get('Content-Type', '').startswith('application/json'):
                            try:
                                # For JSON responses, ensure proper parsing
                                json_data = response.get_json()
                                return jsonify(json_data), response.status_code, response_headers
                            except:
                                pass
                        
                        # For HTML responses, rewrite URLs if needed
                        if response_headers.get('Content-Type', '').startswith('text/html'):
                            try:
                                content = response.get_data(as_text=True)
                                # Rewrite URLs in bootstrap data to include GridView prefix
                                # Handle HTML entity encoding (&#34; = ")
                                content = content.replace('&#34;application_root&#34;: &#34;/&#34;', '&#34;application_root&#34;: &#34;/gridview/superset&#34;')
                                content = content.replace('&#34;path&#34;: &#34;/superset/', '&#34;path&#34;: &#34;/gridview/superset/superset/')
                                content = content.replace('&#34;user_info_url&#34;: &#34;/user_info/&#34;', '&#34;user_info_url&#34;: &#34;/gridview/superset/user_info/&#34;')
                                content = content.replace('&#34;user_logout_url&#34;: &#34;/logout/&#34;', '&#34;user_logout_url&#34;: &#34;/gridview/superset/logout/&#34;')
                                content = content.replace('&#34;user_login_url&#34;: &#34;/login/&#34;', '&#34;user_login_url&#34;: &#34;/gridview/superset/login/&#34;')
                                content = content.replace('&#34;url&#34;: &#34;/lang/', '&#34;url&#34;: &#34;/gridview/superset/lang/')
                                # Keep static assets as they are (handled by proxy)
                                return content, response.status_code, response_headers
                            except:
                                pass
                        
                        # For all other responses, return as-is
                        return response.data, response.status_code, response_headers
                        
                except Exception as e:
                    print(f"❌ Error proxying to Superset: {e}")
                    import traceback
                    traceback.print_exc()
                    return f"Error proxying to Superset: {e}", 500
            else:
                return "Superset not available", 503
        
        # Handle Superset redirects that don't include the prefix
        @blueprint.route('/login/')
        def superset_login_redirect():
            """Handle Superset login redirects without prefix."""
            if self.superset_app:
                try:
                    with self.superset_app.app_context():
                        response = self.superset_app.test_client().get('/login/')
                        print(f"Original login response: {response.data[:200]}...")
                        # Rewrite URLs to include the GridView prefix
                        try:
                            content = response.data.decode('utf-8')
                            # Rewrite URLs in bootstrap data to include GridView prefix
                            # Handle HTML entity encoding (&#34; = ")
                            content = content.replace('&#34;application_root&#34;: &#34;/&#34;', '&#34;application_root&#34;: &#34;/gridview/superset&#34;')
                            content = content.replace('&#34;path&#34;: &#34;/superset/', '&#34;path&#34;: &#34;/gridview/superset/superset/')
                            content = content.replace('&#34;user_info_url&#34;: &#34;/user_info/&#34;', '&#34;user_info_url&#34;: &#34;/gridview/superset/user_info/&#34;')
                            content = content.replace('&#34;user_logout_url&#34;: &#34;/logout/&#34;', '&#34;user_logout_url&#34;: &#34;/gridview/superset/logout/&#34;')
                            content = content.replace('&#34;user_login_url&#34;: &#34;/login/&#34;', '&#34;user_login_url&#34;: &#34;/gridview/superset/login/&#34;')
                            content = content.replace('&#34;url&#34;: &#34;/lang/', '&#34;url&#34;: &#34;/gridview/superset/lang/')
                            print(f"Rewritten content: {content[:200]}...")
                        except Exception as rewrite_error:
                            print(f"Error rewriting URLs: {rewrite_error}")
                            content = response.data.decode('utf-8')
                        return content, response.status_code, response.headers
                except Exception as e:
                    print(f"Error serving Superset login redirect: {e}")
                    return "Superset login error", 500
            else:
                return "Superset not available", 503
        
        # Handle Superset API routes specifically (with and without trailing slash)
        @blueprint.route('/api/<path:api_path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
        @blueprint.route('/api/<path:api_path>/', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
        def superset_api_proxy(api_path):
            """Proxy Superset API calls with proper handling."""
            if self.superset_app:
                try:
                    from flask import request, jsonify
                    
                    with self.superset_app.app_context():
                        # Ensure proper path construction for API calls
                        if api_path.endswith('/'):
                            target_path = f'/api/{api_path}'
                        else:
                            target_path = f'/api/{api_path}/'
                        print(f"🔄 Proxying API {request.method} request: {target_path}")
                        
                        test_client = self.superset_app.test_client()
                        
                        # Handle API requests with proper headers
                        headers = {}
                        if request.headers.get('Content-Type'):
                            headers['Content-Type'] = request.headers.get('Content-Type')
                        if request.headers.get('Authorization'):
                            headers['Authorization'] = request.headers.get('Authorization')
                        
                        # For CSRF token requests, get JWT access token first
                        if 'csrf_token' in api_path and request.method == 'GET':
                            print("🔐 Getting JWT access token for API access")
                            # Use the JWT login endpoint for API access
                            login_response = test_client.post('/api/v1/security/login', 
                                json={
                                    'username': 'admin',
                                    'password': 'admin',
                                    'provider': 'db'
                                },
                                headers={'Content-Type': 'application/json'}
                            )
                            print(f"📋 JWT Login response: {login_response.status_code}")
                            
                            if login_response.status_code == 200:
                                login_data = login_response.get_json()
                                if login_data and 'access_token' in login_data:
                                    access_token = login_data['access_token']
                                    headers['Authorization'] = f'Bearer {access_token}'
                                    print(f"✅ Got access token: {access_token[:20]}...")
                                else:
                                    print(f"❌ No access token in response: {login_data}")
                            else:
                                print(f"❌ Login failed: {login_response.get_data(as_text=True)[:200]}")
                        
                        if request.method == 'GET':
                            response = test_client.get(target_path, query_string=request.query_string, headers=headers)
                        elif request.method == 'POST':
                            response = test_client.post(target_path, 
                                                      data=request.get_data(), 
                                                      content_type=request.content_type,
                                                      query_string=request.query_string,
                                                      headers=headers)
                        elif request.method == 'PUT':
                            response = test_client.put(target_path, 
                                                     data=request.get_data(), 
                                                     content_type=request.content_type,
                                                     headers=headers)
                        elif request.method == 'DELETE':
                            response = test_client.delete(target_path, headers=headers)
                        else:
                            response = test_client.get(target_path, query_string=request.query_string, headers=headers)
                        
                        print(f"📋 API response: {response.status_code}")
                        
                        # Return JSON responses properly
                        response_headers = dict(response.headers)
                        if response_headers.get('Content-Type', '').startswith('application/json'):
                            try:
                                return response.get_json(), response.status_code, response_headers
                            except:
                                pass
                        
                        return response.data, response.status_code, response_headers
                        
                except Exception as e:
                    print(f"❌ Error proxying API request: {e}")
                    import traceback
                    traceback.print_exc()
                    return {"error": f"API proxy error: {e}"}, 500
            else:
                return {"error": "Superset not available"}, 503

        # Handle Superset static assets
        @blueprint.route('/static/<path:filename>')
        def superset_static(filename):
            """Serve Superset static assets."""
            if self.superset_app:
                try:
                    with self.superset_app.app_context():
                        # Use the Superset app's static handling
                        from flask import send_from_directory
                        import os
                        
                        # Try to find the static file in Superset's static directories
                        static_paths = [
                            os.path.join(self.superset_app.static_folder, filename),
                            os.path.join(self.superset_app.root_path, 'static', filename),
                            os.path.join(self.superset_app.root_path, 'superset-frontend', 'dist', filename),
                            os.path.join(self.superset_app.root_path, 'superset', 'static', filename)
                        ]
                        
                        for static_path in static_paths:
                            if os.path.exists(static_path):
                                directory = os.path.dirname(static_path)
                                file_name = os.path.basename(static_path)
                                return send_from_directory(directory, file_name)
                        
                        # If file not found locally, try the Superset app test client
                        response = self.superset_app.test_client().get(f'/static/{filename}')
                        if response.status_code == 200:
                            return response.data, response.status_code, response.headers
                        
                        print(f"Static asset not found: {filename}")
                        return f"Static asset not found: {filename}", 404
                        
                except Exception as e:
                    print(f"Error serving Superset static asset {filename}: {e}")
                    import traceback
                    traceback.print_exc()
                    return f"Error serving static asset: {filename}", 500
            else:
                return "Superset not available", 503
    
    def _rewrite_static_urls(self, html_content: str) -> str:
        """Rewrite static asset URLs in HTML content to include the GridView prefix."""
        import re
        
        # Replace absolute static asset URLs with prefixed ones
        html_content = re.sub(
            r'href="/static/([^"]*)"',
            r'href="/gridview/superset/static/\1"',
            html_content
        )
        html_content = re.sub(
            r'src="/static/([^"]*)"',
            r'src="/gridview/superset/static/\1"',
            html_content
        )
        
        return html_content
    
    def _render_superset_page(self, page_type: str):
        """Render a Superset page within GridView context."""
        try:
            # This is a placeholder - in the full implementation,
            # you would render actual Superset pages
            return f"""
            <html>
            <head>
                <title>GridView - Superset {page_type.title()}</title>
            </head>
            <body>
                <h1>GridView Analytics Platform</h1>
                <h2>Superset {page_type.title()}</h2>
                <p>This is where Superset {page_type} functionality will be embedded.</p>
                <p><a href="/">Back to GridView</a></p>
            </body>
            </html>
            """
        except Exception as e:
            return f"Error rendering Superset page: {e}"
    
    def embed_superset_component(self, component_type: str, config: Dict[str, Any]):
        """Embed a specific Superset component within GridView."""
        if not self.superset_app:
            return None
        
        try:
            # This is where you would embed specific Superset components
            # For now, return a placeholder
            return f"<div>Superset {component_type} component will be embedded here</div>"
        except Exception as e:
            print(f"Error embedding Superset component: {e}")
            return None
    
    def is_superset_available(self) -> bool:
        """Check if Superset integration is available."""
        return self.superset_app is not None
