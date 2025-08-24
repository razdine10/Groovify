"""SQL queries for the employees module.

This module contains all SQL queries used in the employees analytics.
Each query is defined as a string constant and accessed through
dedicated functions.
"""

from src.queries import get_date_bounds_query


def get_employee_performance_query() -> str:
    """SQL for employee performance metrics with sales data."""
    return """
    SELECT e.employee_id
         , e.first_name || ' ' || e.last_name AS employee_name
         , e.title AS job_title
         , COUNT(DISTINCT c.customer_id) AS customers_managed
         , COUNT(DISTINCT i.invoice_id) AS total_orders
         , COALESCE(SUM(i.total), 0) AS total_sales
         , COALESCE(AVG(i.total), 0) AS avg_order_value
         , COALESCE(SUM(i.total) / NULLIF(COUNT(DISTINCT c.customer_id), 0), 0) 
           AS revenue_per_customer
    FROM employee e
    LEFT JOIN customer c ON e.employee_id = c.support_rep_id
    LEFT JOIN invoice i ON c.customer_id = i.customer_id 
                        AND i.invoice_date::date BETWEEN %s AND %s
    GROUP BY e.employee_id
           , e.first_name
           , e.last_name
           , e.title
    ORDER BY total_sales DESC;
    """


def get_customer_satisfaction_query() -> str:
    """SQL for customer satisfaction metrics by employee."""
    return """
    SELECT e.employee_id
         , e.first_name || ' ' || e.last_name AS employee_name
         , COUNT(DISTINCT c.customer_id) AS total_customers
         , COUNT(DISTINCT i.invoice_id) AS total_transactions
         , COALESCE(AVG(i.total), 0) AS avg_transaction_value
         , COUNT(DISTINCT i.invoice_id) * 1.0 / NULLIF(COUNT(DISTINCT c.customer_id), 0) 
           AS transactions_per_customer
    FROM employee e
    LEFT JOIN customer c ON e.employee_id = c.support_rep_id
    LEFT JOIN invoice i ON c.customer_id = i.customer_id 
                        AND i.invoice_date::date BETWEEN %s AND %s
    GROUP BY e.employee_id
           , e.first_name
           , e.last_name
    HAVING COUNT(DISTINCT c.customer_id) > 0
    ORDER BY transactions_per_customer DESC;
    """


def get_territorial_performance_query() -> str:
    """SQL for territorial performance analysis by employee."""
    return """
    SELECT e.employee_id
         , e.first_name || ' ' || e.last_name AS employee_name
         , c.country
         , c.state
         , COUNT(DISTINCT c.customer_id) AS customers_in_territory
         , COUNT(DISTINCT i.invoice_id) AS orders_in_territory
         , COALESCE(SUM(i.total), 0) AS territory_revenue
    FROM employee e
    JOIN customer c ON e.employee_id = c.support_rep_id
    LEFT JOIN invoice i ON c.customer_id = i.customer_id 
                        AND i.invoice_date::date BETWEEN %s AND %s
    GROUP BY e.employee_id
           , e.first_name
           , e.last_name
           , c.country
           , c.state
    HAVING COUNT(DISTINCT c.customer_id) > 0
    ORDER BY territory_revenue DESC;
    """


def get_employee_efficiency_query() -> str:
    """SQL for employee efficiency metrics."""
    return """
    WITH monthly_performance AS (
        SELECT e.employee_id
             , e.first_name || ' ' || e.last_name AS employee_name
             , DATE_TRUNC('month', i.invoice_date) AS month
             , COUNT(DISTINCT i.invoice_id) AS monthly_orders
             , SUM(i.total) AS monthly_revenue
        FROM employee e
        LEFT JOIN customer c ON e.employee_id = c.support_rep_id
        LEFT JOIN invoice i ON c.customer_id = i.customer_id 
                            AND i.invoice_date::date BETWEEN %s AND %s
        GROUP BY e.employee_id
               , e.first_name
               , e.last_name
               , DATE_TRUNC('month', i.invoice_date)
    )
    SELECT employee_id
         , employee_name
         , COUNT(*) AS active_months
         , AVG(monthly_orders) AS avg_monthly_orders
         , AVG(monthly_revenue) AS avg_monthly_revenue
         , STDDEV(monthly_revenue) AS revenue_consistency
    FROM monthly_performance
    WHERE monthly_orders > 0
    GROUP BY employee_id
           , employee_name
    ORDER BY avg_monthly_revenue DESC;
    """


def get_top_customers_by_employee_query() -> str:
    """SQL for top customers managed by each employee."""
    return """
    SELECT e.employee_id
         , e.first_name || ' ' || e.last_name AS employee_name
         , c.first_name || ' ' || c.last_name AS customer_name
         , c.country AS customer_country
         , COUNT(i.invoice_id) AS customer_orders
         , SUM(i.total) AS customer_total_spent
         , RANK() OVER (
               PARTITION BY e.employee_id 
               ORDER BY SUM(i.total) DESC
           ) AS customer_rank
    FROM employee e
    JOIN customer c ON e.employee_id = c.support_rep_id
    JOIN invoice i ON c.customer_id = i.customer_id
    WHERE i.invoice_date::date BETWEEN %s AND %s
    GROUP BY e.employee_id
           , e.first_name
           , e.last_name
           , c.customer_id
           , c.first_name
           , c.last_name
           , c.country
    HAVING SUM(i.total) > 0
    ORDER BY e.employee_id
           , customer_total_spent DESC;
    """


# ---- Compatibility shims (legacy imports) ----

def get_sales_by_employee_query() -> str:
    """Legacy: sales metrics by employee (orders, customers, revenue)."""
    return """
    SELECT e.employee_id
         , e.first_name || ' ' || e.last_name AS employee_name
         , e.title
         , e.city
         , e.country
         , COUNT(DISTINCT i.invoice_id) AS order_count
         , COUNT(DISTINCT c.customer_id) AS unique_customers
         , COALESCE(SUM(i.total), 0) AS total_revenue
         , COALESCE(AVG(i.total), 0) AS avg_order_value
    FROM employee e
    LEFT JOIN customer c ON e.employee_id = c.support_rep_id
    LEFT JOIN invoice i ON c.customer_id = i.customer_id
                        AND i.invoice_date::date BETWEEN %s AND %s
    GROUP BY e.employee_id
           , e.first_name
           , e.last_name
           , e.title
           , e.city
           , e.country
    ORDER BY total_revenue DESC;
    """


def get_team_hierarchy_query() -> str:
    """Legacy: team hierarchy listing with manager info."""
    return """
    SELECT e.employee_id
         , e.first_name || ' ' || e.last_name AS employee_name
         , e.title
         , e.city
         , e.country
         , e.reports_to
         , m.first_name || ' ' || m.last_name AS manager_name
    FROM employee e
    LEFT JOIN employee m ON e.reports_to = m.employee_id
    ORDER BY e.reports_to NULLS FIRST
           , e.employee_id;
    """


def get_customer_management_query() -> str:
    """Legacy: customer management metrics by employee."""
    return """
    SELECT e.employee_id
         , e.first_name || ' ' || e.last_name AS employee_name
         , COUNT(DISTINCT c.customer_id) AS customer_count
         , COALESCE(SUM(i.total), 0) AS total_customer_value
         , COALESCE(AVG(i.total), 0) AS avg_customer_value
    FROM employee e
    LEFT JOIN customer c ON e.employee_id = c.support_rep_id
    LEFT JOIN invoice i ON c.customer_id = i.customer_id
                        AND i.invoice_date::date BETWEEN %s AND %s
    GROUP BY e.employee_id
           , e.first_name
           , e.last_name
    ORDER BY total_customer_value DESC;
    """


def get_employee_productivity_query() -> str:
    """Legacy: employee productivity metrics over a date range."""
    return """
    WITH stats AS (
        SELECT e.employee_id
             , e.first_name || ' ' || e.last_name AS employee_name
             , COUNT(DISTINCT i.invoice_id) AS total_orders
             , COUNT(DISTINCT c.customer_id) AS total_customers
             , COALESCE(SUM(i.total), 0) AS total_revenue
             , COUNT(DISTINCT i.invoice_date::date) AS active_days
        FROM employee e
        LEFT JOIN customer c ON e.employee_id = c.support_rep_id
        LEFT JOIN invoice i ON c.customer_id = i.customer_id
                            AND i.invoice_date::date BETWEEN %s AND %s
        GROUP BY e.employee_id
               , e.first_name
               , e.last_name
    )
    SELECT employee_id
         , employee_name
         , total_orders
         , total_customers
         , total_revenue
         , active_days
         , CASE WHEN active_days > 0 THEN ROUND(total_orders::decimal / active_days, 2)
                ELSE 0 END AS orders_per_day
         , CASE WHEN active_days > 0 THEN ROUND(total_revenue / active_days, 2)
                ELSE 0 END AS revenue_per_day
    FROM stats
    ORDER BY revenue_per_day DESC;
    """


def get_territory_analysis_query() -> str:
    """Legacy alias: territory analysis per employee (same as territorial performance)."""
    return get_territorial_performance_query()  # reuse SQL 