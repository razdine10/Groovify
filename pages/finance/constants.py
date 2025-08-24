"""Finance module constants."""

# CSS class names
FINANCE_CONTAINER_CLASS = "finance-container"
FINANCE_HEADER_CLASS = "finance-header"
FINANCE_CARD_CLASS = "finance-card"
METRIC_ITEM_CLASS = "metric-item"

# Color constants
PRIMARY_COLOR = "#6D28D9"
SECONDARY_COLOR = "#8B5CF6"
ACCENT_COLOR = "#A78BFA"
SUCCESS_COLOR = "#10b981"
ERROR_COLOR = "#ef4444"
TEXT_MUTED = "#64748b"

# Time periods
DEFAULT_SHORT_PERIOD = 30
DEFAULT_MEDIUM_PERIOD = 90

# Chart configuration
CHART_HEIGHT = 400
COMPACT_CHART_HEIGHT = 350
SMALL_CHART_HEIGHT = 300

# Pagination and limits
TOP_COUNTRIES_LIMIT = 10
AUTO_SCROLL_DURATION = 25

# Amount ranges for invoice analysis
AMOUNT_RANGES = [
    (5, "< $5"),
    (10, "$5 - $10"),
    (20, "$10 - $20"),
    (50, "$20 - $50"),
    (float('inf'), "$50+")
]

# Days of week mapping
WEEKDAYS = {
    0: 'Sunday',
    1: 'Monday',
    2: 'Tuesday',
    3: 'Wednesday',
    4: 'Thursday',
    5: 'Friday',
    6: 'Saturday'
}

# Font family
FONT_FAMILY = "Inter"

# Page configuration
PAGE_TITLE = "Groovify - Finance"
PAGE_ICON = "💰" 