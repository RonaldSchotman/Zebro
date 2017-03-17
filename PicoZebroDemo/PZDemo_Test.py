#!/usr/bin/env python
# TU Delft Pico Zebro Demo
# PZ_DEMO recognition determination. (This code is for recognizing Pico Zebro)
# Writer: Martijn de Rooij
# Version 0.03

# Everything is being tested from 120 cm height.

# Python 3 compatability
from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass

# import detection functions
from Functions.detection import detection_functions
from Functions.calibration import calibration_functions

Detect = detection_functions()
Calib = calibration_functions()

# import the necessary packages
from picamera.array import PiRGBArray   # Pi camera Libary capture BGR video
from picamera import PiCamera           # PiCamera liberary
import time                             # For real time video (using openCV)
import numpy as np                      # Optimized library for numerical operations
import cv2                              # Include OpenCV library (Most important one)

# Step 1 Calibration Camera

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (1648, 928) #1920, 1088 #1648, 928 #1280, 720 #2592, 1944	
camera.framerate = 2
rawCapture = PiRGBArray(camera, size=(1648, 928))

# allow the camera to warmup (So this is only during start up once).
time.sleep(0.1)

#Standard hsv color values. 
green = [([40,33,40],[92,153,255])] #=green

firstFrame = None

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the NumPy array representing the image, the initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array

    # Calibrate on light level
    image_light = Calib.calibrate_light(image)

    # Adjusting Gamma level if highly needed 1 means nothing changes
    image_gamma = Calib.adjust_gamma(image_light, 1)

    #Blur image for better detection
    image_blur = cv2.blur(image_gamma,(1,1))
    image_blurred = cv2.GaussianBlur(image_gamma, (11, 11), 0)
    
    #USeless functions
    image_gray = cv2.cvtColor(image_blur, cv2.COLOR_BGR2GRAY)

    image_hsv = cv2.cvtColor(image_blurred, cv2.COLOR_BGR2HSV)

    #green the important color
    for(lower,upper) in green:
            lower = np.array(lower,dtype=np.uint8)
            upper = np.array(upper,dtype=np.uint8) 
    # the mask 
    mask_green = cv2.inRange(image_hsv,lower,upper)

    image_green = cv2.bitwise_and(image_blurred, image_blurred, mask = mask_green)

    image_green_gray = cv2.cvtColor(image_green, cv2.COLOR_BGR2GRAY)
    
    #Pico_Zebro = []
    #Found_Zebro = Detect.Green(image, image_green)
    #Pico_Zebro.append(Found_Zebro)
   # Found_BW = Detect.Green(image, image_green)
    Found_zebro = Detect.Filter_Green(image, image_gray, mask_green)

    Timetest = time.strftime("%d-%m-%Y")
    # Show the current view for debugging
    #cv2.imshow("original %s" % Timetest,image)
    #cv2.imwrite("Found_Zebro_Filter.jpg", image_Filter)

    # show the frame
    key = cv2.waitKey(1) & 0xFF

    #clear the stream in preparation of the next frame
    rawCapture.truncate(0)

    # if the 'q' key was pressed, break from the loop
    if key == ord("q"):
        # cleanup the camera and close any open windows
        cv2.destroyAllWindows()
        break
