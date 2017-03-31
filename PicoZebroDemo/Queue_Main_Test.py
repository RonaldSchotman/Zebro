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

import random

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

class Control_Zebro_Thread(threading.Thread):
    def __init__(self,Serial_Lock, Zebro, q_PicoZebro, q_Pico_Direction, q_Pico_Angle):
        ''' Constructor. of Control Thread '''
        threading.Thread.__init__(self)

        self.daemon = True
        self.Serial_Lock = Serial_Lock
        self.Zebro = Zebro  #Name of the Zebro

        self.q_PicoZebro = q_PicoZebro
        self.q_Pico_Direction = q_Pico_Direction
        self.q_Pico_Angle = q_Pico_Angle
        
        self.start()

    def run(self):
        print(self.Zebro)
        Connected = 1
        Sleep = 0
        Last_Movement = "Stop"
        
        Middle_point_x = 0
        Middle_point_y = 0
        Movement_Blocked = 0
        DONT_Send = 0
        Blocked_Direction = []
        Current_Direction = "North"
        time.sleep(5)
        while True:
            if Connected == 0:
                Last_Movement = "Stop"

                Connected_Devices = []
                
                # Obtain Serial condition
                self.Serial_Lock.acquire(blocking=True, timeout=-1)
                #self.Serial_Lock.mutex.acquire()
                print(self.Zebro+" acquired Lock")
                Writing = "Connected_devices"
                Writing = Writing.encode('utf-8')
                ser.write(Writing)
                time.sleep(0.2)   # Wait for sending of data (depends on Arduino)
                Connected_Devices = ser.readline()
                Connected_Devices = Connected_Devices.decode('utf8')
                
                print(self.Zebro+" Released Lock")
                #self.Serial_Lock.mutex.release()
                self.Serial_Lock.release()
                
                # Release serial Connection
                for Connected_D in Connected_Devices:
                    if Connected_D == self.Zebro:   # Needs to be Pico_N1
                        print("Yeah")
                        Connected = 1
                        PicoZebro = self.q_PicoZebro.get(block=True, timeout=None)
                    
                        Middle_point_x = PicoZebro[0]
                        Middle_point_y = PicoZebro[1]
                        Blocked_Direction = PicoZebro[2]
                        
                        Current_Direction = self.q_Pico_Direction.get(block=True, timeout=None)
                        
                    else:
                        print("Go to SLEEP")
                        Connected = 0
                        Sleep = 1
                print(Connected_Devices)
                if Connected_Devices == "":
                    Sleep = 1
                    
                if Sleep == 1:
                    print("SLEEEPING")
                    time.sleep(60) # only here is sleeping allowed considering it is not connected anyway and only every 60 seconds needs to check
                    Sleep = 0
                
            if Connected == 1:
                # Here comes a test command to check if we are still connected. (if possible)
                # This means read a register and get a expected value otherwise connected == 0
                # if expected value == True then:
                
            # From here on out the actual controlling

            #obtain from Queue the middle point. Also here you need to wait with controlling untill the first value is set. 
                try: 
                    PicoZebro = self.q_PicoZebro.get(block=True, timeout=3)
                    Middle_point_x = PicoZebro[0]
                    Middle_point_y = PicoZebro[1]
                    Blocked_Direction = PicoZebro[2]
                except queue.Empty:
                    Middle_point_x = Middle_point_x
                    Middle_point_y = Middle_point_y
                    Blocked_Direction = Blocked_Direction
                    print("No new Data")
                
                try:
                    Current_Direction = self.q_Pico_Direction.get(block=True, timeout=3)
                except queue.Empty:
                    Current_Direction = Current_Direction
                #Angle = self.q_Pico_Angle.get(block=True, timeout=None)
                #print(PicoZebro)
                #print(Middle_point_x)
                #print(Middle_point_y)
                #print(Blocked_Direction)
                #print(Current_Direction)
                
                if (Middle_point_x == 0) or (Middle_point_y == 0):
                    Last_Movement == "Stop"
                    
                else:
                    for Names in Blocked_Direction:
                        if Current_Direction == Names:
                            Movement_Blocked = 1
                    
                    if Movement_Blocked == 1:  # If this is the case the last movement cannot be the next direction so we make the change smaller
                        if Last_Movement == "Forward":
                            Last_Movement = "Right"
                        elif Last_Movement == "Right":
                            Last_Movement = "Forward"
                        elif Last_Movement == "Left":
                            Last_Movement = "Forward"
                        elif Last_Movement == "Stop":
                            Last_Movement = "Left"
                        Movement_Blocked = 0
                            
                    if Last_Movement == "Stop":
                        Random_N = random.randrange(1,100)
                        if Random_N <= 60:
                            Movement = "Forward"
                        elif Random_N > 60 and Random_N <= 70:
                            Movement = "Stop"
                        elif Random_N > 70 and  Random_N <= 85:
                            Movement = "Right"
                        elif Random_N > 85 and  Random_N <= 100:
                            Movement = "Left"

                    if Last_Movement == "Forward":
                        Random_N = random.randrange(1,100)
                        if Random_N <= 80:
                            Movement = "Forward"
                        elif Random_N > 80 and Random_N <= 90:
                            Movement = "Stop"
                        elif Random_N > 90 and Random_N <= 95:
                            Movement = "Right"
                        elif Random_N > 95 and Random_N <= 100:
                            Movement = "Left"

                    if Last_Movement == "Right":
                        Random_N = random.randrange(1,100)
                        if Random_N <= 30:
                            Movement = "Forward"
                        elif Random_N > 30 and Random_N <= 35:
                            Movement = "Stop"
                        elif Random_N > 35 and Random_N <= 95:
                            Movement = "Right"
                        elif Random_N > 95 and Random_N <= 100:
                            Movement = "Left"
     
                    if Last_Movement == "Left":
                        Random_N = random.randrange(1,100)
                        if Random_N <= 30:
                            Movement = "Forward"
                        elif Random_N > 30 and Random_N <= 35:
                            Movement = "Stop"
                        elif Random_N > 35 and Random_N <= 40:
                            Movement = "Right"
                        elif Random_N > 40 and Random_N <= 100:
                            Movement = "Left"

                    if Movement == "Forward":
                        Direction = Current_Direction
                    elif Movement == "Stop":
                        Direction = Current_Direction
                    elif Movement == "Right":
                        if Current_Direction == "North":
                            Direction = "East"
                        elif Current_Direction == "East":
                            Direction = "South"
                        elif Current_Direction == "South":
                            Direction = "West"
                        elif Current_Direction == "West":
                            Direction = "North"
                    elif Movement == "Left":
                        if Current_Direction == "North":
                            Direction = "West"
                        elif Current_Direction == "West":
                            Direction = "South"
                        elif Current_Direction == "South":
                            Direction = "East"
                        elif Current_Direction == "East":
                            Direction = "North"

                    for Names in Blocked_Direction:
                        if Direction == Names:
                            DONT_Send = 1
                            
                    if DONT_Send == 1:
                        # Obtain Serial Write
                        #self.Serial_Lock.mutex.acquire()
                        print("We Blocking Boys")
                        print(Current_Direction)
                        print(Movement)
                        print(Blocked_Direction)
                        self.Serial_Lock.acquire(blocking=True, timeout=-1)
                        Writing = (self.Zebro + " Stop")
                        Writing = Writing.encode('utf-8')
                        ser.write(Writing)
                        self.Serial_Lock.release()
                        #self.Serial_Lock.mutex.release()
                        # Release Serial Write
                    else:
                        # Obtain Serial Write
                        #self.Serial_Lock.mutex.acquire()
                        print(Movement)
                        print(Current_Direction)
                        print(Middle_point_x)
                        print(Middle_point_y)
                        self.Serial_Lock.acquire(blocking=True, timeout=-1)
                        Writing = (self.Zebro + Movement)
                        Writing = Writing.encode('utf-8')
                        ser.write(Writing)
                        self.Serial_Lock.release()
                        #self.Serial_Lock.mutex.release()
                        # Release Serial Write
                        Last_Movement = Movement
                        Current_Direction = Direction
                        
                    DONT_Send = 0

def Image_Difference(Image):
    # making sure light doesn't matter
    lowValY = 150
    highValY = 100
    New_image = np.asarray(Image)
    low_values_indices = New_image > lowValY  # Where values are low
    high_values_indices = New_image < highValY #Where values are high
    New_image[low_values_indices] = 0  # All low values set to 0
    New_image[high_values_indices] = 0 # All high values set to 0
    return New_image

def Find_Orientation(x_Led_1,x_Led_3,y_Led_1,y_Led_3):
    x_middle = 0
    y_middle = 0
    Angle = 0
    Direction = None
    
    #No points Found
    if(x_Led_1 or x_Led_3 or y_Led_1 or y_Led_3) == 0:
        return x_middle, y_middle, Direction, Angle
    
    #Facing North (dermine middle point)
    elif (x_Led_1 < x_Led_3) and (y_Led_1 < y_Led_3):
        # Pico Zebro is facing North
        # Middle Point Zebro is:
        x_middle = ((x_Led_3 - x_Led_1) + x_Led_1)
        y_middle = ((y_Led_3 - y_Led_1) + y_Led_1)
        Angle = 360 - (abs(x_Led_3 - x_Led_1)*1.384)    #From 360-270
        Direction = "North"
        return x_middle, y_middle, Direction, Angle
    
    elif (x_Led_1 < x_Led_3) and (y_Led_1 > y_Led_3):
        # Pico Zebro is facing East
        # Middle Point Zebro is:
        x_middle = ((x_Led_3 - x_Led_1) + x_Led_1)
        y_middle = ((y_Led_1 - y_Led_3) + y_Led_3)
        Angle = 0 + (abs(x_Led_3 - x_Led_1)*1.384)    #From 0-90
        Direction = "East"
        return x_middle, y_middle, Direction, Angle
    
    elif (x_Led_1 > x_Led_3) and (y_Led_1 > y_Led_3):
        # Pico Zebro is facing South
        # Middle Point Zebro is:
        x_middle = ((x_Led_1 - x_Led_3) + x_Led_3)
        y_middle = ((y_Led_1 - y_Led_3) + y_Led_3)
        Angle = 180 - (abs(x_Led_1 - x_Led_3)*1.384)    #From 180-90
        Direction = "South"
        return x_middle, y_middle, Direction, Angle
    
    elif (x_Led_1 > x_Led_3) and (y_Led_1 < y_Led_3):
        # Pico Zebro is facing West
        # Middle Point Zebro is:
        x_middle = ((x_Led_1 - x_Led_3) + x_Led_3)
        y_middle = ((y_Led_3 - y_Led_1) + y_Led_1)
        Angle = 270 - (abs(x_Led_1 - x_Led_3)*1.384)    #From 270-180
        Direction = "West"
        return x_middle, y_middle, Direction, Angle
    return x_middle, y_middle, Direction, Angle

def main(Serial_Lock,q_PicoZebro_1,
         q_Pico_Direction_1,
         q_Pico_Angle_1):
    
    # Initialize Picture to 0 for the first time when program starts.
    Picture = 0
    Devices = 0
    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the NumPy array representing the image, the initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array

        # Take current day for testing purposes.
        Timetest = time.strftime("%d-%m-%Y")
        # Show the current view for debugging
        cv2.imshow("original %s" % Timetest,image)

        # Take original Picture minimal after first loop for the first frame to avoid weird pictures.
        if Picture == 1:

            #Global command turn all leds off. (This needs to be tested how long this takes.)
            #Like this with condition. With I am writing now on the serial Bus. The rest needs to wait for me. (So all zebro Thread wait with sending next movement.)
            #Release condition only at end so the Zebro Treads cannot interfere, This is at Picture 4.

            Serial_Lock.acquire(blocking=True, timeout=-1)
            #Serial_Lock.mutex.acquire()
            print("MAIN Acquired LOCK")
            Writing_0 = ("Global Stop")
            Writing_0 = Writing_0.encode('utf-8')
            ser.write(Writing_0)
            Writing_1 = ("Global Leds_off")
            Writing_1 = Writing_1.encode('utf-8')
            ser.write(Writing_1)
            
            time.sleep(0.001)
            Zebro_1_Middle_x = 0
            Zebro_1_Middle_y = 0
            PicoZebro_1 = []
            
            cv2.imwrite("Image%s.jpg"%Picture, image)   # Save a picture to Image1.jpg
            
            #Original = cv2.imread("Image1.jpg")     # This is the original picture where the diferences will be compared with.
            Original = cv2.imread("Leds_off.jpg")
        
        if Picture == 2:    # Make Picture 2 for taking Picture 2 with Led 1 on.
            Devices_Serial = Devices + 1

            #If Correctly done we still have the lock of Serial Write/read
            Writing_2 = ("PicoN%s Led1_on" % Devices_Serial)
            Writing_2 = Writing_2.encode('utf-8')
            ser.write(Writing_2)

            time.sleep(0.001)
            #Wait until said back in register it is turned on for certain time (Now it is a hard wait)
            
            cv2.imwrite("Image%s.jpg"%Picture, image)   # Take the second picture with led 1 on. Which is
            
            #If Correctly done we still have the lock of Serial Write/read
            Writing_3 = ("PicoN%s Leds_off\n" % Devices_Serial)
            Writing_3 = Writing_3.encode('utf-8')
            ser.write(Writing_3) # Turn led 1 of again

         #Again do some other stuff
        if Picture == 3:
            print("Picture %d"%Picture)
            #If Correctly done we still have the lock of Serial Write/read
            Writing_4 = ("PicoN%s Led3_on\n" % Devices_Serial)
            Writing_4 = Writing_4.encode('utf-8')
            ser.write(Writing_4) # Turn led 3 on

            #Wait until said back in register it is turned on for certain time (Now it is a hard wait)
            time.sleep(0.001)
            cv2.imwrite("Image%s.jpg"%Picture, image)
            
            Writing_5 = ("PicoN%s Leds_off\n" % Devices_Serial)
            Writing_5 = Writing_5.encode('utf-8')
            ser.write(Writing_5) # Turn led 1 of again
            
        if Picture == 4:
            print("Picture %d"%Picture)
            # Take both pictures with the leds.
            Led_1 = cv2.imread("Led1_on.jpg")
            Led_3 = cv2.imread("Led3_on.jpg")
            #Led_1 = cv2.imread("Image2.jpg")
            #Led_3 = cv2.imread("Image3.jpg")

            New_image_Led_1 = abs(Original - Led_1)
            New_image_Led_3 = abs(Original - Led_3)
            Difference_led_1 = Image_Difference(New_image_Led_1) # Make only the led visible
            Difference_led_3 = Image_Difference(New_image_Led_3) # Make only the led visible

            Finding_Canny_Led_1 = cv2.Canny(Difference_led_1, 15, 200)
            Finding_Canny_Led_3 = cv2.Canny(Difference_led_3, 15, 200)
                    
            Finding_Canny_Led_1 = cv2.morphologyEx(Finding_Canny_Led_1, cv2.MORPH_CLOSE, np.ones((8,8),np.uint8))
            Finding_Canny_Led_3 = cv2.morphologyEx(Finding_Canny_Led_3, cv2.MORPH_CLOSE, np.ones((8,8),np.uint8))

            Finding_Canny_Led_1 = cv2.Canny(Finding_Canny_Led_1, 100, 200)
            Finding_Canny_Led_3 = cv2.Canny(Finding_Canny_Led_3, 100, 200)

            (_, contours_Led_1, _) = cv2.findContours(Finding_Canny_Led_1.copy(), cv2.RETR_EXTERNAL,
                                                      cv2.CHAIN_APPROX_NONE) # Find the contours of Led 1
            (_, contours_Led_3, _) = cv2.findContours(Finding_Canny_Led_3.copy(), cv2.RETR_EXTERNAL,
                                                      cv2.CHAIN_APPROX_NONE) # Find the contours of Led 3
            x_Led_1 = 0
            y_Led_1 = 0
            w_Led_1 = 0
            h_Led_1 = 0

            x_Led_3 = 0
            y_Led_3 = 0
            w_Led_3 = 0
            h_Led_3 = 0 
                
            areaArray_Led_1 = []
            areaArray_Led_3 = []
                
            for i, c in enumerate(contours_Led_1):
                area_led_1 = cv2.contourArea(c)
                areaArray_Led_1.append(area_led_1)

            for i, c in enumerate(contours_Led_3):
                area_led_3 = cv2.contourArea(c)
                areaArray_Led_3.append(area_led_3)

            sorteddata_Led_1 = sorted(zip(areaArray_Led_1, contours_Led_1), key=lambda x: x[0], reverse=True)
            sorteddata_Led_3 = sorted(zip(areaArray_Led_3, contours_Led_3), key=lambda x: x[0], reverse=True)

            try:
                Largest_contour_led_1 = sorteddata_Led_1[0][1]
                [x_Led_1,y_Led_1,w_Led_1,h_Led_1] = cv2.boundingRect(Largest_contour_led_1)
            except (IndexError, cv2.error) as e:
                print("Nothing Found")
                pass

            try:
                Largest_contour_led_3 = sorteddata_Led_3[0][1]
                [x_Led_3,y_Led_3,w_Led_3,h_Led_3] = cv2.boundingRect(Largest_contour_led_3)
            except (IndexError, cv2.error) as e:
                print("Nothing Found")
                pass

            (Zebro_Middle_x,Zebro_Middle_y,Direction, Angle) = Find_Orientation(x_Led_1,x_Led_3,y_Led_1,y_Led_3)
            print(Zebro_Middle_x,Zebro_Middle_y,Direction, Angle)  # Debug print

            if Devices == 0: 
                #set data from PZ 1
                Zebro_1_Middle_x = Zebro_Middle_x
                Zebro_1_Middle_y = Zebro_Middle_y
                Direction_Zebro_1 = Direction
                Angle_Zebro_1 = Angle
                Picture = 5
                
            Devices = Devices + 1

        if Picture == 5:
            Devices = 0
            #once every value for every possible Zebro is determind then
            for Zebros in range(1): # total of maximum of 20 Zebro's so 0-19 is 20 Zebro's
                Blocking_Zebro = []   #Here will be the blocking in
                if Zebros == 0:
                    Blocking_Zebro = Block.Block_2(Zebro_1_Middle_x,Zebro_1_Middle_y)
                    
                    PicoZebro_1 = [Zebro_1_Middle_x , Zebro_1_Middle_y, Blocking_Zebro]
                    
                    if q_PicoZebro_1.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_1.put(PicoZebro_1)
                    elif q_PicoZebro_1.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_1.mutex.acquire()
                        q_PicoZebro_1.queue.clear()
                        q_PicoZebro_1.all_tasks_done.notify_all()
                        q_PicoZebro_1.unfinished_tasks = 0
                        q_PicoZebro_1.mutex.release()
                        q_PicoZebro_1.put(PicoZebro_1)

                    if q_Pico_Direction_1.empty() == True:   #if the queue is empty fill it
                        q_Pico_Direction_1.put(Direction_Zebro_1)
                    elif q_Pico_Direction_1.empty() == False: #else empty it before filling it again with the next data.
                        q_Pico_Direction_1.mutex.acquire()
                        q_Pico_Direction_1.queue.clear()
                        q_Pico_Direction_1.all_tasks_done.notify_all()
                        q_Pico_Direction_1.unfinished_tasks = 0
                        q_Pico_Direction_1.mutex.release()
                        q_Pico_Direction_1.put(Direction_Zebro_1)
                    print(PicoZebro_1)
                    print(Direction_Zebro_1)
                    Picture = 6
                    Writing_6 = ("Global Leds_off")
                    Writing_6 = Writing_6.encode('utf-8')
                    ser.write(Writing_6) # Turn led 1 of again
                    
                    Writing_7 = ("Global Led1_on")
                    Writing_7 = Writing_7.encode('utf-8')
                    ser.write(Writing_7)
                    print("MAIN RELEASE SERIAL LOCK")
                    #Serial_Lock.mutex.release()
                    Serial_Lock.release()
                    # Release Condition Serial Write. (Now movement can start.)
                    Picture_1_start_time = time.time() # Testing Function for how long a part of a code takes.

        if Picture == 6:
            if (time.time() - Picture_1_start_time) > 600:
                Picture = 0
                print("Restarting program reinit")
                Picture_1_start_time = 0
                
            Follow_Led_1 = cv2.imread("Led1_on.jpg")
            #Global Command Turn all leds off
            #Glabal Command turn all led 1 on.  #Do this once
            #Wait untill this is done.
            gray = cv2.cvtColor(Follow_Led_1, cv2.COLOR_BGR2GRAY)  # Take a gray picture
            blurred = cv2.GaussianBlur(gray, (11, 11), 0)   # Blur image for noise reduction
            # threshold the image to reveal light regions in the
            # blurred image
            thresh = cv2.threshold(blurred, 240, 250, cv2.THRESH_BINARY)[1]
            # perform a series of erosions and dilations to remove
            # any small blobs of noise from the thresholded image
            thresh = cv2.erode(thresh, None, iterations=2)
            thresh = cv2.dilate(thresh, None, iterations=4)

            # find the contours in the mask, then sort them from left to
            # right
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if imutils.is_cv2() else cnts[1]
            try:
                cnts = contours.sort_contours(cnts)[0]
            except ValueError:
                pass
                #print("There are no zebros")
             
            # loop over the contours
            for (i, c) in enumerate(cnts):
                # draw the bright spot on the image
                (x, y, w, h) = cv2.boundingRect(c)
                x_compare_1 = x + 80
                y_compare_1 = y + 50
                x_compare_2 = x - 80
                y_compare_2 = y - 50
                if (x_compare_2 < Zebro_1_Middle_x < x_compare_1) and (y_compare_2 < Zebro_1_Middle_y < y_compare_1):
                    cv2.putText(Follow_Led_1, "#1", (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                    Zebro_1_Middle_x = x
                    Zebro_1_Middle_y = y
                    print("This is Zebro 1")
                    
            for Zebros in range(1):
                Blocking_Zebro = []   #Here will be the blocking in
                if Zebros == 0:
                    Blocking_Zebro = Block.Block_2(Zebro_1_Middle_x,Zebro_1_Middle_y)
                    
                    PicoZebro_1 = [Zebro_1_Middle_x , Zebro_1_Middle_y, Blocking_Zebro]
                    
                    if q_PicoZebro_1.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_1.put(PicoZebro_1)
                    elif q_PicoZebro_1.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_1.mutex.acquire()
                        q_PicoZebro_1.queue.clear()
                        q_PicoZebro_1.all_tasks_done.notify_all()
                        q_PicoZebro_1.unfinished_tasks = 0
                        q_PicoZebro_1.mutex.release()
                        q_PicoZebro_1.put(PicoZebro_1)
                Picture = 5
                
        Picture = Picture + 1
        
        # show the frame
        key = cv2.waitKey(1) & 0xFF

        #clear the stream in preparation of the next frame
        rawCapture.truncate(0)

        # if the 'q' key was pressed, break from the loop
        if key == ord("q"):
            # cleanup the camera and close any open windows
            print("Ending program")
            ser.close()
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    #The Serial write mutex lock.
    #Serial connection init 
    ser = serial.Serial(
      port='/dev/ttyS0',
      baudrate = 9600,
      parity=serial.PARITY_NONE,
      stopbits=serial.STOPBITS_ONE,
      bytesize=serial.EIGHTBITS,
      timeout=1
    )

    #Check if connection is made otherwise restart program.
    print (("Serial is open: {0}".format(ser.isOpen())))

    if (ser.isOpen()) == False:
        print("Couldnt open UART")
        sys.exit("aa! errors!")

    Serial_Lock = threading.Lock()
    #Serial_Lock = queue.Queue()

    # All Queue objects Constructor for a FIFO queue
    # These Queue objects are only data obtained by main loop and read by Pico Zebro loops.
    q_PicoZebro_1 = queue.Queue(maxsize=1) #This is a list with in it [Zebro_1_Middle_x , Zebro_1_Middle_y, Blocking_Zebro]
    # With a maximum of 1 list. so maxsize = 1.

    #In here will be the direection. Only at the start the main will put something in here afterwards for 10 mins the Zebro thread needs to put himself something in there with guessing.
    q_Pico_Direction_1 = queue.Queue(maxsize=1) # With a maximum of 1 list. so maxsize = 1.

    #If higher Precision with direction is required
    q_Pico_Angle_1 = queue.Queue(maxsize=1) # With a maximum of 1 list. so maxsize = 1.

    #All Pico Zebro Names 1 - 20
    Pico_N1 = "Pico_N1"
    
    # Start all Pico Zebro Threads.
    Pico_Zebro_1 = Control_Zebro_Thread(Serial_Lock,Pico_N1,q_PicoZebro_1,q_Pico_Direction_1,q_Pico_Angle_1)
    Pico_Zebro_1.setName('Pico_Zebro_1')
    
    main(Serial_Lock,q_PicoZebro_1, q_Pico_Direction_1, q_Pico_Angle_1)

