# ================= config.py ==================

# Window setup
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
CENTER_X = WINDOW_WIDTH // 2
CENTER_Y = WINDOW_HEIGHT // 2
CIRCLE_RADIUS = 120
DOT_COUNT = 19   # EEG 10-20 standard positions

# Colors - Enhanced aesthetic
COLOR_BG = "#0A0E27"  # Deep blue-black
COLOR_CIRCLE_OUTLINE = "#4A90E2"  # Soft blue
COLOR_CIRCLE_GLOW = "#2A5F9E"  # Darker blue for inner circle
COLOR_BOX_INACTIVE = "#2C3E50"  # Slate gray
COLOR_BOX_GAZE = "#00FF88"    # Bright green
COLOR_BOX_NEURO = "#A855F7"   # Purple
COLOR_PROGRESS_BG = "#1A1A2E"
COLOR_PROGRESS_FILL = "#00D9FF"  # Cyan
COLOR_DOT_GLOW = "#FFFFFF"  # White glow

# Dot appearance - More vibrant colors
DOT_RADIUS = 4.0
DOT_COLORS = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8", "#F7DC6F"]

# Animation timing
UPDATE_INTERVAL = 16  # ~60fps for smoother animation
HOVER_THRESHOLD_OPTIONS = [1.0, 1.5, 2.0, 2.5, 3.0]  # Configurable hover times
DEFAULT_HOVER_THRESHOLD = 2.0
RETURN_DELAY = 0.3  # seconds before dots return when focus lost

# Progress settings
PROGRESS_DECAY = 30.0  # percent per second decay rate

# Layout of 8 stimulus boxes
BOX_POSITIONS = {
    1: (-280, -240),
    2: (0, -240),
    3: (280, -240),
    4: (-380, 0),
    5: (380, 0),
    6: (-280, 240),
    7: (0, 240),
    8: (280, 240),
}

BOX_WIDTH = 130
BOX_HEIGHT = 90

# Responsiveness
BASE_WIDTH = 1200
BASE_HEIGHT = 700

# Input modes
INPUT_MODE_MOUSE = "Mouse (Manual)"
INPUT_MODE_TOBII = "Tobii Eye Tracker"
INPUT_MODES = [INPUT_MODE_MOUSE, INPUT_MODE_TOBII]

# UI Control panel
CONTROL_PANEL_HEIGHT = 50
CONTROL_PANEL_BG = "#1A1A2E"
DROPDOWN_BG = "#2C3E50"
DROPDOWN_FG = "#FFFFFF"