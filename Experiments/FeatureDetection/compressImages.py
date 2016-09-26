import cv2
import numpy as np
from pprint import pprint

class ImageCompression:
    
    def lengthOfImageBytes(image):
        lengthOfImage = len(image)
        return lengthOfImage

    def encodeImage(image):
        # When calling the build cv2.imencode iamage, the parameters take inthe file extension of the image
        # along with the image to be written.
        # Worth noting that the function returns a single row matrix of type CV_8UC1 which contains encoded image
        # as array of bytes according to the API.
        enc = cv2.imencode('.jpg', image)[1]
        return enc

    # This method is useful if we strictly wish to compress data as a string.
    def encodeImageAsString(image):
        img_str = cv2.imencode('.jpg', image)[1].tostring()
        return img_str

    # Returns image from buffer in memory.
    def decodeImage(stringEncoding):
        # Convert encoded Message into int8 bytes size elements within a matrix.
        nparr = np.fromstring(stringEncoding, np.uint8)
        # The function reads values in as a vector of bytes, colors are stored in  BGR format,
        # we want the image only in color...for NOW.
        img = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)
        return img

    def windowDestroyer(numberOfFramesOpen):
        totalFrames = numberOfFramesOpen * 4        # Every frame takes 4 wait keys.
        totalFrames = totalFrames + 1               # Everything is 0 indexed, so we gotta add 1 bad boy on there.
        cv2.destroyAllWindows()
        for i in range(1, totalFrames):
            cv2.waitKey(1)

    '''while True:
        img1 = cv2.imread('testAli.jpg')

        grayImage = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

        encodingConversion = encodeImage(grayImage)
        encodingReg = encodeImage(img1)

        decodingConversion = decodeImage(encodingConversion)
        decodingReg = decodeImage(encodingReg)
        
        cv2.imshow('decoded', decodingConversion)
        cv2.imshow('regDecode', decodingReg)
        k = cv2.waitKey(30) & 0xFF
        if k == 27:
            break

    windowDestroyer(2)'''
