"""Constants used by the SQL Explorer module."""

# Default SQL queries
DEFAULT_SQL_QUERY = """-- Example: list tables
SELECT * FROM artist LIMIT 10;"""

# UI configuration
SQL_TEXTAREA_HEIGHT = 220
QUERY_RESULTS_LIMIT = 1000

# File size thresholds
MB_THRESHOLD = 1024 * 1024
KB_THRESHOLD = 1024

# Database schema
PUBLIC_SCHEMA = "public"

# External links
CHINOOK_GITHUB_URL = "https://github.com/lerocha/chinook-database"

# Session state keys
TABLES_DF_KEY = "tables_df"
TABLES_DF_ERROR_KEY = "tables_df_error"
STATS_DF_KEY = "stats_df"
STATS_DF_ERROR_KEY = "stats_df_error"

# Button labels
BUTTON_LIST_TABLES = "🔍 List tables"
BUTTON_TABLE_STATS = "📊 Table statistics"
BUTTON_EXECUTE_QUERY = "Execute query"

# Section headers
HEADER_AVAILABLE_TABLES = "Available tables"
HEADER_DB_STATISTICS = "📊 Database Statistics"
HEADER_TABLE_DETAILS = "#### Table Details"
HEADER_FREE_SQL_QUERY = "Free SQL query"

# Column mappings
TABLE_STATS_COLUMNS = {
    "table_name": "Table",
    "row_count": "Rows",
    "column_count": "Columns",
    "table_size": "Size",
}

# Default fallback values
DEFAULT_FALLBACK_COUNT = 0
DEFAULT_FALLBACK_SIZE = "N/A" 