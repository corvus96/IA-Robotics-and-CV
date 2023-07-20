import cv2
import mediapipe as mp

class FaceMesh:

    def __init__(self, static_image_mode=False, max_num_faces=1, detection_conf=0.5, track_conf=0.5):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=static_image_mode,
            max_num_faces=max_num_faces,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=track_conf,
        )

    def find_mesh(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(frame)
        return results

    def draw_points(self, results, frame):
        height, width, _ = frame.shape
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                for lm in face_landmarks.landmark:
                    cv2.circle(frame, (int(lm.x * width), int(lm.y * height)), 1, (0, 255, 0), 1)

        return frame

    def find_positions(self, results, frame):
        self.lm_list = []
        height, width, _ = frame.shape
        if results.multi_face_landmarks:
            for id, face_landmarks in enumerate(results.multi_face_landmarks):
                for lm in face_landmarks.landmark:
                    self.lm_list.append([id, int(lm.x * width), int(lm.y * height)])

        return self.lm_list