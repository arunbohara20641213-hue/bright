# Bright ✨  
**Gesture-Controlled Screen Brightness using Computer Vision**

Bright is a Python-based computer vision project that allows users to control their system’s screen brightness using simple hand gestures captured through a webcam. It leverages OpenCV and MediaPipe for real-time hand tracking and maps finger distance to brightness levels.

---

## Features

- Real-time webcam-based hand tracking  
- Thumb–index finger distance controls brightness  
- Smooth brightness adjustment (0–100%)  
- Fast, lightweight, and responsive  
- No external hardware required  

---

## 🛠️ Technologies Used

- Python  
- OpenCV  
- MediaPipe  
- NumPy  
- screen-brightness-control  

---

## Installation

Ensure Python is installed, then install the required dependencies:

```bash
pip install opencv-python mediapipe numpy screen-brightness-control

 ```




## Notes

Works best in good lighting conditions

Webcam access is required

Brightness control may vary depending on OS and hardware support





## How It Works

The webcam captures live video input.

MediaPipe detects hand landmarks.

The distance between:

Thumb tip (Landmark 4)

Index finger tip (Landmark 8)
is calculated.

This distance is mapped to a brightness range of 0–100%.

The system brightness updates instantly.

