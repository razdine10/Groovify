"""
Visualization functions for customer analysis module
"""

import plotly.express as px
import plotly.graph_objects as go

from .constants import (
    AMATEUR_MINUTES,
    CHURN_COLORS,
    DEFAULT_CHART_HEIGHT,
    DIVERSIFIED_GENRES,
    DIVERSIFIED_TRACKS,
    ECLECTIC_GENRES,
    ECLECTIC_TRACKS,
    EXPLORER_GENRES,
    EXPLORER_TRACKS,
    HOVER_BG_COLOR,
    HOVER_BORDER_COLOR,
    HOVER_FONT_SIZE,
    MUSIC_LOVER_MINUTES,
    OCCASIONAL_MINUTES,
    OCCASIONAL_TRACKS,
    SELECTIVE_GENRES,
    SELECTIVE_TRACKS,
    SPECIALIZED_GENRES,
    SPECIALIZED_TRACKS,
)


def _get_musical_profile(genres, tracks):
    """Determine musical profile based on genres and tracks count."""
    if genres >= ECLECTIC_GENRES and tracks >= ECLECTIC_TRACKS:
        return "Eclectic"
    if genres >= DIVERSIFIED_GENRES and tracks >= DIVERSIFIED_TRACKS:
        return "Diversified"
    if genres >= SELECTIVE_GENRES and tracks >= SELECTIVE_TRACKS:
        return "Selective"
    if genres <= SPECIALIZED_GENRES and tracks >= SPECIALIZED_TRACKS:
        return "Specialized"
    if tracks < OCCASIONAL_TRACKS:
        return "Occasional"
    if genres >= EXPLORER_GENRES and tracks < EXPLORER_TRACKS:
        return "Explorer"
    return "Regular"


def _get_listening_profile(minutes):
    """Determine listening profile based on total minutes."""
    if minutes >= MUSIC_LOVER_MINUTES:
        return "Music Lover"
    if minutes >= AMATEUR_MINUTES:
        return "Amateur"
    if minutes >= OCCASIONAL_MINUTES:
        return "Occasional"
    return "Beginner"


def create_cluster_pie_chart(rfm_df):
    """Create pie chart for RFM clusters distribution."""
    cluster_counts = rfm_df["rfm_cluster"].value_counts()
    fig = px.pie(
        values=cluster_counts.values,
        names=cluster_counts.index,
        title="🎯 RFM Clusters Distribution",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{label}</b><br>Customers: <b>%{value:,}</b>"
            "<br>Share: %{percent}<extra></extra>"
        )
    )
    fig.update_layout(
        hoverlabel=dict(
            bgcolor=HOVER_BG_COLOR, bordercolor=HOVER_BORDER_COLOR,
            font_size=HOVER_FONT_SIZE,
        )
    )
    return fig


def create_musical_profile_chart(rfm_df):
    """Create pie chart for musical profiles distribution."""
    rfm_df["musical_profile"] = rfm_df.apply(
        lambda row: _get_musical_profile(
            row["nb_different_genres"], row["nb_purchased_tracks"]
        ),
        axis=1,
    )
    profile_counts = rfm_df["musical_profile"].value_counts()
    fig = px.pie(
        values=profile_counts.values,
        names=profile_counts.index,
        title="🎵 Musical Profiles",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{label}</b><br>Customers: <b>%{value:,}</b>"
            "<br>Share: %{percent}<extra></extra>"
        )
    )
    fig.update_layout(
        hoverlabel=dict(
            bgcolor=HOVER_BG_COLOR, bordercolor=HOVER_BORDER_COLOR,
            font_size=HOVER_FONT_SIZE,
        )
    )
    return fig


def create_cluster_heatmap(rfm_df):
    """Create heatmap of normalized cluster characteristics."""
    cluster_means = rfm_df.groupby("rfm_cluster")[
        ["recency_days", "frequency", "monetary", "nb_different_genres"]
    ].mean()
    cluster_normalized = (cluster_means - cluster_means.min()) / (
        cluster_means.max() - cluster_means.min()
    )
    fig = px.imshow(
        cluster_normalized.T,
        text_auto=".2f",
        title="🔥 Normalized Profile by Cluster",
        color_continuous_scale="RdYlBu_r",
        aspect="auto",
    )
    fig.update_traces(
        hovertemplate=(
            "Metric: <b>%{y}</b><br>Cluster: <b>%{x}</b>"
            "<br>Score: <b>%{z:.2f}</b><extra></extra>"
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


def create_scatter_plot(rfm_df):
    """Create scatter plot for value vs frequency analysis."""
    fig = px.scatter(
        rfm_df,
        x="frequency",
        y="monetary",
        size="nb_purchased_tracks",
        color="rfm_cluster",
        title="💎 Value vs Frequency (Size = Nb Tracks)",
        labels={
            "frequency": "Purchase Frequency",
            "monetary": "Total Value ($)",
        },
    )
    fig.update_traces(
        hovertemplate=(
            "Frequency: <b>%{x:,}</b><br>Value: <b>$%{y:,.2f}</b>"
            "<br>Tracks: %{marker.size:,}<extra></extra>"
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


def create_churn_pie_chart(churn_df):
    """Create pie chart for churn status distribution."""
    fig = px.pie(
        churn_df,
        names="churn_status",
        title="Churn Distribution",
        color_discrete_map=CHURN_COLORS,
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{label}</b><br>Customers: <b>%{value:,}</b>"
            "<br>Share: %{percent}<extra></extra>"
        )
    )
    fig.update_layout(
        hoverlabel=dict(
            bgcolor=HOVER_BG_COLOR, bordercolor=HOVER_BORDER_COLOR,
            font_size=HOVER_FONT_SIZE,
        )
    )
    return fig


def create_churn_histogram(churn_df):
    """Create histogram of days since last order."""
    fig = px.histogram(
        churn_df,
        x="days_since_last",
        nbins=20,
        title="Distribution - Days Since Last Order",
        color="churn_status",
        color_discrete_map=CHURN_COLORS,
    )
    fig.update_traces(
        hovertemplate=(
            "Days: <b>%{x}</b><br>Customers: <b>%{y:,}</b><extra></extra>"
        )
    )
    fig.update_layout(
        hoverlabel=dict(
            bgcolor=HOVER_BG_COLOR, bordercolor=HOVER_BORDER_COLOR,
            font_size=HOVER_FONT_SIZE,
        )
    )
    fig.update_xaxes(title_text="Days since last order")
    fig.update_yaxes(title_text="Number of customers")
    return fig


def create_listening_profile_chart(sorted_df):
    """Create pie chart for listening profiles distribution."""
    profile_counts = sorted_df["listening_profile"].value_counts()
    fig = px.pie(
        values=profile_counts.values,
        names=profile_counts.index,
        title="🎧 Distribution of Listening Profiles",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{label}</b><br>Customers: <b>%{value:,}</b>"
            "<br>Share: %{percent}<extra></extra>"
        )
    )
    fig.update_layout(
        hoverlabel=dict(
            bgcolor=HOVER_BG_COLOR, bordercolor=HOVER_BORDER_COLOR,
            font_size=HOVER_FONT_SIZE,
        )
    )
    return fig


def create_diversity_scatter(sorted_df):
    """Create scatter plot for musical diversity analysis."""
    fig = px.scatter(
        sorted_df,
        x="nb_different_genres",
        y="nb_different_artists",
        size="total_spending",
        color="nb_different_albums",
        title="🎨 Diversity: Genres vs Artists (Size = Spending)",
        labels={
            "nb_different_genres": "Different Genres",
            "nb_different_artists": "Different Artists",
        },
    )
    fig.update_traces(
        hovertemplate=(
            "Genres: <b>%{x}</b><br>Artists: <b>%{y}</b>"
            "<br>Spending: $%{marker.size:,.2f}<br>Albums: %{marker.color}"
            "<extra></extra>"
        )
    )
    fig.update_layout(
        hoverlabel=dict(
            bgcolor=HOVER_BG_COLOR, bordercolor=HOVER_BORDER_COLOR,
            font_size=HOVER_FONT_SIZE,
        )
    )
    return fig


def create_engagement_timeline(sorted_df):
    """Create scatter plot for customer engagement analysis."""
    fig = px.scatter(
        sorted_df,
        x="activity_days",
        y="order_frequency",
        size="total_spending",
        color="nb_orders",
        title="📈 Engagement: Duration vs Frequency (Size = Spending)",
        labels={
            "activity_days": "Activity Days",
            "order_frequency": "Orders/month",
        },
    )
    fig.update_traces(
        hovertemplate=(
            "Activity: <b>%{x}</b> days<br>Frequency: <b>%{y:.2f}</b> "
            "orders/month<br>Spending: $%{marker.size:,.2f}"
            "<br>Orders: %{marker.color}<extra></extra>"
        )
    )
    fig.update_layout(
        hoverlabel=dict(
            bgcolor=HOVER_BG_COLOR, bordercolor=HOVER_BORDER_COLOR,
            font_size=HOVER_FONT_SIZE,
        )
    )
    return fig 