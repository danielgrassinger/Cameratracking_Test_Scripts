import cv2
import numpy as np
from time import sleep
from matplotlib import pyplot as plt

def nothing(x):
    pass

img = cv2.imread('saves/image_10.png')
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 600, 600)
# cv2.namedWindow("ref",cv2.WINDOW_NORMAL)
# cv2.resizeWindow("ref",600,600)

# create trackbars for color change
cv2.createTrackbar('Hue max', 'image', 0, 179, nothing)
cv2.createTrackbar('Hue min', 'image', 0, 179, nothing)
cv2.createTrackbar('Saturation', 'image', 0, 255, nothing)
cv2.createTrackbar('Value', 'image', 0, 255, nothing)

cv2.setTrackbarPos('Hue max', 'image', 90)
cv2.setTrackbarPos('Hue min', 'image', 70)
cv2.setTrackbarPos('Saturation', 'image', 100)
cv2.setTrackbarPos('Value', 'image', 60)
cap = cv2.VideoCapture('saves/video_3.avi')

img = cv2.blur(img,(5,5))

while not cv2.waitKey(1) & 0xFF == ord('q'):
    #ret, img = cap.read()
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
    res = cv2.blur(res,(5,5))
    im = np.array(img)

    edged = cv2.Canny(res, 30, 110)
    im2, contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cont = np.array(img)
    cont[:,:,:]=0
    cv2.drawContours(cont, contours, -1, (0, 255, 0), 3)
    edged2 = cv2.Canny(cont, 30, 150)
    im2, contours, hierarchy = cv2.findContours(edged2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:3]
    cv2.drawContours(im, contours, -1, (0, 255, 0), 2)
    for contour in contours:
        pass
        #print(cv2.contourArea(contour))
    #break
    try:
        cnt = contours[0]

        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        im = cv2.drawContours(im, [box], 0, (0, 0, 255), 1)
    except Exception:
        pass
    cv2.imshow('image', im)

    sleep(0.05)
    #while True:
     #   sleep(1)

cv2.destroyAllWindows()


