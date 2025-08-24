"""Finance module visualization functions."""

import plotly.express as px
import plotly.graph_objects as go
import plotly.colors as pc
import numpy as np
import pandas as pd
import streamlit as st
from textwrap import dedent

try:
    # Try relative imports first (when imported as module)
    from .constants import (
        PRIMARY_COLOR, SECONDARY_COLOR, CHART_HEIGHT, COMPACT_CHART_HEIGHT,
        SMALL_CHART_HEIGHT, FONT_FAMILY, TOP_COUNTRIES_LIMIT
    )
except ImportError:
    # Fall back to absolute imports (when run directly or from app.py)
    from pages.finance.constants import (
        PRIMARY_COLOR, SECONDARY_COLOR, CHART_HEIGHT, COMPACT_CHART_HEIGHT,
        SMALL_CHART_HEIGHT, FONT_FAMILY, TOP_COUNTRIES_LIMIT
    )


def create_trends_chart(trends_df, period_view):
    """Create financial trends chart."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=trends_df['period_label'],
        y=trends_df['revenue'],
        mode='lines+markers',
        name='Revenue',
        line=dict(color=PRIMARY_COLOR, width=3),
        marker=dict(size=8, color=PRIMARY_COLOR),
        fill='tonexty',
        fillcolor=f'rgba(109, 40, 217, 0.12)'
    ))
    fig.update_traces(
        customdata=np.stack(
            [
                trends_df['invoice_count'],
                trends_df['avg_invoice'],
                trends_df['unique_customers'],
            ],
            axis=-1,
        ),
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Revenue: %{y:$,.0f}<br>"
            "Invoices: %{customdata[0]:,}<br>"
            "Avg invoice: %{customdata[1]:$,.0f}<br>"
            "Unique customers: %{customdata[2]:,}"
            "<extra></extra>"
        ),
    )
    
    fig.update_layout(
        height=CHART_HEIGHT,
        margin=dict(l=0, r=0, t=20, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        font=dict(family=FONT_FAMILY)
    )
    
    if period_view == "Year":
        years_list = sorted(trends_df['period'].unique())
        fig.update_xaxes(
            showgrid=True, 
            gridcolor='rgba(0,0,0,0.05)',
            tickmode='array',
            tickvals=years_list,
            ticktext=years_list
        )
    else:
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    
    fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    
    return fig


def create_geographic_pie_chart(geographic_df):
    """Create geographic distribution pie chart."""
    top_countries = geographic_df.head(TOP_COUNTRIES_LIMIT).copy()
    top_countries = top_countries.sort_values('total_revenue', ascending=False)
    
    revenues = top_countries['total_revenue'].values
    normalized_revenues = ((revenues - revenues.min()) / 
                          (revenues.max() - revenues.min()))
    
    colors = []
    for norm_val in normalized_revenues:
        if norm_val == 0:
            colors.append('rgb(245, 240, 255)')
        elif norm_val == 1:
            colors.append('rgb(109, 40, 217)')
        else:
            intensity = norm_val
            r = int(245 - (245 - 109) * intensity)
            g = int(240 - (240 - 40) * intensity) 
            b = int(255 - (255 - 217) * intensity)
            colors.append(f'rgb({r},{g},{b})')
    
    fig = px.pie(
        top_countries,
        values='total_revenue',
        names='country',
        title="🗺️ Revenue Distribution by Country",
        hover_data={'customers': True, 'invoices': True}
    )
    
    fig.update_traces(
        marker=dict(colors=colors),
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Revenue: %{value:$,.0f}<br>"
            "Share: %{percent}<br>"
            "Customers: %{customdata[0]:,}<br>"
            "Invoices: %{customdata[1]:,}"
            "<extra></extra>"
        ),
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        height=CHART_HEIGHT,
        margin=dict(l=0, r=0, t=40, b=0),
        font=dict(family=FONT_FAMILY),
        showlegend=False
    )
    
    return fig


def create_geographic_bar_chart(geographic_df):
    """Create geographic bar chart."""
    df_bar = geographic_df.head(TOP_COUNTRIES_LIMIT).copy()
    df_bar = df_bar.assign(
        tooltip=(
            "<b>" + df_bar['country'].astype(str) + "</b><br>"
            + "Revenue: $" + df_bar['total_revenue'].round(0).astype(int).astype(str) + "<br>"
            + "Customers: " + df_bar['customers'].astype(int).astype(str) + "<br>"
            + "Invoices: " + df_bar['invoices'].astype(int).astype(str) + "<br>"
            + "Revenue / Customer: $" + df_bar['revenue_per_customer'].round(0).astype(int).astype(str)
        )
    )
    fig = px.bar(
        df_bar,
        x='total_revenue',
        y='country',
        orientation='h',
        title="💰 Top 10 Countries by Revenue",
        labels={'total_revenue': 'Revenue ($)', 'country': ''},
        color='total_revenue',
        color_continuous_scale='Purples',
        custom_data=['customers', 'invoices', 'revenue_per_customer']
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Revenue: %{x:$,.0f}<br>"
            "Customers: %{customdata[0]:,}<br>"
            "Invoices: %{customdata[1]:,}<br>"
            "Revenue / Customer: %{customdata[2]:$,.0f}"
            "<extra></extra>"
        )
    )
    
    fig.update_layout(
        height=COMPACT_CHART_HEIGHT,
        margin=dict(l=0, r=0, t=40, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        font=dict(family=FONT_FAMILY)
    )
    
    return fig


def create_invoice_distribution_chart(invoice_analysis_df):
    """Create invoice distribution pie chart."""
    df = invoice_analysis_df.copy()
    df["revenue_fmt"] = df["total_revenue"].apply(lambda v: f"${v:,.0f}")
    df["avg_fmt"] = df["avg_amount"].apply(lambda v: f"${v:,.2f}")
    df["share_fmt"] = df["percentage"].apply(lambda v: f"{v:.1f}%")

    fig = px.pie(
        df,
        values="invoice_count",
        names="amount_range",
        title="📊 Invoice Distribution by Amount",
        color_discrete_sequence=px.colors.sequential.Purples,
        custom_data=["revenue_fmt", "avg_fmt", "share_fmt"],
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Invoices: %{value:,}<br>"
            "Revenue: %{customdata[0]}<br>"
            "Average: %{customdata[1]}<br>"
            "Share: %{customdata[2]}"
            "<extra></extra>"
        )
    )

    fig.update_layout(
        height=COMPACT_CHART_HEIGHT,
        margin=dict(l=0, r=0, t=40, b=0),
        font=dict(family=FONT_FAMILY),
    )

    return fig


def create_revenue_by_range_chart(invoice_analysis_df):
    """Create revenue by amount range bar chart."""
    fig = px.bar(
        invoice_analysis_df,
        x='amount_range',
        y='total_revenue',
        title="💰 Revenue by Amount Range",
        color='total_revenue',
        color_continuous_scale='Purples',
        custom_data=['invoice_count', 'avg_amount', 'percentage']
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Revenue: %{y:$,.0f}<br>"
            "Invoices: %{customdata[0]:,}<br>"
            "Average: %{customdata[1]:$,.2f}<br>"
            "Share: %{customdata[2]:.1f}%"
            "<extra></extra>"
        )
    )
    
    fig.update_layout(
        height=COMPACT_CHART_HEIGHT,
        margin=dict(l=0, r=0, t=40, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        font=dict(family=FONT_FAMILY)
    )
    
    return fig


def create_seasonality_chart(seasonality_df):
    """Create seasonality line chart."""
    fig = px.line(
        seasonality_df,
        x='month_name',
        y='total_revenue',
        title="🌟 Sales Seasonality (Revenue by Month)",
        markers=True,
        color_discrete_sequence=[PRIMARY_COLOR],
        custom_data=['invoice_count', 'avg_invoice']
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Revenue: %{y:$,.0f}<br>"
            "Invoices: %{customdata[0]:,}<br>"
            "Avg invoice: %{customdata[1]:$,.0f}"
            "<extra></extra>"
        )
    )
    
    fig.update_layout(
        height=COMPACT_CHART_HEIGHT,
        margin=dict(l=0, r=0, t=40, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family=FONT_FAMILY),
        xaxis_title="Month",
        yaxis_title="Revenue ($)"
    )
    
    return fig


def create_weekly_revenue_chart(weekly_df):
    """Create weekly revenue bar chart."""
    fig = px.bar(
        weekly_df,
        x='day_name',
        y='total_revenue',
        title="📈 Revenue by Day of Week",
        color='total_revenue',
        color_continuous_scale='Purples',
        custom_data=['invoice_count', 'avg_invoice']
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Revenue: %{y:$,.0f}<br>"
            "Invoices: %{customdata[0]:,}<br>"
            "Avg invoice: %{customdata[1]:$,.0f}"
            "<extra></extra>"
        )
    )
    
    fig.update_layout(
        height=SMALL_CHART_HEIGHT,
        margin=dict(l=0, r=0, t=40, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        font=dict(family=FONT_FAMILY),
        xaxis_title="Day",
        yaxis_title="Revenue ($)"
    )
    
    return fig


def create_weekly_invoices_chart(weekly_df):
    """Create weekly invoices bar chart."""
    fig = px.bar(
        weekly_df,
        x='day_name',
        y='invoice_count',
        title="📋 Invoices by Day of Week",
        color_discrete_sequence=[SECONDARY_COLOR],
        custom_data=['total_revenue', 'avg_invoice']
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Invoices: %{y:,}<br>"
            "Revenue: %{customdata[0]:$,.0f}<br>"
            "Avg invoice: %{customdata[1]:$,.0f}"
            "<extra></extra>"
        )
    )
    
    fig.update_layout(
        height=SMALL_CHART_HEIGHT,
        margin=dict(l=0, r=0, t=40, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        font=dict(family=FONT_FAMILY),
        xaxis_title="Day",
        yaxis_title="Invoices"
    )
    
    return fig


def create_basket_evolution_chart(basket_df, period_view):
    """Create basket evolution chart."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=basket_df['period_label'],
        y=basket_df['avg_basket'],
        mode='lines+markers',
        name='Average Basket',
        line=dict(color=PRIMARY_COLOR, width=3),
        marker=dict(size=8, color=PRIMARY_COLOR),
        fill='tonexty',
        fillcolor='rgba(109, 40, 217, 0.12)',
        customdata=np.stack(
            [
                basket_df['invoice_count'],
                basket_df['total_revenue'],
                basket_df['basket_std'],
            ],
            axis=-1,
        ),
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Avg basket: %{y:$,.2f}<br>"
            "Invoices: %{customdata[0]:,}<br>"
            "Revenue: %{customdata[1]:$,.0f}<br>"
            "Std dev: %{customdata[2]:$,.2f}"
            "<extra></extra>"
        )
    ))
    
    fig.update_layout(
        height=COMPACT_CHART_HEIGHT,
        margin=dict(l=0, r=0, t=20, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        font=dict(family=FONT_FAMILY),
        xaxis_title="Period",
        yaxis_title="Average Basket ($)"
    )
    
    if period_view == "Year":
        years_list = sorted(basket_df['period'].unique())
        fig.update_xaxes(
            showgrid=True, 
            gridcolor='rgba(0,0,0,0.05)',
            tickmode='array',
            tickvals=years_list,
            ticktext=years_list
        )
    else:
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    
    fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    
    return fig


def display_financial_metrics(financial_metrics):
    """Display financial metrics in HTML format."""
    metrics_html = '<div class="metric-row">'
    for icon, value, label in financial_metrics:
        metrics_html += f"""
        <div class="metric-item">
            <div class="metric-icon">{icon}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>"""
    metrics_html += '</div>'
    
    st.markdown(metrics_html, unsafe_allow_html=True)


def create_auto_scroll_countries(shuffled_df):
    """Create auto-scrolling countries container."""
    # First add the CSS for auto-scroll
    css = dedent("""
    <style>
    .auto-scroll-container {
        height: 700px;
        overflow-y: auto;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        background: #fafafa;
        position: relative;
        scrollbar-width: thin;
        scrollbar-color: #cbd5e0 #f7fafc;
    }
    .auto-scroll-container::-webkit-scrollbar { width: 6px; }
    .auto-scroll-container::-webkit-scrollbar-track { background: #f7fafc; border-radius: 3px; }
    .auto-scroll-container::-webkit-scrollbar-thumb { background: #cbd5e0; border-radius: 3px; }
    .auto-scroll-container::-webkit-scrollbar-thumb:hover { background: #a0aec0; }
    .auto-scroll-content { animation: autoScroll 25s linear infinite; padding: 10px; }
    @keyframes autoScroll { 0% { transform: translateY(0); } 100% { transform: translateY(-50%); } }
    .auto-scroll-container:hover .auto-scroll-content { animation-play-state: paused; }
    .auto-scroll-container:active .auto-scroll-content { animation-play-state: paused; }
    </style>
    """)
    st.markdown(css, unsafe_allow_html=True)
    
    countries_html = ""
    for _ in range(2):  # Duplicate for loop effect
        for _, row in shuffled_df.iterrows():
            status_class = ("status-high" if row['market_share_percent'] >= 10 
                          else "status-medium" if row['market_share_percent'] >= 5 
                          else "status-low")
            
            country = str(row['country'])
            customers = str(int(row['customers']))
            invoices = str(int(row['invoices']))
            market = str(round(row['market_share_percent'], 1))
            revenue = str(int(row['total_revenue']))
            avg_inv = str(int(row['avg_invoice_amount']))
            
            countries_html += f"""
            <div class="country-item">
                <div>
                    <div class="country-name">{country}</div>
                    <div style="font-size: 0.8rem; color: #64748b;">
                        {customers} customers • {invoices} invoices
                    </div>
                    <div class="invoice-status {status_class}">{market}% market share</div>
                </div>
                <div style="text-align: right;">
                    <div class="country-value">${revenue}</div>
                </div>
            </div>"""
    
    countries_html = dedent(countries_html)
    scroll_html = dedent(f"""
    <div class="auto-scroll-container">
      <div class="auto-scroll-content">
        {countries_html}
      </div>
    </div>
    """)
    st.markdown(scroll_html, unsafe_allow_html=True) 