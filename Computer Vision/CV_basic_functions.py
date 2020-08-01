import numpy as np
import cv2
import random

def onlyOneChannel(image, selectChannel):
    """ Inputs:
    image: A BGR format image 
    selectChannel: This argument can be red, blue or green 
    in UPPERCASE or lowercase
    output: An image with only selecChannel Non zero"""
    output = image.copy()
    if selectChannel.lower() == 'blue':
        output[:, :, 1] = 0
        output[:, :, 2] = 0
    elif selectChannel.lower() == 'green':
        output[:, :, 0] = 0
        output[:, :, 2] = 0
    elif  selectChannel.lower() == 'red':
        output[:, :, 0] = 0
        output[:, :, 1] = 0
    else:
        raise AssertionError('selectChannel will be: red or blue or green') 
    return output

path = './Resources/135.jpg'
# cv2.imread by default Loads a color image where 
# any transparency of image will be neglected, then
# -1 argument Loads image with unchanged
img = cv2.imread(path,-1)
cv2.namedWindow('image with sensor', cv2.WINDOW_NORMAL)
cv2.imshow('image with sensor', img)
cv2.namedWindow('image with sensor RED', cv2.WINDOW_NORMAL)
red = onlyOneChannel(img, 'red')
cv2.imshow('image with sensor RED', red)

cv2.waitKey(0)
cv2.destroyAllWindows()