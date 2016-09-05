import cv2
import numpy as np

img_bgr = cv2.imread('/home/pi/Desktop/opencv-MainMatch.jpg') # Retrieve image from directory and assign it to variable.
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)          # Convert the image to gray.

template = cv2.imread('/home/pi/Desktop/opencv-templateMatch.jpg', 0)

w, h = template.shape[::-1]             # We assign the width and height of the template image to w & h through the command stated.

result = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)    # Lets match the grayscale image to the template image, see if we find it within
threshold = 0.8                         # Define a threshold opacity, lowering the treshold allows the image to be more flexible with locating the same image, the higher the more specific essentially.You may want higher than .8
location = np.where(result >= threshold)    # Location wherever our result is above our threshold value.

for pt in zip(*location[::-1]):          # For every location within the image
    cv2.rectangle(img_bgr, pt, (pt[0]+w, pt[1]+h), (0,255,255), 2)
    # Lets draw a rectangle around our image_bgr which is the original
    # and lets draw the point itself and put it as the size of our template hence
    # the pt[0] + w, and the same goes for height, basically we are getting the exact constraints of our template and outlining it.
    # We want to color that rectangle yellow, and a thickness of 2 for the line.

cv2.imshow('detected', img_bgr)     # Show the image after detection.

cv2.waitKey(0)
cv2.destroyAllWindows()
for i in range(1,5):
    cv2.waitKey(1)
    
