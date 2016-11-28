import numpy as np
import cv2

cam_index=0
cap=cv2.VideoCapture(cam_index)


print cap.isOpened()
ret, frame=cap.read()

#print frame.shape[0]
#print frame.shape[1]

while (cap.isOpened()):
    ret, frame=cap.read()
    #gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    cv2.imshow('frame', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#release and close 
cap.release()
cv2.destroyAllWindows() 
