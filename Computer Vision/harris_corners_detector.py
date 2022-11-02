import numpy as np
import cv2 as cv


def corners_harris(img, k=0.04, threshold=0.45):
    dx2 = cv.Sobel(img, -1, 2, 0, ksize=3)
    dy2 = cv.Sobel(img, -1, 0, 2, ksize=3)
    dxy = cv.Sobel(img, -1, 1, 1, ksize=3)
    dyx = cv.Sobel(img, -1, 1, 1, ksize=3)
    # determinant of Moment matrix
    det = (dx2 * dy2) - (dxy * dyx)
    # Trace is the sum of eigenvalues
    trace = dx2 + dy2
    # normalize tensor
    cornerness_func = det - k * (trace * trace)
    new_img = normalize_tensor(cornerness_func)
    # threshold the points of interest
    harris_filtered = np.greater(new_img, threshold).astype(np.float32)
    return harris_filtered

def normalize_tensor(tensor):
    new_img = tensor - tensor.min()
    img_span = new_img.max() - new_img.min()
    new_img /= img_span
    return new_img

filename = 'Computer Vision/Resources/photo_3.png'

img = cv.imread(filename)
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
gray = np.float32(gray)

dst = corners_harris(gray)
# dst = cv.cornerHarris(gray, 2, 3, 0.04)
# dst = cv.dilate(dst,None)
# # Threshold for an optimal value, it may vary depending on the image.
# img[dst>0.01*dst.max()]=[0,0,255]

cv.imshow('dst',dst)
if cv.waitKey(0) & 0xff == 27:
    cv.destroyAllWindows()