import keyboard
from gestures.Gesture import Gesture
import mediapipe as mp

class OpenHand(Gesture):
    def __init__(self, key_left, key_right):
        super().__init__()
        self.is_open = False
        self.hand_label = ""
        self.key_left = key_left
        self.key_right = key_right

    def detect(self, frame, results_face, results_hands):
        left_hand_open = False
        right_hand_open = False

        if results_hands.multi_hand_landmarks and results_hands.multi_handedness:
            for idx, hand_landmarks in enumerate(results_hands.multi_hand_landmarks):
                hand_label = results_hands.multi_handedness[idx].classification[0].label
                is_open = self._is_hand_open(hand_landmarks)
                if hand_label == 'Left':
                    left_hand_open = is_open
                elif hand_label == 'Right':
                    right_hand_open = is_open

                # Actualizamos el estado de la mano actual
                if self.hand_label == hand_label:
                    self.is_open = is_open

        if left_hand_open and not right_hand_open:
            keyboard.release(self.key_right)
            keyboard.press(self.key_left)
        elif right_hand_open and not left_hand_open:
            keyboard.release(self.key_left)
            keyboard.press(self.key_right)
        else:
            keyboard.release(self.key_left)
            keyboard.release(self.key_right)

        self.draw_landmarks(frame, results_face, results_hands)

    @staticmethod
    def _is_hand_open(hand_landmarks):
        thumb_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
        index_finger_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
        middle_finger_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring_finger_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.RING_FINGER_TIP]
        pinky_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.PINKY_TIP]
        return (index_finger_tip.y < thumb_tip.y or
                middle_finger_tip.y < thumb_tip.y or
                ring_finger_tip.y < thumb_tip.y or
                pinky_tip.y < thumb_tip.y)


