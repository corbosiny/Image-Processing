from gpiozero import MotionSensor
import picamera
import os
import datetime
import time
from SendImages import emailPictures

# Change location of saved files for directory location.
os.chdir("/home/pi/Desktop/PythonFiles/ImageProcessing/FeatureDetection/Snapshots/")

camera = picamera.PiCamera()        # Create our instance of the picamera object.
camera.brightness = 50              # Change camera brightness
camera.sharpness = 10               # Change camera sharpness

ts = time.time()                    # Retrieve current timing.
st = datetime.datetime.fromtimestamp(ts).strftime('_TS:%Y-%m-%d::%H:%M:%S')


# We import library package for MotionSensor which uses the PIR (Passive Infrared)
pir = MotionSensor(4)   # Assign the PIR to the correct GPIO pin

counter = 0     # A counter for now to set a limit of pictures taken.
# Now we instantiate our email program so we can email any photos captured.
emailSnaps = emailPictures()
while True:
    if pir.motion_detected:
        timeStampString = st
        camera.capture("snapped:" + str(counter) + timeStampString + ".jpg")
        directoryPath = "/home/pi/Desktop/PythonFiles/ImageProcessing/FeatureDetection/Snapshots/snapped:" + str(counter) + timeStampString + ".jpg" 
        emailSnaps.SendMail(directoryPath)
        counter = counter + 1
        #for x in range(2):
         #   timeStampString = st
          #  camera.capture("snapped:" + str(counter) + timeStampString + ".jpg")
           # emailSnaps.SendMail("/home/pi/Desktop/PythonFiles/ImageProcessing/Snapshots/snapped:" + str(counter) + timeStampString + ".jpg")
            #counter = counter + 1
#        emailSnaps.SendMail("/home/pi/Desktop/PythonFiles/ImageProcessing/Snapshots/")
        # We also have to convert counter to string for filename above using str.
    else:
        counter = 0
        # Reset our counter after first encounter.

#while (counter < 8):
#while True:     # Want to be continuously checking for motion
 #   if pir.motion_detected:     # If our PIR detects motion while checking for it
  #      camera.capture("snapped:" + str(counter) + st + ".jpg")
        # We also have to convert counter to string for filename above using str.
   #     counter = counter + 1   # Increment up
        # Here we capture image whenever motion is detected for up to 5 pictures.
