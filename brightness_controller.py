"""
Brightness Controller Module

Handles system brightness control with error handling and smoothing.
Provides a cross-platform interface for setting screen brightness.
"""

import screen_brightness_control as sbc
import numpy as np
import config


class BrightnessController:
    """
    Controls system screen brightness based on gesture input.
    
    This class manages brightness changes with optional smoothing,
    error handling, and bounds checking.
    """
    
    def __init__(self):
        """
        Initialize the brightness controller.
        
        Raises:
            RuntimeError: If brightness control is unavailable on this system.
        """
        self.current_brightness = self._get_current_brightness()
        self.previous_brightness = self.current_brightness
        self.min_brightness = config.MIN_BRIGHTNESS
        self.max_brightness = config.MAX_BRIGHTNESS
        self.smoothing_factor = config.SMOOTHING_FACTOR
        self.smooth_enabled = config.SMOOTH_BRIGHTNESS
    
    def _get_current_brightness(self):
        """
        Get current system brightness.
        
        Returns:
            float: Current brightness level (0-100), or None if unavailable.
        """
        try:
            brightness = sbc.get_brightness()
            if isinstance(brightness, list):
                return brightness[0]  # Get first display
            return float(brightness)
        except Exception as e:
            print(f"Warning: Could not read current brightness: {e}")
            return 50.0  # Default to 50%
    
    def map_distance_to_brightness(self, distance):
        """
        Map finger distance to brightness level using linear interpolation.
        
        Args:
            distance (float): Distance between fingers in pixels.
            
        Returns:
            float: Brightness level (0-100).
        """
        if distance is None:
            return self.current_brightness
        
        # Linear interpolation from distance range to brightness range
        brightness = np.interp(
            distance,
            [config.MIN_DISTANCE, config.MAX_DISTANCE],
            [self.min_brightness, self.max_brightness]
        )
        
        return brightness
    
    def apply_smoothing(self, target_brightness):
        """
        Apply exponential smoothing to brightness changes.
        
        This creates smoother transitions instead of abrupt jumps.
        
        Args:
            target_brightness (float): Target brightness level.
            
        Returns:
            float: Smoothed brightness level.
        """
        if not self.smooth_enabled:
            return target_brightness
        
        # Exponential moving average
        smoothed = (
            self.smoothing_factor * target_brightness +
            (1 - self.smoothing_factor) * self.previous_brightness
        )
        
        return smoothed
    
    def set_brightness(self, distance):
        """
        Set system brightness based on finger distance.
        
        Args:
            distance (float): Distance between fingers in pixels.
            
        Returns:
            float: Applied brightness level (0-100), or None on error.
        """
        try:
            # Map distance to brightness
            target_brightness = self.map_distance_to_brightness(distance)
            
            # Apply smoothing
            brightness = self.apply_smoothing(target_brightness)
            
            # Clamp to valid range
            brightness = np.clip(brightness, self.min_brightness, self.max_brightness)
            
            # Convert to int for setting
            brightness_int = int(brightness)
            
            # Set brightness on all displays
            sbc.set_brightness(brightness_int)
            
            # Update state
            self.previous_brightness = brightness
            self.current_brightness = brightness
            
            return brightness
        
        except Exception as e:
            print(f"Error setting brightness: {e}")
            return None
    
    def get_brightness(self):
        """
        Get current brightness level.
        
        Returns:
            float: Current brightness level (0-100).
        """
        return self._get_current_brightness()
    
    def reset(self):
        """Reset brightness controller to defaults."""
        self.current_brightness = self._get_current_brightness()
        self.previous_brightness = self.current_brightness
