# import the necessary packages
import datetime
import time
import cv2
import numpy as np
from Filters import Filters

# A thought possibly worth pursuing further down the line..
# Allow MotionDetection to take a parameter that is the first frame to be read
# and perform the motion tracking on it.
# Thus each time the object is created we are reading a new frame.
# Basically we want someway to call a method that will continuously update the first
# frame when need be.
class MotionDetection:

    def __init__(self):
        self.firstFrame = None      # Uninitialized static first frame variable.
        self.cornerDetectionThresh = 5000

    def refreshFirstFrame(self, frame):
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # So here we convert to grayscale cause color is irelevant
        #gray = cv2.GaussianBlur(gray, (31, 31), 0)      # We can change the region from 21 21 later for smoothing out noise.
        self.firstFrame = frame

    def increaseCornerDetectionThresh(self, threshValue):
        self.cornerDetectionThresh += threshValue
        print ("Value is now: " + str(self.cornerDetectionThresh))
    
    def decreaseCornerDetectionThresh(self, threshValue):
        self.cornerDetectionThresh -= threshValue
        print ("Value is now: " + str(self.cornerDetectionThresh))
    
    def showMotion(self, gray):

        frameDelta = cv2.absdiff(self.firstFrame, gray)  # The absdiff function will perform what its name is, so here though theres more to it.
            
        # We take the first original frame read (remember assumption that first frame has no movement
        # and we deduce the first frame from the grayscale to see the difference in frames
        # to compute the differences we are working with the array representation of the image in the background
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        # We apply a thresh to say hey, any change detected in the frame delta above a edge of 25 is motion from the original starting frame
        # and anything below 25 we ignore, and we do a simple thresh binary, either you have edges to make out or you dont. No gray area (pun)

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        #print thresh
        (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)

        return cnts, frameDelta



