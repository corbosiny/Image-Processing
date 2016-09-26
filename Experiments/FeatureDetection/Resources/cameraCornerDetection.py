import cv2
import numpy as np

cap = cv2.VideoCapture(0)       # Start up the webcame, we want to read edges from this.

while True:
    ret, img = cap.read()   # First return our boolean verification we got something, then return the frame to img.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    # Grayscale our image up.
    # We will convert image to a int for detecting edges.
    gray = np.float32(gray)
## Parameters for goodFeaturesToTrack function are as follows,
    # Image, Max corners to detect, quality of detection, minimum distance between corners.
    #corners = cv2.goodFeaturesToTrack(gray, 100, 3, 0.04)
    dst = cv2.cornerHarris(gray, 30, 5, 0.06)
    # Dilating the image for markings.
    dst = cv2.dilate(dst, None)
    # Here we set our threshold/beginning of entrance.
    # ALLEGEDLY
    # We say, hey if our image is above the threshold for edge detection, mark it red as it is a edge.
    #The Corner Harris method finds us displacement in intensity for all directions of a corner.
    img[dst>0.04*dst.max()] = [0,255,0]
    

    '''#corners = np.uint8(corners)  # Converting feature track results for algorithmic usage below.

    for corner in corners:
        # Ravel will return a contiguous flattened array, which would have our x y coordinates basically.
        # Because we are grabbing a distinct corner per corner found in image. We will draw a shape around this corner.
        x, y = corner.ravel()
        # Draw a circle on frame with the center being the corner, a radius of 3,
        # our color will be blue based on scalar, -1 for thickness means fill our circle in.
        cv2.circle(img, (x,y), 3, 255, -1)
    '''
    # Now that we are done rendering the frame to be shown,
    # or basically now that we are done processing
    # lets show the image/frame.
    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break

# Turn off camera.
cap.release()
cv2.destroyAllWindows()     # Destroy windows with a 4 ns stall.
for i in range(1,5):
    cv2.waitKey(1)
