import pandas as pd
import streamlit as st
from datetime import date
from pathlib import Path

import streamlit as st
import pandas as pd
from datetime import date
from pathlib import Path

from utils import apply_sidebar_logo, run_query
from pages.music.queries import (
    get_album_analytics_query,
    get_artist_insights_query,
    get_content_discovery_query,
    get_date_bounds_query,
    get_genre_analysis_query,
    get_playlist_performance_query,
    get_revenue_analysis_query,
    get_track_performance_query,
    get_trend_analysis_query,
)
from pages.music.visualization import (
    create_artist_bar_chart,
    create_artist_summary_chart,
    create_discovery_funnel,
    create_duration_distribution,
    create_genre_pie_chart,
    create_genre_trend_chart,
    create_playlist_heatmap,
    create_pricing_analysis,
    create_revenue_trend_chart,
    create_track_performance_chart,
    create_trend_line_chart,
)
from pages.music.constants import (
    ARTIST_LIMIT,
    AVAILABLE_GENRES,
    MIN_ARTIST_ALBUMS,
    MIN_PLAYLIST_APPEARANCES,
    MIN_TRACK_SALES,
    MUSIC_CATEGORIES,
    PLAYLIST_DISCOVERY_LIMIT,
    TOP_ARTISTS_DISPLAY,
    TOP_PLAYLISTS_DISPLAY,
    TRACK_LIMIT,
)

st.set_page_config(
    page_title="Music Analytics", page_icon="🎵", layout="wide"
)
apply_sidebar_logo()

# Apply custom CSS
try:
    css_path = Path(__file__).parent / "style.css"
    if css_path.exists():
        st.markdown(
            f"<style>{css_path.read_text()}</style>",
            unsafe_allow_html=True,
        )
except Exception:
    pass

# Header
st.markdown(
    """
<div class="finance-header">
  <h1 class="header-title">🎵 Music Analytics</h1>
  <p class="header-subtitle">Tracks • Albums • Artists • Playlists • Revenue</p>
</div>
""",
    unsafe_allow_html=True,
)

# Get default date range
min_max = run_query(get_date_bounds_query())
min_d = (
    pd.to_datetime(min_max.iloc[0]["min_d"]).date() if not min_max.empty
    else date(2000, 1, 1)
)
max_d = (
    pd.to_datetime(min_max.iloc[0]["max_d"]).date() if not min_max.empty
    else date.today()
)

# Analysis selector
try:
    analysis_choice = st.segmented_control(
        "",
        options=MUSIC_CATEGORIES,
        selection_mode="single",
        default="🎵 Tracks & Albums",
        key="music_view_seg",
    )
except Exception:
    analysis_choice = st.radio(
        "",
        MUSIC_CATEGORIES,
        horizontal=True,
        key="music_view_radio",
    )


def _create_data_table(df, columns_mapping, title):
    """Create a formatted data table with ranking column."""
    display_df = df[list(columns_mapping.keys())].copy()
    display_df = display_df.rename(columns=columns_mapping)
    display_df.insert(0, "#", range(1, len(display_df) + 1))
    st.markdown(f"#### {title}")
    st.dataframe(display_df, use_container_width=True, hide_index=True)


# ========================================
# TRACKS & ALBUMS
# ========================================
if analysis_choice == "🎵 Tracks & Albums":
    st.markdown("### 🎵 Track & Album Performance")

    with st.sidebar:
        st.markdown("### 📅 Analysis filters")
        date_range = st.date_input(
            "Sales period",
            value=(min_d, max_d),
            min_value=min_d,
            max_value=max_d,
            key="tracks_dates",
        )
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_d, end_d = date_range
        else:
            start_d, end_d = min_d, max_d

        show_genre = st.multiselect(
            "Filter by genre",
            options=AVAILABLE_GENRES,
            key="genre_filter",
        )

    try:
        track_df = run_query(
            get_track_performance_query(),
            (start_d, end_d, MIN_TRACK_SALES, TRACK_LIMIT),
        )

        if not track_df.empty:
            if show_genre:
                track_df = track_df[track_df["genre"].isin(show_genre)]

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(
                    "Total tracks sold",
                    f"{track_df['times_purchased'].sum():,}",
                )
            with col2:
                st.metric(
                    "Total revenue",
                    f"${track_df['total_revenue'].sum():,.2f}",
                )
            with col3:
                st.metric(
                    "Avg track price",
                    f"${track_df['avg_price'].mean():.2f}",
                )
            with col4:
                st.metric(
                    "Max sales per track",
                    f"{track_df['times_purchased'].max():,}",
                )

            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:
                sorted_df = track_df.sort_values(
                    "times_purchased", ascending=False
                )
                _create_data_table(
                    sorted_df,
                    {
                        "track_name": "Track",
                        "artist_name": "Artist",
                        "album_title": "Album",
                        "genre": "Genre",
                        "times_purchased": "Sales",
                        "total_revenue": "Revenue ($)",
                        "avg_price": "Avg price",
                        "duration_minutes": "Duration (min)",
                    },
                    "📋 Tracks table",
                )

            with col2:
                fig = create_genre_pie_chart(track_df)
                st.plotly_chart(fig, use_container_width=True)

            album_df = run_query(get_album_analytics_query(), (start_d, end_d))
            if not album_df.empty:
                st.markdown("#### 💿 Top Album Performance")

                col1, col2 = st.columns([2, 1])

                with col1:
                    _create_data_table(
                        album_df.head(TOP_PLAYLISTS_DISPLAY),
                        {
                            "album_title": "Album",
                            "artist_name": "Artist",
                            "track_count": "Tracks",
                            "total_sales": "Sales",
                            "album_revenue": "Revenue ($)",
                        },
                        "Top Albums",
                    )

                with col2:
                    fig = create_duration_distribution(album_df)
                    st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("No track data available for the selected period.")

    except Exception as e:  # noqa: BLE001
        st.error(f"Error loading track data: {e}")

# ========================================
# ARTISTS
# ========================================
elif analysis_choice == "👨‍🎤 Artists":
    st.markdown("### 👨‍🎤 Artist Performance")

    with st.sidebar:
        st.markdown("### 📅 Analysis filters")
        date_range = st.date_input(
            "Sales period",
            value=(min_d, max_d),
            min_value=min_d,
            max_value=max_d,
            key="artist_dates",
        )
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_d, end_d = date_range
        else:
            start_d, end_d = min_d, max_d

        metric_choice = st.selectbox(
            "Performance metric",
            ["total_revenue", "total_tracks_sold", "album_count"],
            format_func=lambda x: x.replace("_", " ").title(),
        )

    try:
        artist_df = run_query(
            get_artist_insights_query(),
            (start_d, end_d, MIN_ARTIST_ALBUMS, ARTIST_LIMIT),
        )

        if not artist_df.empty:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total artists", len(artist_df))
            with col2:
                st.metric(
                    "Total revenue",
                    f"${artist_df['total_revenue'].sum():,.2f}",
                )
            with col3:
                st.metric(
                    "Avg tracks per artist",
                    f"{artist_df['track_count'].mean():.1f}",
                )

            col1, col2 = st.columns(2)

            with col1:
                fig = create_artist_bar_chart(
                    artist_df.head(TOP_ARTISTS_DISPLAY),
                    metric_choice,
                    f"Top Artists by {metric_choice.replace('_', ' ').title()}",
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = create_artist_summary_chart(artist_df)
                st.plotly_chart(fig, use_container_width=True)

            _create_data_table(
                artist_df,
                {
                    "artist_name": "Artist",
                    "album_count": "Albums",
                    "track_count": "Tracks",
                    "total_tracks_sold": "Total Sales",
                    "total_revenue": "Revenue ($)",
                    "avg_price": "Avg Price ($)",
                    "avg_track_duration": "Avg Duration (min)",
                },
                "📋 Artist Details",
            )

        else:
            st.warning("No artist data available for the selected period.")

    except Exception as e:  # noqa: BLE001
        st.error(f"Error loading artist data: {e}")

# ========================================
# PLAYLISTS
# ========================================
elif analysis_choice == "🎧 Playlists":
    st.markdown("### 🎧 Playlist Analysis")

    try:
        playlist_df = run_query(get_playlist_performance_query())
        discovery_df = run_query(
            get_content_discovery_query(),
            (MIN_PLAYLIST_APPEARANCES, PLAYLIST_DISCOVERY_LIMIT),
        )

        if not playlist_df.empty:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total playlists", len(playlist_df))
            with col2:
                st.metric(
                    "Avg tracks per playlist",
                    f"{playlist_df['track_count'].mean():.1f}",
                )
            with col3:
                st.metric(
                    "Avg duration per playlist",
                    f"{playlist_df['total_duration_hours'].mean():.1f}h",
                )

            col1, col2 = st.columns(2)

            with col1:
                fig = create_playlist_heatmap(playlist_df)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                if not discovery_df.empty:
                    fig = create_discovery_funnel(discovery_df)
                    st.plotly_chart(fig, use_container_width=True)

            _create_data_table(
                playlist_df.head(TOP_PLAYLISTS_DISPLAY),
                {
                    "playlist_name": "Playlist",
                    "track_count": "Tracks",
                    "avg_track_duration": "Avg Track Duration (min)",
                    "total_duration_hours": "Total Duration (h)",
                    "genre_diversity": "Genre Diversity",
                    "artist_diversity": "Artist Diversity",
                },
                "📋 Playlist Details",
            )

        else:
            st.warning("No playlist data available.")

    except Exception as e:  # noqa: BLE001
        st.error(f"Error loading playlist data: {e}")

# ========================================
# REVENUE
# ========================================
elif analysis_choice == "💰 Revenue":
    st.markdown("### 💰 Revenue Analysis")

    with st.sidebar:
        st.markdown("### 📅 Analysis filters")
        date_range = st.date_input(
            "Revenue period",
            value=(min_d, max_d),
            min_value=min_d,
            max_value=max_d,
            key="revenue_dates",
        )
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_d, end_d = date_range
        else:
            start_d, end_d = min_d, max_d

    try:
        revenue_df = run_query(get_revenue_analysis_query(), (start_d, end_d))

        if not revenue_df.empty:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    "Total revenue",
                    f"${revenue_df['total_revenue'].sum():,.2f}",
                )
            with col2:
                st.metric(
                    "Total units sold",
                    f"{revenue_df['units_sold'].sum():,}",
                )
            with col3:
                st.metric(
                    "Avg price",
                    f"${revenue_df['avg_price'].mean():.2f}",
                )

            col1, col2 = st.columns(2)

            with col1:
                fig = create_revenue_trend_chart(revenue_df, "Genre")
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                track_df = run_query(
                    get_track_performance_query(),
                    (start_d, end_d, MIN_TRACK_SALES, TRACK_LIMIT),
                )
                if not track_df.empty:
                    fig = create_pricing_analysis(track_df)
                    st.plotly_chart(fig, use_container_width=True)

            _create_data_table(
                revenue_df,
                {
                    "genre": "Genre",
                    "units_sold": "Units Sold",
                    "total_revenue": "Revenue ($)",
                    "avg_price": "Avg Price ($)",
                    "unique_tracks": "Unique Tracks",
                    "unique_artists": "Unique Artists",
                    "avg_duration": "Avg Duration (min)",
                },
                "📋 Revenue by Genre",
            )

        else:
            st.warning("No revenue data available for the selected period.")

    except Exception as e:  # noqa: BLE001
        st.error(f"Error loading revenue data: {e}")

# ========================================
# TRENDS
# ========================================
elif analysis_choice == "📈 Trends":
    st.markdown("### 📈 Sales Trends")

    with st.sidebar:
        st.markdown("### 📅 Analysis filters")
        date_range = st.date_input(
            "Trend period",
            value=(min_d, max_d),
            min_value=min_d,
            max_value=max_d,
            key="trend_dates",
        )
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_d, end_d = date_range
        else:
            start_d, end_d = min_d, max_d

        selected_genres = st.multiselect(
            "Focus on genres",
            options=AVAILABLE_GENRES,
            default=AVAILABLE_GENRES[:3],
            key="trend_genres",
        )

    try:
        trend_df = run_query(get_trend_analysis_query(), (start_d, end_d))

        if not trend_df.empty:
            col1, col2 = st.columns(2)

            with col1:
                fig = create_trend_line_chart(trend_df)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                if selected_genres:
                    fig = create_genre_trend_chart(trend_df, selected_genres)
                    st.plotly_chart(fig, use_container_width=True)

            daily_summary = (
                trend_df.groupby("sale_date")
                .agg({
                    "quantity_sold": "sum",
                    "revenue": "sum",
                    "unique_tracks_sold": "sum",
                })
                .reset_index()
            )
            _create_data_table(
                daily_summary.tail(10),
                {
                    "sale_date": "Date",
                    "quantity_sold": "Units Sold",
                    "revenue": "Revenue ($)",
                    "unique_tracks_sold": "Unique Tracks",
                },
                "📋 Recent Daily Summary",
            )

        else:
            st.warning("No trend data available for the selected period.")

    except Exception as e:  # noqa: BLE001
        st.error(f"Error loading trend data: {e}")

# Footer
from src.utils.ui_components import render_footer
render_footer() 