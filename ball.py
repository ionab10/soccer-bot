import numpy as np
from glob import glob
import cv2

from matplotlib import pyplot as plt

def get_mask(resized):

    rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    hls = cv2.cvtColor(resized, cv2.COLOR_BGR2HLS)
    lower_black = np.array([0,0,0], dtype=np.uint8)
    upper_black = np.array([255,10,255], dtype=np.uint8)
    black_mask = cv2.inRange(hls, lower_black, upper_black)
    lower_white = np.array([0,50,0], dtype=np.uint8)
    upper_white = np.array([255,255,255], dtype=np.uint8)
    white_mask = cv2.inRange(hls, lower_white, upper_white)
    lower_green = np.array([0,100,0], dtype=np.uint8)
    upper_green = np.array([100,255,100], dtype=np.uint8)
    green_mask = cv2.inRange(rgb, lower_green, upper_green)
    mask = np.bitwise_or(white_mask, black_mask)
    mask = np.bitwise_and(mask, np.bitwise_not(green_mask))
    return mask

def find_ball(image, plot=False):

    center = (image.shape[0]/2, image.shape[1]/2)

    # detect circles in the image
    mask = get_mask(image)
    circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 2, 500, maxRadius=250)
    
    fig, ax = plt.subplots(1, 2, figsize=(6,2))
    ax[0].imshow(image)
    ax[1].imshow(mask)
    
    if circles is None:
        if plot:
            plt.show()
        return None, center, mask
    else:
        
        circles = np.round(circles[0, :]).astype("int")
    
        if plot:
            
            for (x, y, r) in circles:
                circle = plt.Circle((x, y), r, color='r', fill=False)
                #print(x,y)
                ax[0].add_patch(circle)
                break
            plt.show()

        return circles[0], center, mask

def load_img(fn):
    return cv2.imread(fn)

