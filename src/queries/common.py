"""Common SQL queries shared across modules."""


def get_date_bounds_query() -> str:
    """SQL to fetch minimum and maximum invoice dates."""
    return """
    SELECT MIN(invoice_date)::date AS min_d
         , MAX(invoice_date)::date AS max_d
    FROM invoice;
    """ 