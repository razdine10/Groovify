"""SQL queries for the SQL Explorer module.

This module contains all SQL queries used in the SQL Explorer.
Each query is defined as a string constant and accessed through
dedicated functions.
"""


def get_tables_list_query() -> str:
    """SQL to list all tables in the public schema."""
    return """
    SELECT table_name
    FROM information_schema.tables 
    WHERE table_schema = 'public'
    ORDER BY table_name;
    """


def get_table_row_count_query(table_name: str) -> str:
    """SQL to get accurate row count for a specific table."""
    return f"SELECT COUNT(*) AS row_count FROM {table_name};"


def get_table_info_query() -> str:
    """SQL to get column count and size info for a table."""
    return """
    SELECT COUNT(c.column_name) AS column_count
         , COALESCE(pg_size_pretty(pg_total_relation_size(pg_class.oid)), 'N/A') 
           AS table_size
         , COALESCE(pg_total_relation_size(pg_class.oid), 0) AS size_bytes
    FROM information_schema.columns c
    LEFT JOIN pg_class ON pg_class.relname = c.table_name
    WHERE c.table_name = %s AND c.table_schema = 'public'
    GROUP BY pg_class.oid;
    """


def get_database_schema_query() -> str:
    """SQL to get comprehensive database schema information."""
    return """
    SELECT t.table_name
         , c.column_name
         , c.data_type
         , c.is_nullable
         , c.column_default
    FROM information_schema.tables t
    JOIN information_schema.columns c ON t.table_name = c.table_name
    WHERE t.table_schema = 'public' AND c.table_schema = 'public'
    ORDER BY t.table_name
           , c.ordinal_position;
    """


def get_table_relationships_query() -> str:
    """SQL to get foreign key relationships between tables."""
    return """
    SELECT tc.table_name AS source_table
         , kcu.column_name AS source_column
         , ccu.table_name AS target_table
         , ccu.column_name AS target_column
         , tc.constraint_name
    FROM information_schema.table_constraints tc
    JOIN information_schema.key_column_usage kcu 
        ON tc.constraint_name = kcu.constraint_name
    JOIN information_schema.constraint_column_usage ccu 
        ON ccu.constraint_name = tc.constraint_name
    WHERE tc.constraint_type = 'FOREIGN KEY'
        AND tc.table_schema = 'public'
    ORDER BY tc.table_name
           , tc.constraint_name;
    """ 