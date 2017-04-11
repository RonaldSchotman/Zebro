#!/usr/bin/env python
# TU Delft Pico Zebro Demo
# PZ_DEMO Fallback method 1
# Full Code for controlling and Detecting 1 Pico Zebro 
# Writer: Martijn de Rooij
# Version 0.03

# import the necessary packages
from picamera.array import PiRGBArray                                       # Pi camera Libary capture BGR video
from picamera import PiCamera                                               # PiCamera liberary
import time                                                                 # For sleep functions and video
import bluetooth
import numpy as np                                                          # Optimized library for numerical operations
import cv2                                                                  # Include OpenCV library for vision recognition
import queue                                                                # Library for Queueing. Savetly sharing variables between threads
import threading                                                            # Library for Multithreading

import serial                                                               # Serial uart library for raspberry pi
import serial.tools.list_ports;                                             # Library for obtaining evry port on the raspberry Pi

import random                                                               # Library so the Pico walks random in any direction without a pattern

# import the necessary packages for tracking
from imutils import contours                                                # A library from http://www.pyimagesearch.com/2016/10/31/detecting-multiple-bright-spots-in-an-image-with-python-and-opencv/
import imutils                                                              # For detecting bright spots in a image.

from Functions.Blocking import Blocking                                     # py program for comparing every zebro middlepoint with eachother

Block = Blocking()                                                          # For using the functions in Blocking.py with Block.Function_Name

# http://picamera.readthedocs.io/en/latest/fov.html
# initialize the Pi camera and grab a reference to the raw camera capture
camera = PiCamera()                                                         # Set the camera as PiCamera
camera.resolution = (1648, 928)                                             # Maximum Resolution with full FOV
camera.framerate = 40                                                       # Maximum Frame Rate with this resolution
rawCapture = PiRGBArray(camera, size=(1648, 928))                           # Rawcapture of vision with RGB

# allow the camera to warmup.
time.sleep(0.1)
avg = None
# capture frames from the camera
for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image and initialize
	# the timestamp and occupied/unoccupied text
	frame = f.array
	text = "Unoccupied"
 
	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
 
	# if the average frame is None, initialize it
	if avg is None:
		print "[INFO] starting background model..."
		avg = gray.copy().astype("float")
		rawCapture.truncate(0)
		continue
	    
	# accumulate the weighted average between the current frame and
	# previous frames, then compute the difference between the current
	# frame and running average
	cv2.accumulateWeighted(gray, avg, 0.5)
	frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg)
