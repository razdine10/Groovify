"""SQL queries for the customers module.

This module contains all SQL queries used in the customers analytics.
Each query is defined as a string constant and accessed through
dedicated functions.
"""

from src.queries import get_date_bounds_query


def get_rfm_clustering_query() -> str:
    """SQL for RFM clustering with musical preferences."""
    return """
    WITH customer_rfm AS (
        SELECT c.customer_id
             , c.first_name || ' ' || c.last_name AS customer_name
             , EXTRACT(DAYS FROM (CURRENT_DATE - MAX(i.invoice_date))) AS recency_days
             , COUNT(i.invoice_id) AS frequency
             , ROUND(SUM(i.total), 2) AS monetary
        FROM customer c
        JOIN invoice i ON c.customer_id = i.customer_id
        WHERE i.invoice_date::date BETWEEN %s AND %s
        GROUP BY c.customer_id
               , c.first_name
               , c.last_name
    ),
    customer_music_preferences AS (
        SELECT c.customer_id
             , COUNT(DISTINCT g.genre_id) AS nb_different_genres
             , COUNT(il.invoice_line_id) AS nb_purchased_tracks
        FROM customer c
        JOIN invoice i ON c.customer_id = i.customer_id
        JOIN invoice_line il ON i.invoice_id = il.invoice_id
        JOIN track t ON il.track_id = t.track_id
        JOIN genre g ON t.genre_id = g.genre_id
        WHERE i.invoice_date::date BETWEEN %s AND %s
        GROUP BY c.customer_id
    )
    SELECT rfm.*
         , COALESCE(mp.nb_different_genres, 0) AS nb_different_genres
         , COALESCE(mp.nb_purchased_tracks, 0) AS nb_purchased_tracks
         , CASE
               WHEN recency_days <= 90 AND frequency >= 5 AND monetary >= 40
                   THEN 'Champions'
               WHEN recency_days <= 90 AND frequency >= 3 AND monetary >= 25
                   THEN 'Loyal Customers'
               WHEN recency_days <= 180 AND frequency >= 2
                   THEN 'Potential Loyalists'
               WHEN recency_days <= 90 AND frequency < 3
                   THEN 'New Customers'
               WHEN recency_days > 180 AND recency_days <= 365
                   THEN 'At Risk'
               WHEN recency_days > 365
                   THEN 'Lost'
               ELSE 'Others'
           END AS rfm_cluster
    FROM customer_rfm rfm
    LEFT JOIN customer_music_preferences mp ON rfm.customer_id = mp.customer_id;
    """


def get_customer_journey_query() -> str:
    """SQL for customer journey and lifecycle analysis."""
    return """
    WITH customer_timeline AS (
        SELECT c.customer_id
             , c.first_name || ' ' || c.last_name AS customer_name
             , c.country
             , c.city
             , MIN(i.invoice_date) AS first_purchase
             , MAX(i.invoice_date) AS last_purchase
             , COUNT(i.invoice_id) AS total_orders
             , SUM(i.total) AS total_spent
             , AVG(i.total) AS avg_order_value
             , EXTRACT(DAYS FROM (MAX(i.invoice_date) - MIN(i.invoice_date))) AS customer_lifespan_days
        FROM customer c
        JOIN invoice i ON c.customer_id = i.customer_id
        WHERE i.invoice_date::date BETWEEN %s AND %s
        GROUP BY c.customer_id
               , c.first_name
               , c.last_name
               , c.country
               , c.city
    )
    SELECT *
         , CASE
               WHEN total_orders = 1 THEN 'One-time'
               WHEN total_orders <= 3 THEN 'Occasional'
               WHEN total_orders <= 6 THEN 'Regular'
               ELSE 'Frequent'
           END AS customer_type
         , CASE
               WHEN total_spent >= 50 THEN 'High Value'
               WHEN total_spent >= 25 THEN 'Medium Value'
               ELSE 'Low Value'
           END AS value_segment
    FROM customer_timeline
    ORDER BY total_spent DESC;
    """


def get_churn_analysis_query() -> str:
    """SQL for churn analysis and prediction with date filtering.

    Expects parameters: (start_date, end_date, active_months, risk_months)
    """
    return """
    WITH customer_activity AS (
        SELECT c.customer_id
             , c.first_name || ' ' || c.last_name AS customer_name
             , c.country
             , MAX(i.invoice_date) AS last_purchase_date
             , COUNT(i.invoice_id) AS total_orders
             , SUM(i.total) AS total_value
             , AVG(i.total) AS avg_order_value
             , EXTRACT(DAYS FROM (CURRENT_DATE - MAX(i.invoice_date))) 
               AS days_since_last_purchase
        FROM customer c
        LEFT JOIN invoice i ON c.customer_id = i.customer_id
                            AND i.invoice_date::date BETWEEN %s AND %s
        GROUP BY c.customer_id
               , c.first_name
               , c.last_name
               , c.country
    )
    SELECT *
         , CASE
               WHEN days_since_last_purchase IS NULL THEN 'Never Purchased'
               WHEN days_since_last_purchase <= %s * 30 THEN 'Active'
               WHEN days_since_last_purchase <= %s * 30 THEN 'At Risk'
               ELSE 'Churn Risk'
           END AS churn_status
         , CASE
               WHEN total_value >= 50 THEN 'High'
               WHEN total_value >= 25 THEN 'Medium'
               WHEN total_value > 0 THEN 'Low'
               ELSE 'Zero'
           END AS value_tier
    FROM customer_activity
    ORDER BY total_value DESC NULLS LAST;
    """


def get_geographic_analysis_query() -> str:
    """SQL for geographic customer distribution analysis."""
    return """
    SELECT c.country
         , c.state
         , c.city
         , COUNT(DISTINCT c.customer_id) AS customer_count
         , COUNT(DISTINCT i.invoice_id) AS total_orders
         , COALESCE(SUM(i.total), 0) AS total_revenue
         , COALESCE(AVG(i.total), 0) AS avg_order_value
         , COALESCE(SUM(i.total) / NULLIF(COUNT(DISTINCT c.customer_id), 0), 0) 
           AS revenue_per_customer
    FROM customer c
    LEFT JOIN invoice i ON c.customer_id = i.customer_id 
                        AND i.invoice_date::date BETWEEN %s AND %s
    GROUP BY c.country
           , c.state
           , c.city
    ORDER BY total_revenue DESC;
    """


def get_customer_preferences_query() -> str:
    """SQL for customer music preferences and behavior analysis."""
    return """
    WITH customer_genre_prefs AS (
        SELECT c.customer_id
             , c.first_name || ' ' || c.last_name AS customer_name
             , g.name AS preferred_genre
             , COUNT(il.invoice_line_id) AS tracks_purchased
             , SUM(il.unit_price * il.quantity) AS spent_on_genre
             , RANK() OVER (
                   PARTITION BY c.customer_id 
                   ORDER BY COUNT(il.invoice_line_id) DESC
               ) AS genre_rank
        FROM customer c
        JOIN invoice i ON c.customer_id = i.customer_id
        JOIN invoice_line il ON i.invoice_id = il.invoice_id
        JOIN track t ON il.track_id = t.track_id
        JOIN genre g ON t.genre_id = g.genre_id
        WHERE i.invoice_date::date BETWEEN %s AND %s
        GROUP BY c.customer_id
               , c.first_name
               , c.last_name
               , g.genre_id
               , g.name
    ),
    customer_totals AS (
        SELECT c.customer_id
             , COUNT(il.invoice_line_id) AS total_tracks
             , SUM(il.unit_price * il.quantity) AS total_spent
             , COUNT(DISTINCT g.genre_id) AS genres_explored
             , SUM(t.milliseconds) / 1000.0 / 60.0 AS total_minutes_purchased
        FROM customer c
        JOIN invoice i ON c.customer_id = i.customer_id
        JOIN invoice_line il ON i.invoice_id = il.invoice_id
        JOIN track t ON il.track_id = t.track_id
        JOIN genre g ON t.genre_id = g.genre_id
        WHERE i.invoice_date::date BETWEEN %s AND %s
        GROUP BY c.customer_id
    )
    SELECT cgp.customer_id
         , cgp.customer_name
         , cgp.preferred_genre
         , cgp.tracks_purchased AS tracks_in_preferred_genre
         , cgp.spent_on_genre
         , ct.total_tracks
         , ct.total_spent
         , ct.genres_explored
         , ct.total_minutes_purchased
         , ROUND((cgp.spent_on_genre / ct.total_spent * 100), 1) AS genre_preference_pct
    FROM customer_genre_prefs cgp
    JOIN customer_totals ct ON cgp.customer_id = ct.customer_id
    WHERE cgp.genre_rank = 1
    ORDER BY ct.total_spent DESC;
    """


def get_cohort_analysis_query() -> str:
    """SQL for cohort analysis based on first purchase month."""
    return """
    WITH customer_cohorts AS (
        SELECT c.customer_id
             , DATE_TRUNC('month', MIN(i.invoice_date)) AS cohort_month
             , MIN(i.invoice_date) AS first_purchase_date
        FROM customer c
        JOIN invoice i ON c.customer_id = i.customer_id
        GROUP BY c.customer_id
    ),
    customer_purchases AS (
        SELECT cc.customer_id
             , cc.cohort_month
             , DATE_TRUNC('month', i.invoice_date) AS purchase_month
             , SUM(i.total) AS monthly_revenue
        FROM customer_cohorts cc
        JOIN invoice i ON cc.customer_id = i.customer_id
        WHERE i.invoice_date::date BETWEEN %s AND %s
        GROUP BY cc.customer_id
               , cc.cohort_month
               , DATE_TRUNC('month', i.invoice_date)
    ),
    cohort_sizes AS (
        SELECT cohort_month
             , COUNT(DISTINCT customer_id) AS cohort_size
        FROM customer_cohorts
        GROUP BY cohort_month
    )
    SELECT cp.cohort_month
         , cp.purchase_month
         , EXTRACT(MONTH FROM AGE(cp.purchase_month, cp.cohort_month)) AS period_number
         , COUNT(DISTINCT cp.customer_id) AS customers
         , cs.cohort_size
         , ROUND(
               COUNT(DISTINCT cp.customer_id)::decimal / cs.cohort_size * 100, 
               2
           ) AS retention_rate
         , SUM(cp.monthly_revenue) AS cohort_revenue
    FROM customer_purchases cp
    JOIN cohort_sizes cs ON cp.cohort_month = cs.cohort_month
    GROUP BY cp.cohort_month
           , cp.purchase_month
           , cs.cohort_size
    ORDER BY cp.cohort_month
           , cp.purchase_month;
    """ 


def get_top_clients_query() -> str:
    """Compatibility: top clients analysis using two date params (start, end)."""
    return """
    WITH customer_totals AS (
        SELECT c.customer_id
             , COUNT(DISTINCT i.invoice_id) AS nb_orders
             , COUNT(il.invoice_line_id) AS nb_purchased_tracks
             , SUM(il.unit_price * il.quantity) AS total_spending
             , COUNT(DISTINCT g.genre_id) AS nb_different_genres
             , COUNT(DISTINCT ar.artist_id) AS nb_different_artists
             , COUNT(DISTINCT al.album_id) AS nb_different_albums
             , SUM(t.milliseconds) / 1000.0 / 60.0 AS total_minutes
             , MIN(i.invoice_date) AS first_order
             , MAX(i.invoice_date) AS last_order
             , ROUND(AVG(i.total), 2) AS avg_basket
        FROM customer c
        JOIN invoice i ON c.customer_id = i.customer_id
        JOIN invoice_line il ON i.invoice_id = il.invoice_id
        JOIN track t ON il.track_id = t.track_id
        JOIN album al ON t.album_id = al.album_id
        JOIN artist ar ON al.artist_id = ar.artist_id
        JOIN genre g ON t.genre_id = g.genre_id
        WHERE i.invoice_date::date BETWEEN %s AND %s
        GROUP BY c.customer_id
    )
    SELECT c.customer_id
         , c.first_name || ' ' || c.last_name AS client
         , c.country
         , ct.nb_orders
         , ct.nb_purchased_tracks
         , ct.total_minutes
         , ct.nb_different_genres
         , ct.nb_different_artists
         , ct.nb_different_albums
         , ct.total_spending
         , ct.avg_basket
         , ct.first_order
         , ct.last_order
    FROM customer c
    JOIN customer_totals ct ON ct.customer_id = c.customer_id
    ORDER BY ct.total_spending DESC;
    """ 