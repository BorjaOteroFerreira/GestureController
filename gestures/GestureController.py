import mediapipe as mp
import cv2

class GestureController:
    def __init__(self):
        self.gestures = []
        self.cap = cv2.VideoCapture(1)
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

    def add_gesture(self, gesture):
        self.gestures.append(gesture)

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results_face = self.face_mesh.process(rgb_frame)
            results_hands = self.hands.process(rgb_frame)
            for gesture in self.gestures:
                gesture.detect(frame, results_face, results_hands)
            cv2.imshow("Hand and Face Gesture Controller", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()
