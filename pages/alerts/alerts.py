import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st

from utils import apply_sidebar_logo, run_query
from pages.alerts.queries import (
    get_low_performance_albums_query,
    get_low_performance_tracks_query,
)
from pages.alerts.visualization import create_genre_issues_chart
from pages.alerts.constants import (
    ALBUM_LIMIT,
    ALBUM_SALES_THRESHOLD,
    MIN_SALES_THRESHOLD,
    TRACK_LIMIT,
)

st.set_page_config(
    page_title="Alert System", page_icon="🚨", layout="wide"
)
apply_sidebar_logo()


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
  <h1 class="header-title">🚨 Alert System</h1>
  <p class="header-subtitle">Tracks • Albums to investigate</p>
</div>
""",
    unsafe_allow_html=True,
)


def _create_data_table(df, columns_mapping, title):
    """Create a formatted data table with ranking column."""
    display_df = df[list(columns_mapping.keys())].copy()
    display_df = display_df.rename(columns=columns_mapping)
    display_df.insert(0, "#", range(1, len(display_df) + 1))
    st.markdown(f"#### {title}")
    st.dataframe(display_df, use_container_width=True, hide_index=True)



st.markdown("### 🔍 Tracks to Investigate")

try:
    tracks_df = run_query(
        get_low_performance_tracks_query(),
        (MIN_SALES_THRESHOLD, TRACK_LIMIT),
    )

    if not tracks_df.empty:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Tracks to investigate", len(tracks_df))
        with col2:
            no_sales = len(tracks_df[tracks_df["total_sales"] == 0])
            st.metric("No sales", no_sales)
        with col3:
            avg_duration = tracks_df["duration_minutes"].mean()
            st.metric("Avg duration", f"{avg_duration:.1f} min")

        fig = create_genre_issues_chart(tracks_df)
        st.plotly_chart(fig, use_container_width=True)

        _create_data_table(
            tracks_df,
            {
                "track_name": "Track",
                "artist_name": "Artist",
                "album_title": "Album",
                "genre": "Genre",
                "total_sales": "Sales",
                "avg_price": "Price ($)",
                "duration_minutes": "Duration (min)",
                "alert_level": "Alert Level",
            },
            "📋 Track Details",
        )

    else:
        st.info("No tracks found that need investigation with current filters.")

except Exception as e:  # noqa: BLE001
    st.error(f"Error loading track data: {e}")

st.markdown("---")

st.markdown("### 💿 Albums to Investigate")

try:
    albums_df = run_query(
        get_low_performance_albums_query(),
        (ALBUM_SALES_THRESHOLD, ALBUM_LIMIT),
    )

    if not albums_df.empty:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Albums to investigate", len(albums_df))
        with col2:
            no_sales_albums = len(albums_df[albums_df["total_sales"] == 0])
            st.metric("Albums with no sales", no_sales_albums)
        with col3:
            avg_tracks = albums_df["track_count"].mean()
            st.metric("Avg tracks/album", f"{avg_tracks:.1f}")

        _create_data_table(
            albums_df,
            {
                "album_title": "Album",
                "artist_name": "Artist",
                "track_count": "Tracks",
                "total_sales": "Sales",
                "album_revenue": "Revenue ($)",
                "alert_level": "Alert Level",
            },
            "📋 Album Details",
        )

    else:
        st.info("No albums found that need investigation with current filters.")

except Exception as e:  # noqa: BLE001
    st.error(f"Error loading album data: {e}")

# Footer
from src.utils.ui_components import render_footer
render_footer() 