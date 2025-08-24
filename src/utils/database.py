import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "chinook",
    "user": "razdinesaid",
    "password": "0000",
}


def get_engine() -> Engine:
    """Create and return PostgreSQL engine."""
    connection_string = (
        f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
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