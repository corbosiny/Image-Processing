import cv2
import numpy as np
import time
import datetime
from Cascading import Cascading
from Detect_Blur import DetectBlur

blurDetection = DetectBlur(140)
cascade = Cascading()
#capture = cv2.VideoCapture(0)   # Load video feed, we can also load a video from the directory if we wanted too, all we would do is place the path to the directory in here instead of the 0.
capture = cv2.VideoCapture('testFlight.MP4')   # Loading a actual video.
# Will need to change directory for future testing, unless files are in same directory path.
fgbg = cv2.BackgroundSubtractorMOG2()         # The foreground for objects we want, we will subtract those from the actual background.


# Define size of video for reading in
size = (int(capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
        int(capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
# Define FPS
fps = 20

#fourcc = cv2.cv.CV_FOURCC(*'XVID')
fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
#vout = cv2.VideoWriter()
#success = vout.open('output.mov', fourcc, fps, size, True)

#out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
ts = time.time()
counter = 0
while True:
    ret, frame = capture.read()     # Load the file into our boolean, then asssign it to a frame object.
    fgmask = fgbg.apply(frame)      # Lets apply the foregroundbackground to our frame, and assign that to a mask object.
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    blurVariance = blurDetection.variance_of_laplacian(gray)
    edged = cv2.Canny(blurred, 50, 150)
    # May need to perform a frame = cv2.flip(frame, 0) for writing video because it will be flipped otherwise...POSSIBLY.
    #out.write(frame)               # Write video file.
    #vout.write(casc)
    if (blurVariance > ((blurDetection.getBlurThresh()/2)+blurDetection.getBlurThresh())):
        st = datetime.datetime.fromtimestamp(ts).strftime('_TS:%Y-%m-%d::%H:%M:%S')
        cv2.imwrite("NonBlurVideoInput/" + str(counter) + st + ".jpg", frame)
        counter = counter + 1


  
    cv2.imshow('original', frame)       # Create our frame for the original.
    cv2.imshow('foreground', edged)    # Creat the frame for the mask after subtraction.

    k = cv2.waitKey(30) & 0xff          # Assign the waitKey to read from our keyboard.
    if k == 27:                         # If we press the esc key, we want to terminate the windows.
        break

capture.release()                   # Release the camera feed.
#vout.release
#vout = None
cv2.destroyAllWindows()
for i in range(1, 9):               # Since we have 2 frames, we need to execute a wait key 8 times.
    cv2.waitKey(1)
