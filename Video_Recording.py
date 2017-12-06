
import numpy as np
import cv2
from random import randint

cap = cv2.VideoCapture(1 )

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
vid_name = 'Video_Saves/output_' + str(randint(0,30000000))+ '.avi'
out = cv2.VideoWriter(vid_name,fourcc, 20.0,(640,480))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        #frame = cv2.flip(frame,0)

        # write the flipped frame
        out.write(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()

