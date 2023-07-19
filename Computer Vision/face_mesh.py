import cv2
import mediapipe as mp

class FaceMesh:

    """
    A class to find and draw the face mesh in a frame.

    Args:
        static_image_mode: Whether to run in static image mode.
        max_num_faces: The maximum number of faces to detect.
        detection_conf: The minimum detection confidence.
        track_conf: The minimum tracking confidence.
    """

    def __init__(self, static_image_mode=False, max_num_faces=1, detection_conf=0.5, track_conf=0.5):
        """
        Constructor.
        """
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=static_image_mode,
            max_num_faces=max_num_faces,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=track_conf,
        )

    def find_mesh(self, frame):
        """
        Finds the face mesh in the frame.

        Args:
            frame: The frame to find the face mesh in.

        Returns:
            The results of the face mesh detection.
        """
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(frame)
        return results

    def draw_mesh(self, results, frame):
        """
        Draws the face mesh in the frame.

        Args:
            results: The results of the face mesh detection.
            frame: The frame to draw the face mesh on.

        Returns:
            The frame with the face mesh drawn on it.
        """
        height, width, _ = frame.shape
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                for lm in face_landmarks.landmark:
                    cv2.circle(frame, (int(lm.x * width), int(lm.y * height)), 1, (0, 255, 0), 1)

        return frame

    def find_positions(self, results, frame):
        """
        Finds the positions of the face mesh landmarks in the frame.

        Args:
            results: The results of the face mesh detection.
            frame: The frame to find the face mesh landmarks in.

        Returns:
            A list of the face mesh landmark positions.
        """
        self.lm_list = []
        height, width, _ = frame.shape
        if results.multi_face_landmarks:
            for id, face_landmarks in enumerate(results.multi_face_landmarks):
                for lm in face_landmarks.landmark:
                    self.lm_list.append([id, int(lm.x * width), int(lm.y * height)])

        return self.lm_list