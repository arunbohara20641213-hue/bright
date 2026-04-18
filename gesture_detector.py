"""
Gesture Detection Module

Handles hand tracking and gesture recognition using MediaPipe.
Provides functionality to detect hand landmarks and calculate distances between fingers.
"""

import cv2
import mediapipe as mp
from math import hypot
import config


class GestureDetector:
    """
    Detects hand gestures using MediaPipe hand tracking.
    
    This class wraps MediaPipe's hand detection and provides convenient methods
    for extracting hand landmarks and calculating distances between fingers.
    """
    
    def __init__(self):
        """Initialize MediaPipe hand detector."""
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        
        try:
            self.hands = self.mp_hands.Hands(
                static_image_mode=False,
                model_complexity=config.HAND_MODEL_COMPLEXITY,
                min_detection_confidence=config.HAND_DETECTION_CONFIDENCE,
                min_tracking_confidence=config.HAND_TRACKING_CONFIDENCE,
                max_num_hands=config.MAX_NUM_HANDS
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize MediaPipe hands: {e}")
    
    def process_frame(self, frame):
        """
        Process a video frame to detect hands.
        
        Args:
            frame (numpy.ndarray): Input frame from video capture (BGR format).
            
        Returns:
            tuple: (frame_rgb, results) where results contains hand landmarks.
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        return frame_rgb, results
    
    def get_hand_landmarks(self, frame, results):
        """
        Extract hand landmarks from detection results.
        
        Args:
            frame (numpy.ndarray): Original video frame.
            results: MediaPipe hand detection results.
            
        Returns:
            list: List of hand landmarks. Each landmark is [id, x, y].
        """
        landmarks = []
        
        if results.multi_hand_landmarks:
            height, width = frame.shape[:2]
            
            for hand_landmarks in results.multi_hand_landmarks:
                for landmark_id, landmark in enumerate(hand_landmarks.landmark):
                    x = int(landmark.x * width)
                    y = int(landmark.y * height)
                    landmarks.append([landmark_id, x, y])
        
        return landmarks
    
    def draw_hand_landmarks(self, frame, results):
        """
        Draw hand skeleton and landmarks on the frame.
        
        Args:
            frame (numpy.ndarray): Input frame to draw on.
            results: MediaPipe hand detection results.
            
        Returns:
            numpy.ndarray: Frame with drawn landmarks.
        """
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
        
        return frame
    
    def get_finger_distance(self, landmarks, finger1_id, finger2_id):
        """
        Calculate Euclidean distance between two fingers.
        
        Args:
            landmarks (list): List of hand landmarks [id, x, y].
            finger1_id (int): MediaPipe landmark ID for first finger.
            finger2_id (int): MediaPipe landmark ID for second finger.
            
        Returns:
            float: Distance in pixels, or None if fingers not detected.
        """
        # Find the landmarks for the specified fingers
        finger1 = None
        finger2 = None
        
        for landmark in landmarks:
            if landmark[0] == finger1_id:
                finger1 = landmark
            if landmark[0] == finger2_id:
                finger2 = landmark
        
        # Calculate distance if both fingers are found
        if finger1 and finger2:
            x1, y1 = finger1[1], finger1[2]
            x2, y2 = finger2[1], finger2[2]
            distance = hypot(x2 - x1, y2 - y1)
            return distance
        
        return None
    
    def draw_finger_distance(self, frame, landmarks, finger1_id, finger2_id):
        """
        Draw circles and line connecting two fingers.
        
        Args:
            frame (numpy.ndarray): Frame to draw on.
            landmarks (list): List of hand landmarks.
            finger1_id (int): First finger landmark ID.
            finger2_id (int): Second finger landmark ID.
            
        Returns:
            numpy.ndarray: Frame with drawn distance visualization.
        """
        finger1 = None
        finger2 = None
        
        for landmark in landmarks:
            if landmark[0] == finger1_id:
                finger1 = landmark
            if landmark[0] == finger2_id:
                finger2 = landmark
        
        if finger1 and finger2:
            x1, y1 = finger1[1], finger1[2]
            x2, y2 = finger2[1], finger2[2]
            
            # Draw circles on finger tips
            cv2.circle(frame, (x1, y1), config.CIRCLE_RADIUS, 
                      config.CIRCLE_COLOR, cv2.FILLED)
            cv2.circle(frame, (x2, y2), config.CIRCLE_RADIUS, 
                      config.CIRCLE_COLOR, cv2.FILLED)
            
            # Draw line between fingers
            cv2.line(frame, (x1, y1), (x2, y2), 
                    config.LINE_COLOR, config.LINE_THICKNESS)
        
        return frame
    
    def release(self):
        """Release MediaPipe resources."""
        if self.hands:
            self.hands.close()
