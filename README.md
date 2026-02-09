# Gesture Drop

A gesture-based application for quickly transferring text and images from your computer to your mobile device using hand gestures.

## Features

- Copy text on your computer and send it to your phone with a closed fist gesture
- Display text and images on your mobile device
- Control content display using hand gestures on your mobile device
- Simple web interface for both computer and mobile

## How It Works

1. The desktop application (gesture_sender.py) monitors your webcam for hand gestures
2. When you make a closed fist gesture, it sends the content of your clipboard to the server
3. Open the web interface on your mobile device to see the transferred content
4. Use different hand gestures on your mobile to control what content is displayed:
   - Open palm: Show both text and image
   - Thumbs up with fingers down: Show image only

## Requirements

- Python 3.x
- Webcam on your computer
- Modern mobile browser with camera access

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/suryaprabhaz/gesture-drop.git
   cd gesture-drop
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. **Run the application (Windows):**
   ```
   start.bat
   ```
   This script will automatically:
   - Start the secure tunnel (Ngrok)
   - Launch the backend server
   - Start the gesture detection app

   *Alternatively, you can run components individually as described below only if the batch file fails.*

4. **Connect your phone:**
   - Scan the QR code displayed in the Server window.
   - Or manually visit the displayed URL on your mobile device.

## Usage

1. **On your Computer:**
   - Ensure the "Gesture Drop Sender" window is open and can see your hand.
   - Press 'C' to calibrate skin tone if needed.
   - Copy any text (Ctrl+C).
   - Show a **Closed Fist ✊** to the camera.

2. **On your Phone:**
   - The text will automatically appear!
   - You can also view uploaded images.


## Author

Developed by **[@suryaprabhaz](https://github.com/suryaprabhaz)**

## License

This project is licensed under the MIT License - see the LICENSE file for details.
