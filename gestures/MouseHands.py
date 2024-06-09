import pyautogui
from gestures.Gesture import Gesture
import mediapipe as mp

class MouseHands(Gesture):
    def __init__(self):
        super().__init__()
        self.is_left_hand_open = False
        self.is_right_hand_closed = False
        self.screen_width, self.screen_height = pyautogui.size()
        self.mp_hands = mp.solutions.hands

    def detect(self, frame, results_face, results_hands):
        left_hand_pos = None
        right_hand_closed = False

        if results_hands.multi_hand_landmarks and results_hands.multi_handedness:
            for idx, hand_landmarks in enumerate(results_hands.multi_hand_landmarks):
                hand_label = results_hands.multi_handedness[idx].classification[0].label

                if hand_label == 'Left':
                    left_hand_pos = self._get_hand_center(hand_landmarks)
                elif hand_label == 'Right':
                    right_hand_closed = self._is_hand_closed(hand_landmarks)

        # Mover el ratón con la mano izquierda
        if left_hand_pos:
            mouse_x, mouse_y = left_hand_pos
            screen_x = int(self.screen_width * mouse_x)
            screen_y = int(self.screen_height * mouse_y)
            pyautogui.moveTo(screen_x, screen_y)

        # Hacer clic con la mano derecha cerrada
        if right_hand_closed:
            pyautogui.click()

        self.draw_landmarks(frame, results_face, results_hands)

    @staticmethod
    def _get_hand_center(hand_landmarks):
        x = [landmark.x for landmark in hand_landmarks.landmark]
        y = [landmark.y for landmark in hand_landmarks.landmark]
        return sum(x) / len(x), sum(y) / len(y)

    @staticmethod
    def _is_hand_closed(hand_landmarks):
        thumb_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
        index_finger_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
        middle_finger_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring_finger_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.RING_FINGER_TIP]
        pinky_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.PINKY_TIP]

        # Verificar si todos los dedos están cerca del pulgar (lo que indica una mano cerrada)
        return (
            thumb_tip.y > index_finger_tip.y and
            thumb_tip.y > middle_finger_tip.y and
            thumb_tip.y > ring_finger_tip.y and
            thumb_tip.y > pinky_tip.y
        )
