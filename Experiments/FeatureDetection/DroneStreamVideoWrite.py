import cv2
import numpy as np
from Cascading import Cascading

cascade = Cascading()
#capture = cv2.VideoCapture(0)   # Load video feed, we can also load a video from the directory if we wanted too, all we would do is place the path to the directory in here instead of the 0.
capture = cv2.VideoCapture(0)   # Loading a actual video.
# Will need to change directory for future testing, unless files are in same directory path.
fgbg = cv2.BackgroundSubtractorMOG2()         # The foreground for objects we want, we will subtract those from the actual background.
fourcc = cv2.cv.CV_FOURCC(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

while True:
    ret, frame = capture.read()     # Load the file into our boolean, then asssign it to a frame object.
    fgmask = fgbg.apply(frame)      # Lets apply the foregroundbackground to our frame, and assign that to a mask object.

# Perform a check to make sure we are getting video returned before performing
# operations or outputting to screen.
    if ret:
        cascade.faceCascadeDetectionOfImage(frame)
        out.write(frame)               # Write video file.
        cv2.imshow('original', frame)
        cv2.imshow('foreground', fgmask)
    if cv2.waitKey(1) == 27:
        break

    # May need to perform a frame = cv2.flip(frame, 0) for writing video because it will be flipped otherwise...POSSIBLY.
    
#cv2.imshow('original', frame)       # Create our frame for the original.
#   cv2.imshow('foreground', fgmask)    # Creat the frame for the mask after subtraction.

    k = cv2.waitKey(30) & 0xff          # Assign the waitKey to read from our keyboard.
    if k == 27:                         # If we press the esc key, we want to terminate the windows.
        break

capture.release()                   # Release the camera feed.
cv2.destroyAllWindows()
for i in range(1, 9):               # Since we have 2 frames, we need to execute a wait key 8 times.
    cv2.waitKey(1)
