"""
Visualization functions for music analysis module
"""

import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from .constants import (
    DEFAULT_CHART_HEIGHT,
    DURATION_OUTLIER_PERCENTILE,
    HOVER_BG_COLOR,
    HOVER_BORDER_COLOR,
    HOVER_FONT_SIZE,
    SCALE_BLUES,
    SCALE_GREENS,
    SCALE_ORANGES,
    SCALE_PLASMA,
    SCALE_VIRIDIS,
    TOP_TRACKS_DISPLAY,
)


def create_genre_pie_chart(track_df):
    """Create pie chart for genre distribution by sales."""
    genre_data = track_df.groupby("genre")["times_purchased"].sum().reset_index()
    fig = px.pie(
        genre_data,
        values="times_purchased",
        names="genre",
        title="🎭 Genre Distribution by Sales",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{label}</b><br>Sales: <b>%{value:,}</b>"
            "<br>Share: %{percent}<extra></extra>"
        )
    )
    fig.update_layout(
        height=DEFAULT_CHART_HEIGHT,
        hoverlabel=dict(
            bgcolor=HOVER_BG_COLOR, bordercolor=HOVER_BORDER_COLOR,
            font_size=HOVER_FONT_SIZE,
        ),
    )
    return fig


def create_track_performance_chart(track_df):
    """Create bar chart for top track performance."""
    fig = px.bar(
        track_df,
        x="times_purchased",
        y="track_name",
        color="total_revenue",
        title="🎵 Top Track Performance",
        labels={"times_purchased": "Sales Count", "track_name": "Track"},
        color_continuous_scale=SCALE_VIRIDIS,
        orientation="h",
        custom_data=["total_revenue"],
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>Sales: <b>%{x:,}</b>"
            "<br>Revenue: <b>$%{customdata[0]:,.2f}</b><extra></extra>"
        )
    )
    fig.update_layout(
        height=DEFAULT_CHART_HEIGHT,
        yaxis={"categoryorder": "total ascending"},
        hoverlabel=dict(
            bgcolor=HOVER_BG_COLOR, bordercolor=HOVER_BORDER_COLOR,
            font_size=HOVER_FONT_SIZE,
        ),
    )
    return fig


def create_artist_bar_chart(artist_df, metric, title):
    """Create bar chart for artist performance."""
    fig = px.bar(
        artist_df,
        x=metric,
        y="artist_name",
        title=f"👨‍🎤 {title}",
        labels={
            metric: metric.replace("_", " ").title(),
            "artist_name": "Artist",
        },
        color=metric,
        color_continuous_scale=SCALE_BLUES,
        orientation="h",
    )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Value: <b>%{x:,}</b><extra></extra>"
    )
    fig.update_layout(
        height=DEFAULT_CHART_HEIGHT,
        yaxis={"categoryorder": "total ascending"},
        hoverlabel=dict(
            bgcolor=HOVER_BG_COLOR, bordercolor=HOVER_BORDER_COLOR,
            font_size=HOVER_FONT_SIZE,
        ),
    )
    return fig


def create_revenue_trend_chart(revenue_df, granularity):
    """Create bar chart for revenue trends by genre."""
    fig = px.bar(
        revenue_df,
        x="genre",
        y="total_revenue",
        title=f"💰 Revenue Trends by Genre ({granularity})",
        labels={"total_revenue": "Revenue ($)", "genre": "Genre"},
        color="total_revenue",
        color_continuous_scale=SCALE_GREENS,
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>Revenue: <b>$%{y:,.2f}</b><extra></extra>"
        )
    )
    fig.update_layout(
        hovermode="x unified",
        height=DEFAULT_CHART_HEIGHT,
        xaxis_tickangle=-45,
        hoverlabel=dict(
            bgcolor=HOVER_BG_COLOR, bordercolor=HOVER_BORDER_COLOR,
            font_size=HOVER_FONT_SIZE,
        ),
    )
    return fig


def create_playlist_heatmap(playlist_df):
    """Create scatter plot for playlist composition analysis."""
    fig = px.scatter(
        playlist_df,
        x="track_count",
        y="total_duration_hours",
        size="genre_diversity",
        color="artist_diversity",
        title="📋 Playlist Composition Analysis",
        labels={
            "track_count": "Number of Tracks",
            "total_duration_hours": "Duration (Hours)",
            "genre_diversity": "Genre Diversity",
            "artist_diversity": "Artist Diversity",
        },
        color_continuous_scale=SCALE_PLASMA,
    )
    fig.update_traces(
        hovertemplate=(
            "Tracks: <b>%{x:,}</b><br>Duration: <b>%{y:.1f} h</b>"
            "<br>Genre div.: %{marker.size}<br>Artist div.: %{marker.color}"
            "<extra></extra>"
        )
    )
    fig.update_layout(
        height=DEFAULT_CHART_HEIGHT,
        hoverlabel=dict(
            bgcolor=HOVER_BG_COLOR, bordercolor=HOVER_BORDER_COLOR,
            font_size=HOVER_FONT_SIZE,
        ),
    )
    return fig


def create_discovery_funnel(discovery_df):
    """Create bar chart for content discovery performance."""
    fig = px.bar(
        discovery_df.head(TOP_TRACKS_DISPLAY),
        x="playlist_appearances",
        y="track_name",
        color="total_sales",
        title="🔍 Track Discovery Performance",
        labels={
            "playlist_appearances": "Playlist Appearances",
            "track_name": "Track",
        },
        color_continuous_scale=SCALE_ORANGES,
        orientation="h",
        custom_data=["total_sales"],
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>Appearances: <b>%{x:,}</b>"
            "<br>Total sales: <b>%{customdata[0]:,}</b><extra></extra>"
        )
    )
    fig.update_layout(
        height=DEFAULT_CHART_HEIGHT,
        yaxis={"categoryorder": "total ascending"},
        hoverlabel=dict(
            bgcolor=HOVER_BG_COLOR, bordercolor=HOVER_BORDER_COLOR,
            font_size=HOVER_FONT_SIZE,
        ),
    )
    return fig


def create_duration_distribution(album_df):
    """Create scatter plot for duration vs track count analysis."""
    df = album_df.copy()
    if (
        df.empty
        or "total_duration_minutes" not in df.columns
        or "track_count" not in df.columns
    ):
        return px.scatter(title="💿 Duration vs Track Count")

    p95_dur = df["total_duration_minutes"].quantile(DURATION_OUTLIER_PERCENTILE)
    filtered_df = df[df["total_duration_minutes"] <= p95_dur]

    fig = px.scatter(
        filtered_df,
        x="track_count",
        y="total_duration_minutes",
        size="album_revenue",
        color="album_revenue",
        title="💿 Album Duration vs Track Count",
        labels={
            "track_count": "Number of Tracks",
            "total_duration_minutes": "Total Duration (minutes)",
            "album_revenue": "Revenue ($)",
        },
        color_continuous_scale=SCALE_VIRIDIS,
    )
    fig.update_traces(
        hovertemplate=(
            "Tracks: <b>%{x}</b><br>Duration: <b>%{y:.1f} min</b>"
            "<br>Revenue: <b>$%{marker.color:,.2f}</b><extra></extra>"
        )
    )
    fig.update_layout(
        height=DEFAULT_CHART_HEIGHT,
        hoverlabel=dict(
            bgcolor=HOVER_BG_COLOR, bordercolor=HOVER_BORDER_COLOR,
            font_size=HOVER_FONT_SIZE,
        ),
    )
    return fig


def create_pricing_analysis(track_df):
    """Create histogram for track pricing distribution."""
    if track_df.empty or "avg_price" not in track_df.columns:
        return px.histogram(title="💵 Track Pricing Distribution")

    fig = px.histogram(
        track_df,
        x="avg_price",
        nbins=20,
        title="💵 Track Pricing Distribution",
        labels={"avg_price": "Average Price ($)", "count": "Number of Tracks"},
        color_discrete_sequence=[SCALE_BLUES],
    )
    fig.update_traces(
        hovertemplate=(
            "Price: <b>$%{x:.2f}</b><br>Tracks: <b>%{y:,}</b><extra></extra>"
        )
    )
    fig.update_layout(
        height=DEFAULT_CHART_HEIGHT,
        hoverlabel=dict(
            bgcolor=HOVER_BG_COLOR, bordercolor=HOVER_BORDER_COLOR,
            font_size=HOVER_FONT_SIZE,
        ),
    )
    return fig


def create_trend_line_chart(trend_df):
    """Create line chart for sales trends over time."""
    if trend_df.empty:
        return px.line(title="📈 Sales Trends Over Time")

    aggregated_df = (
        trend_df.groupby("sale_date")["revenue"].sum().reset_index()
    )

    fig = px.line(
        aggregated_df,
        x="sale_date",
        y="revenue",
        title="📈 Daily Revenue Trends",
        labels={"sale_date": "Date", "revenue": "Revenue ($)"},
        markers=True,
    )
    fig.update_traces(
        line=dict(color=SCALE_BLUES, width=3),
        hovertemplate=(
            "Date: <b>%{x}</b><br>Revenue: <b>$%{y:,.2f}</b><extra></extra>"
        ),
    )
    fig.update_layout(
        height=DEFAULT_CHART_HEIGHT,
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor=HOVER_BG_COLOR, bordercolor=HOVER_BORDER_COLOR,
            font_size=HOVER_FONT_SIZE,
        ),
    )
    return fig


def create_genre_trend_chart(trend_df, selected_genres=None):
    """Create multi-line chart for genre trends over time."""
    if trend_df.empty:
        return px.line(title="📈 Genre Trends Over Time")

    if selected_genres:
        trend_df = trend_df[trend_df["genre"].isin(selected_genres)]

    fig = px.line(
        trend_df,
        x="sale_date",
        y="revenue",
        color="genre",
        title="📈 Revenue Trends by Genre",
        labels={"sale_date": "Date", "revenue": "Revenue ($)"},
        markers=True,
    )
    fig.update_traces(
        hovertemplate=(
            "Date: <b>%{x}</b><br>Genre: <b>%{fullData.name}</b>"
            "<br>Revenue: <b>$%{y:,.2f}</b><extra></extra>"
        )
    )
    fig.update_layout(
        height=DEFAULT_CHART_HEIGHT,
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor=HOVER_BG_COLOR, bordercolor=HOVER_BORDER_COLOR,
            font_size=HOVER_FONT_SIZE,
        ),
    )
    return fig


def create_artist_summary_chart(artist_df):
    """Create bubble chart for artist performance summary."""
    if artist_df.empty:
        return px.scatter(title="👨‍🎤 Artist Performance Summary")

    fig = px.scatter(
        artist_df,
        x="album_count",
        y="total_revenue",
        size="total_tracks_sold",
        color="avg_track_duration",
        title="👨‍🎤 Artist Performance Matrix",
        labels={
            "album_count": "Number of Albums",
            "total_revenue": "Total Revenue ($)",
            "total_tracks_sold": "Tracks Sold",
            "avg_track_duration": "Avg Track Duration (min)",
        },
        color_continuous_scale=SCALE_PLASMA,
    )
    fig.update_traces(
        hovertemplate=(
            "Albums: <b>%{x}</b><br>Revenue: <b>$%{y:,.2f}</b>"
            "<br>Tracks sold: %{marker.size:,}<br>Avg duration: %{marker.color:.1f} min"
            "<extra></extra>"
        )
    )
    fig.update_layout(
        height=DEFAULT_CHART_HEIGHT,
        hoverlabel=dict(
            bgcolor=HOVER_BG_COLOR, bordercolor=HOVER_BORDER_COLOR,
            font_size=HOVER_FONT_SIZE,
        ),
    )
    return fig 