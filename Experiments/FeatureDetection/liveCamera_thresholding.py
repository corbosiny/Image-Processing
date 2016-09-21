import cv2
import numpy as np
from Filters import Filters          # This should allow us to import the Filters file.
from WebcamVideoStream import WebcamVideoStream
from Cascading import Cascading

# For this program I'm testing the use of thresholding by applying different filters
# and seeing how easy it is to detect corners and objects within the camera frame.

vs = WebcamVideoStream(src=0).start()       # so we want to read video in as a stream now so we can
#cap = cv2.VideoCapture(0)
filters = Filters()
cascades = Cascading()
''' OUR MAIN LOOP WHERE I WILL USE METHODS TO RETRIEVE DIFFERENT RESULTS
    FOR ALL THE THRESHOLDING AND CASCADING.
'''

while True:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()
    frame = cv2.resize(frame, (400, 400))
    # At 400 width we get a real nice frames per second, increasing
    # the value will result in less frames being read per second.
    #instance = vs.getGrabbed()
    #cascades.faceCascadeDetectionOfImage(instance)
    #frame = filters.grayScaleImage(frame)
    frame = filters.simpleThreshBinary(frame)

    # Keep note of error I have run into with colored thresholding.. 

# Important to note that, if we decease the usage of imshow, we can radically increase our FPS reading, adding the imshow function will cause
# our project to have to read in frames, while also outputting frames, which causes a lot of processing and takes up time from which the thread
# could be reading in frames.
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
for i in range(1,5):
    cv2.waitKey(1)

vs.stop()               # Stops the reading in of frames.

    #ret, img = cap.read()
    
    #threshImage = Filters.simpleThreshBinary(img)               # Retrieve a thresholded image.

#grayscale = Filters.grayScaleImage(img)
#grayscaledThresh = Filters.simpleThreshBinary(grayscale)    # Retrieve a thresholded grayscale image.

#    gaussianBlurredImage = Filters.gaussianBlurApplying(img)    # We have a guassian blurred image.
#    adaptiveThreshGaus = Filters.adaptiveThresholding_Gaus(img) # Now we have a adaptive threshold example.

    # Edge detection
    
    
    # Face detection portion
    #faceCascadeDetectionOfImage(gaussianBlurredImage)

    
    #g_img = gaus
    #g_img *= 1./255     # Trying to convert floating image values to CV_8U
    
    #edges = cv2.Canny(gaus_binary_inv, 100, 200)
    
    #cv2.imshow('original', img)
    #cv2.imshow('GaussianBlur', gaussianBlurredImage)
    
    #cv2.imshow('AdaptiveThresh', adaptiveThreshGaus)
    #cv2.imshow('threshold', threshold)
    #cv2.imshow('grayscaledThreshold', grayscaledThreshold)
    #cv2.imshow('threshold2', threshold2)
    #cv2.imshow('gausEdge', edges)
    
'''cap.release()
cv2.destroyAllWindows()
for i in range(1,13):        # A range of 8 becayse we have 4 waitKey's per image.
    cv2.waitKey(1)'''
