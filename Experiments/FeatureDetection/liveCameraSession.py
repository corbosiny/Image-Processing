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
import os.path
from Filters import Filters          # This should allow us to import the Filters file.
from WebcamVideoStream import WebcamVideoStream
from Cascading import Cascading
from Detect_Blur import DetectBlur
from compressImages import ImageCompression
#from MotionDetection import MotionDetection
from WindowDestruction import WindowDestruction

# For this program I'm testing the use of thresholding by applying different filters
# and seeing how easy it is to detect corners and objects within the camera frame.

#vs = WebcamVideoStream(src=1).start()       # so we want to read video in as a stream now so we can
cap = cv2.VideoCapture(1)
filters = Filters()
#cascades = Cascading()
blurDetection = DetectBlur(140) # 100 would be the value to be used for fine tuning.
#imgCmpr = ImageCompression()

destroyWindows = WindowDestruction()
''' OUR MAIN LOOP WHERE I WILL USE METHODS TO RETRIEVE DIFFERENT RESULTS
    FOR ALL THE THRESHOLDING AND CASCADING.
'''
ts = time.time()                    # Retrieve current timing.
counter = 0
while True:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    ret, frame = cap.read()
    #saveFrame = frame                       # For storing a copy for encoding later on.
    frame = cv2.resize(frame, (500, 500))

    
    # At 400 width we get a real nice frames per second, increasing
    # the value will result in less frames being read per second.
    #instance = vs.getGrabbed()
    #cascades.faceCascadeDetectionOfImage(instance)

    # So now we store the grayFrame seperately aside from our regular colored
    # frame so we can perform processing on the grayframe since many open cv
    # operations are dependent upon a grayscaled image.
    grayFrame = filters.grayScaleImage(frame)
    
    # We should add a guassian blur here to reduce noise.
    #grayFrame = filters.gaussianBlurApplying(frame)
    
    # We grayscaled it so we can apply the laplacian variance on the grayscaled
    # frame.
    fm = blurDetection.variance_of_laplacian(grayFrame)
    text = "Not Blurry"

    # if the focus measure is less than the supplied threshold,
    # then the image should be considered "blurry"
   
    if fm < blurDetection.getBlurThresh():
        text = "Blurry"

    # If the image is below our blurThresh value, we want to save that image
    # to encode and send out.
    #instance = vs.getGrabbed()
    
    #cascades.faceCascadeDetectionOfImage(frame)

    # Long term goal would be to compress image into single row matrix as
    # string, write that to txt file, and send that off to mother station
    # to which mother station will decode them all and have picture presented.

#if (fm > ((blurDetection.getBlurThresh()/2)+blurDetection.getBlurThresh())):
    if (fm > (2*blurDetection.getBlurThresh())):

    # So basically we set the conditional to have a limited range of blurDetectionThresh
    # We specify it to be 2 times the threshValue to save it.
        st = datetime.datetime.fromtimestamp(ts).strftime('_TS:%Y-%m-%d::%H:%M:%S')
        # Get a timestamp for the photo.
        
        # Perform encoding and decoding for safe practice & application of use for programs.
        #imgCmpr.encodeImage(frame);                 # Encoding method.
        # Decode
        #imgCmpr.decodeImage(frame);
        #myDirname = os.path.normpath("C:/Users/M4l2l_es/Dropbox/Ali_and_miles_awesome_vision_stuff/FeatureDetection/NoneBlurDetectedPictures/")
        myDirname = os.path.normpath("C:/Users/M4l2l_es/Desktop/Ali_and_miles_awesome_vision_stuff/FeatureDetection/NoneBlurDetectedPictures/")
        cv2.imwrite(myDirname + str(counter) + st + ".jpg", frame)
        print myDirname + str(counter) + st + ".jpg" + " just got saved!"
        counter = counter + 1

    # The blurriness is detected from the grayscaled form of our image
    # which is being detected instantaneously while we stream the regular
    # colored frame, so we are essentially doing parallel frame processing with
    # the stream outputting the frame while we do some grayscaled calculations
    # in the back end side of things.
    # show the image
    cv2.putText(frame, "{}: {:.2f}".format(text, fm), (10, 30),
    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)

    #frame = filters.simpleThreshBinary(frame)

    # Keep note of error I have run into with colored thresholding.. 

# Important to note that, if we decease the usage of imshow, we can radically increase our FPS reading, adding the imshow function will cause
# our project to have to read in frames, while also outputting frames, which causes a lot of processing and takes up time from which the thread
# could be reading in frames.
    cv2.imshow("Frame", frame)
    #cv2.imshow("ThreshFrame", threshedOut)
    #cv2.imshow("DeltaFrame", deltaOut)
    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
destroyWindows.windowDestroyer(1)

cap.release()               # Stops the reading in of frames.
#vs.stop()
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
