#!/usr/bin/env python
# TU Delft Pico Zebro Demo
# PZ_DEMO Fallback
# Full Code inclusive of Pseudo Code.
# Writer: Martijn de Rooij
# Version 0.02

# This is  a test of queue transfer of data.

# import the necessary packages
from picamera.array import PiRGBArray   # Pi camera Libary capture BGR video
from picamera import PiCamera           # PiCamera liberary
import time                             # For real time video (using openCV)
import numpy as np                      # Optimized library for numerical operations
import cv2                              # Include OpenCV library (Most important one)
import queue                            # Library for Queueing sharing variables between threads
import threading                        # Library for Multithreading
import serial                           # Import serial uart library for raspberry pi
import math                             # mathematical functions library

import sys

# import the necessary packages for tracking
from imutils import contours
import imutils

from Functions.Blocking import Blocking

Block = Blocking()

# http://picamera.readthedocs.io/en/latest/fov.html
# initialize the Pi camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (1648, 928) #Maximum Resolution with full FOV
camera.framerate = 40           # Maximum Frame Rate with this resolution
rawCapture = PiRGBArray(camera, size=(1648, 928))

# allow the camera to warmup.
time.sleep(0.1)
