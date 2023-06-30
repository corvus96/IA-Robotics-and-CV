"""
A class for detecting hands in a video stream.

Example:
    hands_detector = HandsDetector()
    capture = cv2.VideoCapture(0)
    while True:
        ret, frame = capture.read()
        results = hands_detector.find_hands(frame)
        frame = hands_detector.draw_landmarkers(results, frame)
        cv2.imshow('Hands', frame)
        if cv2.waitKey(1) == 27:
            break

"""

import cv2
import mediapipe as mp
import math

class HandsDetector():
    """A class for detecting hands in a video stream."""
    def __init__(self, static_image_mode=False, max_hands=2, detection_conf=0.5, track_conf=0.5):
        """Initialize the hands detector.
        Args:
            static_image_mode (bool, optional): Whether to operate in static image mode. Defaults to False.
            max_hands (int, optional): The maximum number of hands to track. Defaults to 2.
            detection_conf (float, optional): The minimum confidence for hand detection. Defaults to 0.5.
            track_conf (float, optional): The minimum confidence for hand tracking. Defaults to 0.5.
        """
        self.mp_hands = mp.solutions.hands.Hands(static_image_mode, max_hands,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=track_conf,
        )
        

    def find_hands(self, frame):
        """Detect hands in the frame.

        Args:
            frame: The frame to detect hands in.

        Returns:
            The results of the hand detection.
        """

        # Convert the frame to RGB.
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect hands in the frame.
        results = self.mp_hands.process(frame)

        # Return the results of the detection.
        return results
    
    def draw_landmarkers(self, results, frame):
        """Draw the hands on the frame.

        Args:
            results: The results of the hand detection.
            frame: The frame to draw the hands on.

        Returns:
            The frame with the hands drawn on it.
        """
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp.solutions.hands.HAND_CONNECTIONS,
                    mp.solutions.drawing_utils.DrawingSpec(
                        color=(255, 0, 0), thickness=2, circle_radius=4
                    ),
                )
    
        return frame

    def find_position(self, results, frame, hand_n=0):
        """Get position of each landmark
        Args:
            results: The results of the hand detection.

        Returns:
            A list with the landmarkers.
        """
        self.lm_list = []
        height, width, _ = frame.shape
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[hand_n]
            for id, lm in enumerate(hand.landmark):
                lx, ly = int(lm.x*width), int(lm.y*height)
                self.lm_list.append([lx, ly, lm.z])

        return self.lm_list
    
    def find_distance(self, p1, p2, frame, draw=True):
        length =None
        if len(self.lm_list) != 0:
            x1, y1 = self.lm_list[p1][0], self.lm_list[p1][1]
            x2, y2 = self.lm_list[p2][0], self.lm_list[p2][1]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            if draw:
                cv2.circle(frame, (x1, y1), 5, (255, 0, 255), cv2.FILLED)
                cv2.circle(frame, (x2, y2), 5, (255, 0, 255), cv2.FILLED)
                cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
                cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            
            length = math.hypot(x2 - x1, y2 - y1)
        return frame, length