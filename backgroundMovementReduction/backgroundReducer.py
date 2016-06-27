import cv2
import numpy as np

#capture = cv2.VideoCapture(0)   # Load video feed, we can also load a video from the directory if we wanted too, all we would do is place the path to the directory in here instead of the 0.
capture = cv2.VideoCapture('people-walking.mp4')   # Loading a actual video.
# Will need to change directory for future testing, unless files are in same directory path.
fgbg = cv2.BackgroundSubtractorMOG2()         # The foreground for objects we want, we will subtract those from the actual background.


while True:
    ret, frame = capture.read()     # Load the file into our boolean, then asssign it to a frame object.
    fgmask = fgbg.apply(frame)      # Lets apply the foregroundbackground to our frame, and assign that to a mask object.

    cv2.imshow('original', frame)       # Create our frame for the original.
    cv2.imshow('foreground', fgmask)    # Creat the frame for the mask after subtraction.

    k = cv2.waitKey(30) & 0xff          # Assign the waitKey to read from our keyboard.
    if k == 27:                         # If we press the esc key, we want to terminate the windows.
        break

capture.release()                   # Release the camera feed.
cv2.destroyAllWindows()
for i in range(1, 9):               # Since we have 2 frames, we need to execute a wait key 8 times.
    cv2.waitKey(1)
