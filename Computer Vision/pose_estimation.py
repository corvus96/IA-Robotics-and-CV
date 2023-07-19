import cv2
import mediapipe as mp

class PoseEstimator:
    def __init__(self, static_image_mode=False, model_complexity= 1, segmentation=False, detection_conf=0.5, track_conf=0.5):
        self.pose = mp.solutions.pose.Pose(static_image_mode=static_image_mode, 
                                                    model_complexity=model_complexity,
                                                    enable_segmentation=segmentation,  
                                                    min_detection_confidence=detection_conf,
                                                    min_tracking_confidence=track_conf)
    
    def find_body(self, frame):

        # Convert the frame to RGB.
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect bodies in the frame.
        results = self.pose.process(frame)

        # Return the results of the detection.
        return results
    
    def draw_landmarkers(self, results, frame):
        """Draw the hands on the frame.

        Args:
            results: The results of the bodies detection.
            frame: The frame to draw the hands on.

        Returns:
            The frame with the hands drawn on it.
        """
        if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                    frame, results.pose_landmarks, mp.solutions.pose.
                    POSE_CONNECTIONS, mp.solutions.drawing_utils.DrawingSpec(
                        color=(255, 0, 0), thickness=2, circle_radius=4
                    ))
    
        return frame

    def find_position(self, results, frame):
        """Get position of each landmark
        Args:
            results: The results of the hand detection.

        Returns:
            A list with the landmarkers.
        """
        self.lm_list = []
        height, width, _ = frame.shape
        if results.pose_landmarks:
            for id, lm in enumerate(results.pose_landmarks.landmark):
                lx, ly = int(lm.x*width), int(lm.y*height)
                self.lm_list.append([lx, ly, lm.z])

        return self.lm_list