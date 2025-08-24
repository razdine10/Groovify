import sys
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st

# Allow importing utils from project root
sys.path.append(str(Path(__file__).parent.parent))
from utils import run_query, apply_sidebar_logo

try:
    # Try relative imports first (when imported as module)
    from .constants import (
        PAGE_TITLE, PAGE_ICON, DEFAULT_SHORT_PERIOD, DEFAULT_MEDIUM_PERIOD,
        SUCCESS_COLOR, ERROR_COLOR
    )
    from .queries import (
        get_date_bounds_query, FINANCIAL_KPIS, MONTHLY_TRENDS, QUARTERLY_TRENDS,
        YEARLY_TRENDS, GEOGRAPHIC_ANALYSIS, INVOICE_ANALYSIS,
        SEASONALITY_ANALYSIS, WEEKLY_TRENDS, MONTHLY_BASKET_ANALYSIS,
        QUARTERLY_BASKET_ANALYSIS, YEARLY_BASKET_ANALYSIS
    )
    from .visualization import (
        create_trends_chart, create_geographic_pie_chart,
        create_geographic_bar_chart, create_invoice_distribution_chart,
        create_revenue_by_range_chart, create_seasonality_chart,
        create_weekly_revenue_chart, create_weekly_invoices_chart,
        create_basket_evolution_chart, display_financial_metrics,
        create_auto_scroll_countries
    )
except ImportError:
    # Fall back to absolute imports (when run directly or from app.py)
    from pages.finance.constants import (
        PAGE_TITLE, PAGE_ICON, DEFAULT_SHORT_PERIOD, DEFAULT_MEDIUM_PERIOD,
        SUCCESS_COLOR, ERROR_COLOR
    )
    from pages.finance.queries import (
        get_date_bounds_query, FINANCIAL_KPIS, MONTHLY_TRENDS, QUARTERLY_TRENDS,
        YEARLY_TRENDS, GEOGRAPHIC_ANALYSIS, INVOICE_ANALYSIS,
        SEASONALITY_ANALYSIS, WEEKLY_TRENDS, MONTHLY_BASKET_ANALYSIS,
        QUARTERLY_BASKET_ANALYSIS, YEARLY_BASKET_ANALYSIS
    )
    from pages.finance.visualization import (
        create_trends_chart, create_geographic_pie_chart,
        create_geographic_bar_chart, create_invoice_distribution_chart,
        create_revenue_by_range_chart, create_seasonality_chart,
        create_weekly_revenue_chart, create_weekly_invoices_chart,
        create_basket_evolution_chart, display_financial_metrics,
        create_auto_scroll_countries
    )


def load_css():
    """Load CSS styles from external file."""
    css_path = Path(__file__).parent / "styles.css"
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


def setup_page():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout="wide"
    )
    apply_sidebar_logo()
    load_css()


def create_header():
    """Create the main header section."""
    st.markdown('<div class="finance-container">', unsafe_allow_html=True)
    st.markdown("""
    <div class="finance-header">
        <h1 class="header-title">💰 Finance</h1>
        <p class="header-subtitle">
            Financial Analysis • Invoices & Geographic Distribution
        </p>
    </div>
    """, unsafe_allow_html=True)


def setup_sidebar():
    """Setup sidebar controls and return date range parameters."""
    # Prevent duplicate widget creation if the page is executed twice in one run
    if st.session_state.get("finance_sidebar_initialized"):
        return (
            st.session_state.get("finance_date_from"),
            st.session_state.get("finance_date_to"),
        )

    with st.sidebar:
        st.markdown("""
        <div class="sidebar-finance">
            <h3 style="margin: 0; font-weight: 600;">
                🎛️ Finance Controls
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        bounds_df = run_query(get_date_bounds_query())
        
        if bounds_df.empty:
            st.error("❌ No data available")
            st.stop()
        
        min_date = pd.to_datetime(bounds_df.loc[0, "min_d"]).date()
        max_date = pd.to_datetime(bounds_df.loc[0, "max_d"]).date()
        
        st.markdown("**📅 Analysis Period**")
        
        col1, col2 = st.columns(2)
        date_from = min_date
        date_to = max_date
        
        with col1:
            if st.button("30d", use_container_width=True):
                date_from = max_date - timedelta(days=DEFAULT_SHORT_PERIOD)
                date_to = max_date
        
        with col2:
            if st.button("90d", use_container_width=True):
                date_from = max_date - timedelta(days=DEFAULT_MEDIUM_PERIOD)
                date_to = max_date
        
        date_range = st.date_input(
            "Custom dates",
            value=(date_from, date_to),
            min_value=min_date,
            max_value=max_date
        )
        
        if len(date_range) == 2:
            date_from, date_to = date_range
        
        st.session_state["finance_sidebar_initialized"] = True
        st.session_state["finance_date_from"] = date_from
        st.session_state["finance_date_to"] = date_to
        
        return date_from, date_to


def display_financial_kpis(date_from, date_to):
    """Display financial KPIs section."""
    params = (str(date_from), str(date_to))
    financial_kpis_df = run_query(FINANCIAL_KPIS, params)
    
    if not financial_kpis_df.empty:
        f = financial_kpis_df.iloc[0]
        days_period = (pd.to_datetime(date_to) - 
                      pd.to_datetime(date_from)).days + 1
        daily_revenue = (f['total_revenue'] / days_period 
                        if days_period > 0 else 0)
        
        financial_metrics = [
            ("💰", f"${f['total_revenue']:,.0f}", "Total Revenue"),
            ("📄", f"{int(f['total_invoices'])}", "Invoices"),
            ("🧾", f"${f['avg_invoice_amount']:.0f}", "Avg Invoice"),
            ("👥", f"{int(f['unique_customers'])}", "Customers"),
            ("🌍", f"{int(f['countries_served'])}", "Countries"),
            ("💎", f"${f['revenue_per_customer']:.0f}", "Revenue/Customer"),
            ("📈", f"${daily_revenue:.0f}", "Revenue/Day"),
            ("⬆️", f"${f['max_invoice']:.0f}", "Max Invoice")
        ]
        
        display_financial_metrics(financial_metrics)


def get_trends_query(period_view):
    """Get the appropriate trends query based on period view."""
    if period_view == "Month":
        return MONTHLY_TRENDS
    elif period_view == "Quarter":
        return QUARTERLY_TRENDS
    else:
        return YEARLY_TRENDS


def display_financial_evolution(date_from, date_to):
    """Display financial evolution section."""
    st.markdown(
        "<h3 style='text-align:center; color:#6D28D9; font-weight:bold;'>"
        "📈 Financial Evolution</h3>",
        unsafe_allow_html=True
    )
    
    period_view = st.radio(
        "Select period granularity",
        ["Month", "Quarter", "Year"],
        index=0,
        horizontal=True,
        label_visibility="collapsed"
    )
    
    params = (str(date_from), str(date_to))
    trends_sql = get_trends_query(period_view)
    trends_df = run_query(trends_sql, params)
    
    if not trends_df.empty:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = create_trends_chart(trends_df, period_view)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            display_performance_stats(trends_df, period_view)


def display_performance_stats(trends_df, period_view):
    """Display performance statistics."""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f0f9ff, #e0f2fe); 
                padding: 0.6rem; border-radius: 8px; 
                border: 1px solid #0ea5e9; margin-bottom: 0.6rem; 
                text-align: center;">
        <h5 style="margin: 0; color: #0369a1; font-weight: 600; 
                   font-size: 0.9rem;">📊 Statistics</h5>
    </div>
    """, unsafe_allow_html=True)
    
    if len(trends_df) >= 2:
        current_revenue = trends_df.iloc[-1]['revenue']
        previous_revenue = trends_df.iloc[-2]['revenue']
        growth = (((current_revenue - previous_revenue) / previous_revenue) 
                 * 100 if previous_revenue > 0 else 0)
        
        growth_color = SUCCESS_COLOR if growth > 0 else ERROR_COLOR
        growth_icon = "📈" if growth > 0 else "📉"
        growth_bg = ("linear-gradient(135deg, #f0fdf4, #dcfce7)" 
                    if growth > 0 else 
                    "linear-gradient(135deg, #fef2f2, #fee2e2)")
        border_color = "#bbf7d0" if growth > 0 else "#fecaca"
        
        st.markdown(f"""
        <div style="background: {growth_bg}; border-radius: 8px; 
                    padding: 0.8rem; margin: 0.5rem 0; 
                    border: 1px solid {border_color}; text-align: center;">
            <div style="font-size: 1.2rem; margin-bottom: 0.2rem;">
                {growth_icon}
            </div>
            <div style="font-weight: 600; color: #374151; 
                       margin-bottom: 0.2rem; font-size: 0.8rem;">
                Growth
            </div>
            <div style="color: {growth_color}; font-size: 1.4rem; 
                       font-weight: 700; margin-bottom: 0.1rem;">
                {growth:+.1f}%
            </div>
            <div style="font-size: 0.7rem; color: #6b7280;">
                vs prev {period_view.lower()}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    display_kpi_metrics(trends_df)


def display_kpi_metrics(trends_df):
    """Display KPI metrics for performance."""
    best_period = trends_df.loc[trends_df['revenue'].idxmax()]
    avg_period = trends_df['revenue'].mean()
    first_revenue = trends_df.iloc[0]['revenue']
    last_revenue = trends_df.iloc[-1]['revenue']
    growth_rate = (((last_revenue - first_revenue) / first_revenue * 100) 
                  if first_revenue > 0 else 0)
    
    st.markdown("### 🏆 Performance")
    
    perf_col1, perf_col2, perf_col3 = st.columns(3)
    
    with perf_col1:
        st.metric(
            label="🥇 Peak",
            value=f"${best_period['revenue']:,.0f}",
            delta=best_period['period_label']
        )
    
    with perf_col2:
        st.metric(
            label="🚀 Growth",
            value=f"{growth_rate:+.1f}%",
            delta="Global"
        )
    
    with perf_col3:
        peak_vs_avg = (((best_period['revenue'] - avg_period) / avg_period 
                       * 100))
        st.metric(
            label="📈 Average",
            value=f"${avg_period:,.0f}",
            delta=f"{peak_vs_avg:+.1f}% vs peak"
        )


def display_geographic_analysis(date_from, date_to):
    """Display geographic analysis section."""
    st.markdown(
        "<h3 style='text-align:center; color:#6D28D9; font-weight:bold;'>"
        "🌍 Geographic Distribution</h3>",
        unsafe_allow_html=True
    )
    
    params = (str(date_from), str(date_to))
    geographic_df = run_query(GEOGRAPHIC_ANALYSIS, params + params)
    
    if not geographic_df.empty:
        col1, col2 = st.columns([3, 2])
        
        with col1:
            fig1 = create_geographic_pie_chart(geographic_df)
            st.plotly_chart(fig1, use_container_width=True)
            
            fig2 = create_geographic_bar_chart(geographic_df)
            st.plotly_chart(fig2, use_container_width=True)
        
        with col2:
            st.markdown("**🎯 Performance by Country**")
            shuffled_df = geographic_df.sample(frac=1).reset_index(drop=True)
            create_auto_scroll_countries(shuffled_df)


def display_invoice_analysis(date_from, date_to):
    """Display invoice analysis section."""
    st.markdown(
        "<h3 style='text-align:center; color:#6D28D9; font-weight:bold;'>"
        "📄 Detailed Invoice Analysis</h3>",
        unsafe_allow_html=True
    )
    
    params = (str(date_from), str(date_to))
    invoice_analysis_df = run_query(INVOICE_ANALYSIS, params + params)
    
    if not invoice_analysis_df.empty:
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            fig1 = create_invoice_distribution_chart(invoice_analysis_df)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = create_revenue_by_range_chart(invoice_analysis_df)
            st.plotly_chart(fig2, use_container_width=True)
        
        with col3:
            display_invoice_summary(invoice_analysis_df)


def display_invoice_summary(invoice_analysis_df):
    """Display invoice summary table."""
    st.markdown("**📋 Summary by Range**")
    
    with st.container(height=350):
        for _, row in invoice_analysis_df.iterrows():
            amount_range = str(row['amount_range'])
            invoice_count = str(int(row['invoice_count']))
            total_revenue = str(int(row['total_revenue']))
            
            st.markdown(f"""
            <div class="country-item">
                <div>
                    <div class="country-name">{amount_range}</div>
                    <div style="font-size: 0.8rem; color: #64748b;">
                        {invoice_count} invoices
                    </div>
                </div>
                <div style="text-align: right;">
                    <div class="country-value">${total_revenue}</div>
                    <div style="font-size: 0.8rem; color: #64748b;">
                        total
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


def display_temporal_analysis(date_from, date_to):
    """Display temporal analysis section."""
    params = (str(date_from), str(date_to))

    # Seasonality chart intentionally removed

    # Weekly trends
    weekly_df = run_query(WEEKLY_TRENDS, params)

    if not weekly_df.empty:
        st.markdown(
            "<h3 style='text-align:center; color:#6D28D9; "
            "font-weight:bold;'>📅 Weekly Trends</h3>",
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([2, 2])

        with col1:
            fig1 = create_weekly_revenue_chart(weekly_df)
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            fig2 = create_weekly_invoices_chart(weekly_df)
            st.plotly_chart(fig2, use_container_width=True)


def display_seasonality_kpis(seasonality_df):
    """Display seasonality KPIs."""
    best_month = seasonality_df.loc[seasonality_df['total_revenue'].idxmax()]
    worst_month = seasonality_df.loc[seasonality_df['total_revenue'].idxmin()]
    
    st.metric(
        "🏆 Best Month",
        best_month['month_name'].strip(),
        f"${best_month['total_revenue']:,.0f}"
    )
    st.metric(
        "📉 Lowest",
        worst_month['month_name'].strip(),
        f"${worst_month['total_revenue']:,.0f}"
    )
    
    revenue_std = seasonality_df['total_revenue'].std()
    revenue_mean = seasonality_df['total_revenue'].mean()
    variation_coeff = (revenue_std / revenue_mean) * 100
    
    st.metric(
        "📊 Variation",
        f"{variation_coeff:.1f}%",
        "Seasonal coefficient"
    )


def get_basket_query(basket_period_view):
    """Get the appropriate basket query based on period view."""
    if basket_period_view == "Month":
        return MONTHLY_BASKET_ANALYSIS
    elif basket_period_view == "Quarter":
        return QUARTERLY_BASKET_ANALYSIS
    else:
        return YEARLY_BASKET_ANALYSIS


def display_basket_analysis(date_from, date_to):
    """Display basket analysis section."""
    params = (str(date_from), str(date_to))
    basket_df = run_query(YEARLY_BASKET_ANALYSIS, params)
    
    if not basket_df.empty:
        st.markdown(
            "<h3 style='text-align:center; color:#6D28D9; "
            "font-weight:bold;'>🛒 Average Basket Evolution</h3>",
            unsafe_allow_html=True
        )
        
        basket_period_view = st.radio(
            "Select basket analysis period",
            ["Month", "Quarter", "Year"],
            index=0,
            horizontal=True,
            key="basket_granularity",
            label_visibility="collapsed"
        )
        
        basket_sql = get_basket_query(basket_period_view)
        basket_df_detailed = run_query(basket_sql, params)
        
        fig = create_basket_evolution_chart(basket_df_detailed, 
                                          basket_period_view)
        st.plotly_chart(fig, use_container_width=True)
        
        display_basket_kpis(basket_df_detailed)


def display_basket_kpis(basket_df_detailed):
    """Display basket KPIs."""
    col1, col2, col3, col4 = st.columns(4)
    
    current_basket = basket_df_detailed.iloc[-1]['avg_basket']
    first_basket = basket_df_detailed.iloc[0]['avg_basket']
    max_basket = basket_df_detailed['avg_basket'].max()
    min_basket = basket_df_detailed['avg_basket'].min()
    
    growth = (((current_basket - first_basket) / first_basket * 100) 
             if first_basket > 0 else 0)
    
    with col1:
        st.metric("📊 Current Basket", f"${current_basket:.2f}")
    
    with col2:
        st.metric("📈 Evolution", f"{growth:+.1f}%", "vs start period")
    
    with col3:
        st.metric("🏆 Maximum", f"${max_basket:.2f}")
    
    with col4:
        st.metric("📉 Minimum", f"${min_basket:.2f}")


def main():
    """Main function to run the finance dashboard."""
    setup_page()
    create_header()
    
    date_from, date_to = setup_sidebar()
    
    display_financial_kpis(date_from, date_to)
    display_financial_evolution(date_from, date_to)
    display_geographic_analysis(date_from, date_to)
    display_invoice_analysis(date_from, date_to)
    display_temporal_analysis(date_from, date_to)
    display_basket_analysis(date_from, date_to)
    
    # Footer
    from utils import apply_sidebar_logo  # noqa: F401 (ensures utils loaded)
    from src.utils.ui_components import render_footer
    render_footer()


if __name__ == "__main__":
    main() 