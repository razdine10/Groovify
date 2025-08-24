"""
Visualization functions for alert system module
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from .constants import (
    ALERT_CATEGORIES,
    DEFAULT_CHART_HEIGHT,
    HOVER_BG_COLOR,
    HOVER_BORDER_COLOR,
    HOVER_FONT_SIZE,
    RISK_COLORS,
    SEVERITY_COLORS,
)


def create_alert_dashboard(revenue_alerts, customer_alerts, inventory_alerts,
                          performance_alerts):
    """Create comprehensive alert dashboard visualization."""
    alert_counts = [
        len(revenue_alerts) if not revenue_alerts.empty else 0,
        len(customer_alerts) if not customer_alerts.empty else 0,
        len(inventory_alerts) if not inventory_alerts.empty else 0,
        len(performance_alerts) if not performance_alerts.empty else 0,
    ]

    fig = px.bar(
        x=ALERT_CATEGORIES,
        y=alert_counts,
        title="🚨 Alert Distribution by Category",
        labels={"x": "Alert Category", "y": "Number of Alerts"},
        color=alert_counts,
        color_continuous_scale="Reds",
    )
    fig.update_layout(height=DEFAULT_CHART_HEIGHT, showlegend=False)
    return fig


def create_anomaly_chart(revenue_alerts_df):
    """Create chart for revenue anomalies."""
    if revenue_alerts_df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No revenue anomalies detected",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )
        fig.update_layout(
            title="📉 Revenue Anomaly Detection",
            height=DEFAULT_CHART_HEIGHT,
        )
        return fig

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=revenue_alerts_df["alert_date"],
            y=revenue_alerts_df["daily_revenue"],
            mode="lines+markers",
            name="Daily Revenue",
            line=dict(color="blue"),
            marker=dict(size=8),
        )
    )

    if "rolling_avg" in revenue_alerts_df.columns:
        fig.add_trace(
            go.Scatter(
                x=revenue_alerts_df["alert_date"],
                y=revenue_alerts_df["rolling_avg"],
                mode="lines",
                name="7-day Average",
                line=dict(color="green", dash="dash"),
            )
        )

    critical_alerts = revenue_alerts_df[
        revenue_alerts_df["severity"] == "Critical"
    ]
    if not critical_alerts.empty:
        fig.add_trace(
            go.Scatter(
                x=critical_alerts["alert_date"],
                y=critical_alerts["daily_revenue"],
                mode="markers",
                name="Critical Alerts",
                marker=dict(color="red", size=12, symbol="x"),
            )
        )

    fig.update_layout(
        title="📉 Revenue Anomaly Detection",
        xaxis_title="Date",
        yaxis_title="Revenue ($)",
        height=DEFAULT_CHART_HEIGHT,
    )
    return fig


def create_alert_timeline(customer_alerts_df):
    """Create timeline chart for customer alerts."""
    if (
        customer_alerts_df.empty
        or "last_purchase" not in customer_alerts_df.columns
    ):
        fig = go.Figure()
        fig.add_annotation(
            text="No customer alerts available",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )
        fig.update_layout(
            title="📅 Customer Alert Timeline",
            height=DEFAULT_CHART_HEIGHT,
        )
        return fig

    fig = px.scatter(
        customer_alerts_df,
        x="last_purchase",
        y="days_inactive",
        size="customer_value",
        color="risk_level",
        title="📅 Customer Churn Risk Timeline",
        labels={
            "last_purchase": "Last Purchase Date",
            "days_inactive": "Days Inactive",
        },
        color_discrete_map=RISK_COLORS,
    )
    fig.update_layout(height=DEFAULT_CHART_HEIGHT)
    return fig


def create_severity_distribution(alerts_df):
    """Create pie chart for alert severity distribution."""
    if alerts_df.empty or "severity" not in alerts_df.columns:
        fig = go.Figure()
        fig.add_annotation(
            text="No severity data available",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )
        fig.update_layout(
            title="⚠️ Alert Severity Distribution",
            height=DEFAULT_CHART_HEIGHT,
        )
        return fig

    severity_counts = alerts_df["severity"].value_counts()

    fig = px.pie(
        values=severity_counts.values,
        names=severity_counts.index,
        title="⚠️ Alert Severity Distribution",
        color_discrete_map=SEVERITY_COLORS,
    )
    fig.update_layout(height=DEFAULT_CHART_HEIGHT)
    return fig


def create_alert_heatmap(security_alerts_df):
    """Create heatmap for security alert patterns."""
    if security_alerts_df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No security alerts detected",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )
        fig.update_layout(
            title="🛡️ Security Alert Heatmap",
            height=DEFAULT_CHART_HEIGHT,
        )
        return fig

    if "invoice_date" in security_alerts_df.columns:
        security_alerts_df["hour"] = pd.to_datetime(
            security_alerts_df["invoice_date"]
        ).dt.hour
        security_alerts_df["day_of_week"] = pd.to_datetime(
            security_alerts_df["invoice_date"]
        ).dt.day_name()

        heatmap_data = (
            security_alerts_df.groupby(["day_of_week", "hour"])
            .size()
            .unstack(fill_value=0)
        )

        fig = px.imshow(
            heatmap_data,
            title="🛡️ Security Alert Patterns",
            color_continuous_scale="Reds",
            aspect="auto",
        )
        fig.update_layout(
            height=DEFAULT_CHART_HEIGHT,
            xaxis_title="Hour of Day",
            yaxis_title="Day of Week",
        )
        return fig

    severity_by_type = security_alerts_df.groupby(
        ["alert_type", "severity"]
    ).size().unstack(fill_value=0)

    fig = px.imshow(
        severity_by_type,
        title="🛡️ Security Alert Analysis",
        color_continuous_scale="Reds",
        aspect="auto",
    )
    fig.update_layout(height=DEFAULT_CHART_HEIGHT)
    return fig


def create_performance_trends(performance_data):
    """Create trend chart for system performance metrics."""
    if performance_data.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No performance data available",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )
        fig.update_layout(
            title="📊 Performance Trends",
            height=DEFAULT_CHART_HEIGHT,
        )
        return fig

    fig = px.line(
        performance_data,
        x="date",
        y="metric_value",
        color="metric_name",
        title="📊 System Performance Trends",
        labels={"date": "Date", "metric_value": "Performance Score"},
    )
    fig.update_layout(
        height=DEFAULT_CHART_HEIGHT,
        hoverlabel=dict(
            bgcolor=HOVER_BG_COLOR,
            bordercolor=HOVER_BORDER_COLOR,
            font_size=HOVER_FONT_SIZE,
        ),
    )
    return fig


def create_genre_issues_chart(tracks_df):
    """Create bar chart showing genres with the most problematic tracks."""
    if tracks_df.empty or "genre" not in tracks_df.columns:
        fig = go.Figure()
        fig.add_annotation(
            text="No genre data available",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )
        fig.update_layout(
            title="🎭 Genres with Track Issues",
            height=350,
        )
        return fig

    genre_counts = tracks_df["genre"].value_counts().head(10)
    fig = px.bar(
        x=genre_counts.values,
        y=genre_counts.index,
        title="🎭 Genres with Track Issues",
        labels={"x": "Number of tracks", "y": "Genre"},
        color=genre_counts.values,
        color_continuous_scale="Reds",
        orientation="h",
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>Problem tracks: <b>%{x:,}</b><extra></extra>"
        )
    )
    fig.update_layout(
        height=350,
        yaxis={"categoryorder": "total ascending"},
        hoverlabel=dict(
            bgcolor=HOVER_BG_COLOR,
            bordercolor=HOVER_BORDER_COLOR,
            font_size=HOVER_FONT_SIZE,
        ),
    )
    return fig


def create_alert_summary_gauge(total_alerts, critical_count):
    """Create gauge chart for alert summary."""
    if total_alerts == 0:
        percentage = 0
    else:
        percentage = (critical_count / total_alerts) * 100

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=critical_count,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Critical Alerts"},
            delta={"reference": 0},
            gauge={
                "axis": {"range": [None, max(10, total_alerts)]},
                "bar": {"color": SEVERITY_COLORS["Critical"]},
                "steps": [
                    {"range": [0, total_alerts * 0.5], "color": "lightgray"},
                    {
                        "range": [total_alerts * 0.5, total_alerts],
                        "color": "gray",
                    },
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": total_alerts * 0.8,
                },
            },
        )
    )
    fig.update_layout(height=300)
    return fig 