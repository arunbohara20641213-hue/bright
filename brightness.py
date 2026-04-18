"""
Bright - Gesture-Controlled Screen Brightness [LEGACY ENTRY POINT]

This file is maintained for backward compatibility.
For new usage, please use: python main.py

The application has been refactored into modular components:
- main.py: Main application entry point
- gesture_detector.py: Hand gesture detection
- brightness_controller.py: Brightness control logic
- config.py: Configuration constants

This entry point simply delegates to the new main.py module.
"""

import sys

# Import and run the main application
if __name__ == "__main__":
    try:
        from main import main
        main()
    except ImportError as e:
        print(f"Error: Could not import main module. {e}")
        print("Please ensure all required modules are in the same directory.")
        sys.exit(1)
    except Exception as e:
        print(f"Error running application: {e}")
        sys.exit(1)