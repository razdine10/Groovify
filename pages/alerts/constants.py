"""Constants used by the alerts analytics module."""

from src.ui.constants import (
    DEFAULT_CHART_HEIGHT,
    HOVER_BG_COLOR,
    HOVER_BORDER_COLOR,
    HOVER_FONT_SIZE,
)

# Alert thresholds
MIN_SALES_THRESHOLD = 3
ALBUM_SALES_THRESHOLD = 5
TRACK_LIMIT = 25
ALBUM_LIMIT = 20

# Revenue anomaly detection
REVENUE_ANALYSIS_DAYS = 30
CRITICAL_DROP_THRESHOLD = 30
WARNING_DROP_THRESHOLD = 15

# Customer churn thresholds
CHURN_DAYS_THRESHOLD = 180
HIGH_VALUE_CUSTOMER_MIN = 50
MEDIUM_VALUE_CUSTOMER_MIN = 25

# Performance thresholds
LOW_PERFORMANCE_ORDERS = 30
MEDIUM_PERFORMANCE_ORDERS = 50
HIGH_PERFORMANCE_ORDERS = 100

# Fraud detection
FRAUD_AMOUNT_THRESHOLD = 100
SUSPICIOUS_ITEMS_THRESHOLD = 15
BULK_PURCHASE_THRESHOLD = 20
HIGH_VALUE_SINGLE_ITEM = 50

# Alert severity colors
SEVERITY_COLORS = {
    "Critical": "#dc3545",
    "Warning": "#ffc107",
    "Normal": "#28a745",
    "Good": "#17a2b8",
}

# Risk level colors
RISK_COLORS = {
    "High": "#dc3545",
    "Medium": "#ffc107",
    "Low": "#28a745",
    "Active": "#17a2b8",
}

# Alert categories
ALERT_CATEGORIES = ["Revenue", "Customer", "Inventory", "Performance"] 