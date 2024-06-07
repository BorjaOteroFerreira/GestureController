import math
import keyboard
from gestures.Gesture import Gesture

class OpenMouth(Gesture):
    def __init__(self, key, threshold=15):
        super().__init__()
        self.threshold = threshold
        self.key = key 
        self.accelerate_pressed = False

    def detect(self, frame, results_face, results_hands):
        if results_face.multi_face_landmarks:
            for face_landmarks in results_face.multi_face_landmarks:
                upper_lip_points = [
                    (int(face_landmarks.landmark[61].x * frame.shape[1]), int(face_landmarks.landmark[61].y * frame.shape[0])),
                    (int(face_landmarks.landmark[40].x * frame.shape[1]), int(face_landmarks.landmark[40].y * frame.shape[0])),
                    (int(face_landmarks.landmark[37].x * frame.shape[1]), int(face_landmarks.landmark[37].y * frame.shape[0]))
                ]
                lower_lip_points = [
                    (int(face_landmarks.landmark[91].x * frame.shape[1]), int(face_landmarks.landmark[91].y * frame.shape[0])),
                    (int(face_landmarks.landmark[84].x * frame.shape[1]), int(face_landmarks.landmark[84].y * frame.shape[0])),
                    (int(face_landmarks.landmark[88].x * frame.shape[1]), int(face_landmarks.landmark[88].y * frame.shape[0]))
                ]
                upper_lip_center = (
                    (upper_lip_points[0][0] + upper_lip_points[1][0] + upper_lip_points[2][0]) // 3,
                    (upper_lip_points[0][1] + upper_lip_points[1][1] + upper_lip_points[2][1]) // 3
                )
                lower_lip_center = (
                    (lower_lip_points[0][0] + lower_lip_points[1][0] + lower_lip_points[2][0]) // 3,
                    (lower_lip_points[0][1] + lower_lip_points[1][1] + lower_lip_points[2][1]) // 3
                )
                lip_distance = self.calculate_distance(upper_lip_center, lower_lip_center)
                if lip_distance > self.threshold:
                    if not self.accelerate_pressed:
                        keyboard.press(self.key)
                        self.accelerate_pressed = True
                else:
                    if self.accelerate_pressed:
                        keyboard.release(self.key)
                        self.accelerate_pressed = False

        self.draw_landmarks(frame, results_face, results_hands)

    @staticmethod
    def calculate_distance(point1, point2):
        return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)
