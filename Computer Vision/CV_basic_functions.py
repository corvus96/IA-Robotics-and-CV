import numpy as np
import cv2
import random

def only_one_channel(image, selectChannel):
    """ Inputs:
        image: A BGR format image 
        selectChannel: This argument can be red, blue or green 
    in UPPERCASE or lowercase
    output: 
        An image with only selecChannel Non zero
    """
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

def add_gaussian_noise(image, mean, std):
    """ This is a function that add gaussian noise 
    to an image in colored format or grayscale format
    Inputs: 
        image: source image
        mean: this is mean value
        std: this is standard desviation value
    Output:
        An image with gaussian noise added
    """
    row, col, ch = image.shape
    gaussian = np.random.normal(mean, std, (row, col)) #  One layer gaussian noise
    noisy_image = np.zeros(image.shape, np.float32)
    # In case that an image is in gray scale
    if len(image.shape) == 2:
        noisy_image = image + gaussian
    # In case that an image is in colored format
    else:
        noisy_image[:, :, 0] = image[:, :, 0] + gaussian
        noisy_image[:, :, 1] = image[:, :, 1] + gaussian
        noisy_image[:, :, 2] = image[:, :, 2] + gaussian
    cv2.normalize(noisy_image, noisy_image, 0, 255, cv2.NORM_MINMAX, dtype=-1)
    noisy_image = noisy_image.astype(np.uint8)
    return noisy_image

def resize_image(image, scale):
    """ This feature resizes an image while maintaning the aspect ratio
    Inputs:
        image: element that wants to be resized
        scale: A number that represents scale in %
    Outputs:
        An image resized by a scale percent
    """
    width = int(image.shape[1] * scale / 100)
    height = int(image.shape[0] * scale / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    return resized


