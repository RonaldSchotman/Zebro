#!/usr/bin/env python
# TU Delft Pico Zebro Demo
# PZ_DEMO Fallback
# Comparing images.
# Writer: Martijn de Rooij
# Version 0.01

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

from random import randint
import threading
import bluetooth

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (1648, 928)
camera.framerate = 5
rawCapture = PiRGBArray(camera, size=(1648, 928))

# allow the camera to warmup (So this is only during start up once).
time.sleep(0.1)

class PictureThread(threading.Thread):
    def __init__(self, Value):
        threading.Thread.__init__(self)
        self.daemon = True
        self.Value = Value
        self.start()

    def run(self):
        while True:
            # grab an image from the camera
            camera.capture(rawCapture, format="bgr")
            image = rawCapture.array

            # display the image on screen and wait for a keypress
            cv2.imshow("Image", image)
            cv2.imwrite("Image%s.jpg"%self.Value, image)

            # show the frame
            key = cv2.waitKey(1) & 0xFF

            rawCapture.truncate(0)

            # if the 'q' key was pressed, break from the loop
            if key == ord("q"):
                # cleanup the camera and close any open windows
                cv2.destroyAllWindows()
                # Wait for the threads to finish...
                print('Terminating')
                break
                time.sleep(15)

class FindingBTDevices(threading.Thread):
    def __init__(self, names, condition):
        threading.Thread.__init__(self)
        self.daemon = True
        
        self.names = names
        self.condition = condition

        self.start()

    def run(self):
        while True:
            #print("performing inquiry...")

            nearby_devices = bluetooth.discover_devices(
                    duration=8, lookup_names=True, flush_cache=True, lookup_class=False)

            print("found %d devices" % len(nearby_devices))
            self.condition.acquire()
            print ('lock acquire by %s' % self.name)
            try:
                names = self.names.pop()
            except IndexError:
                pass
            names = []
            #self.names.append(names)
            self.condition.notify()
            for addr, name in nearby_devices:
                try:
                    names.append(name)
                    print("  %s - %s" % (addr, name))
                except UnicodeEncodeError:
                    print("  %s - %s" % (addr, name.encode('utf-8', 'replace')))
            self.names.append(names)
            self.condition.notify()
            print(names)
            print ('lock released by %s' % self.name)
            self.condition.release()
            time.sleep(30)
            
if __name__ == '__main__':

    names = []
    Value = 0
    condition = threading.Condition()
    
    #Starting Sub threads
    Bluetooth_devices = FindingBTDevices(names, condition)
    Bluetooth_devices.setName("BT Devices")

    #Start Camera thread
    #Camera_Thread = PictureThread(Value)
    #Camera_Thread.setName("Camera_Thread")

    Original = cv2.imread("PZ_leds.jpg")
    Led1 = cv2.imread("PZ_leds_on.jpg")

    New_image = abs(Original - Led1)
    cv2.imshow("Testing image", New_image)
    lowValY = 200
    highValY = 100
    array_np = np.asarray(New_image)
    low_values_indices = array_np > lowValY  # Where values are low
    high_values_indices = array_np < highValY
    array_np[low_values_indices] = 0  # All low values set to 0
    array_np[high_values_indices] = 0

    cv2.imshow("Testing 2 image", array_np)
    cv2.imwrite("new_image.jpg", New_image)

    # show the frame
    cv2.waitKey(0)
    #key = cv2.waitKey(1) & 0xFF
