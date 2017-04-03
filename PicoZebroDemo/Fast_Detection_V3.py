#!/usr/bin/env python
# TU Delft Pico Zebro Demo
# PZ_DEMO Fallback
# Full Code inclusive of Pseudo Code.
# Writer: Martijn de Rooij
# Version 0.02

# Everything is being tested from 120 cm height.

# import the necessary packages fo Vision
from picamera.array import PiRGBArray   # Pi camera Libary capture BGR video
from picamera import PiCamera           # PiCamera liberary
import time                             # For real time video (using openCV)
import numpy as np                      # Optimized library for numerical operations
import cv2                              # Include OpenCV library (Most important one in terms of recognition)

#import packages for multi thread control.
import queue                            # Library for Queueing sharing variables between threads
import threading                        # Library for Multithreading

import serial                           # Import serial uart library for raspberry pi
import math                             # mathematical functions library

import random                           # Library for Random numbers for determing where to go

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

class UART_Thread(threading.Thread):
    def __init__(self,q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main):
        ''' Constructor. of UART Thread '''
        threading.Thread.__init__(self)

        self.daemon = True
        self.q_Control_Serial_Write = q_Control_Serial_Write
        self.q_Data_is_Send = q_Data_is_Send
        self.q_Control_Uart_Main = q_Control_Uart_Main

        self.start()

    def run(self):
        while True:
            Sended_Data = 0
            
            if (self.q_Control_Serial_Write.empty() == False) or (Sended_Data == 1):
                Sended_Data = 1
                Serial = self.q_Control_Serial_Write.get(block=False)
                print(Serial)
                
                if Serial[1][0] == "Main":
                    Writing_To = Serial[1][1]
                    Writing_To = Writing_To.encode('utf-8')
                    
                    Writing = Serial[1][2]
                    Writing = Writing.encode('utf-8')

                    #ser.write(Writing_To+Writing)
                    ser.write(Writing_To)
                    ser.write(Writing)
                    Sended_Data = 0
                    print("Main_Writing")
                    
                    #Data_is_Send_Token = 1
                    #self.q_Data_is_Send.put(Data_is_Send_Token)
                    
                elif Serial[1][0] == "Pico_N1":
                    Writing_To = Serial[1][1]
                    Writing_To = Writing_To.encode('utf-8')
                    
                    Writing = Serial[1][2]
                    Writing = Writing.encode('utf-8')

                    #ser.write(Writing_To+Writing)
                    ser.write(Writing_To)
                    ser.write(Writing)
                    Sended_Data = 0
                    print("Pico_Zebro_1_Writing")
                    
                elif (Sended_Data == 1):
                    Sended_Data = 0

class Control_Zebro_Thread(threading.Thread):
    def __init__(self,q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main, Zebro, q_PicoZebro, q_Pico_Direction, q_Pico_Angle):
        ''' Constructor. of Control Thread '''
        threading.Thread.__init__(self)

        self.daemon = True

        self.q_Control_Serial_Write = q_Control_Serial_Write
        self.q_Data_is_Send = q_Data_is_Send
        self.q_Control_Uart_Main = q_Control_Uart_Main

        self.Zebro = Zebro  #Name of the Zebro

        self.q_PicoZebro = q_PicoZebro
        self.q_Pico_Direction = q_Pico_Direction
        self.q_Pico_Angle = q_Pico_Angle
        
        self.start()
 
    def run(self):
        print(self.Zebro)
        Connected = 0
        Sleep = 0
        Last_Movement = "Stop"

        Middle_point_x = 0
        Middle_point_y = 0
        Movement_Blocked = 0
        DONT_Send = 0
        Blocked_Direction = []
        Current_Direction = ""
        while True:
            if Connected == 0:
                Last_Movement = "Stop"

                Connected_Devices = []

                while (self.q_Control_Uart_Main.empty() == False): #Wait untill you are allowed to write again.
                    pass
                        
                if (self.q_Control_Uart_Main.empty() == True):
                    Writing = (self.Zebro,self.Zebro, "Connected_Devices")        
                    self.q_Control_Serial_Write.put((2, Writing), block=True, timeout=None)
                print(self.Zebro+" Released Lock")

                
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
                if not Connected_Devices:
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
                
                try:
                    Current_Direction = self.q_Pico_Direction.get(block=True, timeout=3)
                except queue.Empty:
                    Current_Direction = Current_Direction
                #Angle = self.q_Pico_Angle.get(block=True, timeout=None)
                
                
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
                        #Check if Main is writing in Uart. If so wait untill main is finished
                        while (self.q_Control_Uart_Main.empty() == False): #Wait untill you are allowed to write again.
                            pass
                        
                        if self.q_Control_Uart_Main.empty() == True:
                            Writing = (self.Zebro,self.Zebro, "Stop")
                            
                            self.q_Control_Serial_Write.put((2, Writing), block=True, timeout=None)
                            print(Writing)
                    else:
                        #Check if Main is writing in Uart. If so wait untill main is finished
                        while (self.q_Control_Uart_Main.empty() == False): #Wait untill you are allowed to write again.
                            pass
                        
                        if self.q_Control_Uart_Main.empty() == True:
                            Writing = (self.Zebro,self.Zebro, Movement)
                            self.q_Control_Serial_Write.put((2, Writing), block=True, timeout=None)
                            print(Writing)
                        
                        Last_Movement = Movement
                        Current_Direction = Direction
                        
                    DONT_Send = 0

# Functions For looking for Pico Zebro
def Image_Difference(Image):
    # making sure light doesn't matter
    lowValY = 150 # Making Flitsing or light level less invluencial
    highValY = 100 # Making shadows less invluential
    New_image = np.asarray(Image)   #put it in a Numpy array for better calculations
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

    #Once known what the max and minimum Distance is between two points
    # The following calculation can be done for saying that angle is the
    # Pico Zebro Turned: (This only needs to be done if just north, south east and west work.
    # 90 - atan(x) with x from 0 -90 and being the difference between Max and Min
    # So x = ? * Factor = 90  for max between max and min 
    
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
    return x_middle, y_middle, Direction, Angle  #extra return to avoid errors



def main(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main,
         q_PicoZebro_1,q_PicoZebro_2,q_PicoZebro_3,q_PicoZebro_4,q_PicoZebro_5,q_PicoZebro_6,q_PicoZebro_7,q_PicoZebro_8,q_PicoZebro_9,q_PicoZebro_10,
         q_PicoZebro_11,q_PicoZebro_12,q_PicoZebro_13,q_PicoZebro_14,q_PicoZebro_15,q_PicoZebro_16,q_PicoZebro_17,q_PicoZebro_18,q_PicoZebro_19,q_PicoZebro_20,
         q_Pico_Direction_1,q_Pico_Direction_2,q_Pico_Direction_3,q_Pico_Direction_4,q_Pico_Direction_5,q_Pico_Direction_6,q_Pico_Direction_7,q_Pico_Direction_8,q_Pico_Direction_9,q_Pico_Direction_10,
         q_Pico_Direction_11,q_Pico_Direction_12,q_Pico_Direction_13,q_Pico_Direction_14,q_Pico_Direction_15,q_Pico_Direction_16,q_Pico_Direction_17,q_Pico_Direction_18,q_Pico_Direction_19,q_Pico_Direction_20,
         q_Pico_Angle_1,q_Pico_Angle_2,q_Pico_Angle_3,q_Pico_Angle_4,q_Pico_Angle_5,q_Pico_Angle_6,q_Pico_Angle_7,q_Pico_Angle_8,q_Pico_Angle_9,q_Pico_Angle_10,
         q_Pico_Angle_11,q_Pico_Angle_12,q_Pico_Angle_13,q_Pico_Angle_14,q_Pico_Angle_15,q_Pico_Angle_16,q_Pico_Angle_17,q_Pico_Angle_18,q_Pico_Angle_19,q_Pico_Angle_20):
    
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

        
        #print ("My program took", time.time() - start_time, "to run")   #print how long it took

        # Take original Picture minimal after first loop for the first frame to avoid weird pictures.
        if Picture == 1:

            #Global command turn all leds off. (This needs to be tested how long this takes.)
            #Like this with condition. With I am writing now on the serial Bus. The rest needs to wait for me. (So all zebro Thread wait with sending next movement.)
            #Release condition only at end so the Zebro Treads cannot interfere, This is at Picture 4.

            if q_Control_Uart_Main.empty() == True:   #if the queue is empty fill it 
                Main_Control_Uart = 1
                print("MAIN Acquired LOCK")
                q_Control_Uart_Main.put((1), Main_Control_Uart)
                
            elif q_Control_Uart_Main.empty() == False: #else empty it before filling it again with the next data.
                Main_Control_Uart = 1
                q_Control_Uart_Main.mutex.acquire()
                q_Control_Uart_Main.queue.clear()
                q_Control_Uart_Main.all_tasks_done.notify_all()
                q_Control_Uart_Main.unfinished_tasks = 0
                q_Control_Uart_Main.mutex.release()
                q_Control_Uart_Main.put(1, Main_Control_Uart)
 
            if q_Control_Serial_Write.empty() == False: #empty all data and let the Pico Zebro's redo their stuff
                q_Control_Serial_Write.mutex.acquire()
                q_Control_Serial_Write.queue.clear()
                q_Control_Serial_Write.all_tasks_done.notify_all()
                q_Control_Serial_Write.unfinished_tasks = 0
                q_Control_Serial_Write.mutex.release()

            Writing = ("Main","Global", "Stop")
            q_Control_Serial_Write.put((1, Writing), block=True, timeout=None)
            print("writing to serial")
                
            Writing = ("Main","Global", "Leds_off")            
            q_Control_Serial_Write.put((1, Writing), block=True, timeout=None)
            
            time.sleep(0.001)
            Zebro_1_Middle_x = 0
            Zebro_2_Middle_x = 0
            Zebro_3_Middle_x = 0
            Zebro_4_Middle_x = 0
            Zebro_5_Middle_x = 0
            Zebro_6_Middle_x = 0
            Zebro_7_Middle_x = 0
            Zebro_8_Middle_x = 0
            Zebro_9_Middle_x = 0
            Zebro_10_Middle_x = 0
            Zebro_11_Middle_x = 0
            Zebro_12_Middle_x = 0
            Zebro_13_Middle_x = 0
            Zebro_14_Middle_x = 0
            Zebro_15_Middle_x = 0
            Zebro_16_Middle_x = 0
            Zebro_17_Middle_x = 0
            Zebro_18_Middle_x = 0
            Zebro_19_Middle_x = 0
            Zebro_20_Middle_x = 0
            Zebro_1_Middle_y = 0
            Zebro_2_Middle_y = 0
            Zebro_3_Middle_y = 0
            Zebro_4_Middle_y = 0
            Zebro_5_Middle_y = 0
            Zebro_6_Middle_y = 0
            Zebro_7_Middle_y = 0
            Zebro_8_Middle_y = 0
            Zebro_9_Middle_y = 0
            Zebro_10_Middle_y = 0
            Zebro_11_Middle_y = 0
            Zebro_12_Middle_y = 0
            Zebro_13_Middle_y = 0
            Zebro_14_Middle_y = 0
            Zebro_15_Middle_y = 0
            Zebro_16_Middle_y = 0
            Zebro_17_Middle_y = 0
            Zebro_18_Middle_y = 0
            Zebro_19_Middle_y = 0
            Zebro_20_Middle_y = 0
            PicoZebro_1 = []
            PicoZebro_2 = []
            PicoZebro_3 = []
            PicoZebro_4 = []
            PicoZebro_5 = []
            PicoZebro_6 = []
            PicoZebro_7 = []
            PicoZebro_8 = []
            PicoZebro_9 = []
            PicoZebro_10 = []
            PicoZebro_11 = []
            PicoZebro_12 = []
            PicoZebro_13 = []
            PicoZebro_14 = []
            PicoZebro_15 = []
            PicoZebro_16 = []
            PicoZebro_17 = []
            PicoZebro_18 = []
            PicoZebro_19 = []
            PicoZebro_20 = []
            
            cv2.imwrite("Image%s.jpg"%Picture, image)   # Save a picture to Image1.jpg
            #time.sleep(10)
            Original = cv2.imread("Image1.jpg")     # This is the original picture where the diferences will be compared with.
        
        if Picture == 2:    # Make Picture 2 for taking Picture 2 with Led 1 on.
            print("Device%d" %Devices)  #Here to show in the terminal which device the program is trying to detect.
            print("Picture %d"%Picture)  # Extra check for testing if the program comes here
            Devices_Serial = Devices + 1

            #If Correctly done we still have the lock of Serial Write/read
            Writing = ("Main","PicoN%s"% Devices_Serial, "Led1_on")            
            q_Control_Serial_Write.put((1, Writing), block=True, timeout=None)

            time.sleep(0.001)
            #Wait until said back in register it is turned on for certain time (Now it is a hard wait)
            
            cv2.imwrite("Image%s.jpg"%Picture, image)   # Take the second picture with led 1 on. Which is

            #If Correctly done we still have the lock of Serial Write/read
            Writing = ("Main","PicoN%s"% Devices_Serial, "Leds_off") # Turn led 1 of again         
            q_Control_Serial_Write.put((1, Writing), block=True, timeout=None)

         #Again do some other stuff
        if Picture == 3:
            print("Picture %d"%Picture)

            #If Correctly done we still have the lock of Serial Write/read
            Writing = ("Main","PicoN%s"% Devices_Serial, "Led3_on") # Turn led 3 on            
            q_Control_Serial_Write.put((1, Writing), block=True, timeout=None)

            #Wait until said back in register it is turned on for certain time (Now it is a hard wait)
            time.sleep(0.001)
            cv2.imwrite("Image%s.jpg"%Picture, image)

            Writing = ("Main","PicoN%s"% Devices_Serial, "Leds_off") # Turn led 3 of again         
            q_Control_Serial_Write.put((1, Writing), block=True, timeout=None)
            
        if Picture == 4:
            print("Picture %d"%Picture)
            # Take both pictures with the leds.
            Led_1 = cv2.imread("Image2.jpg")
            Led_3 = cv2.imread("Image3.jpg")

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
                Picture = 1

            if Devices == 1: 
                #set data from PZ 2
                Zebro_2_Middle_x = Zebro_Middle_x
                Zebro_2_Middle_y = Zebro_Middle_y
                Direction_Zebro_2 = Direction
                Angle_Zebro_2 = Angle
                Picture = 1

            if Devices == 2: 
                #set data from PZ 3
                Zebro_3_Middle_x = Zebro_Middle_x
                Zebro_3_Middle_y = Zebro_Middle_y
                Direction_Zebro_3 = Direction
                Angle_Zebro_3 = Angle
                Picture = 1

            if Devices == 3: 
                #set data from PZ 4
                Zebro_4_Middle_x = Zebro_Middle_x
                Zebro_4_Middle_y = Zebro_Middle_y
                Direction_Zebro_4 = Direction
                Angle_Zebro_4 = Angle
                Picture = 1

            if Devices == 4: 
                #set data from PZ 5
                Zebro_5_Middle_x = Zebro_Middle_x
                Zebro_5_Middle_y = Zebro_Middle_y
                Direction_Zebro_5 = Direction
                Angle_Zebro_5 = Angle
                Picture = 1

            if Devices == 5: 
                #set data from PZ 6
                Zebro_6_Middle_x = Zebro_Middle_x
                Zebro_6_Middle_y = Zebro_Middle_y
                Direction_Zebro_6 = Direction
                Angle_Zebro_6 = Angle
                Picture = 1

            if Devices == 6: 
                #set data from PZ 7
                Zebro_7_Middle_x = Zebro_Middle_x
                Zebro_7_Middle_y = Zebro_Middle_y
                Direction_Zebro_7 = Direction
                Angle_Zebro_7 = Angle
                Picture = 1

            if Devices == 7: 
                #set data from PZ 8
                Zebro_8_Middle_x = Zebro_Middle_x
                Zebro_8_Middle_y = Zebro_Middle_y
                Direction_Zebro_8 = Direction
                Angle_Zebro_8 = Angle
                Picture = 1

            if Devices == 8: 
                #set data from PZ 9
                Zebro_9_Middle_x = Zebro_Middle_x
                Zebro_9_Middle_y = Zebro_Middle_y
                Direction_Zebro_9 = Direction
                Angle_Zebro_9 = Angle
                Picture = 1

            if Devices == 9: 
                #set data from PZ 10
                Zebro_10_Middle_x = Zebro_Middle_x
                Zebro_10_Middle_y = Zebro_Middle_y
                Direction_Zebro_10 = Direction
                Angle_Zebro_10 = Angle
                Picture = 1

            if Devices == 10: 
                #set data from PZ 11
                Zebro_11_Middle_x = Zebro_Middle_x
                Zebro_11_Middle_y = Zebro_Middle_y
                Direction_Zebro_11 = Direction
                Angle_Zebro_11 = Angle
                Picture = 1

            if Devices == 11: 
                #set data from PZ 12
                Zebro_12_Middle_x = Zebro_Middle_x
                Zebro_12_Middle_y = Zebro_Middle_y
                Direction_Zebro_12 = Direction
                Angle_Zebro_12 = Angle
                Picture = 1

            if Devices == 12: 
                #set data from PZ 13
                Zebro_13_Middle_x = Zebro_Middle_x
                Zebro_13_Middle_y = Zebro_Middle_y
                Direction_Zebro_13 = Direction
                Angle_Zebro_13 = Angle
                Picture = 1

            if Devices == 13: 
                #set data from PZ 14
                Zebro_14_Middle_x = Zebro_Middle_x
                Zebro_14_Middle_y = Zebro_Middle_y
                Direction_Zebro_14 = Direction
                Angle_Zebro_14 = Angle
                Picture = 1

            if Devices == 14: 
                #set data from PZ 15
                Zebro_15_Middle_x = Zebro_Middle_x
                Zebro_15_Middle_y = Zebro_Middle_y
                Direction_Zebro_15 = Direction
                Angle_Zebro_15 = Angle
                Picture = 1

            if Devices == 15: 
                #set data from PZ 16
                Zebro_16_Middle_x = Zebro_Middle_x
                Zebro_16_Middle_y = Zebro_Middle_y
                Direction_Zebro_16 = Direction
                Angle_Zebro_16 = Angle
                Picture = 1

            if Devices == 16: 
                #set data from PZ 17
                Zebro_17_Middle_x = Zebro_Middle_x
                Zebro_17_Middle_y = Zebro_Middle_y
                Direction_Zebro_17 = Direction
                Angle_Zebro_17 = Angle
                Picture = 1

            if Devices == 17: 
                #set data from PZ 18
                Zebro_18_Middle_x = Zebro_Middle_x
                Zebro_18_Middle_y = Zebro_Middle_y
                Direction_Zebro_18 = Direction
                Angle_Zebro_18 = Angle
                Picture = 1

            if Devices == 18: 
                #set data from PZ 19
                Zebro_19_Middle_x = Zebro_Middle_x
                Zebro_19_Middle_y = Zebro_Middle_y
                Direction_Zebro_19 = Direction
                Angle_Zebro_19 = Angle
                Picture = 1

            if Devices == 19: 
                #set data from PZ 20
                Zebro_20_Middle_x = Zebro_Middle_x
                Zebro_20_Middle_y = Zebro_Middle_y
                Direction_Zebro_20 = Direction
                Angle_Zebro_20 = Angle
                Picture = 5
                
            Devices = Devices + 1
                    
        if Picture == 5:
            Devices = 0
            #once every value for every possible Zebro is determind then
            for Zebros in range(20): # total of maximum of 20 Zebro's so 0-19 is 20 Zebro's
                Blocking_Zebro = []   #Here will be the blocking in
                if Zebros == 0:
                    Blocking_Zebro = Block.Block_1(Zebro_1_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_1_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)

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
                        
                    #This is only necceassary when something will be done with this data
                    #if q_Pico_Angle_1.empty() == True:   #if the queue is empty fill it
                    #    q_Pico_Angle_1.put(Angle_Zebro_1)
                    #elif q_Pico_Angle_1.empty() == False: #else empty it before filling it again with the next data.
                    #    q_Pico_Angle_1.mutex.acquire()
                    #    q_Pico_Angle_1.queue.clear()
                    #    q_Pico_Angle_1.all_tasks_done.notify_all()
                    #    q_Pico_Angle_1.unfinished_tasks = 0
                    #    q_Pico_Angle_1.mutex.release()
                    #    q_Pico_Angle_1.put(Angle_Zebro_1)
                        
                    #PicoZebro_1[Zebro_1_Middle_x , Zebro_1_Middle_y, Blocking_Zebro, Direction_Zebro_1, Angle_Zebro_1]

                if Zebros == 1:
                    #in here the first value is the one everything will be compared to.
                    Blocking_Zebro = Block.Block_1(Zebro_2_Middle_x, Zebro_1_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_2_Middle_y, Zebro_1_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_2 = [Zebro_2_Middle_x , Zebro_2_Middle_y, Blocking_Zebro]

                    if q_PicoZebro_2.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_2.put(PicoZebro_2)
                    elif q_PicoZebro_2.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_2.mutex.acquire()
                        q_PicoZebro_2.queue.clear()
                        q_PicoZebro_2.all_tasks_done.notify_all()
                        q_PicoZebro_2.unfinished_tasks = 0
                        q_PicoZebro_2.mutex.release()
                        q_PicoZebro_2.put(PicoZebro_2)

                    if q_Pico_Direction_2.empty() == True:   #if the queue is empty fill it
                        q_Pico_Direction_2.put(Direction_Zebro_2)
                    elif q_Pico_Direction_2.empty() == False: #else empty it before filling it again with the next data.
                        q_Pico_Direction_2.mutex.acquire()
                        q_Pico_Direction_2.queue.clear()
                        q_Pico_Direction_2.all_tasks_done.notify_all()
                        q_Pico_Direction_2.unfinished_tasks = 0
                        q_Pico_Direction_2.mutex.release()
                        q_Pico_Direction_2.put(Direction_Zebro_2)
                    #PicoZebro_2[Zebro_2_Middle_x , Zebro_2_Middle_y, Blocking_Zebro, Direction_Zebro_2, Angle_Zebro_2]
                    

                if Zebros == 2:
                    Blocking_Zebro = Block.Block_1(Zebro_3_Middle_x, Zebro_2_Middle_x, Zebro_1_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_3_Middle_y, Zebro_2_Middle_y, Zebro_1_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_3 = [Zebro_3_Middle_x , Zebro_3_Middle_y, Blocking_Zebro]

                    if q_PicoZebro_3.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_3.put(PicoZebro_3)
                    elif q_PicoZebro_3.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_3.mutex.acquire()
                        q_PicoZebro_3.queue.clear()
                        q_PicoZebro_3.all_tasks_done.notify_all()
                        q_PicoZebro_3.unfinished_tasks = 0
                        q_PicoZebro_3.mutex.release()
                        q_PicoZebro_3.put(PicoZebro_3)

                    if q_Pico_Direction_3.empty() == True:   #if the queue is empty fill it
                        q_Pico_Direction_3.put(Direction_Zebro_3)
                    elif q_Pico_Direction_3.empty() == False: #else empty it before filling it again with the next data.
                        q_Pico_Direction_3.mutex.acquire()
                        q_Pico_Direction_3.queue.clear()
                        q_Pico_Direction_3.all_tasks_done.notify_all()
                        q_Pico_Direction_3.unfinished_tasks = 0
                        q_Pico_Direction_3.mutex.release()
                        q_Pico_Direction_3.put(Direction_Zebro_3)
                    #PicoZebro_3[Zebro_3_Middle_x , Zebro_3_Middle_y, Blocking_Zebro, Direction_Zebro_3, Angle_Zebro_3]

                if Zebros == 3:
                    Blocking_Zebro = Block.Block_1(Zebro_4_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_1_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_4_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_1_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_4 = [Zebro_4_Middle_x , Zebro_4_Middle_y, Blocking_Zebro]

                    if q_PicoZebro_4.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_4.put(PicoZebro_4)
                    elif q_PicoZebro_4.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_4.mutex.acquire()
                        q_PicoZebro_4.queue.clear()
                        q_PicoZebro_4.all_tasks_done.notify_all()
                        q_PicoZebro_4.unfinished_tasks = 0
                        q_PicoZebro_4.mutex.release()
                        q_PicoZebro_4.put(PicoZebro_4)

                    if q_Pico_Direction_4.empty() == True:   #if the queue is empty fill it
                        q_Pico_Direction_4.put(Direction_Zebro_4)
                    elif q_Pico_Direction_4.empty() == False: #else empty it before filling it again with the next data.
                        q_Pico_Direction_4.mutex.acquire()
                        q_Pico_Direction_4.queue.clear()
                        q_Pico_Direction_4.all_tasks_done.notify_all()
                        q_Pico_Direction_4.unfinished_tasks = 0
                        q_Pico_Direction_4.mutex.release()
                        q_Pico_Direction_4.put(Direction_Zebro_4)  
                    #PicoZebro_4[Zebro_4_Middle_x , Zebro_4_Middle_y, Blocking_Zebro, Direction_Zebro_4, Angle_Zebro_4]

                if Zebros == 4:
                    Blocking_Zebro = Block.Block_1(Zebro_5_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_1_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_5_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_1_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_5 = [Zebro_5_Middle_x , Zebro_5_Middle_y, Blocking_Zebro]

                    if q_PicoZebro_5.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_5.put(PicoZebro_5)
                    elif q_PicoZebro_5.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_5.mutex.acquire()
                        q_PicoZebro_5.queue.clear()
                        q_PicoZebro_5.all_tasks_done.notify_all()
                        q_PicoZebro_5.unfinished_tasks = 0
                        q_PicoZebro_5.mutex.release()
                        q_PicoZebro_5.put(PicoZebro_5)

                    if q_Pico_Direction_5.empty() == True:   #if the queue is empty fill it
                        q_Pico_Direction_5.put(Direction_Zebro_5)
                    elif q_Pico_Direction_5.empty() == False: #else empty it before filling it again with the next data.
                        q_Pico_Direction_5.mutex.acquire()
                        q_Pico_Direction_5.queue.clear()
                        q_Pico_Direction_5.all_tasks_done.notify_all()
                        q_Pico_Direction_5.unfinished_tasks = 0
                        q_Pico_Direction_5.mutex.release()
                        q_Pico_Direction_5.put(Direction_Zebro_5)
                    #PicoZebro_5[Zebro_5_Middle_x , Zebro_5_Middle_y, Blocking_Zebro, Direction_Zebro_5, Angle_Zebro_5]

                if Zebros == 5:
                    Blocking_Zebro = Block.Block_1(Zebro_6_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_1_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_6_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_1_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_6 = [Zebro_6_Middle_x , Zebro_6_Middle_y, Blocking_Zebro]
                    
                    if q_PicoZebro_6.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_6.put(PicoZebro_6)
                    elif q_PicoZebro_6.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_6.mutex.acquire()
                        q_PicoZebro_6.queue.clear()
                        q_PicoZebro_6.all_tasks_done.notify_all()
                        q_PicoZebro_6.unfinished_tasks = 0
                        q_PicoZebro_6.mutex.release()
                        q_PicoZebro_6.put(PicoZebro_6)

                    if q_Pico_Direction_6.empty() == True:   #if the queue is empty fill it
                        q_Pico_Direction_6.put(Direction_Zebro_6)
                    elif q_Pico_Direction_6.empty() == False: #else empty it before filling it again with the next data.
                        q_Pico_Direction_6.mutex.acquire()
                        q_Pico_Direction_6.queue.clear()
                        q_Pico_Direction_6.all_tasks_done.notify_all()
                        q_Pico_Direction_6.unfinished_tasks = 0
                        q_Pico_Direction_6.mutex.release()
                        q_Pico_Direction_6.put(Direction_Zebro_6)
                    #PicoZebro_6[Zebro_6_Middle_x , Zebro_6_Middle_y, Blocking_Zebro, Direction_Zebro_6, Angle_Zebro_6]

                if Zebros == 6:
                    Blocking_Zebro = Block.Block_1(Zebro_7_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_1_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_7_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_1_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_7 = [Zebro_7_Middle_x , Zebro_7_Middle_y, Blocking_Zebro]

                    if q_PicoZebro_7.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_7.put(PicoZebro_7)
                    elif q_PicoZebro_7.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_7.mutex.acquire()
                        q_PicoZebro_7.queue.clear()
                        q_PicoZebro_7.all_tasks_done.notify_all()
                        q_PicoZebro_7.unfinished_tasks = 0
                        q_PicoZebro_7.mutex.release()
                        q_PicoZebro_7.put(PicoZebro_7)

                    if q_Pico_Direction_7.empty() == True:   #if the queue is empty fill it
                        q_Pico_Direction_7.put(Direction_Zebro_7)
                    elif q_Pico_Direction_7.empty() == False: #else empty it before filling it again with the next data.
                        q_Pico_Direction_7.mutex.acquire()
                        q_Pico_Direction_7.queue.clear()
                        q_Pico_Direction_7.all_tasks_done.notify_all()
                        q_Pico_Direction_7.unfinished_tasks = 0
                        q_Pico_Direction_7.mutex.release()
                        q_Pico_Direction_7.put(Direction_Zebro_7)
                    #PicoZebro_7[Zebro_7_Middle_x , Zebro_7_Middle_y, Blocking_Zebro, Direction_Zebro_7, Angle_Zebro_7]

                if Zebros == 7:
                    Blocking_Zebro = Block.Block_1(Zebro_8_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_1_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_8_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_1_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_8 = [Zebro_8_Middle_x , Zebro_8_Middle_y, Blocking_Zebro]

                    if q_PicoZebro_8.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_8.put(PicoZebro_8)
                    elif q_PicoZebro_8.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_8.mutex.acquire()
                        q_PicoZebro_8.queue.clear()
                        q_PicoZebro_8.all_tasks_done.notify_all()
                        q_PicoZebro_8.unfinished_tasks = 0
                        q_PicoZebro_8.mutex.release()
                        q_PicoZebro_8.put(PicoZebro_8)

                    if q_Pico_Direction_8.empty() == True:   #if the queue is empty fill it
                        q_Pico_Direction_8.put(Direction_Zebro_8)
                    elif q_Pico_Direction_8.empty() == False: #else empty it before filling it again with the next data.
                        q_Pico_Direction_8.mutex.acquire()
                        q_Pico_Direction_8.queue.clear()
                        q_Pico_Direction_8.all_tasks_done.notify_all()
                        q_Pico_Direction_8.unfinished_tasks = 0
                        q_Pico_Direction_8.mutex.release()
                        q_Pico_Direction_8.put(Direction_Zebro_8)
                    #PicoZebro_8[Zebro_8_Middle_x , Zebro_8_Middle_y, Blocking_Zebro, Direction_Zebro_8, Angle_Zebro_8]

                if Zebros == 8:
                    Blocking_Zebro = Block.Block_1(Zebro_9_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_1_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_9_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_1_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_9 = [Zebro_9_Middle_x , Zebro_9_Middle_y, Blocking_Zebro]

                    if q_PicoZebro_9.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_9.put(PicoZebro_9)
                    elif q_PicoZebro_9.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_9.mutex.acquire()
                        q_PicoZebro_9.queue.clear()
                        q_PicoZebro_9.all_tasks_done.notify_all()
                        q_PicoZebro_9.unfinished_tasks = 0
                        q_PicoZebro_9.mutex.release()
                        q_PicoZebro_9.put(PicoZebro_9)

                    if q_Pico_Direction_9.empty() == True:   #if the queue is empty fill it
                        q_Pico_Direction_9.put(Direction_Zebro_9)
                    elif q_Pico_Direction_9.empty() == False: #else empty it before filling it again with the next data.
                        q_Pico_Direction_9.mutex.acquire()
                        q_Pico_Direction_9.queue.clear()
                        q_Pico_Direction_9.all_tasks_done.notify_all()
                        q_Pico_Direction_9.unfinished_tasks = 0
                        q_Pico_Direction_9.mutex.release()
                        q_Pico_Direction_9.put(Direction_Zebro_9)
                    #PicoZebro_9[Zebro_9_Middle_x , Zebro_9_Middle_y, Blocking_Zebro, Direction_Zebro_9, Angle_Zebro_9]

                if Zebros == 9:
                    Blocking_Zebro = Block.Block_1(Zebro_10_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_1_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_10_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_1_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_10 = [Zebro_10_Middle_x , Zebro_10_Middle_y, Blocking_Zebro]
                    
                    if q_PicoZebro_10.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_10.put(PicoZebro_10)
                    elif q_PicoZebro_10.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_10.mutex.acquire()
                        q_PicoZebro_10.queue.clear()
                        q_PicoZebro_10.all_tasks_done.notify_all()
                        q_PicoZebro_10.unfinished_tasks = 0
                        q_PicoZebro_10.mutex.release()
                        q_PicoZebro_10.put(PicoZebro_10)

                    if q_Pico_Direction_10.empty() == True:   #if the queue is empty fill it
                        q_Pico_Direction_10.put(Direction_Zebro_10)
                    elif q_Pico_Direction_10.empty() == False: #else empty it before filling it again with the next data.
                        q_Pico_Direction_10.mutex.acquire()
                        q_Pico_Direction_10.queue.clear()
                        q_Pico_Direction_10.all_tasks_done.notify_all()
                        q_Pico_Direction_10.unfinished_tasks = 0
                        q_Pico_Direction_10.mutex.release()
                        q_Pico_Direction_10.put(Direction_Zebro_10)                        
                    #PicoZebro_10[Zebro_10_Middle_x , Zebro_10_Middle_y, Blocking_Zebro, Direction_Zebro_10, Angle_Zebro_10]

                if Zebros == 10:
                    Blocking_Zebro = Block.Block_1(Zebro_11_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_1_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_11_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_1_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_11 = [Zebro_11_Middle_x , Zebro_11_Middle_y, Blocking_Zebro]

                    if q_PicoZebro_11.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_11.put(PicoZebro_11)
                    elif q_PicoZebro_11.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_11.mutex.acquire()
                        q_PicoZebro_11.queue.clear()
                        q_PicoZebro_11.all_tasks_done.notify_all()
                        q_PicoZebro_11.unfinished_tasks = 0
                        q_PicoZebro_11.mutex.release()
                        q_PicoZebro_11.put(PicoZebro_11)

                    if q_Pico_Direction_11.empty() == True:   #if the queue is empty fill it
                        q_Pico_Direction_11.put(Direction_Zebro_11)
                    elif q_Pico_Direction_11.empty() == False: #else empty it before filling it again with the next data.
                        q_Pico_Direction_11.mutex.acquire()
                        q_Pico_Direction_11.queue.clear()
                        q_Pico_Direction_11.all_tasks_done.notify_all()
                        q_Pico_Direction_11.unfinished_tasks = 0
                        q_Pico_Direction_11.mutex.release()
                        q_Pico_Direction_11.put(Direction_Zebro_11)
                    #PicoZebro_11[Zebro_11_Middle_x , Zebro_11_Middle_y, Blocking_Zebro, Direction_Zebro_11, Angle_Zebro_11]

                if Zebros == 11:
                    Blocking_Zebro = Block.Block_1(Zebro_12_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_1_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_12_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_1_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_12 = [Zebro_12_Middle_x , Zebro_12_Middle_y, Blocking_Zebro]

                    if q_PicoZebro_12.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_12.put(PicoZebro_12)
                    elif q_PicoZebro_12.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_12.mutex.acquire()
                        q_PicoZebro_12.queue.clear()
                        q_PicoZebro_12.all_tasks_done.notify_all()
                        q_PicoZebro_12.unfinished_tasks = 0
                        q_PicoZebro_12.mutex.release()
                        q_PicoZebro_12.put(PicoZebro_12)

                    if q_Pico_Direction_12.empty() == True:   #if the queue is empty fill it
                        q_Pico_Direction_12.put(Direction_Zebro_12)
                    elif q_Pico_Direction_12.empty() == False: #else empty it before filling it again with the next data.
                        q_Pico_Direction_12.mutex.acquire()
                        q_Pico_Direction_12.queue.clear()
                        q_Pico_Direction_12.all_tasks_done.notify_all()
                        q_Pico_Direction_12.unfinished_tasks = 0
                        q_Pico_Direction_12.mutex.release()
                        q_Pico_Direction_12.put(Direction_Zebro_12)                        
                    #PicoZebro_12[Zebro_12_Middle_x , Zebro_12_Middle_y, Blocking_Zebro, Direction_Zebro_12, Angle_Zebro_12]

                if Zebros == 12:
                    Blocking_Zebro = Block.Block_1(Zebro_13_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_1_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_13_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_1_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_13 = [Zebro_13_Middle_x , Zebro_13_Middle_y, Blocking_Zebro]
                    
                    if q_PicoZebro_13.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_13.put(PicoZebro_13)
                    elif q_PicoZebro_13.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_13.mutex.acquire()
                        q_PicoZebro_13.queue.clear()
                        q_PicoZebro_13.all_tasks_done.notify_all()
                        q_PicoZebro_13.unfinished_tasks = 0
                        q_PicoZebro_13.mutex.release()
                        q_PicoZebro_13.put(PicoZebro_13)

                    if q_Pico_Direction_13.empty() == True:   #if the queue is empty fill it
                        q_Pico_Direction_13.put(Direction_Zebro_13)
                    elif q_Pico_Direction_13.empty() == False: #else empty it before filling it again with the next data.
                        q_Pico_Direction_13.mutex.acquire()
                        q_Pico_Direction_13.queue.clear()
                        q_Pico_Direction_13.all_tasks_done.notify_all()
                        q_Pico_Direction_13.unfinished_tasks = 0
                        q_Pico_Direction_13.mutex.release()
                        q_Pico_Direction_13.put(Direction_Zebro_13)
                    #PicoZebro_13[Zebro_13_Middle_x , Zebro_13_Middle_y, Blocking_Zebro, Direction_Zebro_13, Angle_Zebro_13]

                if Zebros == 13:
                    Blocking_Zebro = Block.Block_1(Zebro_14_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_1_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_14_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_1_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_14 = [Zebro_14_Middle_x , Zebro_14_Middle_y, Blocking_Zebro]
                    
                    if q_PicoZebro_14.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_14.put(PicoZebro_14)
                    elif q_PicoZebro_14.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_14.mutex.acquire()
                        q_PicoZebro_14.queue.clear()
                        q_PicoZebro_14.all_tasks_done.notify_all()
                        q_PicoZebro_14.unfinished_tasks = 0
                        q_PicoZebro_14.mutex.release()
                        q_PicoZebro_14.put(PicoZebro_14)

                    if q_Pico_Direction_14.empty() == True:   #if the queue is empty fill it
                        q_Pico_Direction_14.put(Direction_Zebro_14)
                    elif q_Pico_Direction_14.empty() == False: #else empty it before filling it again with the next data.
                        q_Pico_Direction_14.mutex.acquire()
                        q_Pico_Direction_14.queue.clear()
                        q_Pico_Direction_14.all_tasks_done.notify_all()
                        q_Pico_Direction_14.unfinished_tasks = 0
                        q_Pico_Direction_14.mutex.release()
                        q_Pico_Direction_14.put(Direction_Zebro_14)           
                    #PicoZebro_14[Zebro_14_Middle_x , Zebro_14_Middle_y, Blocking_Zebro, Direction_Zebro_14, Angle_Zebro_14]

                if Zebros == 14:
                    Blocking_Zebro = Block.Block_1(Zebro_15_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_1_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_15_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_1_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_15 = [Zebro_15_Middle_x , Zebro_15_Middle_y, Blocking_Zebro]

                    if q_PicoZebro_15.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_15.put(PicoZebro_15)
                    elif q_PicoZebro_15.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_15.mutex.acquire()
                        q_PicoZebro_15.queue.clear()
                        q_PicoZebro_15.all_tasks_done.notify_all()
                        q_PicoZebro_15.unfinished_tasks = 0
                        q_PicoZebro_15.mutex.release()
                        q_PicoZebro_15.put(PicoZebro_15)

                    if q_Pico_Direction_15.empty() == True:   #if the queue is empty fill it
                        q_Pico_Direction_15.put(Direction_Zebro_15)
                    elif q_Pico_Direction_15.empty() == False: #else empty it before filling it again with the next data.
                        q_Pico_Direction_15.mutex.acquire()
                        q_Pico_Direction_15.queue.clear()
                        q_Pico_Direction_15.all_tasks_done.notify_all()
                        q_Pico_Direction_15.unfinished_tasks = 0
                        q_Pico_Direction_15.mutex.release()
                        q_Pico_Direction_15.put(Direction_Zebro_15)  
                    #PicoZebro_15[Zebro_15_Middle_x , Zebro_15_Middle_y, Blocking_Zebro, Direction_Zebro_15, Angle_Zebro_15]

                if Zebros == 15:
                    Blocking_Zebro = Block.Block_1(Zebro_16_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_1_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_16_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_1_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_16 = [Zebro_16_Middle_x , Zebro_16_Middle_y, Blocking_Zebro]

                    if q_PicoZebro_16.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_16.put(PicoZebro_16)
                    elif q_PicoZebro_16.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_16.mutex.acquire()
                        q_PicoZebro_16.queue.clear()
                        q_PicoZebro_16.all_tasks_done.notify_all()
                        q_PicoZebro_16.unfinished_tasks = 0
                        q_PicoZebro_16.mutex.release()
                        q_PicoZebro_16.put(PicoZebro_16)

                    if q_Pico_Direction_16.empty() == True:   #if the queue is empty fill it
                        q_Pico_Direction_16.put(Direction_Zebro_16)
                    elif q_Pico_Direction_16.empty() == False: #else empty it before filling it again with the next data.
                        q_Pico_Direction_16.mutex.acquire()
                        q_Pico_Direction_16.queue.clear()
                        q_Pico_Direction_16.all_tasks_done.notify_all()
                        q_Pico_Direction_16.unfinished_tasks = 0
                        q_Pico_Direction_16.mutex.release()
                        q_Pico_Direction_16.put(Direction_Zebro_16)     
                    #PicoZebro_16[Zebro_16_Middle_x , Zebro_16_Middle_y, Blocking_Zebro, Direction_Zebro_16, Angle_Zebro_16]

                if Zebros == 16:
                    Blocking_Zebro = Block.Block_1(Zebro_17_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_1_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_17_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_1_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_17 = [Zebro_17_Middle_x , Zebro_17_Middle_y, Blocking_Zebro]

                    if q_PicoZebro_17.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_17.put(PicoZebro_17)
                    elif q_PicoZebro_17.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_17.mutex.acquire()
                        q_PicoZebro_17.queue.clear()
                        q_PicoZebro_17.all_tasks_done.notify_all()
                        q_PicoZebro_17.unfinished_tasks = 0
                        q_PicoZebro_17.mutex.release()
                        q_PicoZebro_17.put(PicoZebro_17)

                    if q_Pico_Direction_17.empty() == True:   #if the queue is empty fill it
                        q_Pico_Direction_17.put(Direction_Zebro_17)
                    elif q_Pico_Direction_17.empty() == False: #else empty it before filling it again with the next data.
                        q_Pico_Direction_17.mutex.acquire()
                        q_Pico_Direction_17.queue.clear()
                        q_Pico_Direction_17.all_tasks_done.notify_all()
                        q_Pico_Direction_17.unfinished_tasks = 0
                        q_Pico_Direction_17.mutex.release()
                        q_Pico_Direction_17.put(Direction_Zebro_17)
                    #PicoZebro_17[Zebro_17_Middle_x , Zebro_17_Middle_y, Blocking_Zebro, Direction_Zebro_17, Angle_Zebro_17]

                if Zebros == 17:
                    Blocking_Zebro = Block.Block_1(Zebro_18_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_1_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_18_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_1_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_18 = [Zebro_18_Middle_x , Zebro_18_Middle_y, Blocking_Zebro]

                    if q_PicoZebro_18.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_18.put(PicoZebro_18)
                    elif q_PicoZebro_18.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_18.mutex.acquire()
                        q_PicoZebro_18.queue.clear()
                        q_PicoZebro_18.all_tasks_done.notify_all()
                        q_PicoZebro_18.unfinished_tasks = 0
                        q_PicoZebro_18.mutex.release()
                        q_PicoZebro_18.put(PicoZebro_18)

                    if q_Pico_Direction_18.empty() == True:   #if the queue is empty fill it
                        q_Pico_Direction_18.put(Direction_Zebro_18)
                    elif q_Pico_Direction_18.empty() == False: #else empty it before filling it again with the next data.
                        q_Pico_Direction_18.mutex.acquire()
                        q_Pico_Direction_18.queue.clear()
                        q_Pico_Direction_18.all_tasks_done.notify_all()
                        q_Pico_Direction_18.unfinished_tasks = 0
                        q_Pico_Direction_18.mutex.release()
                        q_Pico_Direction_18.put(Direction_Zebro_18)
                    #PicoZebro_18[Zebro_18_Middle_x , Zebro_18_Middle_y, Blocking_Zebro, Direction_Zebro_18, Angle_Zebro_18]

                if Zebros == 18:
                    Blocking_Zebro = Block.Block_1(Zebro_19_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_1_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_19_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_1_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_19 = [Zebro_19_Middle_x , Zebro_19_Middle_y, Blocking_Zebro]

                    if q_PicoZebro_19.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_19.put(PicoZebro_19)
                    elif q_PicoZebro_19.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_19.mutex.acquire()
                        q_PicoZebro_19.queue.clear()
                        q_PicoZebro_19.all_tasks_done.notify_all()
                        q_PicoZebro_19.unfinished_tasks = 0
                        q_PicoZebro_19.mutex.release()
                        q_PicoZebro_19.put(PicoZebro_19)

                    if q_Pico_Direction_19.empty() == True:   #if the queue is empty fill it
                        q_Pico_Direction_19.put(Direction_Zebro_19)
                    elif q_Pico_Direction_19.empty() == False: #else empty it before filling it again with the next data.
                        q_Pico_Direction_19.mutex.acquire()
                        q_Pico_Direction_19.queue.clear()
                        q_Pico_Direction_19.all_tasks_done.notify_all()
                        q_Pico_Direction_19.unfinished_tasks = 0
                        q_Pico_Direction_19.mutex.release()
                        q_Pico_Direction_19.put(Direction_Zebro_19)
                    #PicoZebro_19[Zebro_19_Middle_x , Zebro_19_Middle_y, Blocking_Zebro, Direction_Zebro_19, Angle_Zebro_19]

                if Zebros == 19:
                    Blocking_Zebro = Block.Block_1(Zebro_20_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_1_Middle_x,
                                                   Zebro_20_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_1_Middle_y)
                    PicoZebro_20 = [Zebro_20_Middle_x , Zebro_20_Middle_y, Blocking_Zebro]

                    if q_PicoZebro_20.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_20.put(PicoZebro_20)
                    elif q_PicoZebro_20.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_20.mutex.acquire()
                        q_PicoZebro_20.queue.clear()
                        q_PicoZebro_20.all_tasks_done.notify_all()
                        q_PicoZebro_20.unfinished_tasks = 0
                        q_PicoZebro_20.mutex.release()
                        q_PicoZebro_20.put(PicoZebro_20)

                    if q_Pico_Direction_20.empty() == True:   #if the queue is empty fill it
                        q_Pico_Direction_20.put(Direction_Zebro_20)
                    elif q_Pico_Direction_20.empty() == False: #else empty it before filling it again with the next data.
                        q_Pico_Direction_20.mutex.acquire()
                        q_Pico_Direction_20.queue.clear()
                        q_Pico_Direction_20.all_tasks_done.notify_all()
                        q_Pico_Direction_20.unfinished_tasks = 0
                        q_Pico_Direction_20.mutex.release()
                        q_Pico_Direction_20.put(Direction_Zebro_20)

                        
                    #PicoZebro_20[Zebro_20_Middle_x , Zebro_20_Middle_y, Blocking_Zebro, Direction_Zebro_20, Angle_Zebro_20]
                    print(PicoZebro_1)
                    print(Direction_Zebro_1)
                    Picture = 6
                    Writing = ("Main","Global", "Leds_off")            
                    q_Control_Serial_Write.put((1, Writing), block=True, timeout=None) # Turn leds of again

                    Writing = ("Main","Global", "Led1_on")            
                    q_Control_Serial_Write.put((1, Writing), block=True, timeout=None) # Turn led 1 on again

                    print("MAIN RELEASE SERIAL LOCK")
                    #Serial_Lock.mutex.release()
                    #Serial_Lock.release()
                    
                    if q_Control_Uart_Main.empty() == False: #empty it so the pico can write again
                        q_Control_Uart_Main.mutex.acquire()
                        q_Control_Uart_Main.queue.clear()
                        q_Control_Uart_Main.all_tasks_done.notify_all()
                        q_Control_Uart_Main.unfinished_tasks = 0
                        q_Control_Uart_Main.mutex.release()
                        
                    # Release Condition Serial Write. (Now movement can start.)
                    Picture_1_start_time = time.time() # Testing Function for how long a part of a code takes.
                    print(Picture_1_start_time)
        if Picture == 6:
            #Global Command Turn all leds off
            #Glabal Command turn all led 1 on.  #Do this once
            #Wait untill this is done.
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Take a gray picture
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
                print("There are no zebros")
                time.sleep(1)
             
            # loop over the contours
            for (i, c) in enumerate(cnts):
                # draw the bright spot on the image
                (x, y, w, h) = cv2.boundingRect(c)
                x_compare_1 = x + 80
                y_compare_1 = y + 50
                x_compare_2 = x - 80
                y_compare_2 = y - 50
                if (x_compare_2 < Zebro_1_Middle_x < x_compare_1) and (y_compare_2 < Zebro_1_Middle_y < y_compare_1):
                    cv2.putText(image, "#1", (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                    Zebro_1_Middle_x = x
                    Zebro_1_Middle_y = y
                    print("This is Zebro 1")
                elif (x_compare_2 < Zebro_2_Middle_x < x_compare_1) and (y_compare_2 < Zebro_2_Middle_y < y_compare_1):
                    Zebro_2_Middle_x = x
                    Zebro_2_Middle_y = y
                    print("This is Zebro 2")
                    cv2.putText(image, "#2", (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                elif (x_compare_2 < Zebro_3_Middle_x < x_compare_1) and (y_compare_2 < Zebro_3_Middle_y < y_compare_1):
                    Zebro_3_Middle_x = x
                    Zebro_3_Middle_y = y
                    print("This is Zebro 3")
                    cv2.putText(image, "#3", (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                elif (x_compare_2 < Zebro_4_Middle_x < x_compare_1) and (y_compare_2 < Zebro_4_Middle_y < y_compare_1):
                    Zebro_4_Middle_x = x
                    Zebro_4_Middle_y = y
                    print("This is Zebro 4")
                    cv2.putText(image, "#4", (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                elif (x_compare_2 < Zebro_5_Middle_x < x_compare_1) and (y_compare_2 < Zebro_5_Middle_y < y_compare_1):
                    Zebro_5_Middle_x = x
                    Zebro_5_Middle_y = y
                    print("This is Zebro 5")
                    cv2.putText(image, "#5", (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                elif (x_compare_2 < Zebro_6_Middle_x < x_compare_1) and (y_compare_2 < Zebro_6_Middle_y < y_compare_1):
                    Zebro_6_Middle_x = x
                    Zebro_6_Middle_y = y
                    print("This is Zebro 6")
                    cv2.putText(image, "#6", (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                elif (x_compare_2 < Zebro_7_Middle_x < x_compare_1) and (y_compare_2 < Zebro_7_Middle_y < y_compare_1):
                    Zebro_7_Middle_x = x
                    Zebro_7_Middle_y = y
                    print("This is Zebro 7")
                    cv2.putText(image, "#7", (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                elif (x_compare_2 < Zebro_8_Middle_x < x_compare_1) and (y_compare_2 < Zebro_8_Middle_y < y_compare_1):
                    Zebro_8_Middle_x = x
                    Zebro_8_Middle_y = y
                    print("This is Zebro 8")
                    cv2.putText(image, "#8", (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                elif (x_compare_2 < Zebro_9_Middle_x < x_compare_1) and (y_compare_2 < Zebro_9_Middle_y < y_compare_1):
                    Zebro_9_Middle_x = x
                    Zebro_9_Middle_y = y
                    print("This is Zebro 9")
                    cv2.putText(image, "#9", (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                elif (x_compare_2 < Zebro_10_Middle_x < x_compare_1) and (y_compare_2 < Zebro_10_Middle_y < y_compare_1):
                    Zebro_10_Middle_x = x
                    Zebro_10_Middle_y = y
                    print("This is Zebro 10")
                    cv2.putText(image, "#10", (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                elif (x_compare_2 < Zebro_11_Middle_x < x_compare_1) and (y_compare_2 < Zebro_11_Middle_y < y_compare_1):
                    Zebro_11_Middle_x = x
                    Zebro_11_Middle_y = y
                    print("This is Zebro 11")
                    cv2.putText(image, "#11", (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                elif (x_compare_2 < Zebro_12_Middle_x < x_compare_1) and (y_compare_2 < Zebro_12_Middle_y < y_compare_1):
                    Zebro_12_Middle_x = x
                    Zebro_12_Middle_y = y
                    print("This is Zebro 12")
                    cv2.putText(image, "#12", (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                elif (x_compare_2 < Zebro_13_Middle_x < x_compare_1) and (y_compare_2 < Zebro_13_Middle_y < y_compare_1):
                    Zebro_13_Middle_x = x
                    Zebro_13_Middle_y = y
                    print("This is Zebro 13")
                    cv2.putText(image, "#13", (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                elif (x_compare_2 < Zebro_14_Middle_x < x_compare_1) and (y_compare_2 < Zebro_14_Middle_y < y_compare_1):
                    Zebro_14_Middle_x = x
                    Zebro_14_Middle_y = y
                    print("This is Zebro 14")
                    cv2.putText(image, "#14", (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                elif (x_compare_2 < Zebro_15_Middle_x < x_compare_1) and (y_compare_2 < Zebro_15_Middle_y < y_compare_1):
                    Zebro_15_Middle_x = x
                    Zebro_15_Middle_y = y
                    print("This is Zebro 15")
                    cv2.putText(image, "#15", (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                elif (x_compare_2 < Zebro_16_Middle_x < x_compare_1) and (y_compare_2 < Zebro_16_Middle_y < y_compare_1):
                    Zebro_16_Middle_x = x
                    Zebro_16_Middle_y = y
                    print("This is Zebro 16")
                    cv2.putText(image, "#16", (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                elif (x_compare_2 < Zebro_17_Middle_x < x_compare_1) and (y_compare_2 < Zebro_17_Middle_y < y_compare_1):
                    Zebro_17_Middle_x = x
                    Zebro_17_Middle_y = y
                    print("This is Zebro 17")
                    cv2.putText(image, "#17", (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                elif (x_compare_2 < Zebro_18_Middle_x < x_compare_1) and (y_compare_2 < Zebro_18_Middle_y < y_compare_1):
                    Zebro_18_Middle_x = x
                    Zebro_18_Middle_y = y
                    print("This is Zebro 18")
                    cv2.putText(image, "#18", (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                elif (x_compare_2 < Zebro_19_Middle_x < x_compare_1) and (y_compare_2 < Zebro_19_Middle_y < y_compare_1):
                    Zebro_19_Middle_x = x
                    Zebro_19_Middle_y = y
                    print("This is Zebro 19")
                    cv2.putText(image, "#19", (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                elif (x_compare_2 < Zebro_20_Middle_x < x_compare_1) and (y_compare_2 < Zebro_20_Middle_y < y_compare_1):
                    Zebro_20_Middle_x = x
                    Zebro_20_Middle_y = y
                    print("This is Zebro 20")
                    cv2.putText(image, "#20", (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
            for Zebros in range(20):
                Blocking_Zebro = []   #Here will be the blocking in
                if Zebros == 0:
                    Blocking_Zebro = Block.Block_1(Zebro_1_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_1_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
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

                if Zebros == 1:
                    #in here the first value is the one everything will be compared to.
                    Blocking_Zebro = Block.Block_1(Zebro_2_Middle_x, Zebro_1_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_2_Middle_y, Zebro_1_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_2 = [Zebro_2_Middle_x , Zebro_2_Middle_y, Blocking_Zebro]
                    
                    if q_PicoZebro_2.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_2.put(PicoZebro_2)
                    elif q_PicoZebro_2.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_2.mutex.acquire()
                        q_PicoZebro_2.queue.clear()
                        q_PicoZebro_2.all_tasks_done.notify_all()
                        q_PicoZebro_2.unfinished_tasks = 0
                        q_PicoZebro_2.mutex.release()
                        q_PicoZebro_2.put(PicoZebro_2)

                if Zebros == 2:
                    Blocking_Zebro = Block.Block_1(Zebro_3_Middle_x, Zebro_2_Middle_x, Zebro_1_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_3_Middle_y, Zebro_2_Middle_y, Zebro_1_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_3 = [Zebro_3_Middle_x , Zebro_3_Middle_y, Blocking_Zebro]
                    
                    if q_PicoZebro_3.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_3.put(PicoZebro_3)
                    elif q_PicoZebro_3.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_3.mutex.acquire()
                        q_PicoZebro_3.queue.clear()
                        q_PicoZebro_3.all_tasks_done.notify_all()
                        q_PicoZebro_3.unfinished_tasks = 0
                        q_PicoZebro_3.mutex.release()
                        q_PicoZebro_3.put(PicoZebro_3)

                if Zebros == 3:
                    Blocking_Zebro = Block.Block_1(Zebro_4_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_1_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_4_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_1_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_4 = [Zebro_4_Middle_x , Zebro_4_Middle_y, Blocking_Zebro]
                    
                    if q_PicoZebro_4.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_4.put(PicoZebro_4)
                    elif q_PicoZebro_4.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_4.mutex.acquire()
                        q_PicoZebro_4.queue.clear()
                        q_PicoZebro_4.all_tasks_done.notify_all()
                        q_PicoZebro_4.unfinished_tasks = 0
                        q_PicoZebro_4.mutex.release()
                        q_PicoZebro_4.put(PicoZebro_4)

                if Zebros == 4:
                    Blocking_Zebro = Block.Block_1(Zebro_5_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_1_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_5_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_1_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_5 = [Zebro_5_Middle_x , Zebro_5_Middle_y, Blocking_Zebro]
                    
                    if q_PicoZebro_5.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_5.put(PicoZebro_5)
                    elif q_PicoZebro_5.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_5.mutex.acquire()
                        q_PicoZebro_5.queue.clear()
                        q_PicoZebro_5.all_tasks_done.notify_all()
                        q_PicoZebro_5.unfinished_tasks = 0
                        q_PicoZebro_5.mutex.release()
                        q_PicoZebro_5.put(PicoZebro_5)

                if Zebros == 5:
                    Blocking_Zebro = Block.Block_1(Zebro_6_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_1_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_6_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_1_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_6 = [Zebro_6_Middle_x , Zebro_6_Middle_y, Blocking_Zebro]
                    
                    if q_PicoZebro_6.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_6.put(PicoZebro_6)
                    elif q_PicoZebro_6.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_6.mutex.acquire()
                        q_PicoZebro_6.queue.clear()
                        q_PicoZebro_6.all_tasks_done.notify_all()
                        q_PicoZebro_6.unfinished_tasks = 0
                        q_PicoZebro_6.mutex.release()
                        q_PicoZebro_6.put(PicoZebro_6)

                if Zebros == 6:
                    Blocking_Zebro = Block.Block_1(Zebro_7_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_1_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_7_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_1_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_7 = [Zebro_7_Middle_x , Zebro_7_Middle_y, Blocking_Zebro]
                    
                    if q_PicoZebro_7.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_7.put(PicoZebro_7)
                    elif q_PicoZebro_7.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_7.mutex.acquire()
                        q_PicoZebro_7.queue.clear()
                        q_PicoZebro_7.all_tasks_done.notify_all()
                        q_PicoZebro_7.unfinished_tasks = 0
                        q_PicoZebro_7.mutex.release()
                        q_PicoZebro_7.put(PicoZebro_7)

                if Zebros == 7:
                    Blocking_Zebro = Block.Block_1(Zebro_8_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_1_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_8_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_1_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_8 = [Zebro_8_Middle_x , Zebro_8_Middle_y, Blocking_Zebro]
                    
                    if q_PicoZebro_8.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_8.put(PicoZebro_8)
                    elif q_PicoZebro_8.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_8.mutex.acquire()
                        q_PicoZebro_8.queue.clear()
                        q_PicoZebro_8.all_tasks_done.notify_all()
                        q_PicoZebro_8.unfinished_tasks = 0
                        q_PicoZebro_8.mutex.release()
                        q_PicoZebro_8.put(PicoZebro_8)

                if Zebros == 8:
                    Blocking_Zebro = Block.Block_1(Zebro_9_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_1_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_9_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_1_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_9 = [Zebro_9_Middle_x , Zebro_9_Middle_y, Blocking_Zebro]
                    
                    if q_PicoZebro_9.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_9.put(PicoZebro_9)
                    elif q_PicoZebro_9.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_9.mutex.acquire()
                        q_PicoZebro_9.queue.clear()
                        q_PicoZebro_9.all_tasks_done.notify_all()
                        q_PicoZebro_9.unfinished_tasks = 0
                        q_PicoZebro_9.mutex.release()
                        q_PicoZebro_9.put(PicoZebro_9)

                if Zebros == 9:
                    Blocking_Zebro = Block.Block_1(Zebro_10_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_1_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_10_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_1_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_10 = [Zebro_10_Middle_x , Zebro_10_Middle_y, Blocking_Zebro]
                    
                    if q_PicoZebro_10.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_10.put(PicoZebro_10)
                    elif q_PicoZebro_10.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_10.mutex.acquire()
                        q_PicoZebro_10.queue.clear()
                        q_PicoZebro_10.all_tasks_done.notify_all()
                        q_PicoZebro_10.unfinished_tasks = 0
                        q_PicoZebro_10.mutex.release()
                        q_PicoZebro_10.put(PicoZebro_10)

                if Zebros == 10:
                    Blocking_Zebro = Block.Block_1(Zebro_11_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_1_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_11_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_1_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_11 = [Zebro_11_Middle_x , Zebro_11_Middle_y, Blocking_Zebro]
                    
                    if q_PicoZebro_11.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_11.put(PicoZebro_11)
                    elif q_PicoZebro_11.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_11.mutex.acquire()
                        q_PicoZebro_11.queue.clear()
                        q_PicoZebro_11.all_tasks_done.notify_all()
                        q_PicoZebro_11.unfinished_tasks = 0
                        q_PicoZebro_11.mutex.release()
                        q_PicoZebro_11.put(PicoZebro_11)

                if Zebros == 11:
                    Blocking_Zebro = Block.Block_1(Zebro_12_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_1_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_12_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_1_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_12 = [Zebro_12_Middle_x , Zebro_12_Middle_y, Blocking_Zebro]
                    
                    if q_PicoZebro_12.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_12.put(PicoZebro_12)
                    elif q_PicoZebro_12.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_12.mutex.acquire()
                        q_PicoZebro_12.queue.clear()
                        q_PicoZebro_12.all_tasks_done.notify_all()
                        q_PicoZebro_12.unfinished_tasks = 0
                        q_PicoZebro_12.mutex.release()
                        q_PicoZebro_12.put(PicoZebro_12)

                if Zebros == 12:
                    Blocking_Zebro = Block.Block_1(Zebro_13_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_1_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_13_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_1_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_13 = [Zebro_13_Middle_x , Zebro_13_Middle_y, Blocking_Zebro]
                    
                    if q_PicoZebro_13.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_13.put(PicoZebro_13)
                    elif q_PicoZebro_13.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_13.mutex.acquire()
                        q_PicoZebro_13.queue.clear()
                        q_PicoZebro_13.all_tasks_done.notify_all()
                        q_PicoZebro_13.unfinished_tasks = 0
                        q_PicoZebro_13.mutex.release()
                        q_PicoZebro_13.put(PicoZebro_13)

                if Zebros == 13:
                    Blocking_Zebro = Block.Block_1(Zebro_14_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_1_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_14_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_1_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_14 = [Zebro_14_Middle_x , Zebro_14_Middle_y, Blocking_Zebro]
                    
                    if q_PicoZebro_14.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_14.put(PicoZebro_14)
                    elif q_PicoZebro_14.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_14.mutex.acquire()
                        q_PicoZebro_14.queue.clear()
                        q_PicoZebro_14.all_tasks_done.notify_all()
                        q_PicoZebro_14.unfinished_tasks = 0
                        q_PicoZebro_14.mutex.release()
                        q_PicoZebro_14.put(PicoZebro_14)

                if Zebros == 14:
                    Blocking_Zebro = Block.Block_1(Zebro_15_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_1_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_15_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_1_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_15 = [Zebro_15_Middle_x , Zebro_15_Middle_y, Blocking_Zebro]
                    
                    if q_PicoZebro_15.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_15.put(PicoZebro_15)
                    elif q_PicoZebro_15.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_15.mutex.acquire()
                        q_PicoZebro_15.queue.clear()
                        q_PicoZebro_15.all_tasks_done.notify_all()
                        q_PicoZebro_15.unfinished_tasks = 0
                        q_PicoZebro_15.mutex.release()
                        q_PicoZebro_15.put(PicoZebro_15)

                if Zebros == 15:
                    Blocking_Zebro = Block.Block_1(Zebro_16_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_1_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_16_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_1_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_16 = [Zebro_16_Middle_x , Zebro_16_Middle_y, Blocking_Zebro]
                    
                    if q_PicoZebro_16.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_16.put(PicoZebro_16)
                    elif q_PicoZebro_16.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_16.mutex.acquire()
                        q_PicoZebro_16.queue.clear()
                        q_PicoZebro_16.all_tasks_done.notify_all()
                        q_PicoZebro_16.unfinished_tasks = 0
                        q_PicoZebro_16.mutex.release()
                        q_PicoZebro_16.put(PicoZebro_16)

                if Zebros == 16:
                    Blocking_Zebro = Block.Block_1(Zebro_17_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_1_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_17_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_1_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_17 = [Zebro_17_Middle_x , Zebro_17_Middle_y, Blocking_Zebro]
                    
                    if q_PicoZebro_17.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_17.put(PicoZebro_17)
                    elif q_PicoZebro_17.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_17.mutex.acquire()
                        q_PicoZebro_17.queue.clear()
                        q_PicoZebro_17.all_tasks_done.notify_all()
                        q_PicoZebro_17.unfinished_tasks = 0
                        q_PicoZebro_17.mutex.release()
                        q_PicoZebro_17.put(PicoZebro_17)

                if Zebros == 17:
                    Blocking_Zebro = Block.Block_1(Zebro_18_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_1_Middle_x, Zebro_19_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_18_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_1_Middle_y, Zebro_19_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_18 = [Zebro_18_Middle_x , Zebro_18_Middle_y, Blocking_Zebro]
                    
                    if q_PicoZebro_18.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_18.put(PicoZebro_18)
                    elif q_PicoZebro_18.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_18.mutex.acquire()
                        q_PicoZebro_18.queue.clear()
                        q_PicoZebro_18.all_tasks_done.notify_all()
                        q_PicoZebro_18.unfinished_tasks = 0
                        q_PicoZebro_18.mutex.release()
                        q_PicoZebro_18.put(PicoZebro_18)

                if Zebros == 18:
                    Blocking_Zebro = Block.Block_1(Zebro_19_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_1_Middle_x, Zebro_20_Middle_x,
                                                   Zebro_19_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_1_Middle_y, Zebro_20_Middle_y)
                    PicoZebro_19 = [Zebro_19_Middle_x , Zebro_19_Middle_y, Blocking_Zebro]
                    
                    if q_PicoZebro_19.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_19.put(PicoZebro_19)
                    elif q_PicoZebro_19.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_19.mutex.acquire()
                        q_PicoZebro_19.queue.clear()
                        q_PicoZebro_19.all_tasks_done.notify_all()
                        q_PicoZebro_19.unfinished_tasks = 0
                        q_PicoZebro_19.mutex.release()
                        q_PicoZebro_19.put(PicoZebro_19)

                if Zebros == 19:
                    Blocking_Zebro = Block.Block_1(Zebro_20_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x, Zebro_4_Middle_x, Zebro_5_Middle_x, Zebro_6_Middle_x, Zebro_7_Middle_x, Zebro_8_Middle_x, Zebro_9_Middle_x, Zebro_10_Middle_x,
                                                   Zebro_11_Middle_x, Zebro_12_Middle_x, Zebro_13_Middle_x, Zebro_14_Middle_x, Zebro_15_Middle_x, Zebro_16_Middle_x, Zebro_17_Middle_x, Zebro_18_Middle_x, Zebro_19_Middle_x, Zebro_1_Middle_x,
                                                   Zebro_20_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y, Zebro_4_Middle_y, Zebro_5_Middle_y, Zebro_6_Middle_y, Zebro_7_Middle_y, Zebro_8_Middle_y, Zebro_9_Middle_y, Zebro_10_Middle_y,
                                                   Zebro_11_Middle_y, Zebro_12_Middle_y, Zebro_13_Middle_y, Zebro_14_Middle_y, Zebro_15_Middle_y, Zebro_16_Middle_y, Zebro_17_Middle_y, Zebro_18_Middle_y, Zebro_19_Middle_y, Zebro_1_Middle_y)
                    PicoZebro_20 = [Zebro_20_Middle_x , Zebro_20_Middle_y, Blocking_Zebro]
                    
                    if q_PicoZebro_20.empty() == True:   #if the queue is empty fill it
                        q_PicoZebro_20.put(PicoZebro_20)
                    elif q_PicoZebro_20.empty() == False: #else empty it before filling it again with the next data.
                        q_PicoZebro_20.mutex.acquire()
                        q_PicoZebro_20.queue.clear()
                        q_PicoZebro_20.all_tasks_done.notify_all()
                        q_PicoZebro_20.unfinished_tasks = 0
                        q_PicoZebro_20.mutex.release()
                        q_PicoZebro_20.put(PicoZebro_20)
                Picture = 5
                
                if (time.time() - Picture_1_start_time) > 600:
                    Picture = 0
                    print(Picture)
                    Picture_1_start_time = time.time()
                    print("Restarting program reinit")
                    print((time.time() - Picture_1_start_time))
                    pass

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

    q_Control_Uart_Main = queue.PriorityQueue(maxsize=1) # This is a 1 or 0 Determined by the main.
    
    q_Control_Serial_Write = queue.PriorityQueue(maxsize=1) # In here is the data for serial Write.
    #q_Control_Serial_Write[0] = Which Device/thread is writing
    #q_Control_Serial_Write[1] = To which Device is writing
    #q_Control_Serial_Write[2] = Wat the data is
    
    q_Data_is_Send = queue.PriorityQueue(maxsize=1)

    # All Queue objects Constructor for a FIFO queue
    # These Queue objects are only data obtained by main loop and read by Pico Zebro loops.
    q_PicoZebro_1 = queue.Queue(maxsize=1) #This is a list with in it [Zebro_1_Middle_x , Zebro_1_Middle_y, Blocking_Zebro]
    q_PicoZebro_2 = queue.Queue(maxsize=1) # With a maximum of 1 list. so maxsize = 1.
    q_PicoZebro_3 = queue.Queue(maxsize=1)
    q_PicoZebro_4 = queue.Queue(maxsize=1)
    q_PicoZebro_5 = queue.Queue(maxsize=1)
    q_PicoZebro_6 = queue.Queue(maxsize=1)
    q_PicoZebro_7 = queue.Queue(maxsize=1)
    q_PicoZebro_8 = queue.Queue(maxsize=1)
    q_PicoZebro_9 = queue.Queue(maxsize=1)
    q_PicoZebro_10 = queue.Queue(maxsize=1)
    q_PicoZebro_11 = queue.Queue(maxsize=1)
    q_PicoZebro_12 = queue.Queue(maxsize=1)
    q_PicoZebro_13 = queue.Queue(maxsize=1)
    q_PicoZebro_14 = queue.Queue(maxsize=1)
    q_PicoZebro_15 = queue.Queue(maxsize=1)
    q_PicoZebro_16 = queue.Queue(maxsize=1)
    q_PicoZebro_17 = queue.Queue(maxsize=1)
    q_PicoZebro_18 = queue.Queue(maxsize=1)
    q_PicoZebro_19 = queue.Queue(maxsize=1)
    q_PicoZebro_20 = queue.Queue(maxsize=1)

    #In here will be the direection. Only at the start the main will put something in here afterwards for 10 mins the Zebro thread needs to put himself something in there with guessing.
    q_Pico_Direction_1 = queue.Queue(maxsize=1) # With a maximum of 1 list. so maxsize = 1.
    q_Pico_Direction_2 = queue.Queue(maxsize=1)
    q_Pico_Direction_3 = queue.Queue(maxsize=1)
    q_Pico_Direction_4 = queue.Queue(maxsize=1)
    q_Pico_Direction_5 = queue.Queue(maxsize=1)
    q_Pico_Direction_6 = queue.Queue(maxsize=1)
    q_Pico_Direction_7 = queue.Queue(maxsize=1)
    q_Pico_Direction_8 = queue.Queue(maxsize=1)
    q_Pico_Direction_9 = queue.Queue(maxsize=1)
    q_Pico_Direction_10 = queue.Queue(maxsize=1)
    q_Pico_Direction_11 = queue.Queue(maxsize=1)
    q_Pico_Direction_12 = queue.Queue(maxsize=1)
    q_Pico_Direction_13 = queue.Queue(maxsize=1)
    q_Pico_Direction_14 = queue.Queue(maxsize=1)
    q_Pico_Direction_15 = queue.Queue(maxsize=1)
    q_Pico_Direction_16 = queue.Queue(maxsize=1)
    q_Pico_Direction_17 = queue.Queue(maxsize=1)
    q_Pico_Direction_18 = queue.Queue(maxsize=1)
    q_Pico_Direction_19 = queue.Queue(maxsize=1)
    q_Pico_Direction_20 = queue.Queue(maxsize=1)

    #If higher Precision with direction is required
    q_Pico_Angle_1 = queue.Queue(maxsize=1) # With a maximum of 1 list. so maxsize = 1.
    q_Pico_Angle_2 = queue.Queue(maxsize=1)
    q_Pico_Angle_3 = queue.Queue(maxsize=1)
    q_Pico_Angle_4 = queue.Queue(maxsize=1)
    q_Pico_Angle_5 = queue.Queue(maxsize=1)
    q_Pico_Angle_6 = queue.Queue(maxsize=1)
    q_Pico_Angle_7 = queue.Queue(maxsize=1)
    q_Pico_Angle_8 = queue.Queue(maxsize=1)
    q_Pico_Angle_9 = queue.Queue(maxsize=1)
    q_Pico_Angle_10 = queue.Queue(maxsize=1)
    q_Pico_Angle_11 = queue.Queue(maxsize=1)
    q_Pico_Angle_12 = queue.Queue(maxsize=1)
    q_Pico_Angle_13 = queue.Queue(maxsize=1)
    q_Pico_Angle_14 = queue.Queue(maxsize=1)
    q_Pico_Angle_15 = queue.Queue(maxsize=1)
    q_Pico_Angle_16 = queue.Queue(maxsize=1)
    q_Pico_Angle_17 = queue.Queue(maxsize=1)
    q_Pico_Angle_18 = queue.Queue(maxsize=1)
    q_Pico_Angle_19 = queue.Queue(maxsize=1)
    q_Pico_Angle_20 = queue.Queue(maxsize=1)

    #All Pico Zebro Names 1 - 20
    Pico_N1 = "Pico_N1"
    Pico_N2 = "Pico_N2"
    Pico_N3 = "Pico_N3"
    Pico_N4 = "Pico_N4"
    Pico_N5 = "Pico_N5"
    Pico_N6 = "Pico_N6"
    Pico_N7 = "Pico_N7"
    Pico_N8 = "Pico_N8"
    Pico_N9 = "Pico_N9"
    Pico_N10 = "Pico_N10"
    Pico_N11 = "Pico_N11"
    Pico_N12 = "Pico_N12"
    Pico_N13 = "Pico_N13"
    Pico_N14 = "Pico_N14"
    Pico_N15 = "Pico_N15"
    Pico_N16 = "Pico_N16"
    Pico_N17 = "Pico_N17"
    Pico_N18 = "Pico_N18"
    Pico_N19 = "Pico_N19"
    Pico_N20 = "Pico_N20"

    # Start Uart Thread
    UART_Thread_1 = UART_Thread(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main)
    UART_Thread_1.setName('UART_Thread')
    
    # Start all Pico Zebro Threads.
    Pico_Zebro_1 = Control_Zebro_Thread(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main,Pico_N1,q_PicoZebro_1,q_Pico_Direction_1,q_Pico_Angle_1)
    Pico_Zebro_1.setName('Pico_Zebro_1')

    Pico_Zebro_2 = Control_Zebro_Thread(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main,Pico_N2,q_PicoZebro_2,q_Pico_Direction_2,q_Pico_Angle_2)
    Pico_Zebro_2.setName('Pico_Zebro_2')

    Pico_Zebro_3 = Control_Zebro_Thread(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main,Pico_N3,q_PicoZebro_3,q_Pico_Direction_3,q_Pico_Angle_3)
    Pico_Zebro_3.setName('Pico_Zebro_3')
    
    Pico_Zebro_4 = Control_Zebro_Thread(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main,Pico_N4,q_PicoZebro_4,q_Pico_Direction_4,q_Pico_Angle_4)
    Pico_Zebro_4.setName('Pico_Zebro_4')
    
    Pico_Zebro_5 = Control_Zebro_Thread(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main,Pico_N5,q_PicoZebro_5,q_Pico_Direction_5,q_Pico_Angle_5)
    Pico_Zebro_5.setName('Pico_Zebro_5')
    
    Pico_Zebro_6 = Control_Zebro_Thread(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main,Pico_N6,q_PicoZebro_6,q_Pico_Direction_6,q_Pico_Angle_6)
    Pico_Zebro_6.setName('Pico_Zebro_6')
    
    Pico_Zebro_7 = Control_Zebro_Thread(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main,Pico_N7,q_PicoZebro_7,q_Pico_Direction_7,q_Pico_Angle_7)
    Pico_Zebro_7.setName('Pico_Zebro_7')
    
    Pico_Zebro_8 = Control_Zebro_Thread(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main,Pico_N8,q_PicoZebro_8,q_Pico_Direction_8,q_Pico_Angle_8)
    Pico_Zebro_8.setName('Pico_Zebro_8')
    
    Pico_Zebro_9 = Control_Zebro_Thread(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main,Pico_N9,q_PicoZebro_9,q_Pico_Direction_9,q_Pico_Angle_9)
    Pico_Zebro_9.setName('Pico_Zebro_9')
    
    Pico_Zebro_10 = Control_Zebro_Thread(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main,Pico_N10,q_PicoZebro_10,q_Pico_Direction_10,q_Pico_Angle_10)
    Pico_Zebro_10.setName('Pico_Zebro_10')
    
    Pico_Zebro_11 = Control_Zebro_Thread(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main,Pico_N11,q_PicoZebro_11,q_Pico_Direction_11,q_Pico_Angle_11)
    Pico_Zebro_11.setName('Pico_Zebro_11')
    
    Pico_Zebro_12 = Control_Zebro_Thread(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main,Pico_N12,q_PicoZebro_12,q_Pico_Direction_12,q_Pico_Angle_12)
    Pico_Zebro_12.setName('Pico_Zebro_12')
    
    Pico_Zebro_13 = Control_Zebro_Thread(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main,Pico_N13,q_PicoZebro_13,q_Pico_Direction_13,q_Pico_Angle_13)
    Pico_Zebro_13.setName('Pico_Zebro_13')
    
    Pico_Zebro_14 = Control_Zebro_Thread(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main,Pico_N14,q_PicoZebro_14,q_Pico_Direction_14,q_Pico_Angle_14)
    Pico_Zebro_14.setName('Pico_Zebro_14')
    
    Pico_Zebro_15 = Control_Zebro_Thread(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main,Pico_N15,q_PicoZebro_15,q_Pico_Direction_15,q_Pico_Angle_15)
    Pico_Zebro_15.setName('Pico_Zebro_15')
    
    Pico_Zebro_16 = Control_Zebro_Thread(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main,Pico_N16,q_PicoZebro_16,q_Pico_Direction_16,q_Pico_Angle_16)
    Pico_Zebro_16.setName('Pico_Zebro_16')
    
    Pico_Zebro_17 = Control_Zebro_Thread(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main,Pico_N17,q_PicoZebro_17,q_Pico_Direction_17,q_Pico_Angle_17)
    Pico_Zebro_17.setName('Pico_Zebro_17')
    
    Pico_Zebro_18 = Control_Zebro_Thread(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main,Pico_N18,q_PicoZebro_18,q_Pico_Direction_18,q_Pico_Angle_18)
    Pico_Zebro_18.setName('Pico_Zebro_18')
    
    Pico_Zebro_19 = Control_Zebro_Thread(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main,Pico_N19,q_PicoZebro_19,q_Pico_Direction_19,q_Pico_Angle_19)
    Pico_Zebro_19.setName('Pico_Zebro_19')
    
    Pico_Zebro_20 = Control_Zebro_Thread(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main,Pico_N20,q_PicoZebro_20,q_Pico_Direction_20,q_Pico_Angle_20)
    Pico_Zebro_20.setName('Pico_Zebro_20')
    
    main(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main,q_PicoZebro_1,q_PicoZebro_2,q_PicoZebro_3,q_PicoZebro_4,q_PicoZebro_5,q_PicoZebro_6,q_PicoZebro_7,q_PicoZebro_8,q_PicoZebro_9,q_PicoZebro_10,
         q_PicoZebro_11,q_PicoZebro_12,q_PicoZebro_13,q_PicoZebro_14,q_PicoZebro_15,q_PicoZebro_16,q_PicoZebro_17,q_PicoZebro_18,q_PicoZebro_19,q_PicoZebro_20,
         q_Pico_Direction_1,q_Pico_Direction_2,q_Pico_Direction_3,q_Pico_Direction_4,q_Pico_Direction_5,q_Pico_Direction_6,q_Pico_Direction_7,q_Pico_Direction_8,q_Pico_Direction_9,q_Pico_Direction_10,
         q_Pico_Direction_11,q_Pico_Direction_12,q_Pico_Direction_13,q_Pico_Direction_14,q_Pico_Direction_15,q_Pico_Direction_16,q_Pico_Direction_17,q_Pico_Direction_18,q_Pico_Direction_19,q_Pico_Direction_20,
         q_Pico_Angle_1,q_Pico_Angle_2,q_Pico_Angle_3,q_Pico_Angle_4,q_Pico_Angle_5,q_Pico_Angle_6,q_Pico_Angle_7,q_Pico_Angle_8,q_Pico_Angle_9,q_Pico_Angle_10,
         q_Pico_Angle_11,q_Pico_Angle_12,q_Pico_Angle_13,q_Pico_Angle_14,q_Pico_Angle_15,q_Pico_Angle_16,q_Pico_Angle_17,q_Pico_Angle_18,q_Pico_Angle_19,q_Pico_Angle_20)
