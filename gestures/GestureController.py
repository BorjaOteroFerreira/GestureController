import cv2
import mediapipe as mp

class GestureController:
    def __init__(self):
        self.gestures = []
        self.cap = None
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.running = False

    def add_gesture(self, gesture):
        self.gestures.append(gesture)

    def start(self):
        self.running = True

    def stop(self):
        self.running = False
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results_face = self.face_mesh.process(rgb_frame)
        results_hands = self.hands.process(rgb_frame)
        for gesture in self.gestures:
            gesture.detect(frame, results_face, results_hands)
        return frame