import streamlit as st
import pandas as pd
from datetime import date
from pathlib import Path

from utils import run_query, apply_sidebar_logo
from pages.customers.queries import (
    get_churn_analysis_query,
    get_date_bounds_query,
    get_rfm_clustering_query,
    get_top_clients_query,
)
from pages.customers.visualization import (
    create_churn_histogram,
    create_churn_pie_chart,
    create_cluster_heatmap,
    create_cluster_pie_chart,
    create_diversity_scatter,
    create_engagement_timeline,
    create_listening_profile_chart,
    create_musical_profile_chart,
    create_scatter_plot,
)
from pages.customers.constants import (
    AMATEUR_MINUTES,
    CHURN_MONTHS_DEFAULT,
    MUSIC_LOVER_MINUTES,
    OCCASIONAL_MINUTES,
    TOP_CLIENTS_LIMIT,
)

st.set_page_config(
    page_title="Customers Dashboard", page_icon="👥", layout="wide"
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
  <h1 class="header-title">👥 Customers</h1>
  <p class="header-subtitle">Clustering • Churn • Top Clients</p>
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

# View selector
try:
    analysis_choice = st.segmented_control(
        "",
        options=["🧩 Clustering", "⚠️ Churn Analysis", "🏆 Top Clients"],
        selection_mode="single",
        default="🧩 Clustering",
        key="customers_view_seg",
    )
except Exception:
    analysis_choice = st.radio(
        "",
        ["🧩 Clustering", "⚠️ Churn Analysis", "🏆 Top Clients"],
        horizontal=True,
        key="customers_view_radio",
    )


def _create_cluster_summary_table(rfm_df):
    """Create cluster performance summary table."""
    cluster_analysis = rfm_df.groupby("rfm_cluster").agg({
        "recency_days": ["mean", "std"],
        "frequency": ["mean", "std"],
        "monetary": ["mean", "std", "sum"],
        "nb_different_genres": "mean",
        "nb_purchased_tracks": "mean",
        "customer_id": "count",
    }).round(2)

    cluster_analysis.columns = [
        "Avg_Recency", "Std_Recency",
        "Avg_Frequency", "Std_Frequency",
        "Avg_Value", "Std_Value", "Total_Revenue",
        "Avg_Genres", "Avg_Tracks", "Nb_Customers",
    ]

    total_revenue = cluster_analysis["Total_Revenue"].sum()
    total_customers = cluster_analysis["Nb_Customers"].sum()

    cluster_analysis["Revenue_Proportion"] = (
        cluster_analysis["Total_Revenue"] / total_revenue * 100
    ).round(1)
    cluster_analysis["Customer_Proportion"] = (
        cluster_analysis["Nb_Customers"] / total_customers * 100
    ).round(1)

    return cluster_analysis


def _get_listening_profile(minutes):
    """Determine listening profile based on total minutes."""
    if minutes >= MUSIC_LOVER_MINUTES:
        return "Music Lover"
    if minutes >= AMATEUR_MINUTES:
        return "Amateur"
    if minutes >= OCCASIONAL_MINUTES:
        return "Occasional"
    return "Beginner"


def _display_top_performers(top_df, metric_col, format_value, ranks):
    """Display top 3 performers with formatted values."""
    for i, (_, row) in enumerate(top_df.head(TOP_CLIENTS_LIMIT).iterrows()):
        st.write(f"{ranks[i]} {row['client']} — {format_value(row[metric_col])}")


if analysis_choice == "🧩 Clustering":
    st.markdown("### 🧩 Customer Clustering (RFM + Musical)")

    with st.sidebar:
        st.markdown("### 📅 Analysis Filters")
        date_range = st.date_input(
            "Analysis Period",
            value=(min_d, max_d),
            min_value=min_d,
            max_value=max_d,
            key="clustering_dates",
        )
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_d, end_d = date_range
        else:
            start_d, end_d = min_d, max_d

    try:
        rfm_df = run_query(
            get_rfm_clustering_query(), (start_d, end_d, start_d, end_d)
        )

        if not rfm_df.empty:
            col1, col2 = st.columns(2)

            with col1:
                fig1 = create_cluster_pie_chart(rfm_df)
                st.plotly_chart(fig1, use_container_width=True)

            with col2:
                fig2 = create_musical_profile_chart(rfm_df)
                st.plotly_chart(fig2, use_container_width=True)

            st.markdown("#### 🎯 Performance by Cluster")
            cluster_analysis = _create_cluster_summary_table(rfm_df)
            st.dataframe(cluster_analysis, use_container_width=True)

            col1, col2 = st.columns(2)

            with col1:
                fig3 = create_cluster_heatmap(rfm_df)
                st.plotly_chart(fig3, use_container_width=True)

            with col2:
                fig4 = create_scatter_plot(rfm_df)
                st.plotly_chart(fig4, use_container_width=True)

        else:
            st.warning("No data available for clustering.")
    except Exception as e:  # noqa: BLE001
        st.error(f"Error during clustering: {e}")


elif analysis_choice == "⚠️ Churn Analysis":
    st.markdown("### ⚠️ Churn Analysis")

    with st.sidebar:
        st.markdown("### 📅 Analysis Filters")
        date_range = st.date_input(
            "Analysis Period",
            value=(min_d, max_d),
            min_value=min_d,
            max_value=max_d,
            key="churn_dates",
        )
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_d, end_d = date_range
        else:
            start_d, end_d = min_d, max_d
        churn_months = CHURN_MONTHS_DEFAULT

    try:
        churn_df = run_query(
            get_churn_analysis_query(),
            (start_d, end_d, churn_months, churn_months // 2),
        )

        if not churn_df.empty:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Customers", len(churn_df))
            with col2:
                churn_count = int(
                    (churn_df["churn_status"] == "Churn Risk").sum()
                )
                st.metric("Churn Risk", churn_count)
            with col3:
                rate = (
                    100 * churn_count / len(churn_df) if len(churn_df) > 0 else 0
                )
                st.metric("Churn Rate", f"{rate:.1f}%")

            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:
                fig1 = create_churn_pie_chart(churn_df)
                st.plotly_chart(fig1, use_container_width=True)

            with col2:
                fig2 = create_churn_histogram(churn_df)
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("No data available for churn analysis.")
    except Exception as e:  # noqa: BLE001
        st.error(f"Error during churn analysis: {e}")


elif analysis_choice == "🏆 Top Clients":
    st.markdown("### 🏆 Top Clients")

    with st.sidebar:
        st.markdown("### 📅 Analysis Filters")
        date_range = st.date_input(
            "Analysis Period",
            value=(min_d, max_d),
            min_value=min_d,
            max_value=max_d,
            key="top_dates",
        )
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_d, end_d = date_range
        else:
            start_d, end_d = min_d, max_d

    try:
        top_clients_df = run_query(get_top_clients_query(), (start_d, end_d))

        if (
            not top_clients_df.empty
            and "listening_profile" not in top_clients_df.columns
        ):
            top_clients_df["listening_profile"] = (
                top_clients_df["total_minutes"].fillna(0).apply(_get_listening_profile)
            )

        # Ensure nb_orders exists for displays and engagement metrics
        if not top_clients_df.empty and "nb_orders" not in top_clients_df.columns:
            if {"total_spending", "avg_basket"}.issubset(top_clients_df.columns):
                tmp_orders = (
                    top_clients_df["total_spending"].fillna(0)
                    / top_clients_df["avg_basket"].replace(0, pd.NA)
                )
                top_clients_df["nb_orders"] = (
                    tmp_orders.fillna(0).round().astype(int)
                )
            else:
                top_clients_df["nb_orders"] = 0

        if not top_clients_df.empty:
            analysis_type = st.selectbox(
                "📊 Analysis Type",
                [
                    "💰 By Spending",
                    "🎵 By Listening Time",
                    "🎨 By Diversity",
                    "📈 By Engagement",
                ],
            )

            ranks = ["1️⃣", "2️⃣", "3️⃣"]

            if analysis_type == "💰 By Spending":
                col1, col2 = st.columns([2, 1])

                with col1:
                    display_df = top_clients_df[
                        [
                            "client",
                            "country",
                            "nb_orders",
                            "total_spending",
                            "avg_basket",
                        ]
                    ].copy()
                    display_df.insert(0, "#", range(1, len(display_df) + 1))
                    st.subheader("🏆 Customer Ranking by Spending")
                    st.dataframe(
                        display_df, use_container_width=True, hide_index=True
                    )

                with col2:
                    st.markdown("#### Top 3")
                    _display_top_performers(
                        top_clients_df,
                        "total_spending",
                        lambda x: f"${x:,.2f}",
                        ranks,
                    )

            elif analysis_type == "🎵 By Listening Time":
                sorted_df = top_clients_df.sort_values(
                    "total_minutes", ascending=False
                )

                col1, col2 = st.columns([2, 1])

                with col1:
                    display_df = sorted_df[
                        [
                            "client",
                            "country",
                            "total_minutes",
                            "nb_purchased_tracks",
                            "listening_profile",
                        ]
                    ]
                    display_df.insert(0, "#", range(1, len(display_df) + 1))
                    st.subheader("🎵 Ranking by Listening Time")
                    st.dataframe(
                        display_df, use_container_width=True, hide_index=True
                    )

                with col2:
                    st.markdown("#### Top 3")
                    _display_top_performers(
                        sorted_df,
                        "total_minutes",
                        lambda x: f"{x:.0f} min",
                        ranks,
                    )

                fig = create_listening_profile_chart(sorted_df)
                st.plotly_chart(fig, use_container_width=True)

            elif analysis_type == "🎨 By Diversity":
                top_clients_df["diversity_score"] = (
                    top_clients_df["nb_different_genres"] * 2
                    + top_clients_df["nb_different_artists"]
                    + top_clients_df["nb_different_albums"]
                ) / 4
                sorted_df = top_clients_df.sort_values(
                    "diversity_score", ascending=False
                )

                col1, col2 = st.columns([2, 1])

                with col1:
                    display_df = sorted_df[
                        [
                            "client",
                            "country",
                            "nb_different_genres",
                            "nb_different_artists",
                            "nb_different_albums",
                        ]
                    ]
                    display_df.insert(0, "#", range(1, len(display_df) + 1))
                    st.subheader("🎨 Ranking by Musical Diversity")
                    st.dataframe(
                        display_df, use_container_width=True, hide_index=True
                    )

                with col2:
                    st.markdown("#### Top 3")
                    _display_top_performers(
                        sorted_df,
                        "diversity_score",
                        lambda x: f"score {x:.1f}",
                        ranks,
                    )

                fig = create_diversity_scatter(sorted_df)
                st.plotly_chart(fig, use_container_width=True)

            elif analysis_type == "📈 By Engagement":
                top_clients_df["activity_days"] = (
                    pd.to_datetime(top_clients_df["last_order"])
                    - pd.to_datetime(top_clients_df["first_order"])
                ).dt.days + 1
                top_clients_df["order_frequency"] = (
                    top_clients_df["nb_orders"]
                    / (top_clients_df["activity_days"] / 30)
                )

                sorted_df = top_clients_df.sort_values(
                    "order_frequency", ascending=False
                )

                col1, col2 = st.columns([2, 1])

                with col1:
                    display_df = sorted_df[
                        [
                            "client",
                            "country",
                            "nb_orders",
                            "activity_days",
                            "order_frequency",
                        ]
                    ]
                    display_df["order_frequency"] = display_df[
                        "order_frequency"
                    ].round(2)
                    display_df.insert(0, "#", range(1, len(display_df) + 1))
                    st.subheader("📈 Ranking by Engagement")
                    st.dataframe(
                        display_df, use_container_width=True, hide_index=True
                    )

                with col2:
                    st.markdown("#### Top 3")
                    _display_top_performers(
                        sorted_df,
                        "order_frequency",
                        lambda x: f"{x:.2f}/month",
                        ranks,
                    )

                fig = create_engagement_timeline(sorted_df)
                st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("No data available for top clients.")
    except Exception as e:  # noqa: BLE001
        st.error(f"Error during top clients analysis: {e}")

# Footer
from src.utils.ui_components import render_footer
render_footer() 