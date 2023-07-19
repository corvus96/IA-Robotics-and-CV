import cv2 
import time
from pose_estimation import PoseEstimator
cap = cv2.VideoCapture(0)

w_cam, h_cam = 640, 480
cap.set(3, w_cam)
cap.set(4, h_cam)

p_time = 0

detector = PoseEstimator(segmentation=True,detection_conf=0.5, track_conf=0.5)

while True:
    succees, img = cap.read()

    c_time = time.time()

    results = detector.find_body(img)
    print(detector.find_position(results, img))
    detector.draw_landmarkers(results, img)
    fps = 1/(c_time-p_time)
    p_time = c_time
    cv2.putText(img, f'FPS: {int(fps)}', (40,70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("Img", img)

    if cv2.waitKey(1) == 27:
        break

cap.release()

cv2.destroyAllWindows()