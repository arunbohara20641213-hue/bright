"""
Configuration constants for the Bright application.
Centralized settings for gesture detection, display, and brightness control.
"""

# ============================================================================
# MEDIAPIPE HAND DETECTION SETTINGS
# ============================================================================
HAND_DETECTION_CONFIDENCE = 0.75
"""Minimum confidence threshold for detecting hands (0.0-1.0)."""

HAND_TRACKING_CONFIDENCE = 0.75
"""Minimum confidence threshold for tracking hands (0.0-1.0)."""

MAX_NUM_HANDS = 2
"""Maximum number of hands to detect simultaneously."""

HAND_MODEL_COMPLEXITY = 1
"""MediaPipe model complexity: 0 (lite) or 1 (full)."""

# ============================================================================
# FINGER DISTANCE & BRIGHTNESS MAPPING
# ============================================================================
MIN_DISTANCE = 15
"""Minimum distance between fingers (in pixels) - maps to 0% brightness."""

MAX_DISTANCE = 220
"""Maximum distance between fingers (in pixels) - maps to 100% brightness."""

MIN_BRIGHTNESS = 0
"""Minimum brightness level (0%)."""

MAX_BRIGHTNESS = 100
"""Maximum brightness level (100%)."""

# ============================================================================
# DISPLAY & VISUAL SETTINGS
# ============================================================================
DISPLAY_WINDOW_NAME = "Bright - Gesture Brightness Control"
"""Name of the OpenCV display window."""

CIRCLE_RADIUS = 7
"""Radius of circles drawn on finger positions (pixels)."""

CIRCLE_COLOR = (0, 255, 0)  # BGR format
"""Color of finger indicator circles (BGR format)."""

LINE_COLOR = (0, 255, 0)  # BGR format
"""Color of distance line between fingers (BGR format)."""

LINE_THICKNESS = 3
"""Thickness of the distance line (pixels)."""

FONT = "FONT_HERSHEY_SIMPLEX"
"""Font for on-screen text."""

FONT_SCALE = 0.7
"""Font scale for on-screen text."""

TEXT_COLOR = (255, 255, 255)  # BGR format (white)
"""Color for on-screen text (BGR format)."""

TEXT_THICKNESS = 2
"""Thickness of text lines."""

# ============================================================================
# CAMERA SETTINGS
# ============================================================================
CAMERA_INDEX = 0
"""Camera device index (0 = default/built-in camera)."""

FRAME_WIDTH = None
"""Frame width (None = use camera default)."""

FRAME_HEIGHT = None
"""Frame height (None = use camera default)."""

FPS = 30
"""Target frames per second."""

# ============================================================================
# CONTROL KEYS
# ============================================================================
EXIT_KEY = 'q'
"""Key to press for graceful exit (lowercase)."""

HELP_KEY = 'h'
"""Key to press to toggle help text."""

RESET_KEY = 'r'
"""Key to reset/recalibrate settings."""

# ============================================================================
# HAND LANDMARKS
# ============================================================================
# Reference: MediaPipe hand landmarks
# 0: Wrist, 4: Thumb tip, 5: Index base, 8: Index tip, etc.
THUMB_TIP = 4
"""Landmark ID for thumb tip."""

INDEX_TIP = 8
"""Landmark ID for index finger tip."""

# ============================================================================
# UI & FEEDBACK
# ============================================================================
SHOW_FPS = True
"""Display frame rate in the window."""

SHOW_BRIGHTNESS_BAR = True
"""Display brightness bar in the window."""

BRIGHTNESS_BAR_HEIGHT = 30
"""Height of brightness bar (pixels)."""

BRIGHTNESS_BAR_WIDTH = 300
"""Width of brightness bar (pixels)."""

# ============================================================================
# PERFORMANCE SETTINGS
# ============================================================================
SMOOTH_BRIGHTNESS = True
"""Enable smoothing of brightness changes."""

SMOOTHING_FACTOR = 0.1
"""Factor for exponential smoothing (0.0-1.0, lower = more smoothing)."""

# ============================================================================
# LOGGING
# ============================================================================
DEBUG_MODE = False
"""Enable debug output to console."""

LOG_FILE = "bright_debug.log"
"""Log file location for debugging."""
