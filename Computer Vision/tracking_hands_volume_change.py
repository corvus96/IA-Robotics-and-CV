import cv2
import time
import numpy as np
from hands_detector import HandsDetector
import math

cap = cv2.VideoCapture(0)
w_cam, h_cam = 640, 480
cap.set(3, w_cam)
cap.set(4, h_cam)
p_time = 0

detector = HandsDetector(detection_conf=0.7, track_conf=0.7)

while True:
    succees, img = cap.read()
    c_time = time.time()
    results = detector.find_hands(img)
    lm_list = detector.find_position(results, img)
    img = detector.draw_landmarkers(results, img)
    img, length = detector.find_distance(4, 8, img)
    print(length)
    fps = 1/(c_time-p_time)
    p_time = c_time

    cv2.putText(img, f'FPS: {int(fps)}', (40,70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
     # Check if the user wants to quit.
    if cv2.waitKey(1) == 27:
        break

# Release the capture object.
cap.release()

cv2.destroyAllWindows()


