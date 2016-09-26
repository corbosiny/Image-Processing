# import the necessary packages
import argparse
import cv2
import os

class DetectBlur:
    # We have our accessor and mutator methods for the blurThresh
    # because we will want to fiddle around with the blur detection
    # to fine tune it to a set level for best blur detection focus range.

    def __init__(self, threshValue):
        self.__threshBlur = threshValue
        
    # Mutator method for changing static blurDetectionThresh value.
    def setBlurThresh(self, newValue):
        self.__threshBlur = newValue

    # Accessor method for static blurDetectionThresh value.
    def getBlurThresh(self):
        return self.__threshBlur
        
    def variance_of_laplacian(self, frame):
            # compute the Laplacian of the image and then return the focus
        # measure, which is simply the variance of the Laplacian
        return cv2.Laplacian(frame, cv2.CV_64F).var()

    def list_images(self,basePath, contains=None):
        # retirm the set of files that are valid.
        return list_files(basePath, validExts=(".jpg", ".jpeg", ".png", ".bmp"), contains=contains)


    def list_files(self, basePath, validExts=(".jpg", ".jpeg", ".png", ".bmp"), contains=None):
        # loop over the directory structure
        for (rootDir, dirNames, filenames) in os.walk(basePath):
        # loop over the filenames in the current directory
                for filename in filenames:
                    # if the contains string is not none and the filename does not contain
                    # the supplied string, then ignore the file
                    if contains is not None and filename.find(contains) == -1:
                            continue

                    # determine the file extension of the current file
                    ext = filename[filename.rfind("."):].lower()

                    # check to see if the file is an image and should be processed
                    if ext.endswith(validExts):
                    # construct the path to the image and yield it
                            imagePath = os.path.join(rootDir, filename).replace(" ", "\\ ")
                    yield imagePath

    '''if __name__ == '__main__':
        cap = cv2.VideoCapture(0)

        # loop over the input images
        #for imagePath in paths.list_images(args["images"]):
        while True:
                ret, image = cap.read()
            # load the image, convert it to grayscale, and compute the
            # focus measure of the image using the Variance of Laplacian
            # method
            #image = cv2.imread(imagePath)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                fm = variance_of_laplacian(gray)
                text = "Not Blurry"

            # if the focus measure is less than the supplied threshold,
            # then the image should be considered "blurry"
                threshValue = 100       # This will be the value we fiddle with most to determine thresh marking.
                if fm < 100:
                        text = "Blurry"

            # show the image
                cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
                cv2.imshow("Image", image)
                #key = cv2.waitKey(0)
                k = cv2.waitKey(30) & 0xFF
                if k == 27:                  # If we press the escape key terminate.
                        break

        cap.release()                   # Turn off the camera.
        cv2.destroyAllWindows()
        for i in range(1,5):            # As always due to delays of processes we want a waitkey of 4 per window open to fully terminate without freezing.
            cv2.waitKey(1)'''
