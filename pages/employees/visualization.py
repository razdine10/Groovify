import plotly.express as px
import plotly.graph_objects as go

from .constants import (
    DEFAULT_CHART_HEIGHT,
    HOVER_BG_COLOR,
    HOVER_BORDER_COLOR,
    HOVER_FONT_SIZE,
    SCALE_BLUES,
    SCALE_GREENS,
    SCALE_PLASMA,
    SCALE_VIRIDIS,
    TOP_N,
)


def create_metric_bar_chart(df, metric_col, y_col, title, color_scale):
    """Create a horizontal bar chart for an arbitrary metric column."""
    fig = px.bar(
        df.head(TOP_N),
        x=metric_col,
        y=y_col,
        title=title,
        orientation="h",
        color=metric_col,
        color_continuous_scale=color_scale,
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>Value: <b>%{x:,.2f}</b><extra></extra>"
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


def create_sales_performance_chart(perf_df):
    """Create bar chart for employee sales performance."""
    fig = px.bar(
        perf_df.head(TOP_N),
        x="total_sales",
        y="employee_name",
        color="performance_score",
        title="📊 Employee Sales Performance",
        labels={
            "total_sales": "Total Sales ($)",
            "employee_name": "Employee",
        },
        color_continuous_scale=SCALE_BLUES,
        orientation="h",
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>Total sales: <b>$%{x:,.2f}</b>"
            "<br>Score: %{marker.color:.1f}<extra></extra>"
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


def create_employee_ranking_chart(perf_df):
    """Create scatter plot for employee ranking."""
    fig = px.scatter(
        perf_df,
        x="customer_count",
        y="avg_order_value",
        size="total_sales",
        color="performance_score",
        title="🏆 Employee Performance Matrix",
        labels={
            "customer_count": "Number of Customers",
            "avg_order_value": "Average Order Value ($)",
            "performance_score": "Performance Score",
        },
        color_continuous_scale=SCALE_VIRIDIS,
    )
    fig.update_traces(
        hovertemplate=(
            "Customers: <b>%{x:,}</b><br>Avg order: <b>$%{y:,.2f}</b>"
            "<br>Total sales: $%{marker.size:,.2f}<br>Score: %{marker.color:.1f}"
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


def create_territory_map(territory_df):
    """Create bar chart for territory revenue (simplified map)."""
    fig = px.bar(
        territory_df.head(TOP_N),
        x="total_revenue",
        y="country",
        title="🌍 Revenue by Territory",
        labels={"total_revenue": "Revenue ($)", "country": "Country"},
        color="total_revenue",
        color_continuous_scale=SCALE_GREENS,
        orientation="h",
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>Revenue: <b>$%{x:,.2f}</b><extra></extra>"
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


def create_customer_satisfaction_chart(customer_df):
    """Create chart for customer distribution by employee."""
    fig = px.pie(
        customer_df,
        values="customer_count",
        names="employee_name",
        title="👥 Customer Distribution by Employee",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{label}</b><br>Customers: <b>%{value:,}</b>"
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


def create_productivity_timeline(productivity_df):
    """Create timeline chart for productivity analysis."""
    fig = px.bar(
        productivity_df.head(TOP_N),
        x="orders_per_day",
        y="employee_name",
        color="efficiency_score",
        title="⚡ Daily Productivity Analysis",
        labels={"orders_per_day": "Orders per Day",
                "employee_name": "Employee"},
        color_continuous_scale=SCALE_PLASMA,
        orientation="h",
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>Orders/day: <b>%{x:,}</b>"
            "<br>Score: %{marker.color:.1f}<extra></extra>"
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


def create_team_comparison_chart(team_df):
    """Create comparison chart for team performance."""
    fig = px.bar(
        team_df,
        x="employee_name",
        y="customer_count",
        color="avg_customer_value",
        title="👥 Team Customer Management",
        labels={"customer_count": "Customer Count",
                "employee_name": "Employee"},
        color_continuous_scale=SCALE_BLUES,
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>Customers: <b>%{y:,}</b>"
            "<br>Avg value: $%{marker.color:,.2f}<extra></extra>"
        )
    )
    fig.update_layout(
        height=DEFAULT_CHART_HEIGHT,
        xaxis_tickangle=-45,
        hoverlabel=dict(
            bgcolor=HOVER_BG_COLOR, bordercolor=HOVER_BORDER_COLOR,
            font_size=HOVER_FONT_SIZE,
        ),
    )
    return fig


def create_sales_trend_chart(sales_df):
    """Create line chart for sales trends by employee."""
    fig = px.line(
        sales_df,
        x="month",
        y="total_revenue",
        color="employee_name",
        title="📈 Sales Trends by Employee",
        labels={"total_revenue": "Revenue ($)", "month": "Month"},
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>Revenue: <b>$%{y:,.2f}</b><extra></extra>"
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


def create_performance_radar_chart(perf_df):
    """Create radar chart for the top employee performance profile."""
    top_employee = perf_df.iloc[0]

    categories = ["Sales", "Customers", "Orders", "Avg Order"]
    values = [
        top_employee["total_sales"] / perf_df["total_sales"].max() * 100,
        top_employee["customer_count"] / perf_df["customer_count"].max() * 100,
        top_employee["order_count"] / perf_df["order_count"].max() * 100,
        top_employee["avg_order_value"] /
        perf_df["avg_order_value"].max() * 100,
    ]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            name=top_employee["employee_name"],
        )
    )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        title="🎯 Top Employee Performance Profile",
        height=DEFAULT_CHART_HEIGHT,
    )
    return fig


def create_workload_distribution_chart(workload_df):
    """Create chart for workload distribution by role."""
    fig = px.box(
        workload_df,
        x="title",
        y="customer_count",
        title="⚖️ Workload Distribution by Role",
        labels={"customer_count": "Customer Count", "title": "Job Title"},
    )
    fig.update_traces(
        hovertemplate=(
            "Role: <b>%{x}</b><br>Customers: <b>%{y:,}</b><extra></extra>"
        )
    )
    fig.update_layout(
        height=DEFAULT_CHART_HEIGHT,
        xaxis_tickangle=-45,
        hoverlabel=dict(
            bgcolor=HOVER_BG_COLOR, bordercolor=HOVER_BORDER_COLOR,
            font_size=HOVER_FONT_SIZE,
        ),
    )
    return fig


def create_efficiency_heatmap(efficiency_df):
    """Create heatmap for efficiency analysis."""
    efficiency_matrix = efficiency_df.pivot_table(
        index="employee_name",
        columns="metric_type",
        values="efficiency_value",
        fill_value=0,
    )

    fig = px.imshow(
        efficiency_matrix,
        text_auto=True,
        aspect="auto",
        title="🔥 Employee Efficiency Heatmap",
        color_continuous_scale="RdYlGn",
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{x}</b> - <b>%{y}</b><br>Efficiency: <b>%{z:.2f}</b>"
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