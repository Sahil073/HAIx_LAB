# ================= CONFIGURATION ==================

# Window setup
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
CENTER_X = WINDOW_WIDTH // 2
CENTER_Y = WINDOW_HEIGHT // 2
CIRCLE_RADIUS = 90
DOT_COUNT = 120

# Colors
COLOR_BG = "#000000"
COLOR_CIRCLE_OUTLINE = "#A0A0A0"
COLOR_BOX_INACTIVE = "#404040"
COLOR_BOX_GAZE = "#00FF00"    # active (gaze) green
COLOR_BOX_NEURO = "#9400D3"   # neuro feedback (purple)
COLOR_PROGRESS_BG = "#1A1A1A"
COLOR_PROGRESS_FILL = "#00FFFF"  # cyan progress bar

# Dot appearance
DOT_RADIUS = 2.0  # slightly larger dots
DOT_COLORS = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00"]  # red, green, blue, yellow

# Progress animation
PROGRESS_SPEED = 1.8
PROGRESS_DECAY = 1.0
UPDATE_INTERVAL = 30  # ms per frame

# Layout of 8 stimulus boxes
BOX_POSITIONS = {
    1: (-250, -220),
    2: (0, -220),
    3: (250, -220),
    4: (-350, 0),
    5: (350, 0),
    6: (-250, 220),
    7: (0, 220),
    8: (250, 220),
}

BOX_WIDTH = 120
BOX_HEIGHT = 80
