#!/usr/bin/env python
# TU Delft Pico Zebro Demo
# Writer: Martijn de Rooij
# Version 0.01
# Take single pictures for classifier program

# Python 3 compat
from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass

# import the necessary packages
from picamera.array import PiRGBArray   # Pi camera Libary capture BGR video
from picamera import PiCamera           # PiCamera liberary
import time                             # For real time video 
import cv2                              # Include OpenCV library (Most important one)
import numpy as np                      # Optimized library for numerical operations for OpenCV

#import zbarlight
#import bluetooth
#import threading 
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (1648, 928)
camera.framerate = 20
rawCapture = PiRGBArray(camera, size=(1648, 928))

# allow the camera to warmup (So this is oly during start up.
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the NumPy array representing the image, the initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array

    # Show the current view
    cv2.imshow("original",image)
    # Save the last frame show.
    # The code was made this way to decide which picture
    # I want to make and with easy framrate and resolution choice
    # %H:%M:%S
    Timetest = time.strftime("%Y_%m_%d_%H")
    mask = np.zeros(image.shape, dtype=np.uint8)
    roi_corners = np.array([[(1260,910), (1430,810), (1420,110), (1230,10), (420,10), (220,130), (225,820), (390,910)]], dtype=np.int32)
    # fill the ROI so it doesn't get wiped out when the mask is applied
    channel_count = image.shape[2]  # i.e. 3 or 4 depending on your image
    ignore_mask_color = (255,)*channel_count
    cv2.fillPoly(mask, roi_corners, ignore_mask_color)
    # from Masterfool: use cv2.fillConvexPoly if you know it's convex

    #cv2.imwrite("/home/pi/Documents/zebro/PicoZebroDemo/Create_Pictures/Single_image/Picture %s.jpg" % Timetest, image) 
    # apply the mask
    masked_image = cv2.bitwise_and(image, mask)

    # save the result
    cv2.imwrite("image_masked%s.jpg" % Timetest, masked_image)
    cv2.imshow("MAsked", masked_image)
    # show the frame
    key = cv2.waitKey(1) & 0xFF

    #clear the stream in preparation of the next frame
    rawCapture.truncate(0)

    # if the 'q' key was pressed, break from the loop
    if key == ord("q"):
        # cleanup the camera and close any open windows
        cv2.destroyAllWindows()
        break
