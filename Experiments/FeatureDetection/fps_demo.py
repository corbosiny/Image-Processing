# import the necessary packages
from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils
import cv2
import numpy as np


face_cascade = cv2.CascadeClassifier('../FeatureDetection/HaarCascades/haarcascade_frontalface_default.xml')    # Assign our face cascade with the attributes of the downloaded xml file.
eye_cascade = cv2.CascadeClassifier('../FeatureDetection/HaarCascades/haarcascade_eye.xml')    
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100,
    help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
    help="Whether or not frames should be displayed")
args = vars(ap.parse_args())

# grab a pointer to the video stream and initialize the FPS counter
print("[INFO] sampling frames from webcam...")
stream = cv2.VideoCapture(0)
fps = FPS().start()
 
# loop over some frames
while fps._numFrames < args["num_frames"]:
    # grab the frame from the stream and resize it to have a maximum
    # width of 400 pixels
    (grabbed, frame) = stream.read()
    frame = imutils.resize(frame, width=400)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    # Easier to read from grayscaled images.
    faces = face_cascade.detectMultiScale(gray, 1.8, 5) # Depending on size and likelihood we would change the numerical values, and we are gonna read from the grayscaled image.
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)    # Lets start at x and y until we width and height of the image, and lets draw a blue rectangle around its detection, accompanied with a width of
        roi_gray = gray[y:y+h, x:x+w]   # So the region of image we want is grayscaled, we take the y region till its end and the x region till its end for the found object within the image, and we assign that to our region of the image.
        # So in summary roi_gray is the region of detection within the image and a rectangle will be surrounding it.
        roi_color = frame[y:y+h, x:x+w]   # Same thing as roi_gray but we want to have the colored region saved.
        # Now we will define the eye detection within the face detection.
        eyes = eye_cascade.detectMultiScale(roi_gray)   # Lets search for eyes within the gray face image.
        for (ex, ey, ew, eh) in eyes:
            # Lets draw a green rectangle around we starting and ending points of the eye detection.
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
         
    # check to see if the frame should be displayed to our screen
    if args["display"] > 0:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    # Easier to read from grayscaled images.
        faces = face_cascade.detectMultiScale(gray, 1.8, 5) # Depending on size and likelihood we would change the numerical values, and we are gonna read from the grayscaled image.
        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)    # Lets start at x and y until we width and height of the image, and lets draw a blue rectangle around its detection, accompanied with a width of
            roi_gray = gray[y:y+h, x:x+w]   # So the region of image we want is grayscaled, we take the y region till its end and the x region till its end for the found object within the image, and we assign that to our region of the image.
            # So in summary roi_gray is the region of detection within the image and a rectangle will be surrounding it.
            roi_color = frame[y:y+h, x:x+w]   # Same thing as roi_gray but we want to have the colored region saved.
            # Now we will define the eye detection within the face detection.
            eyes = eye_cascade.detectMultiScale(roi_gray)   # Lets search for eyes within the gray face image.
            for (ex, ey, ew, eh) in eyes:
                # Lets draw a green rectangle around we starting and ending points of the eye detection.
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        
 
    # update the FPS counter
    fps.update()
 
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
 
# do a bit of cleanup
stream.release()
cv2.destroyAllWindows()
# created a *threaded* video stream, allow the camera sensor to warmup,
# and start the FPS counter
print("[INFO] sampling THREADED frames from webcam...")
vs = WebcamVideoStream(src=0).start()
fps = FPS().start()
 
# loop over some frames...this time using the threaded stream
while fps._numFrames < args["num_frames"]:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    # Easier to read from grayscaled images.
    faces = face_cascade.detectMultiScale(gray, 1.8, 5) # Depending on size and likelihood we would change the numerical values, and we are gonna read from the grayscaled image.
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)    # Lets start at x and y until we width and height of the image, and lets draw a blue rectangle around its detection, accompanied with a width of
        roi_gray = gray[y:y+h, x:x+w]   # So the region of image we want is grayscaled, we take the y region till its end and the x region till its end for the found object within the image, and we assign that to our region of the image.
        # So in summary roi_gray is the region of detection within the image and a rectangle will be surrounding it.
        roi_color = frame[y:y+h, x:x+w]   # Same thing as roi_gray but we want to have the colored region saved.
        # Now we will define the eye detection within the face detection.
        eyes = eye_cascade.detectMultiScale(roi_gray)   # Lets search for eyes within the gray face image.
        for (ex, ey, ew, eh) in eyes:
            # Lets draw a green rectangle around we starting and ending points of the eye detection.
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
 
    # check to see if the frame should be displayed to our screen
    if args["display"] > 0:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    # Easier to read from grayscaled images.
        faces = face_cascade.detectMultiScale(gray, 1.8, 5) # Depending on size and likelihood we would change the numerical values, and we are gonna read from the grayscaled image.
        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)    # Lets start at x and y until we width and height of the image, and lets draw a blue rectangle around its detection, accompanied with a width of
            roi_gray = gray[y:y+h, x:x+w]   # So the region of image we want is grayscaled, we take the y region till its end and the x region till its end for the found object within the image, and we assign that to our region of the image.
            # So in summary roi_gray is the region of detection within the image and a rectangle will be surrounding it.
            roi_color = frame[y:y+h, x:x+w]   # Same thing as roi_gray but we want to have the colored region saved.
            # Now we will define the eye detection within the face detection.
            eyes = eye_cascade.detectMultiScale(roi_gray)   # Lets search for eyes within the gray face image.
            for (ex, ey, ew, eh) in eyes:
                # Lets draw a green rectangle around we starting and ending points of the eye detection.
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
 
    # update the FPS counter
    fps.update()
 
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
 
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
