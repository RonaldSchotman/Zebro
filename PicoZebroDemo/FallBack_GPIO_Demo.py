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

from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS

# import the necessary packages
from picamera.array import PiRGBArray   # Pi camera Libary capture BGR video
from picamera import PiCamera           # PiCamera liberary
import time                             # For real time video (using openCV)
import numpy as np                      # Optimized library for numerical operations
import cv2                              # Include OpenCV library (Most important one)

import random
import threading
import bluetooth


import imutils

# initialize the camera and grab a reference to the raw camera capture
#camera = PiCamera()
#camera.resolution = (1664, 928)
#camera.resolution = (320, 240)
#camera.resolution = (1280, 720)
#camera.framerate_range.low
#camera.framerate = 30
#rawCapture = PiRGBArray(camera)
#stream = camera.capture_continuous(rawCapture, format="bgr",
#	use_video_port=True)
#

# allow the camera to warmup (So this is only during start up once).
time.sleep(0.1)

def Picture(Number):
    # grab an image from the camera
    time.sleep(0.01)
    
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    # write picture
    cv2.imwrite("Image%s.jpg"%Number, image)
    
    #Empty Stream (making it possible to take another picture
    rawCapture.truncate(0)
    return 0

def Image_Difference(Image):
    # making sure light doesn't matter
    lowValY = 180
    highValY = 100
    New_image = np.asarray(Image)
    low_values_indices = New_image > lowValY # Where values are low
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
    if(x_Led_1 == 0) or (x_Led_3 ==0) or (y_Led_1 == 0) or (y_Led_3 == 0):
        return x_middle, y_middle, Direction
    
    #Facing North (dermine middle point)
    elif (x_Led_1 <= x_Led_3) and (y_Led_1 < y_Led_3):
        # Pico Zebro is facing North
        # Middle Point Zebro is:
        x_middle = ((x_Led_3 - x_Led_1) + x_Led_1)
        y_middle = ((y_Led_3 - y_Led_1) + y_Led_1)
        Direction = "North"
        return x_middle, y_middle, Direction
    
    elif (x_Led_1 < x_Led_3) and (y_Led_1 >= y_Led_3):
        # Pico Zebro is facing East
        # Middle Point Zebro is:
        x_middle = ((x_Led_3 - x_Led_1) + x_Led_1)
        y_middle = ((y_Led_1 - y_Led_3) + y_Led_3)
        Direction = "East"
        return x_middle, y_middle, Direction
    
    elif (x_Led_1 >= x_Led_3) and (y_Led_1 > y_Led_3):
        # Pico Zebro is facing South
        # Middle Point Zebro is:
        x_middle = ((x_Led_1 - x_Led_3) + x_Led_3)
        y_middle = ((y_Led_1 - y_Led_3) + y_Led_3)
        Direction = "South"
        return x_middle, y_middle, Direction
    
    elif (x_Led_1 > x_Led_3) and (y_Led_1 <= y_Led_3):
        # Pico Zebro is facing West
        # Middle Point Zebro is:
        x_middle = ((x_Led_1 - x_Led_3) + x_Led_3)
        y_middle = ((y_Led_3 - y_Led_1) + y_Led_1)
        Direction = "West"
        return x_middle, y_middle, Direction
    
    return x_middle, y_middle, Direction

class FindZebroThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        
        self.start()

    def run(self):
        while True:
            start_time = time.time()
            #time.sleep(60) #Because of at startup nothing is connected yet
            #Try to find every Pico Zebro every 60 Seconds

            #First Send global command to all Pico Zebro with Stop.

            #Wait untill connected Pico Zebro's give back yes I am stopped
            #Also Turn all leds off.
            #if within Time not every one has stopped Try sending global
            #command again.
            #Picture(1) 
            
            time1=0
            t_start = time.time()  # start
            e1 = cv2.getTickCount()
            #First Take original Picture
            vs = PiVideoStream().start()
            #time.sleep(2.0)
            fps = FPS().start()
            while fps._numFrames < 10:
                # grab the frame from the threaded video stream and resize it
                # to have a maximum width of 400 pixels
                frame = vs.read()
             
                # check to see if the frame should be displayed to our screen
 #               cv2.imshow("Frame", frame)
                cv2.imwrite("image25.jpg",frame)
                key = cv2.waitKey(1) & 0xFF
             
                # update the FPS counter
                fps.update()
             
            # stop the timer and display FPS information
            fps.stop()
            print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
            print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
             
            # do a bit of cleanup
            cv2.destroyWindow("Frame")
            vs.stop()

            
            Original = cv2.imread("Image1.jpg")
            e2 = cv2.getTickCount()
            
            #With 1 Vor image1 being original image where nothing has moved

            
            time1 = (e2 - e1) / cv2.getTickFrequency() + time1
            elapsedTime = time.time()-t_start
            print (time1, elapsedTime)
            #for Devices in 16:
                #print(Devices)
                #if Devices == 1: # This has to be done for every Zebro
                # Also if Devices is 1 give a value the address of Pico Zebro 1.
                #Say Pico Zebro 1 Turn led 1 on.
                #Wait until said back in register it is turned on for certain time

            #Picture(2) #led 1 on picture 2
          
                #Say Pico Zebro 1 Turn led 1 off and 3 on.
                #wait until Pico Zebro Says Yeah have done that

            #Picture(3) #led 3 on in picture 3
                # Turn All leds of again. # Till here other things needs to be coded for every possible
                
            Led_1 = cv2.imread("Image2.jpg")
            Led_3 = cv2.imread("Image3.jpg")
            picture_test = 0
            
            New_image_Led_1 = abs(Original - Led_1)    #Taking away improved time with 0.05 seconds which is fo 20 zebros: 1 second
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
            x_Led_1 = 0
            y_Led_1 = 0
            w_Led_1 = 0
            h_Led_1 = 0
            for c in contours_Led_1:
                try:
                    [x_Led_1,y_Led_1,w_Led_1,h_Led_1] = cv2.boundingRect(c)
                    cv2.rectangle(Difference_led_1,(x_Led_1,y_Led_1),(x_Led_1+w_Led_1,y_Led_1+h_Led_1),(0,255,0),2)
                    cv2.putText(Difference_led_1,'Found led 1',(x_Led_1+w_Led_1+10,y_Led_1+h_Led_1),0,0.3,(0,255,0))
                except AttributeError:
                    print("Nothing Found")
                    pass
            x_Led_3 = 0
            y_Led_3 = 0
            w_Led_3 = 0
            h_Led_3 = 0    
            for c in contours_Led_3:
                try:
                    [x_Led_3,y_Led_3,w_Led_3,h_Led_3] = cv2.boundingRect(c)
                    cv2.rectangle(Difference_led_3,(x_Led_3,y_Led_3),(x_Led_3+w_Led_3,y_Led_3+h_Led_3),(0,255,0),2)
                    cv2.putText(Difference_led_3,'Found led 3',(x_Led_3+w_Led_3+10,y_Led_3+h_Led_3),0,0.3,(0,255,0))
                except AttributeError:
                    print("Nothing Found")
                    pass
            #For some reason this debug functions gives errors that kille
            #everything which is anoying
                
            #Add led 1 and 3 together for Testing purposes
            #LEDS_Image = cv2.addWeighted(Difference_led_1,1,Difference_led_3,1,0)
            #cv2.imwrite("Leds_image.jpg", LEDS_Image)
            #cv2.imshow("LEds together", LEDS_Image)
                
            try:
                (Zebro_Middle_x,Zebro_Middle_y,Direction) = Find_Orientation(x_Led_1,x_Led_3,y_Led_1,y_Led_3)
                #print(Zebro_Middle_x,Zebro_Middle_y,Direction)
            except TypeError as e:
                print(e)
                pass

           
            #if Devices == 0: in here it is multiple times aquire
                #set data from PZ 1
                #Zebro_1_Middle_x = Zebro_Middle_x
                #Zebro_1_Middle_y,
                #Direction_Zebro_1 = Direction
                #etc every value
                #Now Add To a Value 1- (amount of Robots) These 3 Values and Send it to the thread which
                #Has the control of the Robots
            #once every value for every possible Zebro is determind then
            #Check if any of the x and y values are close to each other.
            #or if any of the x or y values are to close to the edge which is
            # if x == 0 or x == 1600 or y = 0 or y == 920 
            #So a gigantic multiple if statement. which becomes smaller and smaller
            # 
            
            #time.sleep(0.1)
            print ("My program took", time.time() - start_time, "to run")
            

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

class Control_Zebro_Thread(threading.Thread):
    def __init__(self, names, condition, Zebro):
        ''' Constructor. of Control Thread '''
        threading.Thread.__init__(self)

        self.daemon = True

        self.names = names
        self.condition = condition
        self.Zebro = Zebro
        
        self.start()
 
    def run(self):
        while True:
            self.condition.acquire()
            names = self.names
            names  = [val for sublist in names for val in sublist]
            print(names)
            #print(self.Zebro)
            self.condition.release()
            time.sleep(15) # sleep here is only I dont go crazy during testing
            # Try to connect with possible devices in names.
            # for Amount in names:
                # here try to connect with names
                # if connected == True: "Connected_Zebro%s"%Zebro = 1
                # else is Connected = 0 and try again to connect after 60 seconds
            #if connected == 0:
                # previous_movement = Dont Move
                #time.sleep(60) only here is sleeping allowed considering it is not connected any way
                #otherwise sleeping is not allowd considering a global command needs to be able to send
                #to every Zebro wit lights of and dont move. (FREEZE (PIEP)) 
                #pass
            #if connected == 1:
                # Here comes a test command to check if we are still connected.
                # This means read a register and get a expected value otherwise connected == 0
                # if expected value == True then:
        # From here on out the actual controlling
                    # obtain own middle point and information about if needed to avoid an other
                    # Pico Zebro
                    # Do this from Find Zebro Thread.
                    # With this information do the following
                    # if own middle point == 0 then it is not in the demo so
                        # Movement ==  dont move
                    # then checking Battery level
                    # if to low go direction south
                    # This can only be written with knowing what south is and what current direction is
                    # then the next direction can be determind.
                    # if high enough do the following
                    # Movement = Don't Move
                    
                    # if previous movement == Dont Move:
                        # Testing =  random.randrange(1,100)
                        # print(Testing)
                        # if Testing =< 60:
                        # Movement = Go Forwar
                        # if Testing > 60 or Testing =< 70:
                        # Movement = Don't move
                        # if Testing > 70 or Testing =< 85:
                        # Movement = Go right
                        # if Testing > 85 or Testing =< 100:
                        # Movement = Go left
                        
                    # if previous movement == Forward:
                        # Testing =  random.randrange(1,100)
                        # if Testing =< 80:
                        # Movement = Go Forward
                        # if Testing > 80 or Testing =< 90:
                        # Movement = Don't move
                        # if Testing > 90 or Testing =< 95:
                        # Movement = Go right
                        # if Testing > 95 or Testing =< 100:
                        # Movement = Go left
                        
                    # if previous movement == right:
                        # Testing =  random.randrange(1,100)
                        # print(Testing)
                        # if Testing =< 30:
                        # Movement = Go Forward
                        # if Testing > 30 or Testing =< 35:
                        # Movement = Don't move
                        # if Testing > 35 or Testing =< 95:
                        # Movement = Go right
                        # if Testing > 95 or Testing =< 100:
                        # Movement = Go left

                    # if previous movement == left:
                        # Testing =  random.randrange(1,100)
                        # if Testing =< 30:
                        # Movement = Go Forward
                        # if Testing > 30 or Testing =< 35:
                        # Movement = Don't move
                        # if Testing > 35 or Testing =< 40:
                        # Movement = Go right
                        # if Testing > 40 or Testing =< 100:
                        # Movement = Go left

                    # if movement == Blocked Movements:
                        # Movement = Don't Move
                    # send movement
                    # previous_movement = Movement
        
def main():
    
    names = []
    condition = threading.Condition()

    print(cv2.useOptimized())
    
    Picture_number = 0
    condition2 = threading.Condition()
    
    #Starting Sub threads
    Bluetooth_devices = FindingBTDevices(names, condition)
    Bluetooth_devices.setName("BT Devices")

    #Start Finding Zebro Thread
    FindZebro_Thread = FindZebroThread()
    FindZebro_Thread.setName("FindZebro_Thread")

    Pico_Zebro_1 = Control_Zebro_Thread(names, condition, 1)
    Pico_Zebro_1.setName('Pico_Zebro_1')
    
    Original = cv2.imread("Led_on.jpg")
    Led1 = cv2.imread("Led_off.jpg")

    New_image = abs(Original - Led1)
    cv2.imshow("Testing image", New_image)
    
    # show the frame
    cv2.waitKey(0)

if __name__ == '__main__':
    main()


