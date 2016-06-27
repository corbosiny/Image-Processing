import cv2
import numpy as np

# This file will detect all the red within the presence of the camera.

cap = cv2.VideoCapture(0)   # Connect to our USB camera.

while True:
    _, frame = cap.read()   # Store value returned from function to _ variable, and frame as usual if we have a frame.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)    # Working with hue, saturation and value colors.
    # We use hsv for range purposes because we will have more options than RGB & BGR values.

    # Here we will alter the hue sat value by working with our lower & upper red.
    lower_red = np.array([150,150,50])  # Red is in the hue of 160-180
    upper_red = np.array([180,255,150])


    mask = cv2.inRange(hsv, lower_red, upper_red)
    # The mask will take the ranges from lower_red to upper_red. So we have all possible colors.
    res = cv2.bitwise_and(frame, frame, mask= mask)
    # We are combining the mask with the frame. The mask is either a 0 or 1, so it is in the image or isn't, no inbetween.

    cv2.imshow('frame', frame)  # Before applying our mask to find the red.
    #cv2.imshow('mask', mask)
    cv2.imshow('res', res)      # After our mask is applied to original frame.
    
    # We want to gather the average of a certain colored pixel, we'll use a kernel to keep track of it.
    # The averaging of the pixels will create a blur effect because we'll overwrite pixels with the blur effect created.
    # 15X15 data type divided by the total pixels, 15^2
    kernel = np.ones((15,15), np.float32)/225
    smoothed = cv2.filter2D(res, -1, kernel)    # Apply a simple averaging from the kernel to the camera frame.

    blur = cv2.GaussianBlur(res, (15,15), 0)    # Apply a gaussianblur effect to our res image which is the after-mask 
    # Now we shoot for clarity with a median blur effect.
    median = cv2.medianBlur(res, 15)    # Apply to result with a size of 15.
    #bilateral = cv2.bilateralFilter(res, 15, 75, 75)    # Size of 15 with a 75x75 dimension

    #cv2.imshow('smoothed', smoothed)
    #cv2.imshow('gausBlur', blur)
    cv2.imshow('median', median)
    #cv2.imshow('bilateral', bilateral)
    
    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break

cv2.release()   # Release the webcame as well.    
cv2.waitKey(0)
cv2.destroyAllWindows()
for i in range(1,13):
    cv2.waitKey(1)
    



