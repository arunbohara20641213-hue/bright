# Bright ✨  
**Gesture-Controlled Screen Brightness using Computer Vision**

Bright is a Python-based computer vision project that allows users to control their system's screen brightness using simple hand gestures captured through a webcam. It leverages OpenCV and MediaPipe for real-time hand tracking and maps finger distance to brightness levels.

---

## 🎯 Features

- ✅ Real-time webcam-based hand tracking  
- ✅ Thumb–index finger distance controls brightness  
- ✅ Smooth brightness adjustment (0–100%)  
- ✅ Visual feedback with brightness bar and FPS counter
- ✅ Error handling and cross-platform compatibility
- ✅ Configurable settings and calibration options
- ✅ Modular, well-documented codebase  
- ✅ Fast, lightweight, and responsive  
- ✅ No external hardware required  

---

## 🛠️ Technologies Used

| Component | Purpose |
|-----------|---------|
| **Python 3.7+** | Core language |
| **OpenCV** | Video capture and frame processing |
| **MediaPipe** | Hand pose detection and tracking |
| **NumPy** | Numerical computations |
| **screen-brightness-control** | System brightness control |

---

## 📋 Project Structure

```
bright/
├── main.py                      # Main application entry point
├── brightness.py                # Backward-compatible wrapper
├── config.py                    # Configuration constants
├── gesture_detector.py           # Hand detection module
├── brightness_controller.py      # Brightness control module
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

### Module Descriptions

| Module | Responsibility |
|--------|-----------------|
| **main.py** | Application loop, UI rendering, user input handling |
| **config.py** | Centralized configuration constants (distances, colors, thresholds) |
| **gesture_detector.py** | MediaPipe integration, hand landmark extraction, visualization |
| **brightness_controller.py** | Brightness mapping, smoothing, system control |
| **brightness.py** | Legacy entry point (delegates to main.py) |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Working webcam
- Windows, macOS, or Linux

### Installation

1. **Clone or download this repository:**
   ```bash
   cd bright
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or manually:
   ```bash
   pip install opencv-python mediapipe numpy screen-brightness-control
   ```

### Running the Application

**Start the application:**
```bash
python main.py
```

Or use the legacy entry point:
```bash
python brightness.py
```

---

## 🎮 Controls

### Hand Gestures
- **Pinch**: Bring thumb and index finger together → **Decrease brightness**
- **Spread**: Move thumb and index finger apart → **Increase brightness**

### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| **q** | Quit application |
| **h** | Toggle help text on screen |
| **r** | Reset gesture calibration |

---

## ⚙️ Configuration

All settings are centralized in `config.py`. You can customize:

### Hand Detection
```python
HAND_DETECTION_CONFIDENCE = 0.75      # Detection threshold (0.0-1.0)
HAND_TRACKING_CONFIDENCE = 0.75       # Tracking threshold (0.0-1.0)
HAND_MODEL_COMPLEXITY = 1             # 0=lite, 1=full
MAX_NUM_HANDS = 2                     # Maximum hands to detect
```

### Distance & Brightness Mapping
```python
MIN_DISTANCE = 15                     # Distance for 0% brightness
MAX_DISTANCE = 220                    # Distance for 100% brightness
```

### Visual Feedback
```python
SHOW_FPS = True                       # Display FPS counter
SHOW_BRIGHTNESS_BAR = True            # Display brightness bar
```

### Performance
```python
SMOOTH_BRIGHTNESS = True              # Enable smoothing
SMOOTHING_FACTOR = 0.1                # Smoothing strength (lower = more)
```

For a complete list of configurable options, see `config.py`.

---

## 📖 Usage Examples

### Example 1: Basic Usage
```bash
python main.py
```
Press 'q' to exit.

### Example 2: Calibration
If gestures don't map correctly:
1. Press 'r' to reset calibration
2. Pinch your fingers to minimum (very close) - this should set ~0% brightness
3. Spread your fingers to maximum (full arm span) - this should set ~100% brightness

### Example 3: Adjust Distance Mapping
Edit `config.py` to customize the distance range:
```python
# Tighter control (more sensitive)
MIN_DISTANCE = 10
MAX_DISTANCE = 150

# Looser control (less sensitive)
MIN_DISTANCE = 30
MAX_DISTANCE = 300
```

---

## 🔧 Troubleshooting

### Camera Not Found
- **Symptom**: "Could not open camera" error
- **Solution**: 
  - Check if webcam is connected and working
  - Try a different camera index in `config.py`: `CAMERA_INDEX = 1`
  - Ensure no other application is using the camera

### Brightness Not Changing
- **Symptom**: Hand moves but brightness stays same
- **Solution**:
  - Ensure good lighting for hand detection
  - Check if brightness control is available on your system
  - Try pressing 'r' to reset calibration
  - Verify distance values in `config.py` match your hand size

### Poor Hand Detection
- **Symptom**: Hand landmarks not appearing
- **Solution**:
  - Ensure good lighting (avoid backlighting)
  - Keep hand fully visible in frame
  - Reduce `HAND_DETECTION_CONFIDENCE` in `config.py` (e.g., 0.5)
  - Clean webcam lens

### Jittery Brightness Changes
- **Symptom**: Brightness flickering
- **Solution**:
  - Enable smoothing: Set `SMOOTH_BRIGHTNESS = True`
  - Increase `SMOOTHING_FACTOR` (e.g., 0.2 or 0.3)
  - Reduce `HAND_TRACKING_CONFIDENCE` slightly

### Cross-Platform Issues
- **macOS**: Brightness control may require System Preferences access
- **Linux**: Install `python3-xlib` for brightness control
- **Windows**: Works out of the box on most systems

---

## 📊 How It Works

### Detection Pipeline
```
Video Frame
    ↓
OpenCV Capture
    ↓
MediaPipe Hand Detection
    ↓
Landmark Extraction (21 points per hand)
    ↓
Distance Calculation (Thumb ↔ Index)
    ↓
Linear Interpolation to Brightness
    ↓
Smoothing Filter (optional)
    ↓
System Brightness Control
```

### Distance-to-Brightness Mapping
The application uses linear interpolation:
```
distance ∈ [MIN_DISTANCE, MAX_DISTANCE] → brightness ∈ [0%, 100%]
```

Example with defaults:
- Distance = 15 pixels → Brightness = 0%
- Distance = 120 pixels → Brightness = ~50%
- Distance = 220 pixels → Brightness = 100%

---

## 🎓 Code Quality

The codebase is designed for:
- **Readability**: Clear function names and comprehensive docstrings
- **Maintainability**: Modular architecture with single responsibility principle
- **Robustness**: Error handling and graceful degradation
- **Extensibility**: Easy to add new features (volume control, etc.)

### Hand Landmarks Reference
MediaPipe provides 21 landmarks per hand:
- 0: Wrist
- 1-4: Thumb (base to tip)
- 5-8: Index finger (base to tip)
- 9-12: Middle finger (base to tip)
- 13-16: Ring finger (base to tip)
- 17-20: Pinky finger (base to tip)

Current implementation uses:
- **Landmark 4**: Thumb tip
- **Landmark 8**: Index finger tip

---

## 💡 Future Enhancements

Potential improvements:
- [ ] Multi-gesture support (volume, mute, pause/play)
- [ ] Custom gesture recording and playback
- [ ] Settings GUI (instead of code editing)
- [ ] System tray integration
- [ ] Gesture history and statistics
- [ ] Multiple display support
- [ ] Unit tests and CI/CD
- [ ] Performance profiling and optimization
- [ ] Dark mode UI
- [ ] Language localization

---

## ⚠️ Important Notes

- **Permissions**: The application requires webcam access. Grant permissions if prompted.
- **Performance**: Works best on systems with 2+ GHz processor
- **Lighting**: Works best in well-lit environments (avoid backlighting)
- **Distance Range**: The distance range may vary based on hand size and camera angle; adjust `MIN_DISTANCE` and `MAX_DISTANCE` in `config.py` if needed
- **Brightness Control**: Some systems may not support programmatic brightness control; functionality varies by OS and hardware

---

## 📝 License

This project is open-source and available for educational and personal use.

---

## 👥 Contributing

Suggestions for improvements are welcome! Consider:
1. Testing on different systems
2. Optimizing performance
3. Adding new gesture controls
4. Improving documentation
5. Creating unit tests

---

## 📧 Support

For issues, questions, or suggestions:
1. Check the **Troubleshooting** section above
2. Review `config.py` for customization options
3. Examine module docstrings for usage details

---

## 🎉 Enjoy Gesture-Controlled Brightness!

Thank you for using Bright. We hope it enhances your computing experience!
