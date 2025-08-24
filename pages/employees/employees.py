from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

from utils import apply_sidebar_logo, run_query
from pages.employees.queries import (
    get_customer_management_query,
    get_date_bounds_query,
    get_employee_performance_query,
    get_employee_productivity_query,
    get_sales_by_employee_query,
    get_team_hierarchy_query,
    get_territory_analysis_query,
)
from pages.employees.visualization import (
    create_metric_bar_chart,
)


st.set_page_config(
    page_title="Employee Analytics", page_icon="👔", layout="wide"
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
  <h1 class="header-title">👔 Employee Analytics</h1>
  <p class="header-subtitle">
    Performance • Sales • Productivity • Team Management
  </p>
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

# Global filters in sidebar
with st.sidebar:
    st.markdown("### 📅 Analysis Filters")
    date_range = st.date_input(
        "Analysis Period",
        value=(min_d, max_d),
        min_value=min_d,
        max_value=max_d,
        key="employee_dates",
    )
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_d, end_d = date_range
    else:
        start_d, end_d = min_d, max_d

    # Additional filters
    sales_metric = st.selectbox(
        "Sales Focus",
        ["Revenue", "Volume", "Customer Count", "Average Order"],
        key="sales_metric",
    )

# ========================================
# MAIN ANALYTICS DASHBOARD
# ========================================

# Global KPIs
st.markdown("### 📊 Employee Performance Overview")

try:
    # Load all data
    sales_df = run_query(get_sales_by_employee_query(), (start_d, end_d))
    perf_df = run_query(
        get_employee_performance_query(), (start_d, end_d)
    )
    hierarchy_df = run_query(get_team_hierarchy_query())

    if not sales_df.empty:
        # Main KPIs Row (without Total Revenue)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Total Employees",
                len(hierarchy_df) if not hierarchy_df.empty else len(sales_df),
            )
        with col2:
            st.metric("Total Orders", f"{sales_df['order_count'].sum():,}")
        with col3:
            avg_revenue = sales_df["total_revenue"].mean()
            st.metric("Avg Revenue/Employee", f"${avg_revenue:,.2f}")
        with col4:
            top_performer = sales_df["total_revenue"].max()
            st.metric("Top Performer", f"${top_performer:,.2f}")

        st.markdown("---")

        # ========================================
        # SALES ANALYSIS - MAIN SECTION
        # ========================================
        st.markdown("### 💰 Sales Performance Analysis")

        # Sales metric selection and analysis
        if sales_metric == "Revenue":
            sorted_df = sales_df.sort_values(
                "total_revenue", ascending=False
            )
            metric_col = "total_revenue"
            title = "💰 Revenue Performance by Employee"
        elif sales_metric == "Volume":
            sorted_df = sales_df.sort_values("order_count", ascending=False)
            metric_col = "order_count"
            title = "📦 Order Volume Performance by Employee"
        elif sales_metric == "Customer Count":
            sorted_df = sales_df.sort_values(
                "unique_customers", ascending=False
            )
            metric_col = "unique_customers"
            title = "👥 Customer Acquisition Performance"
        else:
            sorted_df = sales_df.sort_values(
                "avg_order_value", ascending=False
            )
            metric_col = "avg_order_value"
            title = "💎 Average Order Value Performance"

        # Sales chart and top performers list
        col_chart, col_list = st.columns([2, 1])
        with col_chart:
            fig = create_metric_bar_chart(
                sorted_df, metric_col, "employee_name", title, "Blues"
            )
            st.plotly_chart(fig, use_container_width=True)
        with col_list:
            st.markdown("#### 🏆 Top Performers")
            top5 = sorted_df.head(5)
            for i, (_, row) in enumerate(top5.iterrows()):
                if sales_metric == "Revenue":
                    st.write(
                        f"{i+1}. **{row['employee_name']}** - "
                        f"${row[metric_col]:,.2f}"
                    )
                elif sales_metric == "Volume":
                    st.write(
                        f"{i+1}. **{row['employee_name']}** - "
                        f"{row[metric_col]:,} orders"
                    )
                elif sales_metric == "Customer Count":
                    st.write(
                        f"{i+1}. **{row['employee_name']}** - "
                        f"{row[metric_col]:,} customers"
                    )
                else:
                    st.write(
                        f"{i+1}. **{row['employee_name']}** - "
                        f"${row[metric_col]:,.2f}"
                    )

        # ========================================
        # DETAILED SALES TABLE
        # ========================================
        st.markdown("### 📊 All Employees")

        # Get all employees and merge with sales data
        if not hierarchy_df.empty:
            # Merge hierarchy with sales data (left join to keep all employees)
            all_employees_df = hierarchy_df.merge(
                sales_df[
                    [
                        "employee_name",
                        "total_revenue",
                        "order_count",
                        "unique_customers",
                        "avg_order_value",
                    ]
                ],
                left_on="employee_name",
                right_on="employee_name",
                how="left",
            )

            # Fill NaN values for employees without sales
            all_employees_df["total_revenue"] = (
                all_employees_df["total_revenue"].fillna(0)
            )
            all_employees_df["order_count"] = (
                all_employees_df["order_count"].fillna(0).astype(int)
            )
            all_employees_df["unique_customers"] = (
                all_employees_df["unique_customers"].fillna(0).astype(int)
            )
            all_employees_df["avg_order_value"] = (
                all_employees_df["avg_order_value"].fillna(0)
            )

            # Display table with all employees
            display_df = all_employees_df[
                [
                    "employee_name",
                    "title",
                    "city",
                    "country",
                    "total_revenue",
                    "order_count",
                    "unique_customers",
                    "avg_order_value",
                ]
            ].copy()
            display_df = display_df.rename(
                columns={
                    "employee_name": "Employee",
                    "title": "Position",
                    "city": "City",
                    "country": "Country",
                    "total_revenue": "Total Revenue ($)",
                    "order_count": "Orders",
                    "unique_customers": "Customers",
                    "avg_order_value": "Avg Order ($)",
                }
            )
            display_df = display_df.sort_values(
                "Total Revenue ($)", ascending=False
            )
            display_df.insert(0, "#", range(1, len(display_df) + 1))
            st.dataframe(
                display_df, use_container_width=True, hide_index=True
            )
        else:
            # Fallback to sales data only if hierarchy is empty
            display_df = sales_df[
                [
                    "employee_name",
                    "title",
                    "total_revenue",
                    "order_count",
                    "unique_customers",
                    "avg_order_value",
                ]
            ].copy()
            display_df = display_df.rename(
                columns={
                    "employee_name": "Employee",
                    "title": "Position",
                    "total_revenue": "Total Revenue ($)",
                    "order_count": "Orders",
                    "unique_customers": "Customers",
                    "avg_order_value": "Avg Order ($)",
                }
            )
            display_df = display_df.sort_values(
                "Total Revenue ($)", ascending=False
            )
            display_df.insert(0, "#", range(1, len(display_df) + 1))
            st.dataframe(
                display_df, use_container_width=True, hide_index=True
            )

    else:
        st.warning("No employee data available for the selected period.")

except Exception as e:  # noqa: BLE001
    st.error(f"Error loading employee analytics: {e}")

# Footer
from src.utils.ui_components import render_footer
render_footer() 