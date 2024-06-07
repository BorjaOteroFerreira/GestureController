import cv2
import math
import keyboard
import mediapipe as mp
from gestures.Gesture import Gesture

class HeadTilt(Gesture):
    def __init__(self, key_left, key_right, threshold_angle=10):
        super().__init__()
        self.threshold_angle = threshold_angle
        self.key_left = key_left
        self.key_right = key_right
        self.last_tilt_direction = None
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.7
        self.font_thickness = 2
        self.text_color = (255, 255, 255)
        self.line_color = (0, 255, 0)
        self.line_thickness = 2

    def detect(self, frame, results_face, results_hands):
        if results_face.multi_face_landmarks:
            for face_landmarks in results_face.multi_face_landmarks:
                landmark_points = face_landmarks.landmark
                if landmark_points:
                    chin_point = (int(landmark_points[152].x * frame.shape[1]), int(landmark_points[152].y * frame.shape[0]))
                    forehead_point = (int(landmark_points[10].x * frame.shape[1]), int(landmark_points[10].y * frame.shape[0]))
                    
                    if forehead_point[0] != chin_point[0]:
                        slope = (forehead_point[1] - chin_point[1]) / (forehead_point[0] - chin_point[0])
                    else:
                        slope = 0  # Pendiente cero para la línea vertical

                    angle_deg = math.degrees(math.atan(slope))

                    if -84 < angle_deg < -1:
                        direction = 'left'
                    elif 1 < angle_deg < 84:
                        direction = 'right'
                    else:
                        direction = None

                    if direction != self.last_tilt_direction:
                        self.last_tilt_direction = direction
                        if direction == 'right':
                            keyboard.press(self.key_right)
                            keyboard.release(self.key_left)
                        elif direction == 'left':
                            keyboard.press(self.key_left)
                            keyboard.release(self.key_right)
                        else:
                            keyboard.release(self.key_left)
                            keyboard.release(self.key_right)

                    # Dibujar la línea de la barbilla a la frente
                    cv2.line(frame, chin_point, forehead_point, self.line_color, self.line_thickness)
                    
                    # Mostrar la inclinación en la pantalla
                    cv2.putText(frame, f'Inclinación: {angle_deg:.2f} grados', (10, 30), self.font, self.font_scale, self.text_color, self.font_thickness)