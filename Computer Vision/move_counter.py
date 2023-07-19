import cv2 
import time
from pose_estimation import PoseEstimator
# Initialize the video capture object
cap = cv2.VideoCapture(0)

# Set the dimensions of the video capture
w_cam, h_cam = 640, 480
cap.set(3, w_cam)
cap.set(4, h_cam)

# Initialize previous time variable
p_time = 0

detector = PoseEstimator(segmentation=True,detection_conf=0.5, track_conf=0.5)

# Start an infinite loop for video processing
while True:
    # Read the video frame from the capture
    succees, img = cap.read()

    # Get the current time
    c_time = time.time()

    results = detector.find_body(img)

    detector.draw_landmarkers(results, img)
    # Calculate and display the frames per second (FPS)
    fps = 1/(c_time-p_time)
    p_time = c_time
    cv2.putText(img, f'FPS: {int(fps)}', (40,70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    # Show the processed frame
    cv2.imshow("Img", img)

    # Check if the user wants to quit (press Esc key)
    if cv2.waitKey(1) == 27:
        break

# Release the capture object
cap.release()

cv2.destroyAllWindows()