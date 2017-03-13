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

Detect = detection_functions()

# import the necessary packages
from picamera.array import PiRGBArray   # Pi camera Libary capture BGR video
from picamera import PiCamera           # PiCamera liberary
import time                             # For real time video (using openCV)
import numpy as np                      # Optimized library for numerical operations
import cv2                              # Include OpenCV library (Most important one)

# Step 1 Calibration Camera

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (1648, 928)
camera.framerate = 20
rawCapture = PiRGBArray(camera, size=(1648, 928))
