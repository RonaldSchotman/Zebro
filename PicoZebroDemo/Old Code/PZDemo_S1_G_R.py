#!/usr/bin/env python
# TU Delft Pico Zebro Demo
# Writer: Martijn de Rooij
# Version 0.01
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
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(1280, 720))

#Standard hsv color values. These are obtained through code converter.py
green_BGR = [([35,70,21],[64,150,76])]
blue = [([110,60,100],[130,255,255])]
green = [([50,100,0],[90,255,100])]
red = [([-10,100,100],[10,255,255])]
yellow = [([20,100,100],[40,255,255])]

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
    cv2.imshow("HSV green", output)

    kernel = np.ones((7,7),np.uint8)

    closing = cv2.morphologyEx(output, cv2.MORPH_CLOSE, kernel)
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

    gray_green = cv2.cvtColor(opening, cv2.COLOR_BGR2GRAY)

    (_, cnts2, _) = cv2.findContours(gray_green.copy(), cv2.RETR_TREE,
                                    cv2.CHAIN_APPROX_SIMPLE)

    #cv2.drawContours(image, cnts2, -1, (0,255,0), 3)

    areaArray = []
    for i, c in enumerate(cnts2):
        area = cv2.contourArea(c)
        areaArray.append(area)

    #first sort the array by area
    sorteddata = sorted(zip(areaArray, cnts2), key=lambda x: x[0], reverse=True)

    #find the nth largest contour [n-1][1], in this case 1
    try:
        largestcontour = sorteddata[0][1]
        secondcontour = sorteddata[1][1]

        #draw it
        x, y, w, h = cv2.boundingRect(largestcontour)
        x1, y1, w1, h1 = cv2.boundingRect(secondcontour)
        
        appelkoek = image[y:y+h, x:x+w]
        cv2.imwrite("appelkoek2.jpg", appelkoek)
        cv2.rectangle(image, (x, y), (x+w, y+h), (0,255,0), 2)
        cv2.putText(image,'GROEN JAHOOR',(x+w+10,y+h),0,0.3,(0,255,0))

        appelkoek2 = image[y1:y1+h1, x1:x1+w1]
        cv2.imwrite("appelkoek3.jpg", appelkoek2)
        cv2.rectangle(image, (x1, y1), (x1+w1, y1+h1), (0,255,0), 2)
        cv2.putText(image,'GROEN JAHOOR2',(x1+w1+10,y1+h1),0,0.3,(0,255,0))
    except IndexError:
        pass

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
