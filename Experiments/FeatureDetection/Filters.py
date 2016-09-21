import cv2
import numpy as np

#cap = cv2.VideoCapture(0)                   # Begin retrieving from our camera feed.
class Filters:

    # Thresholding parameters are as follows:
    # Src image (grayscaled), threshold value to classify pixel values,
    # max value to be given to pixels that surpass the second parameter AKA threshold value
    # Lastly, threshold style, choosing from BINARY, BINARY_INV, TRUNC, TOZERO, TOZERO_INV

    # In this instance of usage, I didn't grayscale the image for threshold. Want to see
    # how it works without thresholding.
    def simpleThreshBinary(self, frame):    # Simple threshold filter.
        retval, threshold = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
        # The threshold here takes the lowest darkness of 127, to a max of 255 and applies the THRESH_BINARY filter.
        return threshold        # We now return the thresholded image.


    
    def grayScaleImage(self, frame):
        grayscaled = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Grayscale the image
        return grayscaled                                   # Return the grayscaled image.



    # Gaussian filter smoothes out the noise in the image.
    # I Personally like this filter the most for thresholding.

    # I'll have to keep playin around with the parameter values.
    # src image, max value, adaptive method, threshold type, block size (pixel neighborhood)
    # Lastly constant to subract from mean or weighted mean.
    # 11 is popular online for block size, 2 is popular for constant.
    def adaptiveThresholding_Gaus(img):
        grayedImg = grayScaleImage(img)
        gaus = cv2.adaptiveThreshold(grayedImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                     cv2.THRESH_BINARY, 11, 2)
        
        #th = cv2.adaptiveThreshold(grayscaled, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
        # If we chose to apply this binary thresh with 115, we could make out words in a textbook as per example available on:
        # https://pythonprogramming.net/thresholding-image-analysis-python-opencv-tutorial/

        return gaus         # We want to return the gaussian filtered adaptive thresholded image.





    # Lets test out some Gaussian filtering with no thresholding.
    # This will allow us to smoothen out the noise, and then we could perhaps
    # grayscale the image, and see if we can detect objects faster than a regular
    # image.
    def gaussianBlurApplying(img):
        gausBlur = cv2.GaussianBlur(img, (5,5), 0)
        return gausBlur

    # This method will take in a colored picture and perform the binary thresh on it,
    # a thresh level of 12 with a max value of 255.
    def coloredThresholding(self, frame):
        retval, coloredThresh = cv2.threshold(frame, 12, 255, cv2.THRESH_BINARY);
        return coloredThresh;




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
