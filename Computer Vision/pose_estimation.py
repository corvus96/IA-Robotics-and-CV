import cv2
import mediapipe as mp

class PoseEstimator:
    """
    A class for estimating the pose of a person in an image or video.

    Args:
        static_image_mode: Whether to run the pose estimator in static image mode or video mode.
        model_complexity: The model complexity to use for pose estimation.
        segmentation: Whether to enable pose segmentation.
        detection_conf: The minimum confidence score for a pose detection to be considered valid.
        track_conf: The minimum confidence score for a pose to be tracked over time.

    """

    def __init__(self, static_image_mode=False, model_complexity=1, segmentation=False, detection_conf=0.5, track_conf=0.5):
        """
        Initializes the pose estimator.

        Args:
            static_image_mode: Whether to run the pose estimator in static image mode or video mode.
            model_complexity: The model complexity to use for pose estimation.
            segmentation: Whether to enable pose segmentation.
            detection_conf: The minimum confidence score for a pose detection to be considered valid.
            track_conf: The minimum confidence score for a pose to be tracked over time.

        """
        self.pose = mp.solutions.pose.Pose(
            static_image_mode=static_image_mode,
            model_complexity=model_complexity,
            enable_segmentation=segmentation,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=track_conf,
        )

    def find_body(self, frame):
        """
        Finds the pose of a person in the given frame.

        Args:
            frame: The image or video frame to process.

        Returns:
            The results of the pose estimation.

        """
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(frame)
        return results

    def draw_landmarkers(self, results, frame):
        """
        Draws the landmarks of the pose on the given frame.

        Args:
            results: The results of the pose estimation.
            frame: The image or video frame to draw on.

        Returns:
            The frame with the landmarks drawn on it.

        """
        if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS,
                mp.solutions.drawing_utils.DrawingSpec(
                    color=(255, 0, 0), thickness=2, circle_radius=4
                )
            )
        return frame

    def find_position(self, results, frame):
        """
        Finds the position of the landmarks of the pose in the given frame.

        Args:
            results: The results of the pose estimation.
            frame: The image or video frame to process.

        Returns:
            The positions of the landmarks in the frame.

        """
        self.lm_list = []
        height, width, _ = frame.shape
        if results.pose_landmarks:
            for id, lm in enumerate(results.pose_landmarks.landmark):
                lx, ly = int(lm.x * width), int(lm.y * height)
                self.lm_list.append([lx, ly, lm.z])
        return self.lm_list