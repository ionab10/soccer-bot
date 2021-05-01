import numpy as np
from glob import glob
import cv2

from matplotlib import pyplot as plt
%matplotlib inline

def find_ball(image, width=640, plot=False):
    resized = cv2.resize(image, (width, int(image.shape[0] * width / image.shape[1])), interpolation = cv2.INTER_AREA)
    
    #mask = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    
    hls = cv2.cvtColor(resized, cv2.COLOR_BGR2HLS)
    lower_black = np.array([0,0,0], dtype=np.uint8)
    upper_black = np.array([255,90,50], dtype=np.uint8)
    black_mask = cv2.inRange(hls, lower_black, upper_black)
    lower_white = np.array([0,255-120,0], dtype=np.uint8)
    upper_white = np.array([255,255,255], dtype=np.uint8)
    white_mask = cv2.inRange(hls, lower_white, upper_white)
    lower_green = np.array([40,0,0], dtype=np.uint8)
    upper_green = np.array([50,255,255], dtype=np.uint8)
    green_mask = cv2.inRange(hls, lower_green, upper_green)
    mask = np.bitwise_or(white_mask, black_mask)
    mask = np.bitwise_and(mask, np.bitwise_not(green_mask))

    center = (resized.shape[0]/2, resized.shape[1]/2)

    # detect circles in the image
    circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 2, 500, maxRadius=250)
    
    fig, ax = plt.subplots(1, 2, figsize=(3,2))
    ax[0].imshow(resized)
    ax[1].imshow(mask)
    
    if circles is None:
        if plot:
            plt.show()
        return None, center
    else:
        
        circles = np.round(circles[0, 🙂).astype("int")
    
        if plot:
            
            for (x, y, r) in circles:
                circle = plt.Circle((x, y), r, color='r', fill=False)
                #print(x,y)
                ax[0].add_patch(circle)
                break
            plt.show()

        return circles[0], center

for fn in glob('./soccer_balls/*'):
    print(fn)
    image = cv2.imread(fn)

    ball, center = find_ball(image, plot=True)
    if ball is not None:
        print(ball, center)
        if ball[0] < center[0]:
            print('left')
        elif ball[0] > center[0]:
            print('right')
