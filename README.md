# gesture-control
Ditch your mouse and control your PC like a wizard! 🖐️✨ This script uses your webcam and AI to turn hand gestures into clicks, scrolls, and cursor movements.

# AI Virtual Mouse 🖱️✋

Control your computer mouse using hand gestures captured through your webcam. This project uses computer vision and hand tracking to provide touchless mouse control with clicking and scrolling capabilities.

## Features

- **Cursor Control**: Move your mouse cursor by moving your index finger
- **Single Click**: Touch your thumb to your middle finger
- **Double Click**: Touch your thumb to your index finger
- **Scrolling**: 
  - Bring index and middle fingers close together
  - Keep thumb away from fingers
  - Raise pinky to scroll up, lower pinky to scroll down
- **Visual Feedback**: Real-time hand landmark visualization and gesture indicators

## Demo

The application displays your webcam feed with:
- Hand skeleton overlay showing tracked landmarks
- Red control area boundary
- Visual indicators for click gestures
- On-screen text for scroll actions

## Requirements

### Python Version
- Python 3.7 or higher

### Dependencies

```bash
pip install opencv-python
pip install mediapipe
pip install pyautogui
pip install numpy
```

Or install all at once:
```bash
pip install -r requirements.txt
```

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/ai-virtual-mouse.git
cd ai-virtual-mouse
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python virtual_mouse.py
```

## Usage

1. **Launch the application** - Your webcam will activate
2. **Position your hand** within the red control box
3. **Move cursor** - Point with your index finger
4. **Single click** - Touch thumb to middle finger
5. **Double click** - Touch thumb to index finger
6. **Scroll** - Bring index and middle fingers close, keep thumb away, use pinky for direction
7. **Exit** - Press 'q' on your keyboard

### Gesture Guide

| Gesture | Action | Description |
|---------|--------|-------------|
| Index finger movement | Cursor control | Move your index finger within the control area |
| Thumb + Middle finger | Single click | Touch tips together briefly |
| Thumb + Index finger | Double click | Touch tips together briefly |
| Index + Middle close, Pinky up | Scroll up | Keep thumb away, raise pinky |
| Index + Middle close, Pinky down | Scroll down | Keep thumb away, lower pinky |

## Configuration

You can adjust the following parameters in the code to customize sensitivity:

```python
SMOOTHING_FACTOR = 0.2     # Cursor smoothness (0.1-0.5)
FRAME_REDUCTION = 100      # Control area border size
CLICK_THRESHOLD = 0.045    # Finger proximity for clicks
SCROLL_MODE_THRESHOLD = 0.06  # Finger distance for scroll mode
THUMB_AWAY_THRESHOLD = 0.1 # Thumb distance for scroll activation
SCROLL_SENSITIVITY = 120   # Scroll speed
```

## How It Works

### Technology Stack
- **OpenCV**: Captures and processes webcam video
- **MediaPipe**: Detects and tracks 21 hand landmarks in real-time
- **PyAutoGUI**: Controls mouse cursor and performs clicks/scrolls
- **NumPy**: Handles coordinate mapping and interpolation

### Key Components

1. **Hand Detection**: MediaPipe's ML model identifies hand landmarks with configurable confidence thresholds (70%)

2. **Coordinate Mapping**: Hand position within the control area maps to full screen coordinates using linear interpolation

3. **Exponential Smoothing**: Reduces jitter in cursor movement for natural control

4. **Gesture Recognition**: Calculates Euclidean distances between finger landmarks to detect gestures

5. **Click Lock Mechanism**: Prevents repeated clicks from a single sustained gesture

## Troubleshooting

### Camera not detected
- Ensure your webcam is connected and not in use by another application
- Try changing `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)` for external webcams

### Cursor too jittery
- Decrease `SMOOTHING_FACTOR` (try 0.1-0.15)
- Ensure good lighting conditions

### Gestures not registering
- Adjust threshold values
- Keep hand clearly visible within the control area
- Ensure good lighting and contrast

### Cursor moving too slowly
- Increase `SMOOTHING_FACTOR` (try 0.3-0.5)
- Reduce `FRAME_REDUCTION` for larger control area

## System Compatibility

- **Windows**: Fully supported
- **macOS**: Supported (may require accessibility permissions)
- **Linux**: Supported (may need X11 display configuration)

## Important Notes

- Good lighting improves hand detection accuracy
- Keep hand within the red control box for best results
- PyAutoGUI fail-safe is disabled - be careful at screen edges
- The webcam feed is mirrored for natural interaction

## Future Enhancements

- [ ] Multi-gesture support
- [ ] Customizable gesture mapping
- [ ] Right-click functionality
- [ ] Drag-and-drop capability
- [ ] Settings GUI
- [ ] Multi-hand support
- [ ] Gesture training mode

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- MediaPipe team for the excellent hand tracking solution
- OpenCV community for computer vision tools
- PyAutoGUI for mouse automation capabilities

## Contact

For questions or suggestions, please open an issue on GitHub.

---

**Made with ❤️ using Python, OpenCV, and MediaPipe**
