import numpy as np
import cv2

cap = cv2.VideoCapture(0)       # Activate camera.
 
while(True):
    ret, frame = cap.read() # Return boolean indication of whether we get video, if so store it in frame object.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Grayscale it for readability of manipulation.
 
    cv2.imshow('frame',gray)                # Show frame.
    if cv2.waitKey(1) & 0xFF == ord('q'):   # Once we hit the letter q, lets de-activate the frame. If we did number 27, that would be the escape key BTW.
        break

cap.release()           # Release the camera.
cv2.destroyAllWindows() # Destroy the window frames we created through imshow command.
for i in range(1,5):
    cv2.waitKey(1)          # We have to do a wait Key of 1, 4 times for delays created through instructions. This will destroy the window, 4 wait's per frame created!
