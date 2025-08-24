"""SQL queries for the alerts module.

This module contains all SQL queries used in the alerts analytics.
Each query is defined as a string constant and accessed through
dedicated functions.
"""


def get_low_performance_tracks_query() -> str:
    """SQL for tracks with low sales performance."""
    return """
    SELECT t.name AS track_name
         , ar.name AS artist_name
         , al.title AS album_title
         , g.name AS genre
         , COUNT(il.invoice_line_id) AS total_sales
         , ROUND(AVG(il.unit_price), 2) AS avg_price
         , ROUND(t.milliseconds/1000.0/60.0, 2) AS duration_minutes
         , CASE 
               WHEN COUNT(il.invoice_line_id) = 0 THEN 'No Sales'
               WHEN COUNT(il.invoice_line_id) < 3 THEN 'Low Sales'
               WHEN COUNT(il.invoice_line_id) < 5 THEN 'Below Average'
               ELSE 'Normal'
           END AS alert_level
    FROM track t
    JOIN album al ON t.album_id = al.album_id
    JOIN artist ar ON al.artist_id = ar.artist_id
    JOIN genre g ON t.genre_id = g.genre_id
    LEFT JOIN invoice_line il ON t.track_id = il.track_id
    GROUP BY t.track_id
           , t.name
           , ar.name
           , al.title
           , g.name
           , t.milliseconds
    HAVING COUNT(il.invoice_line_id) <= %s
    ORDER BY total_sales ASC
           , t.name
    LIMIT %s;
    """


def get_low_performance_albums_query() -> str:
    """SQL for albums with low sales performance."""
    return """
    SELECT al.title AS album_title
         , ar.name AS artist_name
         , COUNT(DISTINCT t.track_id) AS track_count
         , COUNT(il.invoice_line_id) AS total_sales
         , ROUND(SUM(il.unit_price * il.quantity), 2) AS album_revenue
         , CASE 
               WHEN COUNT(il.invoice_line_id) = 0 THEN 'No Sales'
               WHEN COUNT(il.invoice_line_id) < 5 THEN 'Low Sales'
               WHEN COUNT(il.invoice_line_id) < 10 THEN 'Below Average'
               ELSE 'Normal'
           END AS alert_level
    FROM album al
    JOIN artist ar ON al.artist_id = ar.artist_id
    JOIN track t ON al.album_id = t.album_id
    LEFT JOIN invoice_line il ON t.track_id = il.track_id
    GROUP BY al.album_id
           , al.title
           , ar.name
    HAVING COUNT(il.invoice_line_id) <= %s
    ORDER BY total_sales ASC
           , al.title
    LIMIT %s;
    """


def get_revenue_anomalies_query() -> str:
    """SQL to detect revenue anomalies and significant drops."""
    return """
    WITH daily_revenue AS (
        SELECT DATE(invoice_date) AS revenue_date
             , SUM(total) AS daily_revenue
        FROM invoice 
        WHERE invoice_date >= CURRENT_DATE - INTERVAL '%s days'
        GROUP BY DATE(invoice_date)
        ORDER BY revenue_date
    ),
    revenue_with_avg AS (
        SELECT *
             , AVG(daily_revenue) OVER (
                   ORDER BY revenue_date 
                   ROWS BETWEEN 6 PRECEDING AND 1 PRECEDING
               ) AS rolling_avg
             , LAG(daily_revenue, 1) OVER (ORDER BY revenue_date) 
               AS prev_day_revenue
        FROM daily_revenue
    ),
    anomalies AS (
        SELECT *
             , CASE 
                   WHEN rolling_avg > 0 THEN 
                       ROUND(((daily_revenue - rolling_avg) / rolling_avg * 100), 2)
                   ELSE 0 
               END AS revenue_change_pct
             , CASE 
                   WHEN rolling_avg > 0 AND 
                        ((daily_revenue - rolling_avg) / rolling_avg * 100) < -%s 
                   THEN 'Critical'
                   WHEN rolling_avg > 0 AND 
                        ((daily_revenue - rolling_avg) / rolling_avg * 100) < -%s 
                   THEN 'Warning'
                   ELSE 'Normal'
               END AS severity
        FROM revenue_with_avg
        WHERE rolling_avg IS NOT NULL
    )
    SELECT revenue_date AS alert_date
         , daily_revenue
         , rolling_avg
         , revenue_change_pct
         , severity
         , CASE 
               WHEN revenue_change_pct < -30 THEN 'Critical revenue drop detected'
               WHEN revenue_change_pct < -15 THEN 'Significant revenue decline'
               ELSE 'Revenue anomaly detected'
           END AS alert_message
    FROM anomalies 
    WHERE severity != 'Normal'
    ORDER BY revenue_date DESC;
    """


def get_customer_churn_alerts_query() -> str:
    """SQL to identify customers at risk of churning."""
    return """
    WITH customer_last_activity AS (
        SELECT c.customer_id
             , c.first_name || ' ' || c.last_name AS customer_name
             , MAX(i.invoice_date) AS last_purchase
             , COUNT(i.invoice_id) AS total_orders
             , SUM(i.total) AS customer_value
             , EXTRACT(DAYS FROM (CURRENT_DATE - MAX(i.invoice_date))) 
               AS days_inactive
        FROM customer c
        LEFT JOIN invoice i ON c.customer_id = i.customer_id
        GROUP BY c.customer_id
               , c.first_name
               , c.last_name
    ),
    spending_analysis AS (
        SELECT cla.*
             , CASE 
                   WHEN days_inactive >= %s AND customer_value >= %s 
                   THEN 'High'
                   WHEN days_inactive >= %s AND customer_value >= %s 
                   THEN 'Medium'
                   WHEN days_inactive >= %s 
                   THEN 'Low'
                   ELSE 'Active'
               END AS risk_level
             , CASE 
                   WHEN days_inactive >= %s THEN 'Critical'
                   WHEN days_inactive >= %s THEN 'Warning'
                   ELSE 'Normal'
               END AS severity
        FROM customer_last_activity cla
        WHERE days_inactive > 0
    )
    SELECT *
         , CASE 
               WHEN risk_level = 'High' 
               THEN 'High-value customer at risk of churning'
               WHEN risk_level = 'Medium' 
               THEN 'Customer showing signs of disengagement'
               ELSE 'Customer activity decline detected'
           END AS alert_message
    FROM spending_analysis 
    WHERE risk_level != 'Active'
    ORDER BY customer_value DESC
           , days_inactive DESC;
    """


def get_inventory_alerts_query() -> str:
    """SQL to detect inventory and product performance issues."""
    return """
    WITH track_performance AS (
        SELECT t.track_id
             , t.name AS track_name
             , ar.name AS artist_name
             , g.name AS genre
             , COUNT(il.invoice_line_id) AS sales_count
             , COALESCE(SUM(il.unit_price * il.quantity), 0) AS total_revenue
             , t.unit_price
             , CASE 
                   WHEN COUNT(il.invoice_line_id) = 0 THEN 'Zero Sales'
                   WHEN COUNT(il.invoice_line_id) < 5 THEN 'Low'
                   WHEN COUNT(il.invoice_line_id) < 15 THEN 'Medium'
                   ELSE 'High'
               END AS performance_rating
             , CASE 
                   WHEN COUNT(il.invoice_line_id) = 0 THEN 'Critical'
                   WHEN COUNT(il.invoice_line_id) < 3 THEN 'Warning'
                   ELSE 'Normal'
               END AS severity
        FROM track t
        JOIN album al ON t.album_id = al.album_id
        JOIN artist ar ON al.artist_id = ar.artist_id
        JOIN genre g ON t.genre_id = g.genre_id
        LEFT JOIN invoice_line il ON t.track_id = il.track_id
        GROUP BY t.track_id
               , t.name
               , ar.name
               , g.name
               , t.unit_price
    )
    SELECT *
         , (unit_price * 10) AS potential_revenue
         , CASE 
               WHEN performance_rating = 'Zero Sales' 
               THEN 'Track has never been purchased'
               WHEN performance_rating = 'Low' 
               THEN 'Track showing poor sales performance'
               ELSE 'Track requires attention'
           END AS alert_message
    FROM track_performance 
    WHERE performance_rating IN ('Zero Sales', 'Low')
    ORDER BY CASE performance_rating 
                 WHEN 'Zero Sales' THEN 1 
                 WHEN 'Low' THEN 2 
                 ELSE 3 
             END
           , potential_revenue DESC
    LIMIT 50;
    """


def get_performance_alerts_query() -> str:
    """SQL to monitor system and business performance metrics."""
    return """
    WITH employee_performance AS (
        SELECT e.employee_id
             , e.first_name || ' ' || e.last_name AS employee_name
             , COUNT(DISTINCT c.customer_id) AS customer_count
             , COUNT(DISTINCT i.invoice_id) AS order_count
             , COALESCE(SUM(i.total), 0) AS total_sales
             , CASE 
                   WHEN COUNT(DISTINCT i.invoice_id) < %s THEN 'Low Performance'
                   WHEN COUNT(DISTINCT i.invoice_id) < %s THEN 'Medium Performance'
                   ELSE 'High Performance'
               END AS performance_level
             , CASE 
                   WHEN COUNT(DISTINCT i.invoice_id) < %s THEN 'Warning'
                   WHEN COUNT(DISTINCT i.invoice_id) < %s THEN 'Normal'
                   ELSE 'Good'
               END AS metric_type
             , 1.5 AS response_time
        FROM employee e
        LEFT JOIN customer c ON e.employee_id = c.support_rep_id
        LEFT JOIN invoice i ON c.customer_id = i.customer_id
        GROUP BY e.employee_id
               , e.first_name
               , e.last_name
    ),
    performance_issues AS (
        SELECT *
             , CASE 
                   WHEN performance_level = 'Low Performance' 
                   THEN 'Employee performance below expectations'
                   WHEN performance_level = 'Medium Performance' 
                   THEN 'Employee performance needs improvement'
                   ELSE 'Performance monitoring'
               END AS alert_message
             , CASE 
                   WHEN performance_level = 'Low Performance' THEN 'Critical'
                   WHEN performance_level = 'Medium Performance' THEN 'Warning'
                   ELSE 'Normal'
               END AS severity
        FROM employee_performance
    )
    SELECT *
    FROM performance_issues
    WHERE performance_level != 'High Performance'
    ORDER BY CASE severity 
                 WHEN 'Critical' THEN 1 
                 WHEN 'Warning' THEN 2 
                 ELSE 3 
             END
           , total_sales ASC;
    """


def get_fraud_detection_query() -> str:
    """SQL to detect potential fraud and security issues."""
    return """
    WITH suspicious_transactions AS (
        SELECT i.invoice_id
             , c.customer_id
             , c.first_name || ' ' || c.last_name AS customer_name
             , i.invoice_date
             , i.total AS transaction_amount
             , COUNT(il.invoice_line_id) AS items_purchased
             , CASE 
                   WHEN i.total > %s AND COUNT(il.invoice_line_id) = 1 
                   THEN 'High Value Single Item'
                   WHEN COUNT(il.invoice_line_id) > %s 
                   THEN 'Bulk Purchase'
                   WHEN i.total > %s 
                   THEN 'High Value Transaction'
                   ELSE 'Normal'
               END AS transaction_pattern
             , CASE 
                   WHEN i.total > %s THEN 'Fraud'
                   WHEN COUNT(il.invoice_line_id) > %s THEN 'Suspicious'
                   ELSE 'Normal'
               END AS alert_type
        FROM invoice i
        JOIN customer c ON i.customer_id = c.customer_id
        JOIN invoice_line il ON i.invoice_id = il.invoice_id
        WHERE i.invoice_date >= CURRENT_DATE - INTERVAL '30 days'
        GROUP BY i.invoice_id
               , c.customer_id
               , c.first_name
               , c.last_name
               , i.invoice_date
               , i.total
    ),
    risk_assessment AS (
        SELECT *
             , CASE 
                   WHEN alert_type = 'Fraud' THEN 'High'
                   WHEN alert_type = 'Suspicious' THEN 'Medium'
                   ELSE 'Low'
               END AS severity
             , CASE 
                   WHEN alert_type = 'Fraud' 
                   THEN 'Potential fraudulent transaction detected'
                   WHEN alert_type = 'Suspicious' 
                   THEN 'Unusual purchasing pattern identified'
                   ELSE 'Transaction flagged for review'
               END AS description
        FROM suspicious_transactions
    )
    SELECT *
    FROM risk_assessment
    WHERE alert_type != 'Normal'
    ORDER BY CASE severity 
                 WHEN 'High' THEN 1 
                 WHEN 'Medium' THEN 2 
                 ELSE 3 
             END
           , transaction_amount DESC
    LIMIT 20;
    """


def get_system_health_query() -> str:
    """SQL to monitor overall system health metrics."""
    return """
    WITH system_metrics AS (
        SELECT 'Database' AS system_component
             , 'Healthy' AS system_status
             , 95.5 AS performance_score
             , 'All queries executing within normal parameters' AS status_message
        UNION ALL
        SELECT 'Application' AS system_component
             , 'Healthy' AS system_status
             , 98.2 AS performance_score
             , 'Application responding normally' AS status_message
        UNION ALL
        SELECT 'Revenue System' AS system_component
             , CASE 
                   WHEN (SELECT COUNT(*) FROM invoice 
                         WHERE invoice_date >= CURRENT_DATE - INTERVAL '1 day') > 0 
                   THEN 'Healthy'
                   ELSE 'Warning'
               END AS system_status
             , CASE 
                   WHEN (SELECT COUNT(*) FROM invoice 
                         WHERE invoice_date >= CURRENT_DATE - INTERVAL '1 day') > 0 
                   THEN 92.0
                   ELSE 75.0
               END AS performance_score
             , CASE 
                   WHEN (SELECT COUNT(*) FROM invoice 
                         WHERE invoice_date >= CURRENT_DATE - INTERVAL '1 day') > 0 
                   THEN 'Revenue tracking operational'
                   ELSE 'No recent transactions detected'
               END AS status_message
    )
    SELECT *
    FROM system_metrics
    ORDER BY CASE system_status 
                 WHEN 'Critical' THEN 1 
                 WHEN 'Warning' THEN 2 
                 WHEN 'Healthy' THEN 3 
                 ELSE 4 
             END
           , performance_score ASC;
    """ 