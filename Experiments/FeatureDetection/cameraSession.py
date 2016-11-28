import cv2
import numpy as np
import time
import datetime
import sys
import os.path
from Filters import Filters          # This should allow us to import the Filters file.
from WebcamVideoStream import WebcamVideoStream
from Cascading import Cascading
from Detect_Blur import DetectBlur
from compressImages import ImageCompression
from WindowDestruction import WindowDestruction
from MotionDetection import MotionDetection


class CameraSession():


    def __init__(self):
        # If video source is USB device for testing, we will use the vs and cap variables below.
        #self.vs = WebcamVideoStream(src=0).start()       # so we want to read video in as a stream now so we can
        self.capture = cv2.VideoCapture(0)
        # CHANGE MILES
        # 0 for drone,
        # 1 for webcam in the case of Miles computer

        # If video source is drone, we will use the code below.
        self.fourcc = cv2.cv.CV_FOURCC(*'XVID')
        self.out = cv2.VideoWriter('output.mov', self.fourcc, 20.0, (640, 480))
        # So we want to open application for video driver first, and then run file.
        # Currently the webcam video stream class does not work for video capture, therefore we
        # need to stick to cv2.VideoCapture() until WebcamVideoStream can be optimized for working.

        # Instantiate objects
        self.filters = Filters()                             # Filters for filtering the file.
        self.motionDetection = MotionDetection()             # MotionDetection for grabbing motion.
        self.cascadeDetection = Cascading()                  # Cascading for feature recognition.
        self.blurDetection = DetectBlur(150)                 # 100 would be the value to be used for fine tuning.
        self.destroyWindows = WindowDestruction()

        time.sleep(0.25)                                # Allow camera a few miliseconds for booting up.
        self.firstFrame = None                               # First frame is a variable to be used for motion tracking, firstFrame is the frame being compared for motion change.

        # Initiate toggles.
        self.motionTime = False
        self.cascadeTime = False
        self.blurDetectionTime = False

        # Initialize external variables.
        self.numFrames = 0
        self.ts = time.time()
        
    def main(self):
        counter = 0                                 # Counter for gathering image files for blur detection. Counter increments number of pictures for filename.
        while True:
            # grab the frame from the threaded video stream and resize it
            # to have a maximum width of 400 pixels
            # CHANGE MILES
            #frame = self.vs.read()
            ret, frame = self.capture.read()
            
            # If the WebcamVideoStream object has a frame grabbed, lets perform the basic required operations for all the features.
            # CHANGE MILES
            if (ret):
            #if (self.vs.grabbed):
                #self.motionDetection.refreshFirstFrame(frame)
                grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Grayscale the image
                grayGausFrame = cv2.GaussianBlur(grayFrame, (21, 21), 0)            # Second, we want to apply a guassian blur to reduce noise.
            # originally our dimensions for gaussian blur is 21 by 21

                #commandImage = str(input('Enter Image Function to perform:'))           # String input variable for checking.
                
                if (cv2.waitKey(3) & 0xFF == ord('m')):    # Initiate motion tracking feature.
                    print "You initiated the motion tracking featurette"
                    # Toggle switch
                    if (self.motionTime != True):
                        self.motionTime = True
                    else:
                        self.motionTime = False
                        print "Motion tracking is turned off."
                        # Cascade checking.
                elif (cv2.waitKey(3) & 0xFF == ord('c')):  # Initiate cascade detection feature.
                    print "You initiated the cascade image recogntion feature"
                    # Toggle on off the cascading featurette.
                    if (self.cascadeTime != True):
                        self.cascadeTime = True
                    else:
                        self.cascadeTime = False
                        print "Cascading is turned off."
                elif (cv2.waitKey(3) & 0xFF == ord('b')):  # Initiate blur detection feature.
                    print "You initiated the blur detection featurette."
                    if (self.blurDetectionTime != True):
                        self.blurDetectionTime = True
                    else:
                        self.blurDetectionTime = False
                        print "Blur detection is turned off."
                # May want to sub categorize the 'r' 'u' & 'd' keys.
                elif (cv2.waitKey(5) & 0xFF == ord('r')):   # Refresh the first frame for motion tracking.
                    print "You pressed refresh"
                    self.motionDetection.refreshFirstFrame(frame)
                    continue
                elif (cv2.waitKey(5) & 0xFF == ord('i')):  # Increase motion tracking thresh.
                    print("You increased the motion detection thresh value to " + str(self.motionDetection.cornerDetectionThresh))
                    self.motionDetection.increaseCornerDetectionThresh(100)
                    continue
                elif (cv2.waitKey(5) & 0xFF == ord('d')):  # Decrease motion tracking thresh.
                    print("You decreased the motion detection thresh value to " + str(self.motionDetection.cornerDetectionThresh))
                    self.motionDetection.decreaseCornerDetectionThresh(100)
                    continue
                elif (cv2.waitKey(5) & 0xFF == ord('q')):  # Increase blur detection thresh.
                    newBlurThresh = (75 + self.blurDetection.getBlurThresh())
                    self.blurDetection.setBlurThresh(newBlurThresh)
                    print("You increased blur detection thresh to " + str(self.blurDetection.getBlurThresh()))
                    continue
                elif (cv2.waitKey(5) & 0xFF == ord('w')):  # Decrease blur detection thresh.            
                    newBlurThresh = (self.blurDetection.getBlurThresh() - 75)
                    self.blurDetection.setBlurThresh(newBlurThresh)
                    print("You decreased blur detection thresh to " + str(self.blurDetection.getBlurThresh()))
                    continue
                # Alas, apart of the motion tracking, if our first frame is set to none, we will set it up ourselves.
                elif self.motionDetection.firstFrame is None:
                    self.motionDetection.refreshFirstFrame(frame)
                    continue



                ''' End of object featurette toggling via keyboard keys. '''
                # Toggle checks
                if (self.motionTime):
                    cnts, frameDelta = self.motionDetection.showMotion(grayFrame)
                    
                    for c in cnts:
                        # if the contour is too small, ignore it
                        # In respect to fine tuning, it looks like around 500 is optimal for testing in a room like environment.
                        # A change occurs if we want to notice someone walking in, or motion in a undetected scene, then we jump the gun to 4500+.
                        if cv2.contourArea(c) < self.motionDetection.cornerDetectionThresh:     # Value to fine tune.
                            continue
                            # compute the bounding box for the contour, draw it on the frame,
                            # and update the text
                        (x, y, w, h) = cv2.boundingRect(c)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                elif (self.cascadeTime):         # If we chose to perform haarcascading
                    self.cascadeDetection.faceCascadeDetectionOfImage(frame)
                elif (self.blurDetectionTime):
                    # We grayscaled it so we can apply the laplacian variance on the grayscaled frame.
                    fm = self.blurDetection.variance_of_laplacian(grayFrame)             # Return an integer value depicting the varaiance factor of blur detection.
                    # This will be the value that is outputted to the screen.
                    
                    #if (fm > ((self.blurDetection.getBlurThresh()/2)+self.blurDetection.getBlurThresh())):
                    if (fm > (self.blurDetection.getBlurThresh()*5)):
                                                                                    
                    # So basically we set the conditional to have a limited range of blurDetectionThresh
                    # We specify it to be 2 times the threshValue to save it.
                    #myDirname = os.path.normpath("C:/Users/M4l2l_es/Dropbox/Ali_and_miless_awesome_vision_stuff/FeatureDetection/NoneBlurDetectedPictures/")
                        st = datetime.datetime.fromtimestamp(self.ts).strftime('_TS:%Y-%m-%d::%H:%M:%S')
                        # CHANGE MILES
                        #myDirName = os.path.normpath("NoneBlurDetectedPictures/" + str(counter) + st + ".png")  # os.path.normpath will set the directory path for any opreating system.
                        myDirName = str(counter) + "Image" + ".jpg"
                        cv2.imwrite(myDirName, frame)
                        counter = counter + 1
                    text = ""           # will have to get rid of text variable later below and beside.
                    cv2.putText(frame, "{}: {:.2f}".format(text, fm), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 3)

                # Outside of toggle checks lets render the frames
                cv2.imshow("Frame", frame)
                self.out.write(frame)               # Writing frame, so outputting frame to file.
                k = cv2.waitKey(1) & 0xFF
                if k == 27:
                    break

        # CHANGE MILES
        #self.vs.stop()
        self.capture.release()
        cv2.destroyAllWindows()
        self.destroyWindows.windowDestroyer(1)


if __name__ == '__main__':
    cameraSession = CameraSession()
    cameraSession.main()
