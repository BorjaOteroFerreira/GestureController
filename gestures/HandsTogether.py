import math
import keyboard
from gestures.Gesture import Gesture

class HandsTogether(Gesture):
    def __init__(self, key):
        super().__init__()
        self.threshold = 100
        self.wink_pressed = False
        self.key = key

    def detect(self, frame, results_face, results_hands):
        left_hand_center = None
        right_hand_center = None
        if results_hands.multi_hand_landmarks:
            for hand_landmarks in results_hands.multi_hand_landmarks:
                hand_label = results_hands.multi_handedness[results_hands.multi_hand_landmarks.index(hand_landmarks)].classification[0].label
                if hand_label == 'Left':
                    left_hand_center = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
                else:
                    right_hand_center = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]

        if left_hand_center and right_hand_center:
            left_wrist = (int(left_hand_center.x * frame.shape[1]), int(left_hand_center.y * frame.shape[0]))
            right_wrist = (int(right_hand_center.x * frame.shape[1]), int(right_hand_center.y * frame.shape[0]))
            hands_distance = self.calculate_distance(left_wrist, right_wrist)
            if hands_distance < self.threshold:
                if not self.wink_pressed:
                    keyboard.press(self.key)
                    self.wink_pressed = True
            else:
                if self.wink_pressed:
                    keyboard.release(self.key)
                    self.wink_pressed = False

        self.draw_landmarks(frame, results_face, results_hands)

    @staticmethod
    def calculate_distance(point1, point2):
        return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)
