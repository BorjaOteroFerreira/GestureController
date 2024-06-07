# GestureController

GestureController is a Python tool that allows you to control your computer using hand and face gestures captured by your webcam. By detecting various gestures, such as hand movements and facial expressions, GestureController translates them into keyboard inputs, allowing you to interact with your computer in a hands-free manner.

**currently** designed to simulate keyboard inputs for gaming purposes, serving as an alternative to traditional controllers for games or emulators. The implemented gestures translate to keyboard key presses, allowing you to control in-game actions through hand and face gestures captured by your webcam.
Please note that while the current focus is on gaming controls, future updates may include additional functionalities such as opening applications, scrolling through documents, and navigating the desktop interface. These enhancements aim to provide a more comprehensive hands-free interaction experience beyond gaming.
Your feedback and suggestions are valuable as we continue to develop and improve GestureController to meet a broader range of user needs and applications.

## Features
- Control your computer using hand and face gestures.
- Detects gestures such as opening hands, tilting head, and more.
- Customizable gesture mapping to keyboard inputs.
- Real-time feedback and visualization of detected gestures.

## Installation
1. Clone this repository to your local machine.
2. Install the required dependencies using pip:
```bash
pip install -r requirements.txt
```

## Usage
1. Run the `app.py` script.
2. Position yourself in front of your webcam.
3. Perform the supported gestures, such as opening your hands or tilting your head.
4. See the corresponding keyboard inputs being triggered based on your gestures.


## Supported Gestures
- **Opening hands:** Asign 1 key for hand , you can prees one key for hand.
- **Closing hands:** Simulates releasing designated keys for hands.
- **Put hands Toghetter:** Triggers a specific key.
- **Tilting head left or right:** Controls directional input, such as steering in games or navigating interfaces.
- **Opening mouth:** Simulates pressing a key for actions like shooting in a game or capturing an image.


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
