import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def _get_setting(key: str, default: str) -> str:
    """Return setting from Streamlit secrets or environment with fallback.
    Priorities: st.secrets → os.environ → default.
    """
    try:
        # st.secrets behaves like a dict; .get returns default if missing
        secret_val = st.secrets.get(key)
    except Exception:  # noqa: BLE001
        secret_val = None
    return os.getenv(key, secret_val if secret_val is not None else default)


# Database configuration (cloud/local friendly)
DB_CONFIG = {
    "host": _get_setting("DB_HOST", "localhost"),
    "port": int(_get_setting("DB_PORT", "5432")),
    "database": _get_setting("DB_NAME", "chinook"),
    "user": _get_setting("DB_USER", "razdinesaid"),
    "password": _get_setting("DB_PASSWORD", "0000"),
}

# Optional SSL mode (e.g., require for Supabase)
try:
    DB_SSLMODE = st.secrets.get("DB_SSLMODE") or os.getenv("DB_SSLMODE")
except Exception:  # noqa: BLE001
    DB_SSLMODE = os.getenv("DB_SSLMODE")


def get_engine() -> Engine:
    """Create and return PostgreSQL engine."""
    connection_string = (
        f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    if DB_SSLMODE:
        connection_string += f"?sslmode={DB_SSLMODE}"
    return create_engine(connection_string)


def run_query(sql: str, params=None) -> pd.DataFrame:
    """Execute SQL query and return DataFrame.
    
    Args:
        sql: SQL query string to execute
        params: Optional parameters for parameterized queries
        
    Returns:
        DataFrame with query results, empty DataFrame on error
    """
    engine = get_engine()
    try:
        return pd.read_sql(sql, engine, params=params)
    except Exception as e:  # noqa: BLE001
        st.error(f"Database error: {e}")
        return pd.DataFrame() 