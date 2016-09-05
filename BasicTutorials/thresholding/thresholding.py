import cv2
import numpy as np


img = cv2.imread('bookpage.jpg')

retval, threshold = cv2.threshold(img, 12, 255, cv2.THRESH_BINARY)
# The threshold here takes the lowest darkness of 12, to a max of 255 and applies the THRESH_BINARY filter.

grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Grayscale the image
retval, threshold2 = cv2.threshold(grayscaled, 12, 255, cv2.THRESH_BINARY)
# We are creating a black and white threshold above.
gaus = cv2.adaptiveThreshold(grayscaled, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
# Adaptive threshold applied to the grayscaled image to enhance white pixels.

cv2.imshow('original', img)
cv2.imshow('threshold', threshold)
cv2.imshow('threshold2', threshold2)
cv2.imshow('gaus', gaus)
cv2.waitKey(0)
cv2.destroyAllWindows()
for i in range(1,17):        # A range of 8 becayse we have 4 waitKey's per image.
    cv2.waitKey(1)
