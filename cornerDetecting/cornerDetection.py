import cv2
import numpy as np

#img = cv2.imread('/home/pi/Desktop/opencv-corner-detection-sample.jpg')
img = cv2.imread('opencv-corner-detection-sample.jpg')
# We could also take a image from the camera, and perhaps analyze that image after
# converting 2 gray to see how many corners we can detect in the image.

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)         # This int value will be used for the algorithm that detects the corners.

# On what image to call method, how many detections up to, the image quality, and the minimum distance between every corner. 
corners = cv2.goodFeaturesToTrack(gray, 200, 0.01, 10)
#  The greater the number of detections, the more accurate the locating of corners on image.
corners = np.int0(corners)      # Converting to integer value for algorithm usage.

for corner in corners:
    x, y = corner.ravel()
    cv2.circle(img, (x,y), 3, 255, -1)  # Draw a circle around the image at our x y coordinates, a radius of 3, color of blue, with a fill rather a outline.

cv2.imshow('Corner', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
for i in range(1,5):
    cv2.waitKey(1)
