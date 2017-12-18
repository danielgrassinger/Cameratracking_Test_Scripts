import cv2
import numpy as np
from time import sleep

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

cv2.setTrackbarPos('Hue max', 'image', 10)
cv2.setTrackbarPos('Hue min', 'image', 0)
cv2.setTrackbarPos('Saturation', 'image', 1)
cv2.setTrackbarPos('Value', 'image', 1)
cap = cv2.VideoCapture('saves/video_3.avi')

img = cv2.blur(img,(3,3))

while not cv2.waitKey(1) & 0xFF == ord('q'):
    ret, img = cap.read()
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
    res = np.array(img)
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
    try:
        for line in lines:
            for rho, theta in line:
                #print(str(rho) + ' ' + str(theta/np.pi *180))
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))

                cv2.line(res, (x1, y1), (x2, y2), (0, 255, 0), 2)

    except Exception:
        pass

    cv2.imshow('image', res)

    sleep(0.05)
    #while True:
     #   sleep(1)

cv2.destroyAllWindows()


