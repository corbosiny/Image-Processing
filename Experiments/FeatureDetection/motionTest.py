# import the necessary packages
import datetime
import time
import cv2
from WindowDestruction import WindowDestruction
from WebcamVideoStream import WebcamVideoStream
import numpy as np
from MotionDetection import MotionDetection
from Cascading import Cascading

motion = MotionDetection()
destroyWindows = WindowDestruction()
cascades = Cascading()
# camera = cv2.VideoCapture(0)
camera = WebcamVideoStream(src=0).start() 
time.sleep(0.25)
# initialize the first frame in the video stream
# WE WILL WANT TO UPDATE THIS VARIABLE TO OFTEN CHANGE THE FIRST FRAME
# BASED ON MOVEMENT OF MOTION...WILL BE TRICKY.

cascadeTime = False

# loop over the frames of the video
while True:
    # grab the current frame and initialize the occupied/unoccupied
    # text
    
    frame = camera.read()
    #saveFrame = frame                       # For storing a copy for encoding later on.
    frame = cv2.resize(frame, (500, 500))
    #(grabbed, frame) = camera.read()
    #text = "Unoccupied"
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # So here we convert to grayscale cause color is irelevant
    gray = cv2.GaussianBlur(gray, (31, 31), 0)      # We can change the region from 21 21 later for smoothing out noise.

    
    if (cv2.waitKey(20) & 0xFF == ord('r')):    # If r is pressed we want to refresh frame to perform delta on.
        print "You pressed refresh"
        motion.refreshFirstFrame(frame)
        continue
    elif (cv2.waitKey(20) & 0xFF == ord('u')):
        print "You pressed the up arrow key"
        motion.increaseCornerDetectionThresh(100)
        continue
    elif (cv2.waitKey(20) & 0xFF == ord('d')): #Down arrow
        print "You pressed the down arrow key"
        motion.decreaseCornerDetectionThresh(100)
        continue
    elif (cv2.waitKey(20) & 0xFF == ord('c')):
        print "Cascade time"
        if cascadeTime == True:
            cascadeTime = False
        else:
            cascadeTime = True
            print "Cascading is true"
    elif motion.firstFrame is None:
        motion.refreshFirstFrame(frame)
        continue
    '''elif firstFrame is None:
        firstFrame = gray
        continue'''



    cnts, frameDelta = motion.showMotion(gray)
    #print cnts

    for c in cnts:
        # if the contour is too small, ignore it
        # In respect to fine tuning, it looks like around 500 is optimal for testing in a room like environment.
        # A change occurs if we want to notice someone walking in, or motion in a undetected scene, then we jump the gun to 4500+.
        if cv2.contourArea(c) < motion.cornerDetectionThresh:     # Value to fine tune.
            continue
            
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        if cascadeTime:         # If we chose to perform haarcascading
            cascades.eyeCascadeDetectionOfImage(frame)

    '''
    # if the frame could not be grabbed, then we have reached the end
    # of the video
    #if not grabbed:
     #   break
 
    # resize the frame, convert it to grayscale, and blur it
    #frame = cv2.resize(frame, (500, 500))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # So here we convert to grayscale cause color is irelevant
    gray = cv2.GaussianBlur(gray, (31, 31), 0)      # We can change the region from 21 21 later for smoothing out noise.
    # originally our dimensions for gaussian blur is 21 by 21
     
    # if the first frame is None, initialize it

    if (cv2.waitKey(20) & 0xFF == ord('r')):    # If r is pressed we want to refresh frame to perform delta on.
        print "You pressed refresh"
        firstFrame = gray
        continue
    elif (cv2.waitKey(20) & 0xFF == ord('u')):
        print "You pressed the up arrow key"
        counterDetectionValue += 100
        continue
    elif (cv2.waitKey(20) & 0xFF == ord('d')): #Down arrow
        print "You pressed the down arrow key"
        counterDetectionValue -= 100
        continue
    elif firstFrame is None:
        firstFrame = gray
        continue
    
    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)  # The absdiff function will perform what its name is, so here though theres more to it.

    #print frameDelta

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
    #print cnts
    # FindContours simply finds the contours (which are edges), it takes a copy
    # of the dilated image for src image read, we do a cv2.RETR_EXTERNAL which means
    # we only want the eldest contour of the family detection, we could also use RETR_CCOMP to retrieve all levels of counter detection.
    # The contour detection basically has several levels of edges, sort of like layers of edges to detect edges within edges.
    # The chain_approx_simple says hey, lets not worry about edges that are redundant, a good example would be a straight line.
    # We want only the end point edges, we dont need to read every single point on the line as an edge.

    # Keep note that we store each contour found into our cnts value which will be an list of contour points
 
    # loop over the contours in the cnts variable which extracts found contour points from dilated, guassiated, grayscaled image frame.
    for c in cnts:
        # if the contour is too small, ignore it
        # In respect to fine tuning, it looks like around 500 is optimal for testing in a room like environment.
        # A change occurs if we want to notice someone walking in, or motion in a undetected scene, then we jump the gun to 4500+.
        if cv2.contourArea(c) < counterDetectionValue:     # Value to fine tune.
             continue
 
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"
                
    # draw the text and timestamp on the frame
# cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
#       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
#   cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
#       (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
 '''
    
    '''# show the frame and record if the user presses a key
    cv2.imshow("Security Feed", frame)
    #cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    
 '''
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Frame Delta", frameDelta)

    key = cv2.waitKey(1) & 0xFF
    # if the `esc` key is pressed, break from the lop
    if key == 27:
        break
 
# cleanup the camera and close any open windows
camera.stop()
cv2.destroyAllWindows()
destroyWindows.windowDestroyer(2)
        
