"""Configuration settings for Groovify application.

This module contains all configuration constants and settings
used throughout the Groovify music analytics dashboard.

Note: UI theming is handled by .streamlit/config.toml for Streamlit-specific
appearance. This file handles application logic and business configuration.
"""

import os
from pathlib import Path

# Application metadata
APP_NAME = "Groovify"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Music Analytics Dashboard"

# File paths
PROJECT_ROOT = Path(__file__).parent
ASSETS_DIR = PROJECT_ROOT / "assets"
CSS_DIR = ASSETS_DIR / "css"
IMG_DIR = ASSETS_DIR / "img"
PAGES_DIR = PROJECT_ROOT / "pages"

# CSS file paths
GLOBAL_CSS_PATH = CSS_DIR / "global.css"

# Database configuration (cloud-ready with environment variables)
DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "chinook"),
    "user": os.getenv("DB_USER", "razdinesaid"),
    "password": os.getenv("DB_PASSWORD", "0000"),
}

# For cloud deployment, you can use services like:
# - Railway (free PostgreSQL)
# - Supabase (free PostgreSQL)
# - ElephantSQL (free PostgreSQL)
# - PlanetScale (free MySQL)

# Streamlit configuration
STREAMLIT_CONFIG = {
    "page_title": APP_NAME,
    "page_icon": "🎵",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# Analytics modules configuration
MODULES = {
    "music": {
        "name": "Music Analytics",
        "icon": "🎵",
        "description": "Track & album performance, artist insights",
    },
    "employees": {
        "name": "Employee Analytics",
        "icon": "👥",
        "description": "Employee performance metrics",
    },
    "customers": {
        "name": "Customer Analytics",
        "icon": "👤",
        "description": "Customer segmentation & analysis",
    },
    "alerts": {
        "name": "Alert System",
        "icon": "🚨",
        "description": "Performance monitoring & alerts",
    },
    "sql": {
        "name": "SQL Explorer",
        "icon": "🗄️",
        "description": "Database exploration & queries",
    },
}

# Application-level theming (synchronized with .streamlit/config.toml)
UI_THEME = {
    "primary_color": "#B53E84",  # Rose - matches .streamlit/config.toml
    "background_color": "#F5EEEF",  # Light rose - matches config.toml
    "secondary_background_color": "#EFC0E3",  # Light purple - matches config.toml
    "text_color": "#2D3748",  # Dark gray - matches config.toml
}

