#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GridView Analytics Platform
Setup configuration for GridView package
"""

from setuptools import setup, find_packages

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gridview",
    version="0.1.0",
    author="GridView Team",
    author_email="team@gridview.com",
    description="GridView Analytics Platform - Enhanced analytics built on Apache Superset",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gridview/gridview",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Database",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "flask>=2.0.0",
        "jinja2>=3.0.0",
        "werkzeug>=2.0.0",
        "click>=8.0.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
    },
    entry_points={
        "console_scripts": [
            "gridview=gridview.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
