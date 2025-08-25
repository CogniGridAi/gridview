"""
Branding Manager

Manages GridView branding and UI overrides.
"""

from typing import Dict, Any, Optional
from pathlib import Path

class BrandingManager:
    """
    Manages GridView branding and UI overrides.
    """
    
    def __init__(self):
        self.branding_config = self._load_branding_config()
    
    def _load_branding_config(self) -> Dict[str, Any]:
        """Load branding configuration."""
        return {
            'app_name': 'GridView Analytics Platform',
            'logo': 'gridview_logo.png',
            'color_scheme': {
                'primary': '#2E86AB',
                'secondary': '#A23B72',
                'accent': '#F18F01'
            },
            'terminology': {
                'dashboard': 'workspace',
                'chart': 'grid_cell',
                'slice': 'element'
            }
        }
    
    def render_gridview_home(self):
        """Render GridView home page - directly serve Superset."""
        return f"""
        <html>
        <head>
            <title>GridView</title>
            <meta http-equiv="refresh" content="0; url=/gridview/superset/">
        </head>
        <body>
            <p>Redirecting to Superset...</p>
            <p><a href="/gridview/superset/">Click here if not redirected automatically</a></p>
        </body>
        </html>
        """
    
    def render_gridview_dashboard(self):
        """Render GridView main dashboard."""
        return f"""
        <html>
        <head>
            <title>GridView Dashboard</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .header {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 20px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .logo {{
                    font-size: 2em;
                    color: {self.branding_config['color_scheme']['primary']};
                }}
                .dashboard-content {{
                    background: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .grid-placeholder {{
                    border: 2px dashed #ccc;
                    padding: 60px;
                    text-align: center;
                    color: #666;
                    border-radius: 8px;
                }}
                .back-link {{
                    margin-bottom: 20px;
                }}
                .back-link a {{
                    color: {self.branding_config['color_scheme']['primary']};
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <div class="back-link">
                <a href="/">← Back to Home</a>
            </div>
            
            <div class="header">
                <div class="logo">GridView Dashboard</div>
                <p>Your analytics workspace</p>
            </div>
            
            <div class="dashboard-content">
                <div class="grid-placeholder">
                    <h3>Grid Workspace</h3>
                    <p>This is where your grid-based analytics workspace will be displayed.</p>
                    <p>Future features will include:</p>
                    <ul style="text-align: left; display: inline-block;">
                        <li>Grid cell management</li>
                        <li>Data visualization</li>
                        <li>Real-time updates</li>
                        <li>Collaborative editing</li>
                    </ul>
                </div>
            </div>
        </body>
        </html>
        """
    
    def render_about_page(self):
        """Render about GridView page."""
        return f"""
        <html>
        <head>
            <title>About GridView</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background: white;
                    padding: 40px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .logo {{
                    font-size: 2.5em;
                    color: {self.branding_config['color_scheme']['primary']};
                }}
                .back-link {{
                    margin-bottom: 20px;
                }}
                .back-link a {{
                    color: {self.branding_config['color_scheme']['primary']};
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="back-link">
                    <a href="/">← Back to Home</a>
                </div>
                
                <div class="header">
                    <div class="logo">GridView</div>
                </div>
                
                <h2>About GridView Analytics Platform</h2>
                
                <p>GridView is a modern analytics platform built on top of Apache Superset, 
                providing enhanced grid-based analytics capabilities and a unified user experience.</p>
                
                <h3>Key Features</h3>
                <ul>
                    <li><strong>Grid-Based Workspace:</strong> Organize analytics in flexible grid layouts</li>
                    <li><strong>Enhanced Data Processing:</strong> Advanced analytics beyond traditional BI</li>
                    <li><strong>Superset Integration:</strong> Full Apache Superset functionality embedded</li>
                    <li><strong>Unified Branding:</strong> Consistent GridView user experience</li>
                </ul>
                
                <h3>Technology Stack</h3>
                <ul>
                    <li>Built on Apache Superset</li>
                    <li>Python Flask backend</li>
                    <li>Modern web technologies</li>
                    <li>Extensible architecture</li>
                </ul>
                
                <h3>Development Status</h3>
                <p>GridView is currently in development. This is the scaffolding phase where 
                we're building the foundation for future advanced features.</p>
                
                <div style="text-align: center; margin-top: 40px;">
                    <a href="/" style="
                        display: inline-block;
                        padding: 12px 24px;
                        background: {self.branding_config['color_scheme']['primary']};
                        color: white;
                        text-decoration: none;
                        border-radius: 6px;
                    ">Back to Home</a>
                </div>
            </div>
        </body>
        </html>
        """
    
    def apply_branding_overrides(self, html_content: str) -> str:
        """Apply GridView branding overrides to HTML content."""
        # This is where you'd replace Superset branding with GridView branding
        # For now, return the content as-is
        return html_content
    
    def transform_terminology(self, text: str) -> str:
        """Transform Superset terminology to GridView terminology."""
        terminology_map = self.branding_config['terminology']
        for superset_term, gridview_term in terminology_map.items():
            text = text.replace(superset_term, gridview_term)
        return text
