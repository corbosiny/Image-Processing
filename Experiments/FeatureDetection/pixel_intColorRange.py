import cv2
import numpy as np
from pprint import pprint

img1 = cv2.imread('testAli.jpg')

img_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

gaus = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                             cv2.THRESH_BINARY, 11, 2)


face_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_frontalface_default.xml')

#gaus *= 1./255

faces = face_cascade.detectMultiScale(gaus, 1.3, 2)


lengthofImg1 = len(img1)
lengthofImgGray = len(img_gray)
lengthofGaus = len(gaus)

print 'Length of colored image is: ' + str(lengthofImg1)
pprint(img1)
print('\n\n\n\nGRAYSCALE NOW\n\n\n')
print 'Length of grayscaled image is: ' + str(lengthofImgGray)
pprint(img_gray)
print('\n\n\n\GAUS NOW\n\n\n')
print 'Length of Gaus Image is: ' + str(lengthofGaus)
pprint(gaus)
