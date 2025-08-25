"""
GridView CLI

Command-line interface for GridView application.
"""

import click
from .app import GridViewApp

@click.group()
@click.version_option(version="0.1.0", prog_name="GridView")
def main():
    """GridView Analytics Platform CLI"""
    pass

@main.command()
@click.option('--host', default='0.0.0.0', help='Host to bind to')
@click.option('--port', default=8088, help='Port to bind to')
@click.option('--debug', is_flag=True, help='Enable debug mode')
def run(host, port, debug):
    """Run the GridView application"""
    click.echo(f"Starting GridView on http://{host}:{port}")
    click.echo("Superset functionality will be available at /gridview/superset")
    
    app = GridViewApp()
    app.run(host=host, port=port, debug=debug)

@main.command()
def status():
    """Show GridView status"""
    click.echo("GridView Analytics Platform")
    click.echo("Version: 0.1.0")
    click.echo("Status: Running in scaffolding mode")
    click.echo("Features: Basic integration with Apache Superset")

@main.command()
def config():
    """Show GridView configuration"""
    from .config import GridViewConfig
    
    config = GridViewConfig()
    settings = config.get_gridview_settings()
    
    click.echo("GridView Configuration:")
    for key, value in settings.items():
        click.echo(f"  {key}: {value}")

if __name__ == '__main__':
    main()
