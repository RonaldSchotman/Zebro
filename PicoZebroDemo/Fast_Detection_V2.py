#!/usr/bin/env python
# TU Delft Pico Zebro Demo
# PZ_DEMO Fallback
# Full Code inclusive of Pseudo Code.
# Writer: Martijn de Rooij
# Version 0.02

# Everything is being tested from 120 cm height.

# import the necessary packages
from picamera.array import PiRGBArray   # Pi camera Libary capture BGR video
from picamera import PiCamera           # PiCamera liberary
import time                             # For real time video (using openCV)
import numpy as np                      # Optimized library for numerical operations
import cv2                              # Include OpenCV library (Most important one)
import Queue
import threading                        # Library for Multithreading
import serial                           # Import serial uart library for raspberry pi

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

# http://picamera.readthedocs.io/en/latest/fov.html
# initialize the Pi camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (1648, 928) #Maximum Resolution with full FOV
camera.framerate = 40           # Maximum Frame Rate with this resolution
rawCapture = PiRGBArray(camera, size=(1648, 928))

# allow the camera to warmup.
time.sleep(0.1)

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
        Connected = 0
        while True:
            
            if Connected == 0:
                Last_Movement = "Stop"
                # Obtain Serial condition
                ser.write("Connected_devices")
                time.sleep(1)   # Wait for sending of data
                ser.readline(Connected_Devices)
                # Release serial Connection
                for Connected_D in Connected_Devices:
                    if Connected_D == self.Zebro:   # Needs to be Pico_N1
                        Connected = 1
                    else:
                        Connected = 0
                time.sleep(60) # only here is sleeping allowed considering it is not connected anyway and only every 60 seconds needs to check
            if Connected == 1:
                # Here comes a test command to check if we are still connected. (if possible)
                # This means read a register and get a expected value otherwise connected == 0
                # if expected value == True then:
                
            # From here on out the actual controlling
            
                # Obtain condition PicoZebro (try this for 3 seconds)
                
                Middle_point_x = self.PicoZebro[0]
                Middle_point_y = self.PicoZebro[1]
                Current_Direction = self.PicoZebro[2]
                Blocked_Direction = self.PicoZebro[3]

                #release condition PicoZebro
                if (Middle_point_x == 0) or (Middle_Point_y == 0):
                    Movement == "Stop"
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
                        if Random_N =< 60:
                            Movement = "Forward"
                        elif Random_N > 60 and Random_N =< 70:
                            Movement = "Stop"
                        elif Random_N > 70 and  Random_N =< 85:
                            Movement = "Right"
                        elif Random_N > 85 and  Random_N =< 100:
                            Movement = "Left"

                    if Last_Movement == "Forward":
                        Random_N = random.randrange(1,100)
                        if Random_N =< 80:
                            Movement = "Forward"
                        elif Random_N > 80 and Random_N =< 90:
                            Movement = "Stop"
                        elif Random_N > 90 and Random_N =< 95:
                            Movement = "Right"
                        elif Random_N > 95 and Random_N =< 100:
                            Movement = "Left"

                    if Last_Movement == "Right":
                        Random_N = random.randrange(1,100)
                        if Random_N =< 30:
                            Movement = "Forward"
                        elif Random_N > 30 and Random_N =< 35:
                            Movement = "Stop"
                        elif Random_N > 35 and Random_N =< 95:
                            Movement = "Right"
                        elif Random_N > 95 and Random_N =< 100:
                            Movement = "Left"
                            
                    if Last_Movement == "Left":
                        Random_N = random.randrange(1,100)
                        if Random_N =< 30:
                            Movement = "Forward"
                        elif Random_N > 30 and Random_N =< 35:
                            Movement = "Stop"
                        elif Random_N > 35 and Random_N =< 40:
                            Movement = "Right"
                        elif Random_N > 40 and Random_N =< 100:
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
                        if Current_Direction == Names:
                            DONT_Send = 1
                    if DONT_Send == 1:
                        # Obtain Serial Write
                        ser.write(self.Zebro, "Don't Move")
                        # Release Serial Write
                    else:
                        # Obtain Serial Write
                        ser.write(self.Zebro, "Movement")
                        # Release Serial Write
                    #for Names in Blocked_Direction
                         #if Direction == Blocked_Direction:    (THis needs to be in a for loop for every value in Blocked_direction
                            #Movement is Blocked               #With Blocked Direction Cleard at the end (Which Doesn't matter anymore)
                            #Send Movement == Don't Move (don't assign it)
                        #if Movement == Blocked_Movement:
                        #   Don't send Movement
                        
                    # previous_movement = Movement
                    # Block_direction == empty

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
    Direction = None

    # (This only needs to be done if just north, south east and west work.)
    # Once known what the max and minimum distance is between two points
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
        Direction = "North"
        return x_middle, y_middle, Direction
    
    elif (x_Led_1 < x_Led_3) and (y_Led_1 > y_Led_3):
        # Pico Zebro is facing East
        # Middle Point Zebro is:
        x_middle = ((x_Led_3 - x_Led_1) + x_Led_1)
        y_middle = ((y_Led_1 - y_Led_3) + y_Led_3)
        Direction = "East"
        return x_middle, y_middle, Direction
    
    elif (x_Led_1 > x_Led_3) and (y_Led_1 > y_Led_3):
        # Pico Zebro is facing South
        # Middle Point Zebro is:
        x_middle = ((x_Led_1 - x_Led_3) + x_Led_3)
        y_middle = ((y_Led_1 - y_Led_3) + y_Led_3)
        Direction = "South"
        return x_middle, y_middle, Direction
    
    elif (x_Led_1 > x_Led_3) and (y_Led_1 < y_Led_3):
        # Pico Zebro is facing West
        # Middle Point Zebro is:
        x_middle = ((x_Led_1 - x_Led_3) + x_Led_3)
        y_middle = ((y_Led_3 - y_Led_1) + y_Led_1)
        Direction = "West"
        return x_middle, y_middle, Direction
    
    return x_middle, y_middle, Direction #extra return to avoid errors



def main():
    # Initialize Picture to 0 for the first time when program starts.
    Picture = 0
    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the NumPy array representing the image, the initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array

        # Take current day for testing purposes.
        Timetest = time.strftime("%d-%m-%Y")
        # Show the current view for debugging
        cv2.imshow("original %s" % Timetest,image)

        start_time = time.time() # Testing Function for how long a part of a code takes.
        print ("My program took", time.time() - start_time, "to run")   #print how long it took

        # Take original Picture minimal after first loop for the first frame to avoid weird pictures.
        if Picture == 1:
            #Global command turn all leds off. (This needs to be tested how long this takes.)
            #Like this with condition. With I am writing now on the serial Bus. The rest needs to wait for me. (So all zebro Thread wait with sending next movement.)
            ser.write("Global Leds_off\n")
            #Release condition only at end so the Zebro Treads cannot interfere
            
            time.sleep(0.001)
            
            cv2.imwrite("Image%s.jpg"%Picture, image)   # Save a picture to Image1.jpg

        Original = cv2.imread("Image1.jpg")     # This is the original picture where the diferences will be compared with.
        
        # Do some other stuff
        for Devices in range(19):       #range(20) is the maximum amount of pico zebro's 
            Picture = 2     # Make Picture 2 for taking Picture 2 with Led 1 on.
            print(Devices)  #Here to show in the terminal which device the program is trying to detect.

            #Like this with condition. With I am writing now on the serial Bus. The rest needs to wait for me. 
            ser.write("PicoN%s Led1_on\n" % Devices)
            #Release condition  only at end so the Zebro Treads cannot interfere
            time.sleep(0.001)
            #Wait until said back in register it is turned on for certain time (Now it is a hard wait)

            if Picture == 2:
                cv2.imwrite("Image%s.jpg"%Picture, image)   # Take the second picture with led 1 on. Which is    

            #Like this with condition. With I am writing now on the serial Bus. The rest needs to wait for me. 
            ser.write("PicoN%s Leds_off\n" % Devices)   # Turn led 1 of again
            ser.write("PicoN%s Led3_on\n" % Devices)    # Turn led 3 on
            #Release condition  only at end so the Zebro Treads cannot interfere
            time.sleep(0.001)

            Picture = 3

            #Again do some other stuff
            if Picture == 3:
                cv2.imwrite("Image%s.jpg"%Picture, image)

            #Like this with condition. With I am writing now on the serial Bus. The rest needs to wait for me. 
            ser.write("PicoN%s Leds_off\n" % Devices)   # Turn led 1 of again
            ser.write("PicoN%s Led3_on\n" % Devices)    # Turn led 3 on
            #Release condition  only at end so the Zebro Treads cannot interfere
            time.sleep(0.001)

            Picture = 4 # Do the calculations for determing where the Pico Zebro is.
            
            if Picture == 4:
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

                sorteddata_Led_1 = sorted(zip(areaArray, contours2), key=lambda x: x[0], reverse=True)
                sorteddata_Led_3 = sorted(zip(areaArray, contours2), key=lambda x: x[0], reverse=True)

                try:
                    Largest_contour_led_1 = sorteddata_Led_1[0][0]
                    [x_Led_1,y_Led_1,w_Led_1,h_Led_1] = cv2.boundingRect(Largest_contour_led_1)
                except IndexError:
                    print("Nothing Found")
                    pass

                try:
                    Largest_contour_led_3 = sorteddata_Led_3[0][0]
                    [x_Led_3,y_Led_3,w_Led_3,h_Led_3] = cv2.boundingRect(Largest_contour_led_3)
                except IndexError:
                    print("Nothing Found")
                    pass

                #Add led 1 and 3 together for Testing purposes
                #LEDS_Image = cv2.addWeighted(Difference_led_1,1,Difference_led_3,1,0)
                #cv2.imshow("LEds together", LEDS_Image)
                #cv2.imwrite("Leds_Tog1.jpg", LEDS_Image)

                (Zebro_Middle_x,Zebro_Middle_y,Direction) = Find_Orientation(x_Led_1,x_Led_3,y_Led_1,y_Led_3)
                print(Zebro_Middle_x,Zebro_Middle_y,Direction)  # Debug print

                # If someone can tell me how I can make this shorter plz but I don't think I can considering for each zebro three different values need to be set.
                if Devices == 0: 
                    #set data from PZ 1
                    Zebro_1_Middle_x = Zebro_Middle_x
                    Zebro_1_Middle_y = Zebro_Middle_y
                    Direction_Zebro_1 = Direction

                if Devices == 1: 
                    #set data from PZ 2
                    Zebro_2_Middle_x = Zebro_Middle_x
                    Zebro_2_Middle_y = Zebro_Middle_y
                    Direction_Zebro_2 = Direction

                if Devices == 2: 
                    #set data from PZ 3
                    Zebro_3_Middle_x = Zebro_Middle_x
                    Zebro_3_Middle_y = Zebro_Middle_y
                    Direction_Zebro_3 = Direction

                if Devices == 3: 
                    #set data from PZ 4
                    Zebro_4_Middle_x = Zebro_Middle_x
                    Zebro_4_Middle_y = Zebro_Middle_y
                    Direction_Zebro_4 = Direction

                if Devices == 4: 
                    #set data from PZ 5
                    Zebro_5_Middle_x = Zebro_Middle_x
                    Zebro_5_Middle_y = Zebro_Middle_y
                    Direction_Zebro_5 = Direction

                if Devices == 5: 
                    #set data from PZ 6
                    Zebro_6_Middle_x = Zebro_Middle_x
                    Zebro_6_Middle_y = Zebro_Middle_y
                    Direction_Zebro_6 = Direction

                if Devices == 6: 
                    #set data from PZ 7
                    Zebro_7_Middle_x = Zebro_Middle_x
                    Zebro_7_Middle_y = Zebro_Middle_y
                    Direction_Zebro_7 = Direction

                if Devices == 7: 
                    #set data from PZ 8
                    Zebro_8_Middle_x = Zebro_Middle_x
                    Zebro_8_Middle_y = Zebro_Middle_y
                    Direction_Zebro_8 = Direction

                if Devices == 8: 
                    #set data from PZ 9
                    Zebro_9_Middle_x = Zebro_Middle_x
                    Zebro_9_Middle_y = Zebro_Middle_y
                    Direction_Zebro_9 = Direction

                if Devices == 9: 
                    #set data from PZ 10
                    Zebro_10_Middle_x = Zebro_Middle_x
                    Zebro_10_Middle_y = Zebro_Middle_y
                    Direction_Zebro_10 = Direction

                if Devices == 10: 
                    #set data from PZ 11
                    Zebro_11_Middle_x = Zebro_Middle_x
                    Zebro_11_Middle_y = Zebro_Middle_y
                    Direction_Zebro_11 = Direction

                if Devices == 11: 
                    #set data from PZ 12
                    Zebro_12_Middle_x = Zebro_Middle_x
                    Zebro_12_Middle_y = Zebro_Middle_y
                    Direction_Zebro_12 = Direction

                if Devices == 12: 
                    #set data from PZ 13
                    Zebro_13_Middle_x = Zebro_Middle_x
                    Zebro_13_Middle_y = Zebro_Middle_y
                    Direction_Zebro_13 = Direction

                if Devices == 13: 
                    #set data from PZ 14
                    Zebro_14_Middle_x = Zebro_Middle_x
                    Zebro_14_Middle_y = Zebro_Middle_y
                    Direction_Zebro_14 = Direction

                if Devices == 14: 
                    #set data from PZ 15
                    Zebro_15_Middle_x = Zebro_Middle_x
                    Zebro_15_Middle_y = Zebro_Middle_y
                    Direction_Zebro_15 = Direction

                if Devices == 15: 
                    #set data from PZ 16
                    Zebro_16_Middle_x = Zebro_Middle_x
                    Zebro_16_Middle_y = Zebro_Middle_y
                    Direction_Zebro_16 = Direction

                if Devices == 16: 
                    #set data from PZ 17
                    Zebro_17_Middle_x = Zebro_Middle_x
                    Zebro_17_Middle_y = Zebro_Middle_y
                    Direction_Zebro_17 = Direction

                if Devices == 17: 
                    #set data from PZ 18
                    Zebro_18_Middle_x = Zebro_Middle_x
                    Zebro_18_Middle_y = Zebro_Middle_y
                    Direction_Zebro_18 = Direction

                if Devices == 18: 
                    #set data from PZ 19
                    Zebro_19_Middle_x = Zebro_Middle_x
                    Zebro_19_Middle_y = Zebro_Middle_y
                    Direction_Zebro_19 = Direction

                if Devices == 19: 
                    #set data from PZ 20
                    Zebro_20_Middle_x = Zebro_Middle_x
                    Zebro_20_Middle_y = Zebro_Middle_y
                    Direction_Zebro_20 = Direction
                    
                #once every value for every possible Zebro is determind then
                #Check if any of the x and y values are close to each other.
                #or if any of the x or y values are to close to the edge which is
                # if x == 0 or x == 1600 or y = 0 or y == 920 
                #So a gigantic multiple if statement. which becomes smaller and smaller
                # Or if possible like this: (other wise multiple giant for loops if this is not possible
                for Zebros in range(19):
                    Blocking = []   #Here will be the blocking in
                    #For Pico Zebro 1
                    if Zebros == 0:
                        Blocking_x_2 = abs(Zebro_1_Middle_x - Zebro_2_Middle_x)
                        Blocking_y_2 = abs(Zebro_1_Middle_y - Zebro_2_Middle_y)
                        Blocking_x_3 = abs(Zebro_1_Middle_x - Zebro_3_Middle_x)
                        Blocking_y_3 = abs(Zebro_1_Middle_y - Zebro_3_Middle_y)
                        Blocking_x_4 = abs(Zebro_1_Middle_x - Zebro_4_Middle_x)
                        Blocking_y_4 = abs(Zebro_1_Middle_y - Zebro_4_Middle_y)
                        Blocking_x_5 = abs(Zebro_1_Middle_x - Zebro_5_Middle_x)
                        Blocking_y_5 = abs(Zebro_1_Middle_y - Zebro_5_Middle_y)
                        Blocking_x_6 = abs(Zebro_1_Middle_x - Zebro_6_Middle_x)
                        Blocking_y_6 = abs(Zebro_1_Middle_y - Zebro_6_Middle_y)
                        Blocking_x_7 = abs(Zebro_1_Middle_x - Zebro_7_Middle_x)
                        Blocking_y_7 = abs(Zebro_1_Middle_y - Zebro_7_Middle_y)
                        Blocking_x_8 = abs(Zebro_1_Middle_x - Zebro_8_Middle_x)
                        Blocking_y_8 = abs(Zebro_1_Middle_y - Zebro_8_Middle_y)
                        Blocking_x_9 = abs(Zebro_1_Middle_x - Zebro_9_Middle_x)
                        Blocking_y_9 = abs(Zebro_1_Middle_y - Zebro_9_Middle_y)
                        Blocking_x_10 = abs(Zebro_1_Middle_x - Zebro_10_Middle_x)
                        Blocking_y_10 = abs(Zebro_1_Middle_y - Zebro_10_Middle_y)
                        Blocking_x_11 = abs(Zebro_1_Middle_x - Zebro_11_Middle_x)
                        Blocking_y_11 = abs(Zebro_1_Middle_y - Zebro_11_Middle_y)
                        Blocking_x_12 = abs(Zebro_1_Middle_x - Zebro_12_Middle_x)
                        Blocking_y_12 = abs(Zebro_1_Middle_y - Zebro_12_Middle_y)
                        Blocking_x_13 = abs(Zebro_1_Middle_x - Zebro_13_Middle_x)
                        Blocking_y_13 = abs(Zebro_1_Middle_y - Zebro_13_Middle_y)
                        Blocking_x_14 = abs(Zebro_1_Middle_x - Zebro_14_Middle_x)
                        Blocking_y_14 = abs(Zebro_1_Middle_y - Zebro_14_Middle_y)
                        Blocking_x_15 = abs(Zebro_1_Middle_x - Zebro_15_Middle_x)
                        Blocking_y_15 = abs(Zebro_1_Middle_y - Zebro_15_Middle_y)
                        Blocking_x_16 = abs(Zebro_1_Middle_x - Zebro_16_Middle_x)
                        Blocking_y_16 = abs(Zebro_1_Middle_y - Zebro_16_Middle_y)
                        Blocking_x_17 = abs(Zebro_1_Middle_x - Zebro_17_Middle_x)
                        Blocking_y_17 = abs(Zebro_1_Middle_y - Zebro_17_Middle_y)
                        Blocking_x_18 = abs(Zebro_1_Middle_x - Zebro_18_Middle_x)
                        Blocking_y_18 = abs(Zebro_1_Middle_y - Zebro_18_Middle_y)
                        Blocking_x_19 = abs(Zebro_1_Middle_x - Zebro_19_Middle_x)
                        Blocking_y_19 = abs(Zebro_1_Middle_y - Zebro_19_Middle_y)
                        Blocking_x_20 = abs(Zebro_1_Middle_x - Zebro_20_Middle_x)
                        Blocking_y_20 = abs(Zebro_1_Middle_y - Zebro_20_Middle_y)
            
                        if (0 < Blocking_x_2 < 80) or (0 < Blocking_x_3 < 80) or (0 < Blocking_x_4 < 80) or (0 < Blocking_x_5 < 80)
                        or (0 < Blocking_x_6 < 80) or (0 < Blocking_x_7 < 80) or (0 < Blocking_x_8 < 80) or (0 < Blocking_x_9 < 80)
                        or (0 < Blocking_x_10 < 80) or (0 < Blocking_x_11 < 80) or (0 < Blocking_x_12 < 80) or (0 < Blocking_x_13 < 80)
                        or (0 < Blocking_x_14 < 80) or (0 < Blocking_x_15 < 80) or (0 < Blocking_x_16 < 80) or (0 < Blocking_x_17 < 80)
                        or (0 < Blocking_x_18 < 80) or (0 < Blocking_x_19 < 80) or (0 < Blocking_x_20 < 80):
                            if (Zebro_1_Middle_x < Zebro_2_Middle_x) or (Zebro_1_Middle_x < Zebro_3_Middle_x) or (Zebro_1_Middle_x < Zebro_4_Middle_x) or (Zebro_1_Middle_x < Zebro_5_Middle_x)
                            or (Zebro_1_Middle_x < Zebro_6_Middle_x) or (Zebro_1_Middle_x < Zebro_7_Middle_x) or (Zebro_1_Middle_x < Zebro_8_Middle_x) or (Zebro_1_Middle_x < Zebro_9_Middle_x)
                            or (Zebro_1_Middle_x < Zebro_10_Middle_x) or (Zebro_1_Middle_x < Zebro_11_Middle_x) or (Zebro_1_Middle_x < Zebro_12_Middle_x) or (Zebro_1_Middle_x < Zebro_13_Middle_x)
                            or (Zebro_1_Middle_x < Zebro_14_Middle_x) or (Zebro_1_Middle_x < Zebro_15_Middle_x) or (Zebro_1_Middle_x < Zebro_16_Middle_x) or (Zebro_1_Middle_x < Zebro_17_Middle_x)
                            or (Zebro_1_Middle_x < Zebro_18_Middle_x) or (Zebro_1_Middle_x < Zebro_19_Middle_x) or (Zebro_1_Middle_x < Zebro_20_Middle_x):
                                Block = "East"
                                Bloking.append(Block)
                                Block = None
                            if (Zebro_1_Middle_x > Zebro_2_Middle_x) or (Zebro_1_Middle_x > Zebro_3_Middle_x) or (Zebro_1_Middle_x > Zebro_4_Middle_x) or (Zebro_1_Middle_x > Zebro_5_Middle_x)
                            or (Zebro_1_Middle_x > Zebro_6_Middle_x) or (Zebro_1_Middle_x > Zebro_7_Middle_x) or (Zebro_1_Middle_x > Zebro_8_Middle_x) or (Zebro_1_Middle_x > Zebro_9_Middle_x)
                            or (Zebro_1_Middle_x > Zebro_10_Middle_x) or (Zebro_1_Middle_x > Zebro_11_Middle_x) or (Zebro_1_Middle_x > Zebro_12_Middle_x) or (Zebro_1_Middle_x > Zebro_13_Middle_x)
                            or (Zebro_1_Middle_x > Zebro_14_Middle_x) or (Zebro_1_Middle_x > Zebro_15_Middle_x) or (Zebro_1_Middle_x > Zebro_16_Middle_x) or (Zebro_1_Middle_x > Zebro_17_Middle_x)
                            or (Zebro_1_Middle_x > Zebro_18_Middle_x) or (Zebro_1_Middle_x > Zebro_19_Middle_x) or (Zebro_1_Middle_x > Zebro_20_Middle_x):
                                Block = "West"
                                Bloking.append(Block)
                                Block = None
                        if (0 < Blocking_y_2 < 80) or (0 < Blocking_y_3 < 80) or (0 < Blocking_y_4 < 80) or (0 < Blocking_y_5 < 80)
                        or (0 < Blocking_y_6 < 80) or (0 < Blocking_y_7 < 80) or (0 < Blocking_y_8 < 80) or (0 < Blocking_y_9 < 80)
                        or (0 < Blocking_y_10 < 80) or (0 < Blocking_y_11 < 80) or (0 < Blocking_y_12 < 80) or (0 < Blocking_y_13 < 80)
                        or (0 < Blocking_y_14 < 80) or (0 < Blocking_y_15 < 80) or (0 < Blocking_y_16 < 80) or (0 < Blocking_y _17 < 80)
                        or (0 < Blocking_y_18 < 80) or (0 < Blocking_y_19 < 80) or (0 < Blocking_y_20 < 80):
                            if (Zebro_1_Middle_y > Zebro_2_Middle_y) or (Zebro_1_Middle_y > Zebro_3_Middle_y) or (Zebro_1_Middle_y > Zebro_4_Middle_y) or (Zebro_1_Middle_y > Zebro_5_Middle_y)
                            or (Zebro_1_Middle_y > Zebro_6_Middle_y) or (Zebro_1_Middle_y > Zebro_7_Middle_y) or (Zebro_1_Middle_y > Zebro_8_Middle_y) or (Zebro_1_Middle_y > Zebro_9_Middle_y)
                            or (Zebro_1_Middle_y > Zebro_10_Middle_y) or (Zebro_1_Middle_y > Zebro_11_Middle_y) or (Zebro_1_Middle_y > Zebro_12_Middle_y) or (Zebro_1_Middle_y > Zebro_13_Middle_y)
                            or (Zebro_1_Middle_y > Zebro_14_Middle_y) or (Zebro_1_Middle_y > Zebro_15_Middle_y) or (Zebro_1_Middle_y > Zebro_16_Middle_y) or (Zebro_1_Middle_y > Zebro_17_Middle_y)
                            or (Zebro_1_Middle_y > Zebro_18_Middle_y) or (Zebro_1_Middle_y > Zebro_19_Middle_y) or (Zebro_1_Middle_y > Zebro_20_Middle_y):
                                Block = "South"
                                Bloking.append(Block)
                                Block = None
                            if (Zebro_1_Middle_y < Zebro_2_Middle_y) or (Zebro_1_Middle_y < Zebro_3_Middle_y) or (Zebro_1_Middle_y < Zebro_4_Middle_y) or (Zebro_1_Middle_y < Zebro_5_Middle_y)
                            or (Zebro_1_Middle_y < Zebro_6_Middle_y) or (Zebro_1_Middle_y < Zebro_7_Middle_y) or (Zebro_1_Middle_y < Zebro_8_Middle_y) or (Zebro_1_Middle_y < Zebro_9_Middle_y)
                            or (Zebro_1_Middle_y < Zebro_10_Middle_y) or (Zebro_1_Middle_y < Zebro_11_Middle_y) or (Zebro_1_Middle_y < Zebro_12_Middle_y) or (Zebro_1_Middle_y < Zebro_13_Middle_y)
                            or (Zebro_1_Middle_y < Zebro_14_Middle_y) or (Zebro_1_Middle_y < Zebro_15_Middle_y) or (Zebro_1_Middle_y < Zebro_16_Middle_y) or (Zebro_1_Middle_y < Zebro_17_Middle_y)
                            or (Zebro_1_Middle_y < Zebro_18_Middle_y) or (Zebro_1_Middle_y < Zebro_19_Middle_y) or (Zebro_1_Middle_y < Zebro_20_Middle_y):
                                Block = "North"
                                Bloking.append(Block)
                                Block = None
                        # Grab condition zebro 1:
                        PicoZebro_1[Zebro_1_Middle_x , Zebro_1_Middle_y, Direction_Zebro_1, Blocking]
                        #release condition zebro 1
                        
                    # For Pico Zebro 2 (Also here if know how to do this shorter plz do so)
                    if Zebros == 1:
                        Blocking_x_1 = abs(Zebro_2_Middle_x - Zebro_1_Middle_x)
                        Blocking_y_1 = abs(Zebro_2_Middle_y - Zebro_1_Middle_y)
                        Blocking_x_3 = abs(Zebro_2_Middle_x - Zebro_3_Middle_x)
                        Blocking_y_3 = abs(Zebro_2_Middle_y - Zebro_3_Middle_y)
                        Blocking_x_4 = abs(Zebro_2_Middle_x - Zebro_4_Middle_x)
                        Blocking_y_4 = abs(Zebro_2_Middle_y - Zebro_4_Middle_y)
                        Blocking_x_5 = abs(Zebro_2_Middle_x - Zebro_5_Middle_x)
                        Blocking_y_5 = abs(Zebro_2_Middle_y - Zebro_5_Middle_y)
                        Blocking_x_6 = abs(Zebro_2_Middle_x - Zebro_6_Middle_x)
                        Blocking_y_6 = abs(Zebro_2_Middle_y - Zebro_6_Middle_y)
                        Blocking_x_7 = abs(Zebro_2_Middle_x - Zebro_7_Middle_x)
                        Blocking_y_7 = abs(Zebro_2_Middle_y - Zebro_7_Middle_y)
                        Blocking_x_8 = abs(Zebro_2_Middle_x - Zebro_8_Middle_x)
                        Blocking_y_8 = abs(Zebro_2_Middle_y - Zebro_8_Middle_y)
                        Blocking_x_9 = abs(Zebro_2_Middle_x - Zebro_9_Middle_x)
                        Blocking_y_9 = abs(Zebro_2_Middle_y - Zebro_9_Middle_y)
                        Blocking_x_10 = abs(Zebro_2_Middle_x - Zebro_10_Middle_x)
                        Blocking_y_10 = abs(Zebro_2_Middle_y - Zebro_10_Middle_y)
                        Blocking_x_11 = abs(Zebro_2_Middle_x - Zebro_11_Middle_x)
                        Blocking_y_11 = abs(Zebro_2_Middle_y - Zebro_11_Middle_y)
                        Blocking_x_12 = abs(Zebro_2_Middle_x - Zebro_12_Middle_x)
                        Blocking_y_12 = abs(Zebro_2_Middle_y - Zebro_12_Middle_y)
                        Blocking_x_13 = abs(Zebro_2_Middle_x - Zebro_13_Middle_x)
                        Blocking_y_13 = abs(Zebro_2_Middle_y - Zebro_13_Middle_y)
                        Blocking_x_14 = abs(Zebro_2_Middle_x - Zebro_14_Middle_x)
                        Blocking_y_14 = abs(Zebro_2_Middle_y - Zebro_14_Middle_y)
                        Blocking_x_15 = abs(Zebro_2_Middle_x - Zebro_15_Middle_x)
                        Blocking_y_15 = abs(Zebro_2_Middle_y - Zebro_15_Middle_y)
                        Blocking_x_16 = abs(Zebro_2_Middle_x - Zebro_16_Middle_x)
                        Blocking_y_16 = abs(Zebro_2_Middle_y - Zebro_16_Middle_y)
                        Blocking_x_17 = abs(Zebro_2_Middle_x - Zebro_17_Middle_x)
                        Blocking_y_17 = abs(Zebro_2_Middle_y - Zebro_17_Middle_y)
                        Blocking_x_18 = abs(Zebro_2_Middle_x - Zebro_18_Middle_x)
                        Blocking_y_18 = abs(Zebro_2_Middle_y - Zebro_18_Middle_y)
                        Blocking_x_19 = abs(Zebro_2_Middle_x - Zebro_19_Middle_x)
                        Blocking_y_19 = abs(Zebro_2_Middle_y - Zebro_19_Middle_y)
                        Blocking_x_20 = abs(Zebro_2_Middle_x - Zebro_20_Middle_x)
                        Blocking_y_20 = abs(Zebro_2_Middle_y - Zebro_20_Middle_y)
            
                        if (0 < Blocking_x_1 < 80) or (0 < Blocking_x_3 < 80) or (0 < Blocking_x_4 < 80) or (0 < Blocking_x_5 < 80)
                        or (0 < Blocking_x_6 < 80) or (0 < Blocking_x_7 < 80) or (0 < Blocking_x_8 < 80) or (0 < Blocking_x_9 < 80)
                        or (0 < Blocking_x_10 < 80) or (0 < Blocking_x_11 < 80) or (0 < Blocking_x_12 < 80) or (0 < Blocking_x_13 < 80)
                        or (0 < Blocking_x_14 < 80) or (0 < Blocking_x_15 < 80) or (0 < Blocking_x_16 < 80) or (0 < Blocking_x_17 < 80)
                        or (0 < Blocking_x_18 < 80) or (0 < Blocking_x_19 < 80) or (0 < Blocking_x_20 < 80):
                            if (Zebro_2_Middle_x < Zebro_2_Middle_x) or (Zebro_2_Middle_x < Zebro_3_Middle_x) or (Zebro_1_Middle_x < Zebro_4_Middle_x) or (Zebro_1_Middle_x < Zebro_5_Middle_x)
                            or (Zebro_2_Middle_x < Zebro_6_Middle_x) or (Zebro_2_Middle_x < Zebro_7_Middle_x) or (Zebro_1_Middle_x < Zebro_8_Middle_x) or (Zebro_1_Middle_x < Zebro_9_Middle_x)
                            or (Zebro_2_Middle_x < Zebro_10_Middle_x) or (Zebro_1_Middle_x < Zebro_11_Middle_x) or (Zebro_1_Middle_x < Zebro_12_Middle_x) or (Zebro_1_Middle_x < Zebro_13_Middle_x)
                            or (Zebro_2_Middle_x < Zebro_14_Middle_x) or (Zebro_1_Middle_x < Zebro_15_Middle_x) or (Zebro_1_Middle_x < Zebro_16_Middle_x) or (Zebro_1_Middle_x < Zebro_17_Middle_x)
                            or (Zebro_2_Middle_x < Zebro_18_Middle_x) or (Zebro_1_Middle_x < Zebro_19_Middle_x) or (Zebro_1_Middle_x < Zebro_20_Middle_x):
                                Block = "East"
                                Bloking.append(Block)
                                Block = None
                            if (Zebro_2_Middle_x > Zebro_2_Middle_x) or (Zebro_2_Middle_x > Zebro_3_Middle_x) or (Zebro_2_Middle_x > Zebro_4_Middle_x) or (Zebro_1_Middle_x > Zebro_5_Middle_x)
                            or (Zebro_2_Middle_x > Zebro_6_Middle_x) or (Zebro_2_Middle_x > Zebro_7_Middle_x) or (Zebro_2_Middle_x > Zebro_8_Middle_x) or (Zebro_1_Middle_x > Zebro_9_Middle_x)
                            or (Zebro_2_Middle_x > Zebro_10_Middle_x) or (Zebro_2_Middle_x > Zebro_11_Middle_x) or (Zebro_2_Middle_x > Zebro_12_Middle_x) or (Zebro_1_Middle_x > Zebro_13_Middle_x)
                            or (Zebro_2_Middle_x > Zebro_14_Middle_x) or (Zebro_2_Middle_x > Zebro_15_Middle_x) or (Zebro_2_Middle_x > Zebro_16_Middle_x) or (Zebro_1_Middle_x > Zebro_17_Middle_x)
                            or (Zebro_2_Middle_x > Zebro_18_Middle_x) or (Zebro_2_Middle_x > Zebro_19_Middle_x) or (Zebro_2_Middle_x > Zebro_20_Middle_x):
                                Block = "West"
                                Bloking.append(Block)
                                Block = None
                        if (0 < Blocking_y_1 < 80) or (0 < Blocking_y_3 < 80) or (0 < Blocking_y_4 < 80) or (0 < Blocking_y_5 < 80)
                        or (0 < Blocking_y_6 < 80) or (0 < Blocking_y_7 < 80) or (0 < Blocking_y_8 < 80) or (0 < Blocking_y_9 < 80)
                        or (0 < Blocking_y_10 < 80) or (0 < Blocking_y_11 < 80) or (0 < Blocking_y_12 < 80) or (0 < Blocking_y_13 < 80)
                        or (0 < Blocking_y_14 < 80) or (0 < Blocking_y_15 < 80) or (0 < Blocking_y_16 < 80) or (0 < Blocking_y _17 < 80)
                        or (0 < Blocking_y_18 < 80) or (0 < Blocking_y_19 < 80) or (0 < Blocking_y_20 < 80):
                            if (Zebro_2_Middle_y > Zebro_2_Middle_y) or (Zebro_2_Middle_y > Zebro_3_Middle_y) or (Zebro_2_Middle_y > Zebro_4_Middle_y) or (Zebro_1_Middle_y > Zebro_5_Middle_y)
                            or (Zebro_2_Middle_y > Zebro_6_Middle_y) or (Zebro_2_Middle_y > Zebro_7_Middle_y) or (Zebro_2_Middle_y > Zebro_8_Middle_y) or (Zebro_1_Middle_y > Zebro_9_Middle_y)
                            or (Zebro_2_Middle_y > Zebro_10_Middle_y) or (Zebro_2_Middle_y > Zebro_11_Middle_y) or (Zebro_2_Middle_y > Zebro_12_Middle_y) or (Zebro_1_Middle_y > Zebro_13_Middle_y)
                            or (Zebro_2_Middle_y > Zebro_14_Middle_y) or (Zebro_2_Middle_y > Zebro_15_Middle_y) or (Zebro_2_Middle_y > Zebro_16_Middle_y) or (Zebro_1_Middle_y > Zebro_17_Middle_y)
                            or (Zebro_2_Middle_y > Zebro_18_Middle_y) or (Zebro_2_Middle_y > Zebro_19_Middle_y) or (Zebro_2_Middle_y > Zebro_20_Middle_y):
                                Block = "South"
                                Bloking.append(Block)
                                Block = None
                            if (Zebro_2_Middle_y < Zebro_2_Middle_y) or (Zebro_2_Middle_y < Zebro_3_Middle_y) or (Zebro_2_Middle_y < Zebro_4_Middle_y) or (Zebro_2_Middle_y < Zebro_5_Middle_y)
                            or (Zebro_2_Middle_y < Zebro_6_Middle_y) or (Zebro_2_Middle_y < Zebro_7_Middle_y) or (Zebro_2_Middle_y < Zebro_8_Middle_y) or (Zebro_2_Middle_y < Zebro_9_Middle_y)
                            or (Zebro_2_Middle_y < Zebro_10_Middle_y) or (Zebro_2_Middle_y < Zebro_11_Middle_y) or (Zebro_2_Middle_y < Zebro_12_Middle_y) or (Zebro_2_Middle_y < Zebro_13_Middle_y)
                            or (Zebro_2_Middle_y < Zebro_14_Middle_y) or (Zebro_2_Middle_y < Zebro_15_Middle_y) or (Zebro_2_Middle_y < Zebro_16_Middle_y) or (Zebro_2_Middle_y < Zebro_17_Middle_y)
                            or (Zebro_2_Middle_y < Zebro_18_Middle_y) or (Zebro_2_Middle_y < Zebro_19_Middle_y) or (Zebro_2_Middle_y < Zebro_20_Middle_y):
                                Block = "North"
                                Bloking.append(Block)
                                Block = None
                        # Grab condition zebro 2:
                        PicoZebro = []
                        PicoZebro_2 = Zebro_2_Middle_x , Zebro_2_Middle_y, Direction_Zebro_2, Blocking
                        PicoZebro = PicoZebro_2
                        #release condition zebro 2
                    # Release Condition Serial Write. (Now movement can start.)
                    time.sleep(60)

                        # Once it is known to work for these two Pico Zebro's then the copy and paste will start for the rest
                Picture = 0
                #time.sleep(60)

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
    names = []
    condition = threading.Condition()
    
    Pico_Zebro_1 = Control_Zebro_Thread(names, condition, Pico_N1)
    Pico_Zebro_1.setName('Pico_Zebro_1')

    Pico_Zebro_2 = Control_Zebro_Thread(names, condition, Pico_N2)
    Pico_Zebro_2.setName('Pico_Zebro_2')
    
    main()
