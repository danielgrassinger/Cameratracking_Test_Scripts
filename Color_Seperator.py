
import numpy as np
import cv2
from time import sleep

drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1
nx,ny = -1,-1

# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode,nx,ny

    if event == cv2.EVENT_LBUTTONDOWN:
        print('LButton')
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        #print(str(x) + ' '+str(y))
        if drawing == True:
            if mode == True:
                cv2.rectangle(result,(ix,iy),(x,y),(0,255,0),-1)
                nx = x
                ny = y
            else:
                cv2.circle(result,(x,y),5,(0,0,255),-1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            cv2.rectangle(result,(ix,iy),(x,y),(0,255,0),-1)
            nx = x
            ny = y
        else:
            cv2.circle(result,(x,y),5,(0,0,255),-1)

def nothing(x):
    pass

def find_Blobs(im):
    im = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    im = 255 - im
    params = cv2.SimpleBlobDetector_Params()

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 2000
    params.maxArea = 15000

    params.filterByCircularity = False
    params.filterByConvexity = False
    params.filterByInertia = False
    # Set up the detector with default parameters.
    detector = cv2.SimpleBlobDetector_create(params)

    # Detect blobs.
    keypoints = detector.detect(im)

    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    #im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255),
                                          #cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    return keypoints

img = cv2.imread('saves/image_0.png')
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image',600,600)
#cv2.namedWindow("ref",cv2.WINDOW_NORMAL)
#cv2.resizeWindow("ref",600,600)

# create trackbars for color change
cv2.createTrackbar('Hue max','image',0,179,nothing)
cv2.createTrackbar('Hue min', 'image',0,179,nothing)
cv2.createTrackbar('Saturation','image',0,255,nothing)
cv2.createTrackbar('Value','image',0,255,nothing)

cv2.setTrackbarPos('Hue max','image',90)
cv2.setTrackbarPos('Hue min', 'image',70)
cv2.setTrackbarPos('Saturation','image',1)
cv2.setTrackbarPos('Value','image',1)


#cv2.imshow('ref',img)
cap = cv2.VideoCapture('saves/video_4.avi')
cv2.setMouseCallback('image',draw_circle)
play = True
while not cv2.waitKey(1) & 0xFF == ord('q'):
    if(cv2.waitKey(1) & 0xFF == ord('f')):
        if(play):
            play = False
        else:
            play = True
        print('play')
    if(play):
        ret, img = cap.read()

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV

    # get current positions of four trackbars
    hue_min = cv2.getTrackbarPos('Hue min', 'image')
    hue_max = cv2.getTrackbarPos('Hue max', 'image')
    saturation = cv2.getTrackbarPos('Saturation', 'image')
    value = cv2.getTrackbarPos('Value', 'image')

    lower_blue = np.array([hue_min,100, 100])
    upper_blue = np.array([hue_max, saturation, value])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img, img, mask=mask)
    result = res
    #keypoints = find_Blobs(res)
    #result = cv2.drawKeypoints(res, keypoints, np.array([]), (0, 0, 255),
     #                                      cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.rectangle(result, (ix, iy), (nx, ny), (0, 255, 0), 1)


    cv2.imshow('image',result)


    sleep(0.05)


cv2.destroyAllWindows()
cap.release()


