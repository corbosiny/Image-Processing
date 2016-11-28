'''**
 * Live Camera Session Class
 *
 * ACKNOWLEDGEMENT CREDITS to pyimagesearch:
 *
 * www.pyimagesearch.com
 *
 * Copyright (c) 2016 Alireza Bahremand
 *
 * Permission is hereby5 granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */'''

import cv2
import numpy as np
import time
import datetime
from Filters import Filters          # This should allow us to import the Filters file.
from WebcamVideoStream import WebcamVideoStream
from Cascading import Cascading
from Detect_Blur import DetectBlur
from compressImages import ImageCompression
#from MotionDetection import MotionDetection
from WindowDestruction import WindowDestruction
from MotionDetection import MotionDetection

# For this program I'm testing the use of thresholding by applying different filters
# and seeing how easy it is to detect corners and objects within the camera frame.

vs = WebcamVideoStream(src=0).start()       # so we want to read video in as a stream now so we can
#cap = cv2.VideoCapture(0)
filters = Filters()
fourcc = cv2.cv.CV_FOURCC(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
motion = MotionDetection()

destroyWindows = WindowDestruction()

firstFrame = None

while True:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()
    #saveFrame = frame                       # For storing a copy for encoding later on.
    #frame = cv2.resize(frame, (500, 500))

# If the WebcamVideoStream object has a frame grabbed, lets perform operations.
if (vs.grabbed):
        gray = filters.grayScaleImage(frame)
        gray = filters.gausBlurSpecified(gray, 21, 21)
        # originally our dimensions for gaussian blur is 21 by 21
         
        # if the first frame is None, initialize it
        '''if (cv2.waitKey(20) & 0xFF == ord('r')):    # If r is pressed we want to refresh frame to
            firstFrame = gray
            continue
        else:
            firstFrame = gray
            continue'''
        if firstFrame is None:
            firstFrame = gray
            continue

        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(firstFrame, gray)  # The absdiff function will perform what its name is, so here though theres more to it.

        print frameDelta

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
            if cv2.contourArea(c) < 5000:     # Value to fine tune.
                 continue
     
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
        cv2.imshow("Frame", frame)
        out.write(frame)
    #cv2.imshow("ThreshFrame", threshedOut)
    #cv2.imshow("DeltaFrame", deltaOut)
    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break


vs.stop()               # Stops the reading in of frames.
cv2.destroyAllWindows()
destroyWindows.windowDestroyer(1)


 

