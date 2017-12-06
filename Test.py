
import numpy as np
import cv2
from time import sleep


print("Hello World")
'''
image = cv2.imread('assets/Test3.jpg')
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.resizeWindow('frame',600,600)
#cv2.namedWindow('reference',cv2.WINDOW_NORMAL)
#cv2.resizeWindow('reference',600,600)

#gray = image[:,:,2] #= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#ret, filtered = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# define range of blue color in HSV
lower_blue = np.array([0, 50, 50])
upper_blue = np.array([10, 255, 255])
# Threshold the HSV image to get only blue colors
mask = cv2.inRange(hsv, lower_blue, upper_blue)
# Bitwise-AND mask and original image
res = cv2.bitwise_and(image, image, mask=mask)
print("Test")
#cv2.imshow('reference',image)
cv2.imshow('frame', res)
#cv2.imshow('image', im)



while not cv2.waitKey(1) & 0xFF == ord('q'):
        sleep(0.1)

cv2.destroyAllWindows()
#cv2.imwrite('Red.jpg',res)



cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if(not ret):
        continue
    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #frame[:,:,1:3]=0
    #image = frame


    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_blue = np.array([155, 160, 5])
    upper_blue = np.array([190, 255, 255])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)


    # Display the resulting frame
    cv2.imshow('frame',res)
    cv2.imshow('reference',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

import zbar

from PIL import Image
import cv2


def main():
    """
    A simple function that captures webcam video utilizing OpenCV. The video is then broken down into frames which
    are constantly displayed. The frame is then converted to grayscale for better contrast. Afterwards, the image
    is transformed into a numpy array using PIL. This is needed to create zbar image. This zbar image is then scanned
    utilizing zbar's image scanner and will then print the decodeed message of any QR or bar code. To quit the program,
    press "q".
    :return:


    # Begin capturing video. You can modify what video source to use with VideoCapture's argument. It's currently set
    # to be your webcam.
    capture = cv2.VideoCapture(0)

    while True:
        # To quit this program press q.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Breaks down the video into frames
        ret, frame = capture.read()

        # Displays the current frame
        cv2.imshow('Current', frame)

        # Converts image to grayscale.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Uses PIL to convert the grayscale image into a ndary array that ZBar can understand.
        image = Image.fromarray(gray)
        width, height = image.size
        #zbar_image = zbar.Image(width, height, 'Y800', image.tostring())

        # Scans the zbar image.
        scanner = zbar.Scanner()
        scanner.scan(image)

        # Prints data from image.
        for decoded in image:
            print(decoded.data)


if __name__ == "__main__":
        main()
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