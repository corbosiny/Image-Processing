import cv2
import numpy as np
from pprint import pprint

def lengthOfImage(image):
    lengthOfImage = len(image)
    return lengthOfImage

def ImageToMatrix(image):
    
    return image

def grayToMatrix(image):
    grayedImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    lengthOfImage = len(grayedImage)
    return lengthOfImage

def gausToMatrix(image):
    grayScaledImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gaussianImage = cv2.adaptiveThreshold(grayScaledImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                             cv2.THRESH_BINARY, 11, 2)
    lengthOfImage = len(gaussianImage)
    return lengthOfImage

def encodeImage(image):
    img_str = cv2.imencode('.jpg', image)[1]
    return img_str

def encodeImageAsString(image):
    img_str = cv2.imencode('.jpg', image)[1].tostring()
    return img_str

def decodeImage(stringEncoding):
    nparr = np.fromstring(stringEncoding, np.uint8)
    img = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)
    return img

while True:
    img1 = cv2.imread('testAli.jpg')

    grayImage = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

    encodingConversion = encodeImageAsString(grayImage)

    decodingConversion = decodeImage(encodingConversion)

    cv2.imshow('decoded', decodingConversion)
    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break
    
cv2.destroyAllWindows()
for i in range(1,5):
    cv2.waitKey(1)


#print 'Length of colored image is: ' + str(stringRegLength)
#stringmatrix = pprint(img1)

#stringGrayLength = ImageToMatrix(img1)
#print 'Length of grayscaled image is: ' + str(stringGrayLength)
#pprint(img_gray)

#stringGausLength = ImageToMatrix(img1)
#print 'Length of Gaus Image is: ' + str(stringGausLength)
#pprint(gaus)

