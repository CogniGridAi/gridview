"""
GridView Analytics Platform

A modern analytics platform built on top of Apache Superset,
providing enhanced grid-based analytics capabilities.
"""

__version__ = "0.1.0"
__author__ = "GridView Team"
__email__ = "team@gridview.com"

from .app import create_app, GridViewApp

__all__ = ["create_app", "GridViewApp", "__version__"]
