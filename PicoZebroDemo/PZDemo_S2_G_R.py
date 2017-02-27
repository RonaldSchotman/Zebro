#!/usr/bin/env python
# TU Delft Pico Zebro Demo
# Writer: Martijn de Rooij
# Version 0.02
# From live video find green and put a rectangle around it.
# This is step 1 for finding and recognizing the Pico zebro.
# The needs to be done from 170 cm
# version 0.01 works from 45 cm partly

# Python 3 compat
from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass

# import the functions
from Functions.functions_shape import functions_shape

# import the necessary packages
from picamera.array import PiRGBArray   # Pi camera Libary capture BGR video
from picamera import PiCamera           # PiCamera liberary
import time                             # For real time video (using openCV)
import numpy as np                      # Optimized library for numerical operations
import cv2                              # Include OpenCV library (Most important one)

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (1280, 720)
camera.framerate = 15
rawCapture = PiRGBArray(camera, size=(1280, 720))

#Standard hsv color values. These are obtained through code converter.py
green = [([50,25,25],[80,150,255])] #=green

# allow the camera to warmup (So this is only during start up once).
time.sleep(0.1)

funct = functions_shape()

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the NumPy array representing the image, the initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    
    # color in cube is hsv values for easier detection of green.
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #green the important color
    for(lower,upper) in green:
            lower = np.array(lower,dtype=np.uint8)
            upper = np.array(upper,dtype=np.uint8) 
    # the mask 
    mask_green = cv2.inRange(hsv,lower,upper)

    #Show the green and the current view
    output = cv2.bitwise_and(image, image, mask = mask_green)
    cv2.imshow("HSV green visable  ", output)

    # Use current frame image and hsv green value to find 2 largest
    # green contours, draw rectangle around them and put them in image
    funct.Find_draw(image, output)

    Timetest = time.strftime("%d-%m-%Y")
    # Show the current view
    cv2.imshow("original %s" % Timetest,image)

    # show the frame
    key = cv2.waitKey(1) & 0xFF

    #clear the stream in preparation of the next frame
    rawCapture.truncate(0)

    # if the 'q' key was pressed, break from the loop
    if key == ord("q"):
        # cleanup the camera and close any open windows
        cv2.destroyAllWindows()
        break
