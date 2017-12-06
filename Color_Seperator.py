
import numpy as np
import cv2
from time import sleep

def nothing(x):
    pass

img = cv2.imread('assets/Test3.jpg')
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image',600,600)
cv2.namedWindow("ref",cv2.WINDOW_NORMAL)
cv2.resizeWindow("ref",600,600)

# create trackbars for color change
cv2.createTrackbar('Hue max','image',0,179,nothing)
cv2.createTrackbar('Hue min', 'image',0,179,nothing)
cv2.createTrackbar('Saturation','image',0,255,nothing)
cv2.createTrackbar('Value','image',0,255,nothing)

cv2.imshow('ref',img)

while not cv2.waitKey(1) & 0xFF == ord('q'):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV

    # get current positions of four trackbars
    hue_min = cv2.getTrackbarPos('Hue min', 'image')
    hue_max = cv2.getTrackbarPos('Hue max', 'image')
    saturation = cv2.getTrackbarPos('Saturation', 'image')
    value = cv2.getTrackbarPos('Value', 'image')

    lower_blue = np.array([hue_min, saturation, value])
    upper_blue = np.array([hue_max, 255, 255])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img, img, mask=mask)


    cv2.imshow('image',res)


    sleep(0.05)


cv2.destroyAllWindows()