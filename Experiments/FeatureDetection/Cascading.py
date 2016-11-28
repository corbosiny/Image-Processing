import cv2
import numpy as np


class Cascading:

    def eyeCascadeDetectionOfImage(self, frame):
        eye_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_eye.xml')
        eyes = eye_cascade.detectMultiScale(frame, 1.3, 5)
        for (eye_x, eye_y, eye_width, eye_height) in eyes:
            cv2.rectangle(frame, (eye_x, eye_y),\
                          (eye_x+eye_width, eye_y+eye_height), (0,0,255), 2)

    def faceCascadeDetectionOfImage(self, frame):
        face_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_frontalface_default.xml')
        # Assign our face cascade with the attributes of the downloaded xml file.
        faces = face_cascade.detectMultiScale(frame, 1.3, 5)
        # We have a for loop that continuously iterates through the frames.
        for (face_x, face_y, face_width, face_height) in faces:
            cv2.rectangle(frame, (face_x, face_y),\
                          (face_x+face_width, face_y+face_height), (0,0,255), 2)
