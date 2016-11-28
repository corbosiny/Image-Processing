import cv2
import time
import numpy as np
cap = cv2.cv.CaptureFromCAM(0)
img=cv2.cv.QueryFrame(cap)
#cv2.imshow(img,'img')


i=0
while i in range(0,500):
    #text_file = open("Output.txt", "w")
    #l=str(i)+".jpg\n"
    #text_file.writelines(str(l+"\n"))
    
    #cv2.imshow('go',img)
    #img=cv2.cv.QueryFrame(cap)
    #cv2.cv.SaveImage(str(i)+".jpg",img)
    print "F:\Python programs\python ocv\haartraining\opencv-haar-classifier-training-master\positive_images\\"+str(i)+".jpg"
    #time.sleep(.10)
    i+=1
    #print " "

text_file.close()

    
