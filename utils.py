"""Compatibility wrapper for utilities.

This module provides backward compatibility by importing functions
from the reorganized src.utils package.
"""

# Import all functions from the new organized structure
from src.utils import DB_CONFIG, apply_sidebar_logo, get_engine, run_query

# Maintain backward compatibility
__all__ = [
    "DB_CONFIG",
    "get_engine",
    "run_query", 
    "apply_sidebar_logo",
]



