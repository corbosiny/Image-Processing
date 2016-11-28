'''** * Webcam Video Stream Class * * ACKNOWLEDGEMENT CREDITS to
 pyimagesearch: * * www.pyimagesearch.com * * Copyright (c) 2016 Alireza
 Bahremand * * Permission is hereby granted, free of charge, to any
 person obtaining a copy * of this software and associated documentation
 files (the "Software"), to deal * in the Software without restriction,
 including without limitation the rights * to use, copy, modify, merge,
 publish, distribute, sublicense, and/or sell * copies of the Software,
 and to permit persons to whom the Software is * furnished to do so,
 subject to the following conditions: * * The above copyright notice and
 this permission notice shall be included in all * copies or substantial
 portions of the Software. * * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT
 WARRANTY OF ANY KIND, EXPRESS OR * IMPLIED, INCLUDING BUT NOT LIMITED
 TO THE WARRANTIES OF MERCHANTABILITY, * FITNESS FOR A PARTICULAR
 PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE * AUTHORS OR
 COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER *
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 FROM, * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 DEALINGS IN THE * SOFTWARE. */'''


# import the necessary packages
from threading import Thread
import cv2
 
class WebcamVideoStream:
        def __init__(self, src=0):
                # initialize the video camera stream and read the first frame
                # from the stream
                self.stream = cv2.VideoCapture(src)

                self.size = (int(self.stream.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
                        int(self.stream.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
                
                
                (self.grabbed, self.frame) = self.stream.read()

                # initialize the variable used to indicate if the thread should
                # be stopped
                self.stopped = False
        def start(self):
                # start the thread to read frames from the video stream
                Thread(target=self.update, args=()).start()
                # Arguments work as follows, update is the callable object invoked from the run method
                # for the thread, it runs frames from our video stream.
                return self
 
        def update(self):
                # keep looping infinitely until the thread is stopped
                while True:
                        # if the thread indicator variable is set, stop the thread
                        if self.stopped:
                                return          # Break out the statement early and stop the reading of frames.

                        # otherwise, read the next frame from the stream
                        (self.grabbed, self.frame) = self.stream.read()

        def read(self):
        # return the frame most recently read
                return self.frame

        def getGrabbed(self):
                return self.grabbed

        def stop(self):
                # indicate that the thread should be stopped
                self.stopped = True


