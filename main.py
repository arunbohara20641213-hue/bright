"""
Bright - Gesture-Controlled Screen Brightness

A Python application that uses hand gesture recognition via webcam
to control system screen brightness in real-time.

Usage:
    python main.py

Controls:
    - Hand Gesture: Move fingers apart/together to adjust brightness
    - 'q': Quit the application
    - 'h': Toggle help text
    - 'r': Reset gesture calibration
"""

import cv2
import sys
import time
from datetime import datetime
import config
from gesture_detector import GestureDetector
from brightness_controller import BrightnessController


class BrightApplication:
    """
    Main application class for gesture-controlled brightness control.
    
    Manages the main loop, user input, and integration between
    gesture detection and brightness control.
    """
    
    def __init__(self):
        """Initialize the application."""
        self.gesture_detector = None
        self.brightness_controller = None
        self.cap = None
        self.running = False
        self.show_help = False
        self.fps_clock = 0
        self.frame_count = 0
        self.start_time = None
        
    def initialize(self):
        """
        Initialize all components.
        
        Returns:
            bool: True if initialization successful, False otherwise.
        """
        try:
            print("[INFO] Initializing Bright application...")
            
            # Initialize gesture detector
            print("[INFO] Initializing gesture detector...")
            self.gesture_detector = GestureDetector()
            
            # Initialize brightness controller
            print("[INFO] Initializing brightness controller...")
            self.brightness_controller = BrightnessController()
            
            # Initialize camera
            print("[INFO] Opening camera...")
            self.cap = cv2.VideoCapture(config.CAMERA_INDEX)
            
            if not self.cap.isOpened():
                print("[ERROR] Could not open camera. Check if webcam is available.")
                return False
            
            # Set camera properties
            if config.FRAME_WIDTH:
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
            if config.FRAME_HEIGHT:
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
            
            self.running = True
            self.start_time = time.time()
            print("[INFO] Initialization successful!")
            print(f"[INFO] Press '{config.EXIT_KEY}' to quit, '{config.HELP_KEY}' for help")
            
            return True
        
        except Exception as e:
            print(f"[ERROR] Initialization failed: {e}")
            return False
    
    def handle_key_press(self, key):
        """
        Handle keyboard input.
        
        Args:
            key (int): OpenCV key code.
            
        Returns:
            bool: False if application should exit, True otherwise.
        """
        if key == -1:
            return True  # No key pressed
        
        # Convert to lowercase character
        char = chr(key & 0xFF).lower()
        
        if char == config.EXIT_KEY:
            print(f"\n[INFO] '{config.EXIT_KEY}' pressed - exiting...")
            return False
        
        elif char == config.HELP_KEY:
            self.show_help = not self.show_help
            status = "enabled" if self.show_help else "disabled"
            print(f"[INFO] Help text {status}")
        
        elif char == config.RESET_KEY:
            print("[INFO] Resetting gesture calibration...")
            self.gesture_detector.release()
            self.gesture_detector = GestureDetector()
            self.brightness_controller.reset()
        
        return True
    
    def draw_ui(self, frame, landmarks, brightness):
        """
        Draw UI elements on the frame.
        
        Args:
            frame (numpy.ndarray): Video frame to draw on.
            landmarks (list): Hand landmarks.
            brightness (float): Current brightness level.
            
        Returns:
            numpy.ndarray: Frame with UI drawn.
        """
        height, width = frame.shape[:2]
        
        # Draw brightness bar
        if config.SHOW_BRIGHTNESS_BAR:
            frame = self._draw_brightness_bar(frame, brightness)
        
        # Draw FPS counter
        if config.SHOW_FPS:
            fps = self._calculate_fps()
            cv2.putText(
                frame,
                f"FPS: {fps:.1f}",
                (width - 150, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                config.FONT_SCALE,
                config.TEXT_COLOR,
                config.TEXT_THICKNESS
            )
        
        # Draw brightness level
        cv2.putText(
            frame,
            f"Brightness: {int(brightness)}%",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            config.FONT_SCALE,
            config.TEXT_COLOR,
            config.TEXT_THICKNESS
        )
        
        # Draw help text
        if self.show_help:
            frame = self._draw_help_text(frame)
        
        return frame
    
    def _draw_brightness_bar(self, frame, brightness):
        """
        Draw a visual brightness bar on the frame.
        
        Args:
            frame (numpy.ndarray): Video frame.
            brightness (float): Brightness level (0-100).
            
        Returns:
            numpy.ndarray: Frame with brightness bar.
        """
        height, width = frame.shape[:2]
        
        bar_x = (width - config.BRIGHTNESS_BAR_WIDTH) // 2
        bar_y = height - config.BRIGHTNESS_BAR_HEIGHT - 20
        
        # Background bar (gray)
        cv2.rectangle(
            frame,
            (bar_x, bar_y),
            (bar_x + config.BRIGHTNESS_BAR_WIDTH, bar_y + config.BRIGHTNESS_BAR_HEIGHT),
            (100, 100, 100),
            -1
        )
        
        # Brightness bar (green)
        brightness_width = int(config.BRIGHTNESS_BAR_WIDTH * (brightness / 100))
        cv2.rectangle(
            frame,
            (bar_x, bar_y),
            (bar_x + brightness_width, bar_y + config.BRIGHTNESS_BAR_HEIGHT),
            (0, 255, 0),
            -1
        )
        
        # Border
        cv2.rectangle(
            frame,
            (bar_x, bar_y),
            (bar_x + config.BRIGHTNESS_BAR_WIDTH, bar_y + config.BRIGHTNESS_BAR_HEIGHT),
            (255, 255, 255),
            2
        )
        
        return frame
    
    def _draw_help_text(self, frame):
        """Draw help text on the frame."""
        help_lines = [
            "=== CONTROLS ===",
            f"'{config.EXIT_KEY}' - Exit",
            f"'{config.HELP_KEY}' - Toggle help",
            f"'{config.RESET_KEY}' - Reset",
            "Spread/pinch fingers to control brightness"
        ]
        
        y_offset = 60
        for line in help_lines:
            cv2.putText(
                frame,
                line,
                (10, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 255),
                1
            )
            y_offset += 25
        
        return frame
    
    def _calculate_fps(self):
        """
        Calculate frames per second.
        
        Returns:
            float: Current FPS.
        """
        self.frame_count += 1
        elapsed = time.time() - self.start_time
        
        if elapsed > 0:
            return self.frame_count / elapsed
        return 0
    
    def run(self):
        """
        Main application loop.
        
        Processes video frames, detects gestures, and controls brightness.
        """
        if not self.initialize():
            return
        
        try:
            while self.running:
                # Read frame from camera
                ret, frame = self.cap.read()
                if not ret:
                    print("[ERROR] Failed to read frame from camera")
                    break
                
                # Flip frame for selfie-view
                frame = cv2.flip(frame, 1)
                
                # Process frame for hand detection
                frame_rgb, results = self.gesture_detector.process_frame(frame)
                
                # Get hand landmarks
                landmarks = self.gesture_detector.get_hand_landmarks(frame, results)
                
                # Draw hand skeleton
                frame = self.gesture_detector.draw_hand_landmarks(frame, results)
                
                # Calculate brightness based on gesture
                brightness = self.brightness_controller.current_brightness
                
                if landmarks:
                    # Calculate distance between thumb and index finger
                    distance = self.gesture_detector.get_finger_distance(
                        landmarks,
                        config.THUMB_TIP,
                        config.INDEX_TIP
                    )
                    
                    # Set brightness based on distance
                    if distance is not None:
                        brightness = self.brightness_controller.set_brightness(distance)
                        if brightness is None:
                            brightness = self.brightness_controller.current_brightness
                    
                    # Draw distance visualization
                    frame = self.gesture_detector.draw_finger_distance(
                        frame,
                        landmarks,
                        config.THUMB_TIP,
                        config.INDEX_TIP
                    )
                
                # Draw UI elements
                frame = self.draw_ui(frame, landmarks, brightness)
                
                # Display frame
                cv2.imshow(config.DISPLAY_WINDOW_NAME, frame)
                
                # Handle user input
                key = cv2.waitKey(1) & 0xFF
                if not self.handle_key_press(key):
                    break
        
        except KeyboardInterrupt:
            print("\n[INFO] Interrupted by user")
        except Exception as e:
            print(f"[ERROR] Application error: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        print("[INFO] Cleaning up resources...")
        
        if self.cap:
            self.cap.release()
        
        if self.gesture_detector:
            self.gesture_detector.release()
        
        cv2.destroyAllWindows()
        print("[INFO] Cleanup complete. Goodbye!")


def main():
    """Entry point for the application."""
    app = BrightApplication()
    app.run()


if __name__ == "__main__":
    main()
