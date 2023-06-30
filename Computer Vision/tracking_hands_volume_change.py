import cv2  
import time  
import numpy as np  
from hands_detector import HandsDetector  # Custom module for hand detection
import alsaaudio  # Library for audio control

# Initialize the video capture object
cap = cv2.VideoCapture(0)

# Set the dimensions of the video capture
w_cam, h_cam = 640, 480
cap.set(3, w_cam)
cap.set(4, h_cam)

# Initialize previous time variable
p_time = 0

# Initialize hands detector object
detector = HandsDetector(detection_conf=0.7, track_conf=0.7)

# Initialize audio mixer object
mixer = alsaaudio.Mixer('Master')

# Start an infinite loop for video processing
while True:
    # Read the video frame from the capture
    succees, img = cap.read()

    # Get the current time
    c_time = time.time()

    # Find hands in the frame using the detector
    results = detector.find_hands(img)

    # Find landmark positions on the detected hands
    lm_list = detector.find_position(results, img)

    # Draw landmarks on the frame
    img = detector.draw_landmarkers(results, img)

    # Find the distance between two specific landmarks
    img, length = detector.find_distance(4, 8, img)

    # Adjust volume based on the distance if available
    if length != None:
        # Map the distance to volume range
        vol = np.interp(length, [50, 230], [0, 100])

        # Map the distance to volume bar range
        vol_bar = np.interp(length, [50, 230], [400, 150])

        # Draw the volume bar on the frame
        cv2.rectangle(img, (50, 150), (85, 400), (255, 255, 255), 3)
        cv2.rectangle(img, (50, int(vol_bar)), (85, 400), (255, 0, 0), cv2.FILLED)

        # Set the system volume based on the calculated volume
        vol = mixer.setvolume(int(vol))
    else:
        # If distance is not available, get the current system volume
        vol = mixer.getvolume()[0]

        # Set the system volume to the current volume
        vol = mixer.setvolume(vol)

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