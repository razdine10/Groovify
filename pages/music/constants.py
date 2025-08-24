"""Constants used by the music analytics module."""

from src.ui.constants import (
    DEFAULT_CHART_HEIGHT,
    HOVER_BG_COLOR,
    HOVER_BORDER_COLOR,
    HOVER_FONT_SIZE,
)

# Query limits
TRACK_LIMIT = 100
ARTIST_LIMIT = 50
PLAYLIST_DISCOVERY_LIMIT = 50

# Performance thresholds
MIN_TRACK_SALES = 1
MIN_ARTIST_ALBUMS = 1
MIN_PLAYLIST_APPEARANCES = 1

# Data limits for visualization
TOP_ARTISTS_DISPLAY = 10
TOP_TRACKS_DISPLAY = 10
TOP_PLAYLISTS_DISPLAY = 10

# Duration analysis
DURATION_OUTLIER_PERCENTILE = 0.95

# Available genres for filtering
AVAILABLE_GENRES = [
    "Rock",
    "Latin", 
    "Metal",
    "Alternative & Punk",
    "Jazz",
    "Blues",
    "TV Shows",
    "Classical",
    "R&B/Soul",
    "Reggae",
]

# Color scales
SCALE_BLUES = "Blues"
SCALE_GREENS = "Greens"
SCALE_VIRIDIS = "Viridis"
SCALE_PLASMA = "Plasma"
SCALE_ORANGES = "Oranges"

# Analysis categories
MUSIC_CATEGORIES = [
    "🎵 Tracks & Albums",
    "👨‍🎤 Artists", 
    "🎧 Playlists",
    "💰 Revenue",
    "📈 Trends",
] 