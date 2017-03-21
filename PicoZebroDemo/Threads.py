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

from random import randint
import threading
import bluetooth

# Step 1 Calibration Camera

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (1648, 928)
camera.framerate = 5
rawCapture = PiRGBArray(camera, size=(1648, 928))

# allow the camera to warmup (So this is only during start up once).
time.sleep(0.1)

#names = []

class MyThread(threading.Thread):
    def __init__(self, val):
        ''' Constructor. '''
        threading.Thread.__init__(self)
        self.val = val
 
    def run(self):
        for i in range(1, self.val):
            #print('Value %d in thread %s' % (i, self.getName()))
 
            # Sleep for random time between 1 ~ 3 second
            secondsToSleep = randint(1, 5)
            #print('%s sleeping for %d seconds...' % (self.getName(), secondsToSleep))
            time.sleep(secondsToSleep)

class myClassA(threading.Thread):
    def __init__(self, names, condition):
        threading.Thread.__init__(self)
        self.daemon = True

        self.names = names
        self.condition = condition
        
        self.start()

    def run(self):
        while True:
            self.condition.acquire()
            #print ('condition acquired by %s' % self.name)
            #if self.names:
            names = self.names
            names  = [val for sublist in names for val in sublist]
            #print("mario")
            print (names)
            #print ('condition release by %s' % self.name)
            self.condition.release()
            #print('thread %s' % (self.getName()))
            #print ('A')
            time.sleep(5)

class myClassB(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            #print('thread %s' % (self.getName()))
            #print ('B')
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
  
#laurentluce python thread condition
# Run following code when the program starts
if __name__ == '__main__':

    names = []
    condition = threading.Condition()
    
    #Starting Sub threads
    Bluetooth_devices = FindingBTDevices(names, condition)
    Bluetooth_devices.setName("BT Devices")
    
    # Declare objects of MyThread class
    Pico_Zebro_1 = myClassA(names, condition)
    Pico_Zebro_1.setName("Pico_Zebro1")
    
    Pico_Zebro_2 = myClassB()
    Pico_Zebro_2.setName("Pico_Zebro2")
    
    myThreadOb1 = MyThread(4)
    myThreadOb1.setName('Thread 1')

    myThreadOb2 = MyThread(4)
    myThreadOb2.setName('Thread 2')

    # Start running the threads!
#    Pico_Zebro_1.start()
#    Pico_Zebro_2.start()
    myThreadOb1.start()
    myThreadOb2.start()
    
    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the NumPy array representing the image, the initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array
        
        Timetest = time.strftime("%d-%m-%Y")
        # Show the current view for debugging
        cv2.imshow("original %s" % Timetest,image)
        cv2.imwrite("1648_928_image_test.jpg", image)

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

 

