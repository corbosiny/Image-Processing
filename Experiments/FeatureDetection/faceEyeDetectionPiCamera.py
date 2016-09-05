from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

# Currently must force quit application to stop, commands do not work such as destroyAllWindows, or stop_preview, stop_recording, etc.
# Online troubleshooting reveals nothing and leaves an unanswered question regarding the matter on stackoverflow as well. 


# Initialize xml cascade face file, and eye file.
face_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_frontalface_default.xml')    # Assign our face cascade with the attributes of the downloaded xml file.
eye_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_eye.xml')         # Assign directory for eye xml file with all eye detection attributes.
smile_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_smile.xml')  # Want to grab a smile.
fullBody_Cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_fullbody.xml')
upperBody_Cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_upperbody.xml') # Detect the upper body.
# initialize the camera and grab reference to raw camera capture
camera = PiCamera()
camera.resolution = (600, 450)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(600, 450))
# allow camera to startup
time.sleep(0.1)
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Take the raw NumPy array respresenting the image per frame and assign it to our array
    image = frame.array

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)    # Easier to read from grayscaled images.
    # So the detectMultiScale takes the image (as grayscale cause easier to read), the scale factor is the specification of how much the
    # image size is to be reduced at each image scale (deteroating pixels for easier reading im guessing,
    # lastly a minimum detection of objects, so image, scale, #of objects.
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bodyDetect= fullBody_Cascade.detectMultiScale(gray, 1.6, 3)
    upperBodyDetect = upperBody_Cascade.detectMultiScale(gray, 1.3, 4)

    #for (upper_x, upper_y, upper_width, upper_height) in upperBodyDetect:
     #   cv2.rectangle(image, (upper_x, upper_y), (upper_x+upper_width, upper_y+upper_height), (0,0,255), 3)
        
    
    #for (body_x, body_y, body_width, body_height) in bodyDetect:
      #  cv2.rectangle(image, (body_x, body_y), (body_x+body_width, body_y+body_height), (0,0,255), 3)
            
    

    # Multi line comments in python '''

    # Once we have the grayscale, we will search for the face first, then we will search for specific features. We will make a region of the image to look at for outlining.
    for (x,y,w,h) in faces:
        # Note first parameter is the image itself, the original image isn't grayscaled so thats why we use it, also after this we
        # use regions of images to square up.
        cv2.rectangle(image, (x,y), (x+w, y+h), (255,0,0), 2)    # Lets start at x and y until we width and height of the image, and lets draw a blue rectangle around its detection, accompanied with a width of 2.
        roi_gray = gray[y:y+h, x:x+w]   # So the region of image we want is grayscaled, we take the y region till its end and the x region till its end for the found object within the image, and we assign that to our region of the image.
        # So in summary roi_gray is the region of detection within the image and a rectangle will be surrounding it.
        roi_color = image[y:y+h, x:x+w]   # Same thing as roi_gray but we want to have the colored region saved.
        # Now we will define the eye detection within the face detection.
        
        eyes = eye_cascade.detectMultiScale(roi_gray)   # Lets search for eyes within the gray face image.
        smiling = smile_cascade.detectMultiScale(roi_gray)  # Lets search the grayscale image for the eyeglasses within our detected face.
        for (ex, ey, ew, eh) in eyes:
            # Lets draw a green rectangle around we starting and ending points of the eye detection.
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
            # We do a for loop because we are saying, for as long as we detect the haarcascade AKA object, lets highlight it with a rectangle.
            #for (smile_x, smile_y, smile_width, smile_height) in smiling:
                # Draw a rectangle around the eyeglasses.
                # Since coloring is B G R, we do Red for glasses which a larger thickness.
                ###cv2.rectangle(roi_color, (smile_x, smile_y), (smile_x+smile_width, smile_y+smile_height), (0,0,255), 4)


    cv2.imshow('Frame', image)
    key = cv2.waitKey(1) & 0xff          # Assign the waitKey to read from our keyboard.

    # Clear frame in preperation for next frame after iteration of loop, cause remember each iteration is a frame instance, so like an image instance.
    rawCapture.truncate(0)
    

    #if k == 27:       # If we press the esc key, we want to terminate the windows.
    if key == ord('q'):
        break

#camera.stop_recording(0)
cv2.destoryAllWindows()
for i in range(1,5):
    cv2.waitKey(1)


