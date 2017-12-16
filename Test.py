
import numpy as np
import cv2
from time import sleep


print("Hello World")

'''
img = cv2.imread('assets/Test3.jpg')
#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# define range of blue color in HSV
lower_blue = np.array([0, 50, 50])
upper_blue = np.array([10, 255, 255])
# Threshold the HSV image to get only blue colors
mask = cv2.inRange(hsv, lower_blue, upper_blue)
# Bitwise-AND mask and original image
res = cv2.bitwise_and(img, img, mask=mask)
edges = cv2.Canny(res,200,300,apertureSize = 3)

lines = cv2.HoughLines(edges,1,np.pi/180,200)
for rho,theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.resizeWindow('frame',600,600)
cv2.imshow('frame',img)
while not cv2.waitKey(1) & 0xFF == ord('q'):
        sleep(0.1)

cv2.destroyAllWindows()
'''
im = cv2.imread("saves/image_0.png", cv2.IMREAD_GRAYSCALE)
params = cv2.SimpleBlobDetector_Params()


# Filter by Area.
params.filterByArea = True
params.minArea = 2900
# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create(params)


# Detect blobs.
keypoints = detector.detect(im)


# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255),
                                      cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show keypoints
cv2.namedWindow('Keypoints', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Keypoints',600,600)
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)