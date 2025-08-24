"""Data operations for the SQL Explorer module.

This module contains functions for database operations, data processing,
and utility functions for the SQL Explorer.
"""

from typing import Any, Optional, Tuple

import pandas as pd
import streamlit as st

from utils import run_query
from .queries import (
    get_table_info_query,
    get_table_row_count_query,
    get_tables_list_query,
)
from .constants import (
    DEFAULT_FALLBACK_COUNT,
    DEFAULT_FALLBACK_SIZE,
    KB_THRESHOLD,
    MB_THRESHOLD,
)


@st.cache_data(show_spinner=False)
def run_sql_query(sql: str, params: Optional[Tuple[Any, ...]] = None) -> pd.DataFrame:
    """Execute SQL query with caching for performance."""
    return run_query(sql, params)


def list_tables() -> pd.DataFrame:
    """Get list of all tables in the public schema."""
    return run_query(get_tables_list_query())


def _format_file_size(size_bytes: int) -> str:
    """Format file size in bytes to human-readable format."""
    if size_bytes > MB_THRESHOLD:
        return f"{size_bytes / MB_THRESHOLD:.1f} MB"
    elif size_bytes > KB_THRESHOLD:
        return f"{size_bytes / KB_THRESHOLD:.1f} KB"
    else:
        return f"{size_bytes} B"


def _get_table_statistics(table_name: str) -> dict:
    """Get comprehensive statistics for a single table."""
    try:
        # Get accurate row count
        count_result = run_query(get_table_row_count_query(table_name))
        row_count = (
            count_result.iloc[0]["row_count"] if not count_result.empty else 0
        )

        # Get column count and size info
        info_result = run_query(get_table_info_query(), (table_name,))

        if not info_result.empty:
            column_count = info_result.iloc[0]["column_count"]
            table_size = info_result.iloc[0]["table_size"]
            size_bytes = info_result.iloc[0]["size_bytes"]
        else:
            column_count = DEFAULT_FALLBACK_COUNT
            table_size = DEFAULT_FALLBACK_SIZE
            size_bytes = DEFAULT_FALLBACK_COUNT

        return {
            "table_name": table_name,
            "row_count": row_count,
            "column_count": column_count,
            "table_size": table_size,
            "size_bytes": size_bytes,
        }

    except Exception:  # noqa: BLE001
        return {
            "table_name": table_name,
            "row_count": DEFAULT_FALLBACK_COUNT,
            "column_count": DEFAULT_FALLBACK_COUNT,
            "table_size": DEFAULT_FALLBACK_SIZE,
            "size_bytes": DEFAULT_FALLBACK_COUNT,
        }


def get_table_statistics() -> pd.DataFrame:
    """Get comprehensive statistics for all tables."""
    tables_df = run_query(get_tables_list_query())

    stats_list = []
    for _, row in tables_df.iterrows():
        table_name = row["table_name"]
        stats = _get_table_statistics(table_name)
        stats_list.append(stats)

    # Convert to DataFrame and sort by size
    stats_df = pd.DataFrame(stats_list)
    stats_df = stats_df.sort_values("size_bytes", ascending=False)

    return stats_df


def calculate_database_totals(stats_df: pd.DataFrame) -> dict:
    """Calculate total statistics for the entire database."""
    if stats_df.empty:
        return {
            "total_tables": 0,
            "total_rows": 0,
            "total_columns": 0,
            "total_size_display": "N/A",
        }

    total_tables = len(stats_df)
    total_rows = stats_df["row_count"].sum()
    total_columns = stats_df["column_count"].sum()
    total_size_bytes = stats_df["size_bytes"].sum()

    total_size_display = (
        _format_file_size(total_size_bytes) if total_size_bytes > 0 else "N/A"
    )

    return {
        "total_tables": total_tables,
        "total_rows": total_rows,
        "total_columns": total_columns,
        "total_size_display": total_size_display,
    }


def create_table_display_dataframe(stats_df: pd.DataFrame) -> pd.DataFrame:
    """Create a formatted DataFrame for displaying table statistics."""
    from .constants import TABLE_STATS_COLUMNS

    display_df = stats_df[list(TABLE_STATS_COLUMNS.keys())].copy()
    display_df = display_df.rename(columns=TABLE_STATS_COLUMNS)
    display_df.insert(0, "#", range(1, len(display_df) + 1))

    return display_df 