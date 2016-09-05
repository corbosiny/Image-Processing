import cv2
import numpy as np

# For this program I'm testing the use of thresholding by applying different filters
# and seeing how easy it is to detect corners and objects within the camera frame.

cap = cv2.VideoCapture(0)



def simpleThreshBinary(img):    # Simple threshold filter.
    # Thresholding parameters are as follows:
    # Src image (grayscaled), threshold value to classify pixel values,
    # max value to be given to pixels that surpass the second parameter AKA threshold value
    # Lastly, threshold style, choosing from BINARY, BINARY_INV, TRUNC, TOZERO, TOZERO_INV
    
    # In this instance of usage, I didn't grayscale the image for threshold. Want to see
    # how it works without thresholding.
    retval, threshold = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    # The threshold here takes the lowest darkness of 127, to a max of 255 and applies the THRESH_BINARY filter.
    return threshold        # We now return the thresholded image.

def grayScaleImage(img):
    grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Grayscale the image
    return grayscaled                                   # Return the grayscaled image.


def adaptiveThresholding_Gaus(img):
    # Gaussian filter smoothes out the noise in the image.
    # I Personally like this filter the most for thresholding.

    # I'll have to keep playin around with the parameter values.
    # src image, max value, adaptive method, threshold type, block size (pixel neighborhood)
    # Lastly constant to subract from mean or weighted mean.
    # 11 is popular online for block size, 2 is popular for constant.
    grayedImg = grayScaleImage(img)
    gaus = cv2.adaptiveThreshold(grayedImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                     cv2.THRESH_BINARY, 11, 2)
    return gaus         # We want to return the gaussian filtered adaptive thresholded image.

def gaussianBlurApplying(img):
    # Lets test out some Gaussian filtering with no thresholding.
    # This will allow us to smoothen out the noise, and then we could perhaps
    # grayscale the image, and see if we can detect objects faster than a regular
    # image.
    gausBlur = cv2.GaussianBlur(img, (5,5), 0)
    return gausBlur

def cornerDetecting(img):
    imgGrayed = grayScaleImage(img)
    # Since pixels are read as numerical indexes, we convert our grayscaled image into a series of
    # numbers so we may detect the pixel differences for edge/corner detection.
    gray = np.float32(imgGrayed)

    dst = cv2.cornerHarris(gray, 40, 5, 0.14)
    dst = cv2.dilate(dst, None)
    # Want to apply edge detection with our gausian filter thresholded image.
    img[dst>0.01*dst.max()] = [0,0,255]    # Apply little red pixels around corners for object
    # standing out. AKA a human in front of a wall.
    return img


''' CASCADE SELECTION '''
            
def eyeCascadeDetectionOfImage(img):
    eye_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_eye.xml')
    eyes = eye_cascade.detectMultiScale(img, 1.3, 5)
    for (eye_x, eye_y, eye_width, eye_height) in eyes:
        cv2.rectangle(img, (face_x, face_y),\
                      (eye_x+eye_width, eye_y+eye_height), (0,0,255), 2)

def faceCascadeDetectionOfImage(img):
    face_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_frontalface_default.xml')    # Assign our face cascade with the attributes of the downloaded xml file.
    faces = face_cascade.detectMultiScale(img, 1.3, 5)
    # We have a for loop that continuously iterates through the frames.
    for (face_x, face_y, face_width, face_height) in faces:
        cv2.rectangle(img, (face_x, face_y),\
                      (face_x+face_width, face_y+face_height), (0,0,255), 2)


''' OUR MAIN LOOP WHERE I WILL USE METHODS TO RETRIEVE DIFFERENT RESULTS
    FOR ALL THE THRESHOLDING AND CASCADING.
'''


while True:
    ret, img = cap.read()
    
    threshImage = simpleThreshBinary(img)               # Retrieve a thresholded image.

    grayscale = grayScaleImage(img)
    grayscaledThresh = simpleThreshBinary(grayscale)    # Retrieve a thresholded grayscale image.

    gaussianBlurredImage = gaussianBlurApplying(img)    # We have a guassian blurred image.
    adaptiveThreshGaus = adaptiveThresholding_Gaus(img) # Now we have a adaptive threshold example.

    # Edge detection
    cornerDetecting(img)
    
    # Face detection portion
    faceCascadeDetectionOfImage(gaussianBlurredImage)

    
    #g_img = gaus
    #g_img *= 1./255     # Trying to convert floating image values to CV_8U
    
    #edges = cv2.Canny(gaus_binary_inv, 100, 200)
    
    cv2.imshow('original', img)
    cv2.imshow('GaussianBlur', gaussianBlurredImage)
    cv2.imshow('AdaptiveThresh', adaptiveThreshGaus)
    #cv2.imshow('threshold', threshold)
    #cv2.imshow('grayscaledThreshold', grayscaledThreshold)
    #cv2.imshow('threshold2', threshold2)
    #cv2.imshow('gausEdge', edges)
    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break
    
cap.release()
cv2.destroyAllWindows()
for i in range(1,13):        # A range of 8 becayse we have 4 waitKey's per image.
    cv2.waitKey(1)
