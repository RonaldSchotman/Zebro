#!/usr/bin/env python
# TU Delft Pico Zebro Demo
# PZ_DEMO recognition determination. (This code is for recognizing Pico Zebro)
# Using leds on Pico Zebro
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
from Functions.calibration import calibration_functions

Calib = calibration_functions()

# import the necessary packages
from picamera.array import PiRGBArray   # Pi camera Libary capture BGR video
from picamera import PiCamera           # PiCamera liberary
import time                             # For real time video (using openCV)
import numpy as np                      # Optimized library for numerical operations
import cv2                              # Include OpenCV library (Most important one)
import threading                        # Trheading library
import bluetooth                        # BLuetooth library

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (1648, 928)
camera.framerate = 5
rawCapture = PiRGBArray(camera, size=(1648, 928))

# allow the camera to warmup (So this is only during start up once).
time.sleep(0.1)

class FindingBTDevices(threading.Thread):
    def __init__(self, names, condition):
        threading.Thread.__init__(self)
        self.daemon = True
        
        self.names = names
        self.condition = condition

        self.start()

    def run(self):
        while True:
            print("performing inquiry...")

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

class CompareImage(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

        self.start()

    def run(self):
        while True:
            original = cv2.imread("1648_928_image_test.jpg")

            #Send global command turn all leds off to all conected devices
            #this information from all the BT Threads for setting a number 1
            #To stop doing anything and set 0

            #Say First device turn leds on

            #Take a new pictue.

            #Compare orig
            

# Run following code when the program starts
if __name__ == '__main__':
    names = []
    condition = threading.Condition()
    
    #Starting Sub threads
    Bluetooth_devices = FindingBTDevices(names, condition)
    Bluetooth_devices.setName("BT Devices")

    #Starting Sub threads
    Bluetooth_devices = CompareImage()
    Bluetooth_devices.setName("Compare Images")

    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the NumPy array representing the image, the initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array

        image = Calib.calibrate_light(image)
        
        Timetest = time.strftime("%d-%m-%Y")

        # Show the current view for debugging
        cv2.imshow("original %s" % Timetest,image)

        #Save image always.
        cv2.imwrite("1648_928_image_test.jpg", image)
        time.sleep(10)
        # show the frame
        key = cv2.waitKey(1) & 0xFF

        #clear the stream in preparation of the next frame
        rawCapture.truncate(0)

        # if the 'q' key was pressed, break from the loop
        if key == ord("q"):
            # cleanup the camera and close any open windows
            cv2.destroyAllWindows()
            # Wait for the threads to finish...
            myThreadOb1.join()
            myThreadOb2.join()
            print('Main Terminating...')
            break
