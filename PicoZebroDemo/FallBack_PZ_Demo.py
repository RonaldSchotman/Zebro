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
#camera = PiCamera()
#camera.resolution = (1640, 922)
#camera.framerate = 5
#rawCapture = PiRGBArray(camera)
#size=(1648, 928)
# allow the camera to warmup (So this is only during start up once).
time.sleep(0.1)

def Picture(Number):
    # grab an image from the camera
    camera = PiCamera()
    camera.resolution = (1640, 922)
    #camera.framerate = 5
    rawCapture = PiRGBArray(camera)

    time.sleep(0.1)

    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array

    # Take picture
    cv2.imwrite("Image%s.jpg"%Number, image)
    rawCapture.truncate(0)

def Image_Difference(Image):
    # making sure light doesn't matter
    lowValY = 200
    highValY = 100
    New_image = np.asarray(image)
    low_values_indices = New_image > lowValY  # Where values are low
    high_values_indices = New_image < highValY #Where values are high
    New_image[low_values_indices] = 0  # All low values set to 0
    New_image[high_values_indices] = 0 # All high values set to 0
    return New_image

def Find_Orientation(x_Led_1,x_Led_3,y_Led_1,y_Led_3):
    x_middle = 0
    y_middle = 0
    Direction = None

    #Once known what the max and minimum Distance is between two points
    # The following calculation can be done for saying that angle is the
    # Pico Zebro Turned:
    # 90 - atan(x) with x from 0 -90 and being the difference between Max and Min
    # So x = ? * Factor = 90  for max between max and min
    
    #No points Found
    if(x_Led_1 or x_Led_3 or y_Led_1 or y_Led_3) == 0:
        return x_middle, y_middle, Direction
    
    #Facing North (dermine middle point)
    elif (x_Led_1 < x_Led_3) and (y_Led_1 < y_Led_3):
        # Pico Zebro is facing North
        # Middle Point Zebro is:
        x_middle = ((x_Led_3 - x_Led_1) + x_Led_1)
        y_middle = ((y_Led_3 - y_Led_1) + y_Led_1)
        Direction = North
        return x_middle, y_middle. Direction
    
    elif (x_Led_1 < x_Led_3) and (y_Led_1 > y_Led_3):
        # Pico Zebro is facing East
        # Middle Point Zebro is:
        x_middle = ((x_Led_3 - x_Led_1) + x_Led_1)
        y_middle = ((y_Led_1 - y_Led_3) + y_Led_3)
        Direction = East
        return x_middle, y_middle. Direction
    
    elif (x_Led_1 > x_Led_3) and (y_Led_1 > y_Led_3):
        # Pico Zebro is facing South
        # Middle Point Zebro is:
        x_middle = ((x_Led_1 - x_Led_3) + x_Led_3)
        y_middle = ((y_Led_1 - y_Led_3) + y_Led_3)
        Direction = South
        return x_middle, y_middle. Direction
    
    elif (x_Led_1 > x_Led_3) and (y_Led_1 < y_Led_3):
        # Pico Zebro is facing West
        # Middle Point Zebro is:
        x_middle = ((x_Led_1 - x_Led_3) + x_Led_3)
        y_middle = ((y_Led_3 - y_Led_1) + y_Led_1)
        Direction = West
        return x_middle, y_middle. Direction

class FindZebroThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        while True:            
            #Try to find every Pico Zebro every 60 Seconds

            #First Send global command to all Pico Zebro with Stop.

            #Wait untill connected Pico Zebro's give back yes I am stopped
            #Also Turn all leds off.
            #if within Time not every one has stopped Try sending global
            #command again.
            
            #First Take original Picture
            Picture(1)  #With 1 Vor image1 being original image where nothing has moved

            Original = cv2.imread("image1.jpg") 
            
            #for Devices in 16:
                #if Devices == 1:
                #Say Pico Zebro 1 Turn led 1 on.
                #Wait until said back in register it is turned on
            Picture(2) #led 1 on picture 2
                #Say Pico Zebro 1 Turn led 1 off and 3 on.
                #wait until Pico Zebro Says Yeah have done that
            Picture(3) #led 3 on in picture 3
                # Turn All leds of again.
            Led_1 = cv2.imread("image2.jpg")
            Led_3 = cv2.imread("image3.jpg")

            New_image_Led_1 = abs(Original - Led_1)
            New_image_Led_3 = abs(Original - Led_3)
            Difference_led_1 = Image_Difference(New_image_Led_1)
            Difference_led_3 = Image_Difference(New_image_Led_3)

            Finding_Canny_Led_1 = cv2.Canny(Difference_led_1, 15, 200)
            Finding_Canny_Led_3 = cv2.Canny(Difference_led_3, 15, 200)
            
            Finding_Canny_Led_1 = cv2.morphologyEx(Finding_Canny_Led_1, cv2.MORPH_CLOSE, np.ones((8,8),np.uint8))
            Finding_Canny_Led_3 = cv2.morphologyEx(Finding_Canny_Led_3, cv2.MORPH_CLOSE, np.ones((8,8),np.uint8))

            Finding_Canny_Led_1 = cv2.Canny(Finding_Canny_Led_1, 100, 200)
            Finding_Canny_Led_3 = cv2.Canny(Finding_Canny_Led_3, 100, 200)

            (_, contours_Led_1, _) = cv2.findContours(Finding_Canny_Led_1.copy(), cv2.RETR_EXTERNAL,
                                                cv2.CHAIN_APPROX_NONE)
            (_, contours_Led_3, _) = cv2.findContours(Finding_Canny_Led_3.copy(), cv2.RETR_EXTERNAL,
                                                cv2.CHAIN_APPROX_NONE)
            [x_Led_1,y_Led_1,w_Led_1,h_Led_1] = 0
            for c in contours_Led_1:
                try:
                    [x_Led_1,y_Led_1,w_Led_1,h_Led_1] = cv2.boundingRect(c)
                    cv2.rectangle(Difference_led_1,(x_Led_1,y_Led_1),(x_Led_1+w_Led_1,y_Led_1+h_Led_1),(0,255,0),2)
                    cv2.putText(Difference_led_1,'Found led 1',(x_Led_1+w_Led_1+10,y_Led_1+h_Led_1),0,0.3,(0,255,0))
                except AttributeError:
                    print("Nothing Found")
                    pass
            [x_Led_3,y_Led_3,w_Led_3,h_Led_3] = 0    
            for c in contours_Led_3:
                try:
                    [x_Led_3,y_Led_3,w_Led_3,h_Led_3] = cv2.boundingRect(c)
                    cv2.rectangle(Difference_led_3,(x_Led_3,y_Led_3),(x_Led_3+w_Led_3,y_Led_3+h_Led_3),(0,255,0),2)
                    cv2.putText(Difference_led_3,'Found led 3',(x_Led_3+w_Led_3+10,y_Led_3+h_Led_3),0,0.3,(0,255,0))
                except AttributeError:
                    print("Nothing Found")
                    pass
            #Add led 1 and 3 together for Testing purposes
            LEDS_Image = cv2.addWeighted(Difference_led_1,1,Difference_led_3,1,0)
            cv2.imshow("LEds together", LEDS_Image)

            (Zebro_Middle_x,Zebro_Middle_x,Direction) = Find_Orientation(x_Led_1,x_Led_3,y_Led_1,y_Led_3)

            #Now Add To a Value 1- (amount of Robots) These 3 Values and Send it to the thread which
            #Has the control of the Robots 
            time.sleep(60)


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
    FindZebro_Thread = FindZebroThread()
    FindZebro_Thread.setName("FindZebro_Thread")
    
    Original = cv2.imread("Led_on.jpg")
    Led1 = cv2.imread("Led_off.jpg")

    New_image = abs(Original - Led1)
    cv2.imshow("Testing image", New_image)
    cv2.imwrite("See_Difference.jpg",New_image)
    lowValY = 200
    highValY = 100
    array_np = np.asarray(New_image)
    low_values_indices = array_np > lowValY  # Where values are low
    high_values_indices = array_np < highValY
    array_np[low_values_indices] = 0  # All low values set to 0
    array_np[high_values_indices] = 0

    cv2.imshow("Testing 2 image", array_np)
    cv2.imwrite("new_image.jpg", array_np)

    Finding = cv2.imread("new_image_2.jpg")
    Finding_Canny = cv2.Canny(Finding, 15, 200)
    kernel = np.ones((8,8),np.uint8)
    Finding_Canny = cv2.morphologyEx(Finding_Canny, cv2.MORPH_CLOSE, kernel)
    Finding_Canny = cv2.Canny(Finding_Canny, 100, 200)
    cv2.imshow("Edge detection", Finding_Canny)
    Finding_Gray = cv2.cvtColor(Finding, cv2.COLOR_BGR2GRAY)

    (_, contours, _) = cv2.findContours(Finding_Canny.copy(), cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_NONE)    
    for c in contours:
        try:
            [x,y,w,h] = cv2.boundingRect(c)
            #cv2.drawContours(Finding, [c], -1, (255, 0, 255), -1)
            cv2.rectangle(Finding,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(Finding,'Found led 1',(x+w+10,y+h),0,0.3,(0,255,0))
        except AttributeError:
            pass
    
    cv2.imshow("Found Objects", Finding)
    # show the frame
    cv2.waitKey(0)
    #key = cv2.waitKey(1) & 0xFF
