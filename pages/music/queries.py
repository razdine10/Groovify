"""SQL queries for the music module.

This module contains all SQL queries used in the music analytics.
Each query is defined as a string constant and accessed through
dedicated functions.
"""

from src.queries.common import get_date_bounds_query


def get_track_performance_query() -> str:
    """SQL for track performance with sales and revenue data."""
    return """
    SELECT t.name AS track_name
         , ar.name AS artist_name
         , al.title AS album_title
         , g.name AS genre
         , COUNT(il.invoice_line_id) AS times_purchased
         , ROUND(SUM(il.unit_price * il.quantity), 2) AS total_revenue
         , ROUND(AVG(il.unit_price), 2) AS avg_price
         , ROUND(t.milliseconds/1000.0/60.0, 2) AS duration_minutes
    FROM track t
    JOIN album al ON t.album_id = al.album_id
    JOIN artist ar ON al.artist_id = ar.artist_id
    JOIN genre g ON t.genre_id = g.genre_id
    JOIN invoice_line il ON t.track_id = il.track_id
    JOIN invoice i ON il.invoice_id = i.invoice_id
    WHERE i.invoice_date::date BETWEEN %s AND %s
    GROUP BY t.track_id
           , t.name
           , ar.name
           , al.title
           , g.name
           , t.milliseconds
    HAVING COUNT(il.invoice_line_id) >= %s
    ORDER BY times_purchased DESC
    LIMIT %s;
    """


def get_genre_analysis_query() -> str:
    """SQL for genre popularity and performance metrics."""
    return """
    SELECT g.name AS genre
         , COUNT(il.invoice_line_id) AS tracks_sold
         , ROUND(SUM(il.unit_price * il.quantity), 2) AS revenue
         , ROUND(AVG(il.unit_price), 2) AS avg_price
         , COUNT(DISTINCT t.track_id) AS unique_tracks
         , COUNT(DISTINCT ar.artist_id) AS unique_artists
    FROM genre g
    JOIN track t ON g.genre_id = t.genre_id
    JOIN invoice_line il ON t.track_id = il.track_id
    JOIN invoice i ON il.invoice_id = i.invoice_id
    JOIN album al ON t.album_id = al.album_id
    JOIN artist ar ON al.artist_id = ar.artist_id
    WHERE i.invoice_date::date BETWEEN %s AND %s
    GROUP BY g.genre_id
           , g.name
    ORDER BY tracks_sold DESC;
    """


def get_artist_insights_query() -> str:
    """SQL for comprehensive artist performance data."""
    return """
    SELECT ar.name AS artist_name
         , COUNT(DISTINCT al.album_id) AS album_count
         , COUNT(DISTINCT t.track_id) AS track_count
         , COUNT(il.invoice_line_id) AS total_tracks_sold
         , ROUND(SUM(il.unit_price * il.quantity), 2) AS total_revenue
         , ROUND(AVG(il.unit_price), 2) AS avg_price
         , ROUND(AVG(t.milliseconds)/1000.0/60.0, 2) AS avg_track_duration
    FROM artist ar
    JOIN album al ON ar.artist_id = al.artist_id
    JOIN track t ON al.album_id = t.album_id
    JOIN invoice_line il ON t.track_id = il.track_id
    JOIN invoice i ON il.invoice_id = i.invoice_id
    WHERE i.invoice_date::date BETWEEN %s AND %s
    GROUP BY ar.artist_id
           , ar.name
    HAVING COUNT(DISTINCT al.album_id) >= %s
    ORDER BY total_revenue DESC
    LIMIT %s;
    """


def get_album_analytics_query() -> str:
    """SQL for album performance with track count and sales data."""
    return """
    SELECT al.title AS album_title
         , ar.name AS artist_name
         , COUNT(DISTINCT t.track_id) AS track_count
         , COUNT(il.invoice_line_id) AS total_sales
         , ROUND(SUM(il.unit_price * il.quantity), 2) AS album_revenue
         , ROUND(AVG(il.unit_price), 2) AS avg_track_price
         , ROUND(AVG(t.milliseconds)/1000.0/60.0, 2) AS avg_track_duration
         , ROUND(SUM(t.milliseconds)/1000.0/60.0, 2) AS total_duration_minutes
    FROM album al
    JOIN artist ar ON al.artist_id = ar.artist_id
    JOIN track t ON al.album_id = t.album_id
    JOIN invoice_line il ON t.track_id = il.track_id
    JOIN invoice i ON il.invoice_id = i.invoice_id
    WHERE i.invoice_date::date BETWEEN %s AND %s
    GROUP BY al.album_id
           , al.title
           , ar.name
    ORDER BY album_revenue DESC;
    """


def get_playlist_performance_query() -> str:
    """SQL for playlist composition and performance metrics."""
    return """
    WITH playlist_stats AS (
        SELECT p.playlist_id
             , p.name AS playlist_name
             , COUNT(pt.track_id) AS track_count
             , ROUND(AVG(t.milliseconds)/1000.0/60.0, 2) AS avg_track_duration
             , ROUND(SUM(t.milliseconds)/1000.0/60.0/60.0, 2) AS total_duration_hours
             , COUNT(DISTINCT g.genre_id) AS genre_diversity
             , COUNT(DISTINCT ar.artist_id) AS artist_diversity
        FROM playlist p
        JOIN playlist_track pt ON p.playlist_id = pt.playlist_id
        JOIN track t ON pt.track_id = t.track_id
        JOIN album al ON t.album_id = al.album_id
        JOIN artist ar ON al.artist_id = ar.artist_id
        JOIN genre g ON t.genre_id = g.genre_id
        GROUP BY p.playlist_id
               , p.name
    ), 
    dedup AS (
        SELECT *
             , ROW_NUMBER() OVER (
                   PARTITION BY playlist_name 
                   ORDER BY playlist_id
               ) AS rn
        FROM playlist_stats
    )
    SELECT playlist_name
         , track_count
         , avg_track_duration
         , total_duration_hours
         , genre_diversity
         , artist_diversity
    FROM dedup
    WHERE rn = 1
    ORDER BY track_count DESC;
    """


def get_content_discovery_query() -> str:
    """SQL for track popularity across playlists and sales correlation."""
    return """
    SELECT t.name AS track_name
         , ar.name AS artist_name
         , COUNT(DISTINCT pt.playlist_id) AS playlist_appearances
         , COALESCE(sales.total_sales, 0) AS total_sales
    FROM track t
    JOIN album al ON t.album_id = al.album_id
    JOIN artist ar ON al.artist_id = ar.artist_id
    JOIN playlist_track pt ON t.track_id = pt.track_id
    LEFT JOIN (
        SELECT il.track_id
             , COUNT(il.invoice_line_id) AS total_sales
        FROM invoice_line il
        GROUP BY il.track_id
    ) sales ON t.track_id = sales.track_id
    GROUP BY t.track_id
           , t.name
           , ar.name
           , sales.total_sales
    HAVING COUNT(DISTINCT pt.playlist_id) > %s
    ORDER BY playlist_appearances DESC
           , total_sales DESC
    LIMIT %s;
    """


def get_revenue_analysis_query() -> str:
    """SQL for detailed revenue analysis by various dimensions."""
    return """
    SELECT g.name AS genre
         , COUNT(il.invoice_line_id) AS units_sold
         , ROUND(SUM(il.unit_price * il.quantity), 2) AS total_revenue
         , ROUND(AVG(il.unit_price), 2) AS avg_price
         , COUNT(DISTINCT t.track_id) AS unique_tracks
         , COUNT(DISTINCT ar.artist_id) AS unique_artists
         , ROUND(AVG(t.milliseconds)/1000.0/60.0, 2) AS avg_duration
    FROM invoice_line il
    JOIN invoice i ON il.invoice_id = i.invoice_id
    JOIN track t ON il.track_id = t.track_id
    JOIN album al ON t.album_id = al.album_id
    JOIN artist ar ON al.artist_id = ar.artist_id
    JOIN genre g ON t.genre_id = g.genre_id
    WHERE i.invoice_date::date BETWEEN %s AND %s
    GROUP BY g.genre_id
           , g.name
    ORDER BY total_revenue DESC;
    """


def get_trend_analysis_query() -> str:
    """SQL for sales trends over time for trend analysis."""
    return """
    SELECT i.invoice_date::date AS sale_date
         , g.name AS genre
         , COUNT(il.invoice_line_id) AS quantity_sold
         , ROUND(SUM(il.unit_price * il.quantity), 2) AS revenue
         , COUNT(DISTINCT t.track_id) AS unique_tracks_sold
    FROM invoice i
    JOIN invoice_line il ON i.invoice_id = il.invoice_id
    JOIN track t ON il.track_id = t.track_id
    JOIN genre g ON t.genre_id = g.genre_id
    WHERE i.invoice_date::date BETWEEN %s AND %s
    GROUP BY i.invoice_date::date
           , g.genre_id
           , g.name
    ORDER BY sale_date
           , genre;
    """ 