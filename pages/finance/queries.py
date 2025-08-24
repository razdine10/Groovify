"""Finance module SQL queries."""

from src.queries.common import get_date_bounds_query

# Financial KPIs query
FINANCIAL_KPIS = """
    SELECT 
        COUNT(i.invoice_id) AS total_invoices,
        ROUND(SUM(i.total), 2) AS total_revenue,
        ROUND(AVG(i.total), 2) AS avg_invoice_amount,
        ROUND(MIN(i.total), 2) AS min_invoice,
        ROUND(MAX(i.total), 2) AS max_invoice,
        ROUND(STDDEV(i.total), 2) AS invoice_stddev,
        COUNT(DISTINCT c.customer_id) AS unique_customers,
        COUNT(DISTINCT c.country) AS countries_served,
        ROUND(SUM(i.total) / COUNT(DISTINCT c.customer_id), 2) AS revenue_per_customer,
        COUNT(DISTINCT DATE(i.invoice_date)) AS active_days
    FROM invoice i
    JOIN customer c ON c.customer_id = i.customer_id
    WHERE i.invoice_date::date BETWEEN %s AND %s;
"""

# Monthly trends query
MONTHLY_TRENDS = """
    SELECT 
        to_char(invoice_date, 'YYYY-MM') AS period,
        to_char(invoice_date, 'Mon YYYY') AS period_label,
        COUNT(*) AS invoice_count,
        ROUND(SUM(total), 2) AS revenue,
        ROUND(AVG(total), 2) AS avg_invoice,
        COUNT(DISTINCT customer_id) AS unique_customers
    FROM invoice 
    WHERE invoice_date::date BETWEEN %s AND %s
    GROUP BY 1, 2
    ORDER BY 1;
"""

# Quarterly trends query
QUARTERLY_TRENDS = """
    SELECT 
        to_char(invoice_date, 'YYYY') || '-Q' || EXTRACT(QUARTER FROM invoice_date) AS period,
        'T' || EXTRACT(QUARTER FROM invoice_date) || ' ' || to_char(invoice_date, 'YYYY') AS period_label,
        COUNT(*) AS invoice_count,
        ROUND(SUM(total), 2) AS revenue,
        ROUND(AVG(total), 2) AS avg_invoice,
        COUNT(DISTINCT customer_id) AS unique_customers
    FROM invoice 
    WHERE invoice_date::date BETWEEN %s AND %s
    GROUP BY 1, 2, EXTRACT(YEAR FROM invoice_date), EXTRACT(QUARTER FROM invoice_date)
    ORDER BY 1;
"""

# Yearly trends query
YEARLY_TRENDS = """
    SELECT 
        to_char(invoice_date, 'YYYY') AS period,
        to_char(invoice_date, 'YYYY') AS period_label,
        COUNT(*) AS invoice_count,
        ROUND(SUM(total), 2) AS revenue,
        ROUND(AVG(total), 2) AS avg_invoice,
        COUNT(DISTINCT customer_id) AS unique_customers
    FROM invoice 
    WHERE invoice_date::date BETWEEN %s AND %s
    GROUP BY 1, 2
    ORDER BY 1;
"""

# Geographic analysis query
GEOGRAPHIC_ANALYSIS = """
    SELECT 
        c.country,
        COUNT(DISTINCT c.customer_id) AS customers,
        COUNT(i.invoice_id) AS invoices,
        ROUND(SUM(i.total), 2) AS total_revenue,
        ROUND(AVG(i.total), 2) AS avg_invoice_amount,
        ROUND(SUM(i.total) / COUNT(DISTINCT c.customer_id), 2) AS revenue_per_customer,
        ROUND(100.0 * SUM(i.total) / (SELECT SUM(total) FROM invoice WHERE invoice_date::date BETWEEN %s AND %s), 2) AS market_share_percent
    FROM customer c
    JOIN invoice i ON c.customer_id = i.customer_id
    WHERE i.invoice_date::date BETWEEN %s AND %s
    GROUP BY c.country
    ORDER BY total_revenue DESC;
"""

# Invoice analysis by amount range
INVOICE_ANALYSIS = """
    SELECT 
        CASE 
            WHEN total < 5 THEN '< $5'
            WHEN total < 10 THEN '$5 - $10'
            WHEN total < 20 THEN '$10 - $20'
            WHEN total < 50 THEN '$20 - $50'
            ELSE '$50+'
        END AS amount_range,
        COUNT(*) AS invoice_count,
        ROUND(SUM(total), 2) AS total_revenue,
        ROUND(AVG(total), 2) AS avg_amount,
        ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM invoice WHERE invoice_date::date BETWEEN %s AND %s), 2) AS percentage
    FROM invoice
    WHERE invoice_date::date BETWEEN %s AND %s
    GROUP BY 1
    ORDER BY MIN(total);
"""

# Seasonality analysis query
SEASONALITY_ANALYSIS = """
    SELECT 
        EXTRACT(MONTH FROM invoice_date) AS month_num,
        to_char(invoice_date, 'Month') AS month_name,
        EXTRACT(QUARTER FROM invoice_date) AS quarter,
        COUNT(*) AS invoice_count,
        ROUND(SUM(total), 2) AS total_revenue,
        ROUND(AVG(total), 2) AS avg_invoice
    FROM invoice
    WHERE invoice_date::date BETWEEN %s AND %s
    GROUP BY 1, 2, 3
    ORDER BY 1;
"""

# Weekly trends query
WEEKLY_TRENDS = """
    SELECT 
        EXTRACT(DOW FROM invoice_date) AS day_num,
        CASE EXTRACT(DOW FROM invoice_date)
            WHEN 0 THEN 'Sunday'
            WHEN 1 THEN 'Monday'
            WHEN 2 THEN 'Tuesday'
            WHEN 3 THEN 'Wednesday'
            WHEN 4 THEN 'Thursday'
            WHEN 5 THEN 'Friday'
            WHEN 6 THEN 'Saturday'
        END AS day_name,
        COUNT(*) AS invoice_count,
        ROUND(SUM(total), 2) AS total_revenue,
        ROUND(AVG(total), 2) AS avg_invoice
    FROM invoice
    WHERE invoice_date::date BETWEEN %s AND %s
    GROUP BY 1, 2
    ORDER BY 1;
"""

# Monthly basket analysis query
MONTHLY_BASKET_ANALYSIS = """
    SELECT 
        to_char(invoice_date, 'YYYY-MM') AS period,
        to_char(invoice_date, 'Mon YYYY') AS period_label,
        COUNT(*) AS invoice_count,
        ROUND(SUM(total), 2) AS total_revenue,
        ROUND(AVG(total), 2) AS avg_basket,
        ROUND(STDDEV(total), 2) AS basket_std
    FROM invoice
    WHERE invoice_date::date BETWEEN %s AND %s
    GROUP BY 1, 2
    ORDER BY 1;
"""

# Quarterly basket analysis query
QUARTERLY_BASKET_ANALYSIS = """
    SELECT 
        to_char(invoice_date, 'YYYY') || '-Q' || EXTRACT(QUARTER FROM invoice_date) AS period,
        'T' || EXTRACT(QUARTER FROM invoice_date) || ' ' || to_char(invoice_date, 'YYYY') AS period_label,
        COUNT(*) AS invoice_count,
        ROUND(SUM(total), 2) AS total_revenue,
        ROUND(AVG(total), 2) AS avg_basket,
        ROUND(STDDEV(total), 2) AS basket_std
    FROM invoice
    WHERE invoice_date::date BETWEEN %s AND %s
    GROUP BY 1, 2, EXTRACT(YEAR FROM invoice_date), EXTRACT(QUARTER FROM invoice_date)
    ORDER BY 1;
"""

# Yearly basket analysis query
YEARLY_BASKET_ANALYSIS = """
    SELECT 
        to_char(invoice_date, 'YYYY') AS period,
        to_char(invoice_date, 'YYYY') AS period_label,
        COUNT(*) AS invoice_count,
        ROUND(SUM(total), 2) AS total_revenue,
        ROUND(AVG(total), 2) AS avg_basket,
        ROUND(STDDEV(total), 2) AS basket_std
    FROM invoice
    WHERE invoice_date::date BETWEEN %s AND %s
    GROUP BY 1, 2
    ORDER BY 1;
""" 