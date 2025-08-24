"""Constants used by the customers analytics module."""

from src.ui.constants import (
    DEFAULT_CHART_HEIGHT,
    HOVER_BG_COLOR,
    HOVER_BORDER_COLOR,
    HOVER_FONT_SIZE,
)

# Color schemes
CHURN_COLORS = {
    "Active": "#2ecc71",
    "At Risk": "#f39c12",
    "Churn Risk": "#e74c3c",
}

# Analysis thresholds
CHURN_MONTHS_DEFAULT = 6
TOP_CLIENTS_LIMIT = 3

# Musical profile thresholds
ECLECTIC_GENRES = 8
ECLECTIC_TRACKS = 30
DIVERSIFIED_GENRES = 5
DIVERSIFIED_TRACKS = 15
SELECTIVE_GENRES = 3
SELECTIVE_TRACKS = 8
SPECIALIZED_GENRES = 2
SPECIALIZED_TRACKS = 5
EXPLORER_GENRES = 4
EXPLORER_TRACKS = 15
OCCASIONAL_TRACKS = 5

# Listening profile thresholds (minutes)
MUSIC_LOVER_MINUTES = 500
AMATEUR_MINUTES = 200
OCCASIONAL_MINUTES = 100 