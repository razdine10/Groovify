from pathlib import Path

import streamlit as st

from utils import DB_CONFIG, apply_sidebar_logo
from pages.sql.constants import (
    BUTTON_EXECUTE_QUERY,
    BUTTON_LIST_TABLES,
    BUTTON_TABLE_STATS,
    CHINOOK_GITHUB_URL,
    DEFAULT_SQL_QUERY,
    HEADER_AVAILABLE_TABLES,
    HEADER_DB_STATISTICS,
    HEADER_FREE_SQL_QUERY,
    HEADER_TABLE_DETAILS,
    SQL_TEXTAREA_HEIGHT,
    STATS_DF_ERROR_KEY,
    STATS_DF_KEY,
    TABLES_DF_ERROR_KEY,
    TABLES_DF_KEY,
)
from pages.sql.data_operations import (
    calculate_database_totals,
    create_table_display_dataframe,
    get_table_statistics,
    list_tables,
    run_sql_query,
)

st.set_page_config(
    page_title="SQL Explorer", page_icon="🗄️", layout="wide"
)
apply_sidebar_logo()

# Apply custom CSS
try:
    css_path = Path("pages/alerts/style.css")
    if css_path.exists():
        st.markdown(
            f"<style>{css_path.read_text()}</style>",
            unsafe_allow_html=True,
        )
except Exception:
    pass

# Header
st.markdown(
    """
<div class="finance-header">
  <h1 class="header-title">🗄️ SQL Explorer</h1>
  <p class="header-subtitle">Explore the Chinook database with SQL queries and statistics</p>
</div>
""",
    unsafe_allow_html=True,
)


def _display_database_info():
    """Display database information in sidebar."""
    st.markdown("---")
    st.markdown("**🗄️ Database**")
    st.info(f"🐘 PostgreSQL: {DB_CONFIG['database']}")
    st.markdown("**📊 Data source**")
    st.markdown(f"[Chinook Database (GitHub)]({CHINOOK_GITHUB_URL})")


def _handle_list_tables_button():
    """Handle list tables button click."""
    if st.button(BUTTON_LIST_TABLES, use_container_width=True):
        try:
            tables_df = list_tables()
            st.session_state[TABLES_DF_KEY] = tables_df
        except Exception as e:  # noqa: BLE001
            st.session_state[TABLES_DF_ERROR_KEY] = str(e)


def _handle_table_stats_button():
    """Handle table statistics button click."""
    if st.button(BUTTON_TABLE_STATS, use_container_width=True):
        try:
            stats_df = get_table_statistics()
            st.session_state[STATS_DF_KEY] = stats_df
        except Exception as e:  # noqa: BLE001
            st.session_state[STATS_DF_ERROR_KEY] = str(e)


def _display_tables_list():
    """Display tables list if available."""
    if TABLES_DF_ERROR_KEY in st.session_state:
        st.error(st.session_state.pop(TABLES_DF_ERROR_KEY))

    if TABLES_DF_KEY in st.session_state:
        st.subheader(HEADER_AVAILABLE_TABLES)
        tables_df = st.session_state.pop(TABLES_DF_KEY)
        st.dataframe(tables_df, use_container_width=True, hide_index=True)


def _display_database_metrics(totals: dict):
    """Display database metrics in columns."""
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Tables", totals["total_tables"])
    with col2:
        st.metric("Total Rows", f"{totals['total_rows']:,}")
    with col3:
        st.metric("Total Columns", totals["total_columns"])
    with col4:
        st.metric("Total Size", totals["total_size_display"])


def _display_table_statistics():
    """Display table statistics if available."""
    if STATS_DF_ERROR_KEY in st.session_state:
        st.error(st.session_state.pop(STATS_DF_ERROR_KEY))

    if STATS_DF_KEY in st.session_state:
        stats_df = st.session_state.pop(STATS_DF_KEY)

        st.subheader(HEADER_DB_STATISTICS)

        if not stats_df.empty:
            totals = calculate_database_totals(stats_df)
            _display_database_metrics(totals)

            st.markdown(HEADER_TABLE_DETAILS)
            display_df = create_table_display_dataframe(stats_df)
            st.dataframe(display_df, use_container_width=True, hide_index=True)


def _display_sql_query_section():
    """Display free SQL query section."""
    st.subheader(HEADER_FREE_SQL_QUERY)
    user_sql = st.text_area(
        "SQL", value=DEFAULT_SQL_QUERY, height=SQL_TEXTAREA_HEIGHT
    )

    if st.button(BUTTON_EXECUTE_QUERY):
        try:
            result_df = run_sql_query(user_sql)
            st.dataframe(result_df, use_container_width=True)
        except Exception as e:  # noqa: BLE001
            st.error(f"Error: {e}")


def main():
    """Main function for SQL Explorer."""
    with st.sidebar:
        _display_database_info()
        _handle_list_tables_button()
        _handle_table_stats_button()

    _display_tables_list()
    _display_table_statistics()
    _display_sql_query_section()

    # Footer
    from src.utils.ui_components import render_footer
    render_footer()


if __name__ == "__main__":
    main() 