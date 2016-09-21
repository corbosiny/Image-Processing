import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('testAli.jpg')
mask = np.zeros(img.shape[:2], np.uint8)    # Return a rray of 2 of 8 bit integers.

bgdModel = np.zeros((1, 65), np.float64)    # The background model we'll use with up to 64 shapes with 64 bit integers.
fgdModel = np.zeros((1,65), np.float64)

rect = (50, 50, 50, 50)

# We take the img read, apply the mask with a outlining of the rect dimensions sepcified, and push this onto the fgdModel.
cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

mask2 = np.where((mask==2) | (mask == 0), 0, 1).astype('uint8')
#We either have a 0 or 2 from the mask declared about.
img = img*mask2[:,:,np.newaxis]
plt.imshow(img)
plt.colorbar()
plt.show()












