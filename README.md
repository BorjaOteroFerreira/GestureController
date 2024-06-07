# GestureController

GestureController is a Python tool that allows you to control your computer using hand and face gestures captured by your webcam. By detecting various gestures, such as hand movements and facial expressions, GestureController translates them into keyboard inputs, allowing you to interact with your computer in a hands-free manner.

## Features
- Control your computer using hand and face gestures.
- Detects gestures such as opening hands, tilting head, and more.
- Customizable gesture mapping to keyboard inputs.
- Real-time feedback and visualization of detected gestures.

## Installation
1. Clone this repository to your local machine.
2. Install the required dependencies using pip:
pip install -r requirements.txt


## Usage
1. Run the `app.py` script.
2. Position yourself in front of your webcam.
3. Perform the supported gestures, such as opening your hands or tilting your head.
4. See the corresponding keyboard inputs being triggered based on your gestures.


## Supported Gestures
- **Opening hands:** Simulates pressing designated keys.
- **Closing hands:** Simulates releasing designated keys.
- **Raising one hand:** Triggers a specific action, such as pausing or resuming a video.
- **Tilting head left or right:** Controls directional input, such as steering in games or navigating interfaces.
- **Blinking:** Triggers a specific action, such as taking a screenshot or opening a menu.
- **Smiling:** Initiates a predefined action, such as changing the volume or switching between applications.
- **Opening mouth:** Simulates pressing a key for actions like shooting in a game or capturing an image.
- **Making a peace sign:** Initiates a specific action, such as starting a video call or muting/unmuting the microphone.
- **Waving:** Triggers an action, such as scrolling through a document or switching tabs in a browser.


## Customization
You can customize the mapping of gestures to keyboard inputs by modifying the configuration in the `app.py` script. Additionally, you can adjust sensitivity and other parameters to fine-tune the gesture detection.

## Requirements
- Python 3.x
- OpenCV
- Mediapipe

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
- This project utilizes the [Mediapipe](https://google.github.io/mediapipe/) library for hand and face gesture recognition.
