#!/usr/bin/env python
# TU Delft Pico Zebro Demo
# Writer: Martijn de Rooij
# Version 0.01
# Take video.h264 for classifier program (at most every hour a new one)

# Python 3 compat
from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass

# import the necessary packages
from picamera.array import PiRGBArray   # Pi camera Libary capture BGR video
from picamera import PiCamera           # PiCamera liberary
from time import sleep                  # For real time video
import sys
import time
import numpy as np

Time_Vid = sys.argv[1]

Video_Time = np.uint8([Time_Vid])

camera = PiCamera()

#Take time once so u know when the video was created.
Timetest = time.strftime("%Y-%m-%d %H:%M")

camera.start_preview() 
camera.start_recording('/home/pi/Documents/Pictures_for_classifier/Video_save/Video%s.h264' % Timetest)

sleep(Video_Time) #in seconds

# if the 'q' key was pressed, break from the loop
camera.stop_recording()
camera.stop_preview()
    
