import cv2
import numpy as np

#face_cascade = cv2.CascadeClassifier('/home/pi/Desktop/PythonFiles/ImageProcessing/haarcascade_frontalface_default.xml')    # Assign our face cascade with the attributes of the downloaded xml file.
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')    # Assign our face cascade with the attributes of the downloaded xml file.
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')         # Assign directory for eye xml file with all eye detection attributes.
#eye_cascade = cv2.CascadeClassifier('/home/pi/Desktop/PythonFiles/ImageProcessing/haarcascade_eye.xml')         # Assign directory for eye xml file with all eye detection attributes.

cap = cv2.VideoCapture(0)       # Activate the video camera feed to start filming.

while True:
    ret, img = cap.read()   # Assign the true if we are able to video then put the feed into the img variable.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    # Easier to read from grayscaled images.
    faces = face_cascade.detectMultiScale(gray, 1.3, 5) # Depending on size and likelihood we would change the numerical values, and we are gonna read from the grayscaled image.
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)    # Lets start at x and y until we width and height of the image, and lets draw a blue rectangle around its detection, accompanied with a width of 2.
        roi_gray = gray[y:y+h, x:x+w]   # So the region of image we want is grayscaled, we take the y region till its end and the x region till its end for the found object within the image, and we assign that to our region of the image.
        # So in summary roi_gray is the region of detection within the image and a rectangle will be surrounding it.
        roi_color = img[y:y+h, x:x+w]   # Same thing as roi_gray but we want to have the colored region saved.
        # Now we will define the eye detection within the face detection.
        eyes = eye_cascade.detectMultiScale(roi_gray)   # Lets search for eyes within the gray face image.
        for (ex, ey, ew, eh) in eyes:
            # Lets draw a green rectangle around we starting and ending points of the eye detection.
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
            
    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xFF
    if k == 27:                  # If we press the escape key terminate.
        break
        
cap.release()                   # Turn off the camera.
cv2.destroyAllWindows()
for i in range(1,5):            # As always due to delays of processes we want a waitkey of 4 per window open to fully terminate without freezing.
    cv2.waitKey(1)
