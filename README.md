Work on learning image processing, to make a fully functional drone camera to extract live data into a 3D model for Feromone Robotics.

Programs currently work with a threaded webcam frame reader class, along with a blur detection model to keep note of non-blurry pictures, haarcascade image recognition is incorporated into the project as well. There is edge detection (to be improved) and data compression/encrpytion within the files. Further implementation will be needed down the line, but stepping stones are the form of progress currently.

These folders all use Python 2 with a pip installation of cv2 and numpy. You will need either a piCamera, or a webcam. These programs give us the tools to work with image recognition, all the tools lead to fine tuning of the faceEyeDetection, which uses HaarCascades which derive from a respository created by Intel.
