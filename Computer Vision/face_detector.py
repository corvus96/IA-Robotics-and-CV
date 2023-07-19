import cv2
import mediapipe as mp

class FaceDetector:
    """
    A class for detecting faces in images and videos.

    """

    def __init__(self, detection_conf=0.5):
        """
        Initializes the face detector.

        """
        self.face = mp.solutions.face_detection.FaceDetection(detection_conf)

    def find_faces(self, frame):
        """
        Finds the faces in the given frame.

        Args:
            frame: The image or video frame to process.

        Returns:
            The results of the face detection.

        """
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face.process(frame)
        return results

    def draw_bounding_boxes(self, results, frame):
        """
        Draws the bounding boxes of the faces in the given frame.

        Args:
            results: The results of the face detection.
            frame: The image or video frame to draw on.

        Returns:
            The frame with the bounding boxes drawn on it.

        """
        if results.detections:
            height, width, _ = frame.shape
            for id, face in enumerate(results.detections):
                mp.solutions.drawing_utils.draw_detection(frame, face)
                bbox_c = face.location_data.relative_bounding_box
                bbox = int(bbox_c.xmin * width), int(bbox_c.ymin * height), int(bbox_c.width * width), int(bbox_c.height * height)
                cv2.putText(frame, f'{int(face.score[0] * 100)} %', (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)
        return frame

    def find_positions(self, results, frame):
        """
        Finds the positions of the faces in the given frame.

        Args:
            results: The results of the face detection.
            frame: The image or video frame to process.

        Returns:
            The positions of the faces in the frame.

        """
        self.bboxes = []
        height, width, _ = frame.shape
        if results.detections:
            for id, detection in enumerate(results.detections):
                bbox_c = detection.location_data.relative_bounding_box
                bbox = int(bbox_c.xmin * width), int(bbox_c.ymin * height), int(bbox_c.width * width), int(bbox_c.height * height)
                self.bboxes.append([detection.score[0], bbox[0], bbox[1], bbox[2], bbox[3]])

        return self.bboxes