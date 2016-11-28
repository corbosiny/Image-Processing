'''**
    * Live Camera Session Class
    *
    * ACKNOWLEDGEMENT CREDITS to pyimagesearch:
    *
    * www.pyimagesearch.com
    *
    * Copyright (c) 2016 Alireza Bahremand
    *
    * Permission is hereby granted, free of charge, to any person obtaining a copy
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
import argparse
import datetime
from dropbox.client import DropboxOAuth2FlowNoRedirect
from dropbox.client import DropboxClient
import json
from Filters import Filters          # This should allow us to import the Filters file.
from WebcamVideoStream import WebcamVideoStream
from tempimage import TempImage
from Cascading import Cascading
from Detect_Blur import DetectBlur
from compressImages import ImageCompression

# For this program I'm testing the use of thresholding by applying different filters
# and seeing how easy it is to detect corners and objects within the camera frame.

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True,
                help="path to the json configuration file")
args = vars(ap.parse_args())


vs = WebcamVideoStream(src=0).start()       # so we want to read video in as a stream now so we can
#cap = cv2.VideoCapture(0)
filters = Filters()
cascades = Cascading()
blurDetection = DetectBlur(120)
imgCmpr = ImageCompression()


conf = json.load(open(args["conf"]))        # Load the json file.
client = None

# check to see if the Dropbox should be used
if conf["use_dropbox"]:
    # connect to dropbox and start the session authorization process
    flow = DropboxOAuth2FlowNoRedirect(conf["dropbox_key"], conf["dropbox_secret"])
    print "[INFO] Authorize this application: {}".format(flow.start())
    authCode = raw_input("Enter auth code here: ").strip()
    
    # finish the authorization and grab the Dropbox client
    (accessToken, userID) = flow.finish(authCode)
    client = DropboxClient(accessToken)
    print "[SUCCESS] dropbox account linked"

# INTEGRATED WITH DROPBOX PAST THIS POINT

''' OUR MAIN LOOP WHERE I WILL USE METHODS TO RETRIEVE DIFFERENT RESULTS
    FOR ALL THE THRESHOLDING AND CASCADING.
    '''
ts = time.time()                    # Retrieve current timing.
counter = 0
while True:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()
    lastUploaded = datetime.datetime.now()
    #saveFrame = frame                       # For storing a copy for encoding later on.
    frame = cv2.resize(frame, (500, 500))
    counter = 0
    # At 400 width we get a real nice frames per second, increasing
    # the value will result in less frames being read per second.
    #instance = vs.getGrabbed()
    #cascades.faceCascadeDetectionOfImage(instance)
    timestamp = 0
    # So now we store the grayFrame seperately aside from our regular colored
    # frame so we can perform processing on the grayframe since many open cv
    # operations are dependent upon a grayscaled image.
    grayFrame = filters.grayScaleImage(frame)
    # May need to take this line out.
    #grayFrame = cv2.GaussianBlur(grayFrame, (21, 21), 0)
    
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
    if (fm > (blurDetection.getBlurThresh()+20)): 
        counter = 0
        ts = timestamp  #.strftime("%A %d %B %Y %I:%M:%S%p")
        #if (timestamp - lastUploaded).seconds >= conf["min_upload_seconds"]:
        # check to see if dropbox sohuld be used
        if conf["use_dropbox"]:
            # write the image to temporary file
            
            t = TempImage()
            cv2.imwrite(t.path, frame)
                
                # upload the image to Dropbox and cleanup the tempory image
            print "[UPLOAD] {}".format(ts)
            path = "{base_path}/{timestamp}.jpg".format(
                                                        base_path=conf["dropbox_base_path"], timestamp=ts)
            client.put_file(path, open(t.path, "rb"))
            t.cleanup()
            
            # update the last uploaded timestamp and reset the motion
            # counter
            #lastUploaded = timestamp
            timestamp = timestamp + 1
        
        '''# So basically we set the conditional to have a limited range of blurDetectionThresh
        # We specify it to be 2 times the threshValue to save it.
        st = datetime.datetime.fromtimestamp(ts).strftime('_TS:%Y-%m-%d::%H:%M:%S')
        # Get a timestamp for the photo.
        
        # Perform encoding and decoding for safe practice & application of use for programs.
        imgCmpr.encodeImage(frame);                 # Encoding method.
        # Decode
        imgCmpr.decodeImage(frame);
        cv2.imwrite("NoneBlurDetectedPictures/" + str(counter) + st + ".jpg", frame)
        counter = counter + 1'''


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
