import cv2
import numpy as np

cap = cv2.VideoCapture(0)   # Connect to our USB camera.

while True:
    _, frame = cap.read()   # Store value returned from function to _ variable, and frame as usual if we have a frame.

    laplacian = cv2.Laplacian(frame, cv2.CV_64F)    # CV_64F is data type.
                                                    # 
    sobelx = cv2.Sobel(frame, cv2.CV_64F, 1, 0, ksize=5) # x-direction gradience
    sobely = cv2.Sobel(frame, cv2.CV_64F, 0, 1, ksize=5)

    edges = cv2.Canny(frame, 100, 200)      # This is our edge detector, the smaller the frame specification the more edges detected, for example 50,50 will show all edges detected
                # apply to frame and use a 100x200 region for edge detection
    cv2.imshow('original', frame)
    cv2.imshow('laplacian', laplacian)
    cv2.imshow('sobelx', sobelx)
    cv2.imshow('sobely', sobely)
    cv2.imshow('edges', edges)      

    if cv2.waitKey(1) & 0xFF == ord('q'):   # Once we hit the letter q, lets de-activate the frame. If we did number 27, that would be the escape key BTW.
        break
    
cv2.waitKey(0)
cv2.destroyAllWindows()
for i in range(1,26):
    cv2.waitKey(1)

    

cv2.release()   # Release the webcame as well.

