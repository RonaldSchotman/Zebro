#!/usr/bin/env python
# TU Delft Pico Zebro Demo
# PZ_DEMO Fallback method 1
# Full Code for controlling and Detecting 1 Pico Zebro 
# Writer: Martijn de Rooij
# Version 0.05
# Using 1 led for tracking

# import the necessary packages
from picamera.array import PiRGBArray                                       # Pi camera Libary capture BGR video
from picamera import PiCamera                                               # PiCamera liberary
import time                                                                 # For sleep functions and video
import bluetooth
import numpy as np                                                          # Optimized library for numerical operations
import cv2                                                                  # Include OpenCV library for vision recognition
import queue                                                                # Library for Queueing. Savetly sharing variables between threads
import threading                                                            # Library for Multithreading

import serial                                                               # Serial uart library for raspberry pi
import serial.tools.list_ports;                                             # Library for obtaining evry port on the raspberry Pi

import random                                                               # Library so the Pico walks random in any direction without a pattern
import math 
# import the necessary packages for tracking
from imutils import contours                                                # A library from http://www.pyimagesearch.com/2016/10/31/detecting-multiple-bright-spots-in-an-image-with-python-and-opencv/
import imutils                                                              # For detecting bright spots in a image.

from Functions.Blocking import Blocking                                     # py program for comparing every zebro middlepoint with eachother

Block = Blocking()                                                          # For using the functions in Blocking.py with Block.Function_Name

# http://picamera.readthedocs.io/en/latest/fov.html
# initialize the Pi camera and grab a reference to the raw camera capture
camera = PiCamera()                                                         # Set the camera as PiCamera
camera.resolution = (1648, 928)                                             # Maximum Resolution with full FOV
camera.framerate = 40                                                       # Maximum Frame Rate with this resolution
rawCapture = PiRGBArray(camera, size=(1648, 928))                           # Rawcapture of vision with RGB

# allow the camera to warmup.
time.sleep(0.1)

# Turn leds on a specific PicoZebro on or off (ledNr = 0 to 5)
#ledNr 0 = Top Left Back Led.
#ledNr 1 = Top Left Front Led.
#ledNr 2 = Top Right Back Led.
#ledNr 3 = Top Right Front Led.
# Values are stored like 0b00000RGB so sending a 7(0b111) will turn all colors of one led package on. 
def setLed(connectionID, ledNr, value):
    global lastCommand
    msg = lastCommand = bytearray([connectionID, 1, 33 + ledNr, value, 255])# Adress 33(0x21) and up is for the leds
    arduino.write(msg)                                                      # Write the command to the zebro through the arduino
    getResult()                                                             # Wait for the arduino to finish the command

# Set the movement of the PicoZebro. Changing this will not force the state, the Zebro will finish what it was doing before entering new state.
# Possible values{ 0: IDLE, 1: FORWARD, 2: BACKWARDS, 3: TURN_LEFT, 4: TURN_RIGHT }
def setMovement(connectionID, value):                                       # Set Movement of Pico Zebro 
    global lastCommand                                                      # A global variable for LastCommand send to BLE module
    msg = lastCommand = bytearray([connectionID, 1, 32, value, 255])        # Adress 32(0x20) and up is for the movement states
    arduino.write(msg)                                                      # Write the command to the zebro through the arduino
    #print("setMovement:", getResult())                                      # Wait for the arduino to finish the command

class Check_Connected_thread(threading.Thread):
    def __init__(self,q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main): # initialize checking Connection
        ''' Constructor. of Connected Thread '''
        threading.Thread.__init__(self) 

        self.daemon = True                                                  # If main end this thread will end as wel with daemon set as True
        self.q_Control_Serial_Write = q_Control_Serial_Write                # Queue variable with maxsize of 1 for dermining what needs to be sent to which Pico Zebro
        self.q_Data_is_Send = q_Data_is_Send                                # An extra Queue variable for if needed to know in main code if something is send
        self.q_Control_Uart_Main = q_Control_Uart_Main                      # Control variable if Main is using Uart control or the Pico Zebro threads.

        self.start()
        
    def run(self):
        while True:
            while (self.q_Control_Uart_Main.empty() == False): # Wait untill you are allowed to write again.
                pass
                            
            if self.q_Control_Uart_Main.empty() == True:        # if the main doesn't have control send next movement otherwise you already should have been stuck before
                Writing = ("Global","Connect", "Devices")     
                self.q_Control_Serial_Write.put((2, Writing), block=True, timeout=None)
                print("checked Devices")
            time.sleep(2)
            print("check")

class UART_Thread(threading.Thread):                                        # UART Thread
    def __init__(self,q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main): # initialize UART thread for communication between BLE and Raspberry pi 
        ''' Constructor. of UART Thread '''
        threading.Thread.__init__(self) 

        self.daemon = True                                                  # If main end this thread will end as wel with daemon set as True
        self.q_Control_Serial_Write = q_Control_Serial_Write                # Queue variable with maxsize of 1 for dermining what needs to be sent to which Pico Zebro
        self.q_Data_is_Send = q_Data_is_Send                                # An extra Queue variable for if needed to know in main code if something is send
        self.q_Control_Uart_Main = q_Control_Uart_Main                      # Control variable if Main is using Uart control or the Pico Zebro threads.

        self.start()                                                        # Start Uart Thread

    def run(self):                                                          # run Uart Thread
        while True:                                                         # Run UArt thread untill main ends.
            Sended_Data = 0                                                 # Extra variable for checking if Data will be send is send
            time.sleep(0.2)
            if (self.q_Control_Serial_Write.empty() == False) or (Sended_Data == 1): # Check if there is data to send.
                Sended_Data = 1                                             # if Yes set Sended_Data to 1 untill data is send.
                Serial = self.q_Control_Serial_Write.get(block=False)       # Try to obtain next Queue variable for sending command 
                print(Serial)                                               # Say what has the be send and if the main or a Pico Zebro thread is sending it.
                #Serial is obtained as follows:
                #Serial[0] = priority of Queue, Serial[1][0] = Which Pico Zebro thread or Main is sending the Data
                #Serial[1][1] = Which device or devices need the command needs to be send to, Serial[1][2] = The actual command
                
                if Serial[1][0] == "Main":                                  # If main has to send data 
                    if Serial[1][1] == 'Global':                            # If it has to be send to each device
                        if Serial[1][2] == 'Leds_off':                      # if the global command is leds off.
                            for x in range(3):                              # Go over each Zebro and set it the leds to 0
                                #print(x)
                                setLed(connectionID=x, ledNr=0, value=0)    # Set led top left  back  OFF(1)
                                time.sleep(0.1)                            # A small delay which was seemingly necessary for BLE communication over UART
                                setLed(connectionID=x, ledNr=1, value=0)    # Set led top left  front OFF(1)
                                time.sleep(0.1)
                                setLed(connectionID=x, ledNr=2, value=0)    # Set led top right back  OFF(1)
                                time.sleep(0.1)
                                setLed(connectionID=x, ledNr=3, value=0)    # Set led top right front OFF(1)
                                time.sleep(0.1)
                                setLed(connectionID=x, ledNr=4, value=0)    # Set led Front left   OFF(1)
                                time.sleep(0.1)
                                setLed(connectionID=x, ledNr=5, value=0)    # Set led Front right  OFF(1)
                                time.sleep(0.1)
                        elif Serial[1][2] == 'Stop':                        # If the global command is Stop
                            for x in range(3):                              # Make every Zebro stop
                                setMovement(x, 0)                           # Set movement to IDLE = Stop.
                        elif Serial[1][2] == 'Led1_on':                     # if the global command is Led1_on
                            for x in range(3):                              # Make every Zebro turn Led1_on
                                setLed(connectionID=0, ledNr=3, value=7)    # Turn led 1 on
                        elif Serial[1][2] == "Led2_on":                     # An extra led if it possible to realtime find the Pico Zebro's
                            for x in range(3):                              # A loop over every possible Zebro
                                setLed(connectionID=0, ledNr=1, value=7)    # Turn led 3 on
                        elif Serial[1][2] == "Led3_on":                     # An extra led if it possible to realtime find the Pico Zebro's
                            for x in range(3):                              # A loop over every possible Zebro
                                setLed(connectionID=0, ledNr=2, value=7)    # Turn led 3 on
                    elif Serial[1][1] == 'Pico_N1':                         # This has to made for every Pico Zebro for controlling it seperatly with the Main
                        if Serial[1][2] == 'Led1_on':                       # The three used commands are Led1_on, Led3_on and Leds_off
                            setLed(connectionID=0, ledNr=3, value=7)        # Turn Led1_on 
                        elif Serial[1][2] == 'Led3_on':                       # For  when led needs to be turned on
                            setLed(connectionID=0, ledNr=2, value=7)        # Turn Led3_on
                        elif Serial[1][2] == 'Led2_on':                       # For  when led needs to be turned on
                            setLed(connectionID=0, ledNr=1, value=7)        # Turn Led3_on
                        elif Serial[1][2] == 'Leds_off':                    # If everything is done correctly ot should not be possible there are more than these 2 leds on
                            setLed(connectionID=0, ledNr=3, value=0)        # Turn Led1_off
                            time.sleep(0.01)                                # A small delay was seemingly necessary the bluetooth bus couldn't take it otherwise
                            setLed(connectionID=0, ledNr=2, value=0)        # Turn Led3_off
                            time.sleep(0.01)                                # A small delay was seemingly necessary the bluetooth bus couldn't take it otherwise
                            setLed(connectionID=0, ledNr=1, value=0)        # Turn Led3_off
                            
                    elif Serial[1][1] == 'Pico_N2':                         # This has to made for every Pico Zebro for controlling it seperatly with the Main
                        if Serial[1][2] == 'Led1_on':                       # The three used commands are Led1_on, Led3_on and Leds_off
                            setLed(connectionID=0, ledNr=3, value=7)        # Turn Led1_on 
                        elif Serial[1][2] == 'Led3_on':                       # For  when led needs to be turned on
                            setLed(connectionID=0, ledNr=2, value=7)        # Turn Led3_on
                        elif Serial[1][2] == 'Led2_on':                       # For  when led needs to be turned on
                            setLed(connectionID=0, ledNr=1, value=7)        # Turn Led3_on
                        elif Serial[1][2] == 'Leds_off':                    # If everything is done correctly ot should not be possible there are more than these 2 leds on
                            setLed(connectionID=0, ledNr=3, value=0)        # Turn Led1_off
                            time.sleep(0.01)                                # A small delay was seemingly necessary the bluetooth bus couldn't take it otherwise
                            setLed(connectionID=0, ledNr=2, value=0)        # Turn Led3_off
                            time.sleep(0.01)                                # A small delay was seemingly necessary the bluetooth bus couldn't take it otherwise
                            setLed(connectionID=0, ledNr=1, value=0)        # Turn Led3_off
                    elif Serial[1][1] == 'Pico_N3':                         # This has to made for every Pico Zebro for controlling it seperatly with the Main
                        if Serial[1][2] == 'Led1_on':                       # The three used commands are Led1_on, Led3_on and Leds_off
                            setLed(connectionID=0, ledNr=3, value=7)        # Turn Led1_on 
                        elif Serial[1][2] == 'Led3_on':                       # For  when led needs to be turned on
                            setLed(connectionID=0, ledNr=2, value=7)        # Turn Led3_on
                        elif Serial[1][2] == 'Led2_on':                       # For  when led needs to be turned on
                            setLed(connectionID=0, ledNr=1, value=7)        # Turn Led3_on
                        elif Serial[1][2] == 'Leds_off':                    # If everything is done correctly ot should not be possible there are more than these 2 leds on
                            setLed(connectionID=0, ledNr=3, value=0)        # Turn Led1_off
                            time.sleep(0.01)                                # A small delay was seemingly necessary the bluetooth bus couldn't take it otherwise
                            setLed(connectionID=0, ledNr=2, value=0)        # Turn Led3_off
                            time.sleep(0.01)                                # A small delay was seemingly necessary the bluetooth bus couldn't take it otherwise
                            setLed(connectionID=0, ledNr=1, value=0)        # Turn Led3_off 
                    Sended_Data = 0                                         # Data is send
                    #print("Main_Wrote")                                     # For debug, for showing which thread was the last to try to write over Uart
                    
                # For Each Pico such an elif:    
                elif Serial[1][0] == "Pico_N1":                             # if Pico_N1 has to send data for now only four commands
                    if Serial[1][1] == "Pico_N1":                           # This should be Pico_Nx or the wrong pico is writing to it.
                        connection_Pico_1 = 0                               # This is the bluetooth address of the Pico Zebro 1 for Zebro 2 it is 1
                        if Serial[1][2] == "Stop":                          # Make Pico Zebro 1 stop
                            setMovement(connection_Pico_1, 0)
                        elif Serial[1][2] == "Forward":                     # Let Pico Zebro 1 Move Forward
                            setMovement(connection_Pico_1, 1)
                        elif Serial[1][2] == "Right":                       # Let Pico Zebro 2 Move Right
                            setMovement(connection_Pico_1, 4)
                        elif Serial[1][2] == "Left":                        # Let Pico Zebro Move Left
                            setMovement(connection_Pico_1, 3)
                    else:
                        print("This is the wrong Pico")                     # Extra check for if it is send to the wrong Pico
                    Sended_Data = 0
                    #print("Pico_Zebro_1_Wrote")

                 # For Each Pico such an elif:    
                elif Serial[1][0] == "Pico_N2":                             # if Pico_N1 has to send data for now only four commands
                    if Serial[1][1] == "Pico_N2":                           # This should be Pico_Nx or the wrong pico is writing to it.
                        connection_Pico_1 = 0                               # This is the bluetooth address of the Pico Zebro 1 for Zebro 2 it is 1
                        if Serial[1][2] == "Stop":                          # Make Pico Zebro 1 stop
                            setMovement(connection_Pico_1, 0)
                        elif Serial[1][2] == "Forward":                     # Let Pico Zebro 1 Move Forward
                            setMovement(connection_Pico_1, 1)
                        elif Serial[1][2] == "Right":                       # Let Pico Zebro 2 Move Right
                            setMovement(connection_Pico_1, 4)
                        elif Serial[1][2] == "Left":                        # Let Pico Zebro Move Left
                            setMovement(connection_Pico_1, 3)
                    else:
                        print("This is the wrong Pico")                     # Extra check for if it is send to the wrong Pico
                    Sended_Data = 0
                    #print("Pico_Zebro_1_Wrote")
                    
                 # For Each Pico such an elif:    
                elif Serial[1][0] == "Pico_N3":                             # if Pico_N1 has to send data for now only four commands
                    if Serial[1][1] == "Pico_N3":                           # This should be Pico_Nx or the wrong pico is writing to it.
                        connection_Pico_1 = 0                               # This is the bluetooth address of the Pico Zebro 1 for Zebro 2 it is 1
                        if Serial[1][2] == "Stop":                          # Make Pico Zebro 1 stop
                            setMovement(connection_Pico_1, 0)
                        elif Serial[1][2] == "Forward":                     # Let Pico Zebro 1 Move Forward
                            setMovement(connection_Pico_1, 1)
                        elif Serial[1][2] == "Right":                       # Let Pico Zebro 2 Move Right
                            setMovement(connection_Pico_1, 4)
                        elif Serial[1][2] == "Left":                        # Let Pico Zebro Move Left
                            setMovement(connection_Pico_1, 3)
                    else:
                        print("This is the wrong Pico")                     # Extra check for if it is send to the wrong Pico
                    Sended_Data = 0
                    #print("Pico_Zebro_1_Wrote")
                        
                elif Serial[1][0] == "Global":                              # A Command which every Pico Zebro can send but not the main. 
                    if Serial[1][1] == "Connect":                           # To check if the specific Pico Zebro is connected to the bluetooth module
                        try:
                            getConnected()                                  # Update the list with connected devices every frame
                        except serial.serialutil.SerialException:           # In case something went wrong
                            pass                                            # Because every Pico Zebro does this check it is allowed to just pass
                    Sended_Data = 0
                    print("Check Connection")
                
                elif (Sended_Data == 1):                                    # Extra check for if data is not send but to make sure code doesn't get stuck
                    print("Didnt Send Data")                                # debug print
                    Sended_Data = 0
                

class Control_Zebro_Thread(threading.Thread):                               # The Control Pico Zebro Thread. For each possible Zebro A thread is created.
    def __init__(self,q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main, Zebro, q_PicoZebro, q_Pico_Direction, q_Pico_Angle):
        ''' Constructor. of Control Thread '''
        threading.Thread.__init__(self)

        self.daemon = True                                                  # If main end this thread will end as wel with daemon set as True
        self.q_Control_Serial_Write = q_Control_Serial_Write                # Queue variable with maxsize of 1 for dermining what needs to be sent to which Pico Zebro
        self.q_Data_is_Send = q_Data_is_Send                                # An extra Queue variable for if needed to know in main code if something is send
        self.q_Control_Uart_Main = q_Control_Uart_Main                      # Control variable if Main is using Uart control or the Pico Zebro threads.
        
        self.Zebro = Zebro                                                  # Name of the Zebro

        self.q_PicoZebro = q_PicoZebro                                      # This is the middle point of the Pico Zebro.
        self.q_Pico_Direction = q_Pico_Direction                            # Which Direction The Pico Zebro is facing
        self.q_Pico_Angle = q_Pico_Angle                                    # A Angle which the Pico Zebro is turned with (This doesn't work yet)
        
        self.start()                                                        # Start the Zebro Thread

    def run(self):
        print(self.Zebro)                                                   # Say which Zebro thread has started

        if self.Zebro == 'Pico_N1':                                         # Elif for every Zebro + 1
            Connected_To = 0                                                # Connected_To for Pico_N2 is then: 1
        elif self.Zebro == 'Pico_N2':                                         # Elif for every Zebro + 1
            Connected_To = 1                                                # Connected_To for Pico_N2 is then: 1
        elif self.Zebro == 'Pico_N3':                                         # Elif for every Zebro + 1
            Connected_To = 2                                                # Connected_To for Pico_N2 is then: 1
        
        Connected = 0                                                       # At the start Connection is always 0
        Sleep = 0                                                           # Also doesn't Need to sleep at the start
        Last_Movement = "Stop"                                              # At start Movement is always stop.
        
        Middle_point_x = 0                                                  # Make middle point X coordinate 0 
        Middle_point_y = 0                                                  # Make middle point Y coordinate 0 
        Movement_Blocked = 0                                                # There are no movements blocked at the start.
        DONT_Send = 0                                                       # if the way is blocked it does not need to send the Movement
        Blocked_Direction = []                                              # Which Directions are Blocked
        Current_Direction = ""                                              # What the Current Direction of the Pico Zebro is 
        
        while True:                                                         # Run thread until Main has ended
            if Connected == 0:                                              # Check if the Zebro has to connect or is connected
                Last_Movement = "Stop"                                      # Last Movement is always Stop when it is not connected
                
                #For checking connected Devices
                Connected_Devices = []                                      # Which Devices are connected
                
                # Obtain Serial condition
                # Check if Main is writing in Uart. If so wait untill main is finished
                while (self.q_Control_Uart_Main.empty() == False):          # Wait untill you are allowed to write again.
                    pass
                        
                if (self.q_Control_Uart_Main.empty() == True):              # Obtain which Zebro has connected
                    Connected_Devices = connectedArray                      # in the global Variable connectedArray must stand which devices are connected
                    #print(self.Zebro+" Checked Devices")

                #print(Connected_Devices)                                    # Extra check for which devices are connected
                
                if Connected_Devices[Connected_To] == 1:                    # self.Zebro:   # Needs to be Pico_Nx
                    print(self.Zebro+" Will be Connected")                  # Yes it is in Connected Devices
                        
                    PicoZebro = self.q_PicoZebro.get(block=True, timeout=None)
                    
                    Middle_point_x = PicoZebro[0]                           # Obtain first found middle Point X , Y and Blocked Direction
                    Middle_point_y = PicoZebro[1]
                    Blocked_Direction = PicoZebro[2]
                    print(PicoZebro)                                        # Debug to check if it is done correctly
                        
                    Current_Direction = self.q_Pico_Direction.get(block=True, timeout=None) # Also obtain current Direction
                        
                    Connected = 1                                           # Connected wil be made 1
                    Sleep = 0                                               # Also the Zebro Will not go to sleep but will try to control
                        
                else:                                                       # Send the Pico Zebro thread to sleep if it isn't connected
                    Connected = 0                                           # Connected stays 0
                    Sleep = 1
                
                if not Connected_Devices:                                   # Extra check if there are no devices connected.
                    Sleep = 1
                    
                if Sleep == 1:
                    print("SLEEEPING "+self.Zebro)                          # check for which Zebro's are sleeping
                    time.sleep(30)                                          # Sleep so that the Pico Zebro thread will not overhead the CPU (if this becomes a problem which might)
                    Sleep = 0
                
            if Connected == 1:
                if Connected_Devices[Connected_To] == 1:                    # Extra check if the Pico Zebro is stil connected
                    Connected_Devices = connectedArray                      # in the global Variable connectedArray must stand which devices are connected
                    #Connected = 1
                elif Connected_Devices[Connected_To] == 0:
                    Connected = 0                                           # just as the print says The connection has been lost with the Pico so stop trying to control it
                    print("Lost Connection")
                    
                # From here on out the actual controlling of the Pico Zebro

                # Obtain from Queue the middle point. Also here you need to wait with controlling untill the first value is set. 
                try: 
                    PicoZebro = self.q_PicoZebro.get(block=True, timeout=3) # obtain middle point and blocked Direction when possible
                    Middle_point_x = PicoZebro[0]
                    Middle_point_y = PicoZebro[1]
                    Blocked_Direction = PicoZebro[2]
                except queue.Empty:                                         # if the queue is empty use old data (Change this happens is extremely small when connected considering detection goes fast)
                    Middle_point_x = Middle_point_x
                    Middle_point_y = Middle_point_y
                    Blocked_Direction = Blocked_Direction
                    print("No new Data")

                # The current Direction
                try:
                    Current_Direction = self.q_Pico_Direction.get(block=True, timeout=3) # For now Direction only gets determined at the start a test is underway to check if it is possible to keep updating it
                except queue.Empty:
                    Current_Direction = Current_Direction
                    print("No new Direction")

                # if the Zebro is connected but not foundt the middle point = 0.
                if (Middle_point_x == 0) or (Middle_point_y == 0):
                    while (self.q_Control_Uart_Main.empty() == False): # Wait untill you are allowed to write again.
                        pass
                        
                    if self.q_Control_Uart_Main.empty() == True:        # if the main doesn't have control send next movement otherwise you already should have been stuck before
                        Last_Movement == "Stop"
                        Writing = (self.Zebro,self.Zebro, Last_Movement)        # Make the Pico Zebro stop no matter what if it is lost
                        self.q_Control_Serial_Write.put((2, Writing), block=True, timeout=None)
                    
                    # In case the Pico Zebro has been removed and placed back let it cricle around on certain pre set points
                    #print("Stopping")
                    Connected = 0
                
                elif (Middle_point_x > 0) and (Middle_point_y > 0):
                    
                    # This is for determing the next Movement with change. Except for Stop the Movement change will be determined with highest change of being the same as Last Movement 
                    if Last_Movement == "Stop":
                        Random_N = random.randrange(1,100)                  # if the last movement of the Pico Zebro was to stop (always this at the start
                        if Random_N <= 70:                                  # it has a 60% change to move forward afterwards
                            Movement = "Forward"
                        elif Random_N > 70 and Random_N <= 80:              # 10% Change to keep standing still
                            Movement = "Stop"
                        elif Random_N > 80 and  Random_N <= 90:             # 10% Change to go to the right
                            Movement = "Right"
                        elif Random_N > 90 and  Random_N <= 100:            # 10% Change to go to the left
                            Movement = "Left"

                    if Last_Movement == "Forward":                          # If the last movement was Forward it has 80% change to keep moving forward
                        Random_N = random.randrange(1,100)                  # It almost always to have the highest change to keep moving forward
                        if Random_N <= 80:                                  # The random.randrange create a number everytime to create a change to change the movement
                            Movement = "Forward"
                        elif Random_N > 80 and Random_N <= 90:              # 10% Change to keep standing still
                            Movement = "Stop"
                        elif Random_N > 90 and Random_N <= 95:              # 5% Change to go to the right
                            Movement = "Right"
                        elif Random_N > 95 and Random_N <= 100:             # 5% Change to go to the left
                            Movement = "Left"

                    if Last_Movement == "Right":                            # Last movement was right so 50% change to keep going right
                        Random_N = random.randrange(1,100)
                        if Random_N <= 25:                                  # 25% change to move Forward after moving right
                            Movement = "Forward"
                        elif Random_N > 25 and Random_N <= 35:              # 10% change to stop again
                            Movement = "Stop"
                        elif Random_N > 35 and Random_N <= 95:              # 60% to keep moving right
                            Movement = "Right"
                        elif Random_N > 95 and Random_N <= 100:             # 5% To go suddenly to left
                            Movement = "Left"
     
                    if Last_Movement == "Left":                             # Last movement was left so 50% to keep moving left
                        Random_N = random.randrange(1,100)
                        if Random_N <= 25:                                  # 25% to go Forward
                            Movement = "Forward"    
                        elif Random_N > 25 and Random_N <= 35:              # 10% to stop
                            Movement = "Stop"
                        elif Random_N > 35 and Random_N <= 40:              # 5% to suddenly go right
                            Movement = "Right"
                        elif Random_N > 40 and Random_N <= 100:             # 60% to keep moving right
                            Movement = "Left"
                            
                    # If Direction works THIS can go away because direction keeps direction updated
                    
                    # Once the movement is determined Create the next direction because this will only be tested once. 
                    if Movement == "Forward":
                        Direction = Current_Direction
                    elif Movement == "Stop":
                        Direction = Current_Direction
                    elif Movement == "Right":
                        if Current_Direction == "North":
                            Direction = None
                        elif Current_Direction == "East":
                            Direction = None
                        elif Current_Direction == "South":
                            Direction = None
                        elif Current_Direction == "West":
                            Direction = None
                    elif Movement == "Left":
                        if Current_Direction == "North":
                            Direction = None
                        elif Current_Direction == "West":
                            Direction = None
                        elif Current_Direction == "South":
                            Direction = None
                        elif Current_Direction == "East":
                            Direction = None
                            
                    # After the next direction is determined then check one more time if the direction is blocked
                    for Names in Blocked_Direction:
                        if Direction == Names:
                            DONT_Send = 1
                    print(Movement)        
                    if DONT_Send == 1: # If the direction is blocked make the Pico Zebro stop and try to figure out his next direction
                        # Obtain Serial Write
                        # Check if Main is writing in Uart. If so wait untill main is finished
                        while (self.q_Control_Uart_Main.empty() == False):  # Wait untill you are allowed to write again.
                            pass
                        
                        if self.q_Control_Uart_Main.empty() == True:        # Stop the Zebro when it tries to go somewhere where it should not go
                            Writing = (self.Zebro,self.Zebro, "Stop")
                            
                            self.q_Control_Serial_Write.put((2, Writing), block=True, timeout=None)
                            print("The Zebro has been stopped")
                            print(Writing)
                            #Release Serial Write
                    else:
                        # Obtain Serial Write
                        # Check if Main is writing in Uart. If so wait untill main is finished
                        while (self.q_Control_Uart_Main.empty() == False): # Wait untill you are allowed to write again.
                            pass
                        
                        if self.q_Control_Uart_Main.empty() == True:        # if the main doesn't have control send next movement otherwise you already should have been stuck before
                            Writing = (self.Zebro,self.Zebro, Movement)     # The change this can go wrong is extremly small but possible.
                            self.q_Control_Serial_Write.put((2, Writing), block=True, timeout=None)
                            print("Zebro is moving")
                            print(Writing)
                            
                        Last_Movement = Movement
                        #Current_Direction = Direction
                        
                    DONT_Send = 0

def Image_Difference(Image):
    # making sure light doesn't matter
    lowValY = 150                       
    highValY = 100
    New_image = np.asarray(Image)
    low_values_indices = New_image > lowValY                                # Where values are low
    high_values_indices = New_image < highValY                              # Where values are high
    New_image[low_values_indices] = 0                                       # All low values set to 0
    New_image[high_values_indices] = 0                                      # All high values set to 0
    return New_image

def Find_Orientation(x_Led_1,x_Led_3,y_Led_1,y_Led_3):                      # A Function to dermine the orientation of the Pico Zebro
    x_middle = 0                                                            # First make everything 0 to make sure the last value will not invluence the result
    y_middle = 0
    Angle = 0
    Direction = None
    # Angle Calculation is not correct yet.
    #print(x_Led_1,x_Led_3,y_Led_1,y_Led_3)

    #No points Found
    if(x_Led_1 or x_Led_3 or y_Led_1 or y_Led_3) == 0:
        x_middle = 0                                                            # First make everything 0 to make sure the last value will not invluence the result
        y_middle = 0
        Angle = 0
        Direction = None
        x_Led_1 = 0
        x_Led_3 = 0
        y_Led_1 = 0
        y_Led_3 = 0
    
    #Facing North (dermine middle point)
    elif (x_Led_1 <= x_Led_3) and (y_Led_1 <= y_Led_3):                      # This means north is upper left of the camera frame with 0.0 being the most north
        # Pico Zebro is facing North
        # Middle Point Zebro is:
        x_middle = ((x_Led_3 - x_Led_1) + x_Led_1)                          # The calculations for finding the middle point of the Zebro
        y_middle = ((y_Led_3 - y_Led_1) + y_Led_1)                          
        Angle = 360 - ((abs(x_Led_3 - x_Led_1))*1.384)                      # From 360-270 in degrees is north
        Direction = "North"
    
    elif (x_Led_1 < x_Led_3) and (y_Led_1 > y_Led_3):
        # Pico Zebro is facing East
        # Middle Point Zebro is:
        x_middle = ((x_Led_3 - x_Led_1) + x_Led_1)
        y_middle = ((y_Led_1 - y_Led_3) + y_Led_3)
        Angle = 0 + ((abs(x_Led_3 - x_Led_1))*1.384)                        # From 0-90 in degress is East which is the upper right
        Direction = "West"
    
    elif (x_Led_1 >= x_Led_3) and (y_Led_1 >= y_Led_3):
        # Pico Zebro is facing South
        # Middle Point Zebro is:
        x_middle = ((x_Led_1 - x_Led_3) + x_Led_3)
        y_middle = ((y_Led_1 - y_Led_3) + y_Led_3)
        Angle = 180 - ((abs(x_Led_1 - x_Led_3))*1.384)                      # From 180-90 in degrees is south which is the lower right
        Direction = "South"
    
    elif (x_Led_1 > x_Led_3) and (y_Led_1 < y_Led_3):
        # Pico Zebro is facing West
        # Middle Point Zebro is:
        x_middle = ((x_Led_1 - x_Led_3) + x_Led_3)
        y_middle = ((y_Led_3 - y_Led_1) + y_Led_1)
        Angle = 270 - ((abs(x_Led_1 - x_Led_3))*1.384)                      # From 270-180 in degrees is West which is the lower left of the picture
        Direction = "East"

    return x_middle, y_middle, Direction, Angle

# Update the connectedArray array with the conencted state of all devices, array is 20 items long
def getConnected():
    global connectedArray
    global lastCommand
    msg = lastCommand = bytearray([20, 0, 0, 0, 255])                       # The command for getting the list of connected devices
    arduino.write(msg)                                                      # Write the command to the zebro through the arduino
    res = getResult()
    if res[-1] == 255 and len(res) == 22:
        connectedArray = res[1:]                                            # Remove the status byte from the front

def main(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main,         # The main in here for every possible Zebro the Direction, Angle and middlepoint queue needs to be given
         q_PicoZebro_1, q_PicoZebro_2, q_PicoZebro_3,
         q_Pico_Direction_1, q_Pico_Direction_2, q_Pico_Direction_3,
         q_Pico_Angle_1, q_Pico_Angle_2, q_Pico_Angle_3):
    
    # Initialize Picture to 0 for the first time when program starts.
    Picture = 0                                                             # Picture is the variable which determines which step the main is at. Now there are 8 steps where some steps will be done multiple times
    Devices = 0                                                             # This is for checking every possible Pico Zebro
    
    Old_Direction_Pico_1 = None
    Old_Zebro_1_Middle_x = 0
    Old_Zebro_1_Middle_y = 0

    Old_Direction_Pico_2 = None
    Old_Zebro_2_Middle_x = 0
    Old_Zebro_2_Middle_y = 0

    Old_Direction_Pico_3 = None
    Old_Zebro_3_Middle_x = 0
    Old_Zebro_3_Middle_y = 0
    
    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):  # BGR is the standard way for OpenCV
        # grab the NumPy array representing the image, the initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array                                                 # from the array put it in image

        # Obtain ROI which is the Hexagon.
        mask = np.zeros(image.shape, dtype=np.uint8)
        roi_corners = np.array([[(1260,910), (1430,810), (1420,110), (1230,10), (420,10), (220,130), (225,820), (390,910)]], dtype=np.int32)
        # fill the ROI so it doesn't get wiped out when the mask is applied
        channel_count = image.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,)*channel_count
        cv2.fillPoly(mask, roi_corners, ignore_mask_color)
        # from Masterfool: use cv2.fillConvexPoly if you know it's convex
        # apply the mask
        image = cv2.bitwise_and(image, mask)
        
        # Take current day for testing purposes.
        Timetest = time.strftime("%d-%m-%Y")
        # Show the current view for debugging and for ending the program savetly
        cv2.imshow("original %s" % Timetest,image)
        
        if Picture == 1:
            if q_Control_Uart_Main.empty() == True:                         # if the queue is empty fill it 
                Main_Control_Uart = 1                                       # Take control of UArt thread so the Pico Zebro threads will not intervere with distinction
                print("MAIN Acquired LOCK")                                 # debug print for saying the Main has total control of the Pico Zebro now
                q_Control_Uart_Main.put((1), Main_Control_Uart)             # Now take complete control by filling the queue
                
            elif q_Control_Uart_Main.empty() == False:                      # else empty it before filling it again with the next data.
                Main_Control_Uart = 1                                       # if the main didnt empty it properly which should not be possible but for savetly done anyway
                q_Control_Uart_Main.mutex.acquire()
                q_Control_Uart_Main.queue.clear()
                q_Control_Uart_Main.all_tasks_done.notify_all()
                q_Control_Uart_Main.unfinished_tasks = 0
                q_Control_Uart_Main.mutex.release()
                q_Control_Uart_Main.put(1, Main_Control_Uart)
 
            if q_Control_Serial_Write.empty() == False:                     # empty all data and let the Pico Zebro's redo their stuff for writing
                q_Control_Serial_Write.mutex.acquire()                      # To make sure there are no commands of the Pico Zebro in the queue in between
                q_Control_Serial_Write.queue.clear()
                q_Control_Serial_Write.all_tasks_done.notify_all()
                q_Control_Serial_Write.unfinished_tasks = 0
                q_Control_Serial_Write.mutex.release()

            Writing = ("Main","Global", "Stop")                             # Send to Uart Thread stop all Pico Zebro's
            q_Control_Serial_Write.put((1, Writing), block=True, timeout=None)
            print("writing to serial")
            time.sleep(1)
                
            Writing = ("Main","Global", "Leds_off")                         # Send to Uart Thread all Leds_off for every Pico Zebro's
            q_Control_Serial_Write.put((1, Writing), block=True, timeout=None)
            
            time.sleep(2)
            
        # Take original Picture minimal after first loop for the first frame to avoid weird pictures.
        if Picture == 2:                                                    # Step 1 for Pico Control is taking the original picture and taking control of thread UART Control
                                                               # Give the command some time to finish with turning all leds off.
            Zebro_1_Middle_x = 0                                            # Reset all values for calculations. This needs to be done for every Zebro
            Zebro_1_Middle_y = 0
            PicoZebro_1 = []

            Zebro_2_Middle_x = 0                                            # Reset all values for calculations. This needs to be done for every Zebro
            Zebro_2_Middle_y = 0
            PicoZebro_2 = []
            
            cv2.imwrite("Image1.jpg", image)                       # Save a picture to Image1.jpg This will be the original picture
            
            Original = cv2.imread("Image1.jpg")                             # This is the original picture where the diferences will be compared with.
            
        if Picture == 3:                                                    # In order to make every step work it is devided in Picture steps. With after each step a new frame is taken
            print("Picture %d"%Picture)                                     # Otherwise you set leds on but do it after the fram is already taken at the top.
            Devices_Serial = Devices + 1                                    # Devices_Serial says which Pico Zebro middle point will be calculated first.
            
            #If Correctly done we still have the lock of Serial Write/read
            Writing = ("Main","Pico_N%s"% Devices_Serial, "Led1_on")        # Turn Led 1 on of the Pico Zebro
            q_Control_Serial_Write.put((1, Writing), block=True, timeout=None)
            time.sleep(1)                                                   # Give the Uart some time to turn it on
        
        if Picture == 4:    # Make Picture 2 for taking Picture 2 with Led 1 on.
            print("Picture %d"%Picture)
            cv2.imwrite("Image2.jpg", image)                 # Take the second picture with led 1 on.
            
            #If Correctly done we still have the lock of Serial Write/read
            Writing = ("Main","Pico_N%s"% Devices_Serial, "Leds_off")       # Turn led 1 off again         
            q_Control_Serial_Write.put((1, Writing), block=True, timeout=None)
            
        if Picture == 5:
            print("Picture %d"%Picture)
            
            #If Correctly done we still have the lock of Serial Write/read
            Writing = ("Main","Pico_N%s"% Devices_Serial, "Led3_on")        # Turn led 3 on            
            q_Control_Serial_Write.put((1, Writing), block=True, timeout=None)
            time.sleep(1)                                                   # Give the Uart some time to turn it on

         #Again do some other stuff
        if Picture == 6:
            print("Picture %d"%Picture)
            cv2.imwrite("Image3.jpg", image)                 # Take the the third picture with Led 3 on.

            Writing = ("Main","Pico_N%s"% Devices_Serial, "Leds_off")       # Turn led 3 off again         
            q_Control_Serial_Write.put((1, Writing), block=True, timeout=None)
            time.sleep(1)                                                   # Give the Uart some time to turn all leds off
            
        if Picture == 7:
            print("Picture %d"%Picture)                                     # Debug print for saying where the code is
            # Take both pictures with the leds.
            
            Led_1 = cv2.imread("Image2.jpg")                                # Take the picture with Led 1 on
            Led_3 = cv2.imread("Image3.jpg")                                # Take the picture with Led 3 on

            New_image_Led_1 = abs(Original - Led_1)                     
            New_image_Led_3 = abs(Original - Led_3)
            Difference_led_1 = Image_Difference(New_image_Led_1)            # Make only the led 1 visible which should be the only difference in the picture
            Difference_led_3 = Image_Difference(New_image_Led_3)            # Make only the led 3 visible

            Finding_Canny_Led_1 = cv2.Canny(Difference_led_1, 15, 200)      # cv2,Canny find all edges in a images
            Finding_Canny_Led_3 = cv2.Canny(Difference_led_3, 15, 200)      # Which finds the original edges of led1 and led3
                    
            Finding_Canny_Led_1 = cv2.morphologyEx(Finding_Canny_Led_1, cv2.MORPH_CLOSE, np.ones((8,8),np.uint8)) # To make sure only led 1 and
            Finding_Canny_Led_3 = cv2.morphologyEx(Finding_Canny_Led_3, cv2.MORPH_CLOSE, np.ones((8,8),np.uint8)) # Led 3 are detected fill up the canny's so it becomes one big one

            Finding_Canny_Led_1 = cv2.Canny(Finding_Canny_Led_1, 100, 200)  # Some techniques to make sure it is only 1 led which is seen.
            Finding_Canny_Led_3 = cv2.Canny(Finding_Canny_Led_3, 100, 200)  # Some techniques to make sure it is only 1 led which is seen.

            (_, contours_Led_1, _) = cv2.findContours(Finding_Canny_Led_1.copy(), cv2.RETR_EXTERNAL,
                                                      cv2.CHAIN_APPROX_NONE) # Find the contours of Led 1
            (_, contours_Led_3, _) = cv2.findContours(Finding_Canny_Led_3.copy(), cv2.RETR_EXTERNAL,
                                                      cv2.CHAIN_APPROX_NONE) # Find the contours of Led 3
            x_Led_1 = 0                                                      # Reset the values so Pico 1 will not be confused with Pico 2 etc.
            y_Led_1 = 0                                                     # For finding Led 1 of the specific Pico Zebro
            w_Led_1 = 0
            h_Led_1 = 0

            x_Led_3 = 0                                                     # For finding Led 3 of the specific Pico Zebro
            y_Led_3 = 0
            w_Led_3 = 0
            h_Led_3 = 0 
                
            areaArray_Led_1 = []                                            # For putting all found contours in a list
            areaArray_Led_3 = []                                            # By doing this only the largest which should be the led will be detected 
                
            for i, c in enumerate(contours_Led_1):                          # Put all contours of led 1 in a array
                area_led_1 = cv2.contourArea(c)
                areaArray_Led_1.append(area_led_1)

            for i, c in enumerate(contours_Led_3):                          # Put all contours of led 3 in a array
                area_led_3 = cv2.contourArea(c)
                areaArray_Led_3.append(area_led_3)

            sorteddata_Led_1 = sorted(zip(areaArray_Led_1, contours_Led_1), key=lambda x: x[0], reverse=True) # Sort the contours from largest (Led should be the largest)
            sorteddata_Led_3 = sorted(zip(areaArray_Led_3, contours_Led_3), key=lambda x: x[0], reverse=True)

            try:
                Largest_contour_led_1 = sorteddata_Led_1[0][1]              # Take the largest contour of Led 1
                [x_Led_1,y_Led_1,w_Led_1,h_Led_1] = cv2.boundingRect(Largest_contour_led_1) # And find the top left coordinates of the led with x and y and the width and height of the led 
            except (IndexError, cv2.error) as e:                            # In case there is no led a cv2,error will occur.
                print("Nothing Found")
                pass

            try:
                Largest_contour_led_3 = sorteddata_Led_3[0][1]              # Take the largest contour of Led 3
                [x_Led_3,y_Led_3,w_Led_3,h_Led_3] = cv2.boundingRect(Largest_contour_led_3)
            except (IndexError, cv2.error) as e:                            # In case there is no led a cv2,error will occur.
                print("Nothing Found")
                pass
            #LEDS_Image = cv2.addWeighted(Difference_led_1,1,Difference_led_3,1,0) # Debug for showing the picture is taken correctly
            #cv2.imwrite("Leds_Tog1.jpg", LEDS_Image)                        # it will be written to Leds_Tog1.jpg
            
            (Zebro_Middle_x,Zebro_Middle_y,Direction, Angle) = Find_Orientation(x_Led_1,x_Led_3,y_Led_1,y_Led_3) # Find the orientation of the Pico Zebro
            print(Zebro_Middle_x,Zebro_Middle_y,Direction, Angle)           # Debug print
            
            if Devices == 0:                                                # For every Pico Zebro these values have to be assigned
                #set data from PZ 1
                Zebro_1_Middle_x = Zebro_Middle_x                           # The middle point of the Pico Zebro
                Zebro_1_Middle_y = Zebro_Middle_y
                Direction_Zebro_1 = Direction                               # The current direction the Pico Zebro is going
                Angle_Zebro_1 = Angle                                       # For when a higher precision is needed the angle (Which is not correctly calculated yet
                Picture = 2                                                 # For the last Pico Zebro this has to be 8 for every other one it is 2.
            elif Devices == 1:                                                # For every Pico Zebro these values have to be assigned
                #set data from PZ 2
                Zebro_2_Middle_x = Zebro_Middle_x                           # The middle point of the Pico Zebro
                Zebro_2_Middle_y = Zebro_Middle_y
                Direction_Zebro_2 = Direction                               # The current direction the Pico Zebro is going
                Angle_Zebro_2 = Angle                                       # For when a higher precision is needed the angle (Which is not correctly calculated yet
                Picture = 2                                                 # For the last Pico Zebro this has to be 8 for every other one it is 2.
            elif Devices == 2:                                                # For every Pico Zebro these values have to be assigned
                #set data from PZ 3
                Zebro_3_Middle_x = Zebro_Middle_x                           # The middle point of the Pico Zebro
                Zebro_3_Middle_y = Zebro_Middle_y
                Direction_Zebro_3 = Direction                               # The current direction the Pico Zebro is going
                Angle_Zebro_3 = Angle                                       # For when a higher precision is needed the angle (Which is not correctly calculated yet
                Picture = 8                                                 # For the last Pico Zebro this has to be 8 for every other one it is 2.

            Devices = Devices + 1                                           # Go to the next device

        if Picture == 8:
            Devices = 0                                                     # Reset Devices so for the next time it will start with Pico 1.
            #once every value for every possible Zebro is determind then
            for Zebros in range(2):                                         # total of maximum of x Zebro's
                Blocking_Zebro = []                                         # Here will be the blocking in
                if Zebros == 0:                                             # The comming step has to be done for every possible Zebro 
                    # The reason Block function is in another python script is to make this one easier to read because the BLocked functions got a lot of if statements. 
                    
                    Blocking_Zebro = Block.Block_6(Zebro_1_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x,
                                                   Zebro_1_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y)
                    PicoZebro_1 = [Zebro_1_Middle_x , Zebro_1_Middle_y, Blocking_Zebro] # Set PicoZebro_x with new values
                    
                    if q_PicoZebro_1.empty() == True:                       # if the queue is empty fill it
                        q_PicoZebro_1.put(PicoZebro_1)
                    elif q_PicoZebro_1.empty() == False:                    # else empty it before filling it again with the next data.
                        q_PicoZebro_1.mutex.acquire()                       # Which is the middle point and every blocked direction of the Pico Zebro
                        q_PicoZebro_1.queue.clear()
                        q_PicoZebro_1.all_tasks_done.notify_all()
                        q_PicoZebro_1.unfinished_tasks = 0
                        q_PicoZebro_1.mutex.release()
                        q_PicoZebro_1.put(PicoZebro_1)

                    if q_Pico_Direction_1.empty() == True:                  # if the queue is empty fill it
                        q_Pico_Direction_1.put(Direction_Zebro_1)
                    elif q_Pico_Direction_1.empty() == False:               # else empty it before filling it again with the next data.
                        q_Pico_Direction_1.mutex.acquire()                  # Which is the current direction of the Pico Zebro
                        q_Pico_Direction_1.queue.clear()
                        q_Pico_Direction_1.all_tasks_done.notify_all()
                        q_Pico_Direction_1.unfinished_tasks = 0
                        q_Pico_Direction_1.mutex.release()
                        q_Pico_Direction_1.put(Direction_Zebro_1)
                elif Zebros == 1:                                             # The comming step has to be done for every possible Zebro 
                    # The reason Block function is in another python script is to make this one easier to read because the BLocked functions got a lot of if statements. 
                    
                    Blocking_Zebro = Block.Block_6(Zebro_2_Middle_x, Zebro_1_Middle_x, Zebro_3_Middle_x,
                                                   Zebro_2_Middle_y, Zebro_1_Middle_y, Zebro_3_Middle_y)
                    PicoZebro_2 = [Zebro_2_Middle_x , Zebro_2_Middle_y, Blocking_Zebro] # Set PicoZebro_x with new values
                    
                    if q_PicoZebro_2.empty() == True:                       # if the queue is empty fill it
                        q_PicoZebro_2.put(PicoZebro_2)
                    elif q_PicoZebro_2.empty() == False:                    # else empty it before filling it again with the next data.
                        q_PicoZebro_2.mutex.acquire()                       # Which is the middle point and every blocked direction of the Pico Zebro
                        q_PicoZebro_2.queue.clear()
                        q_PicoZebro_2.all_tasks_done.notify_all()
                        q_PicoZebro_2.unfinished_tasks = 0
                        q_PicoZebro_2.mutex.release()
                        q_PicoZebro_2.put(PicoZebro_2)

                    if q_Pico_Direction_2.empty() == True:                  # if the queue is empty fill it
                        q_Pico_Direction_2.put(Direction_Zebro_2)
                    elif q_Pico_Direction_2.empty() == False:               # else empty it before filling it again with the next data.
                        q_Pico_Direction_2.mutex.acquire()                  # Which is the current direction of the Pico Zebro
                        q_Pico_Direction_2.queue.clear()
                        q_Pico_Direction_2.all_tasks_done.notify_all()
                        q_Pico_Direction_2.unfinished_tasks = 0
                        q_Pico_Direction_2.mutex.release()
                        q_Pico_Direction_2.put(Direction_Zebro_2)
                        
                elif Zebros == 2:
                    # The reason Block function is in another python script is to make this one easier to read because the BLocked functions got a lot of if statements. 
                    
                    Blocking_Zebro = Block.Block_6(Zebro_3_Middle_x, Zebro_2_Middle_x, Zebro_1_Middle_x,
                                                   Zebro_3_Middle_y, Zebro_2_Middle_y, Zebro_1_Middle_y)
                    PicoZebro_3 = [Zebro_3_Middle_x , Zebro_3_Middle_y, Blocking_Zebro] # Set PicoZebro_x with new values
                    
                    if q_PicoZebro_3.empty() == True:                       # if the queue is empty fill it
                        q_PicoZebro_3.put(PicoZebro_3)
                    elif q_PicoZebro_3.empty() == False:                    # else empty it before filling it again with the next data.
                        q_PicoZebro_3.mutex.acquire()                       # Which is the middle point and every blocked direction of the Pico Zebro
                        q_PicoZebro_3.queue.clear()
                        q_PicoZebro_3.all_tasks_done.notify_all()
                        q_PicoZebro_3.unfinished_tasks = 0
                        q_PicoZebro_3.mutex.release()
                        q_PicoZebro_3.put(PicoZebro_3)

                    if q_Pico_Direction_3.empty() == True:                  # if the queue is empty fill it
                        q_Pico_Direction_3.put(Direction_Zebro_3)
                    elif q_Pico_Direction_3.empty() == False:               # else empty it before filling it again with the next data.
                        q_Pico_Direction_3.mutex.acquire()                  # Which is the current direction of the Pico Zebro
                        q_Pico_Direction_3.queue.clear()
                        q_Pico_Direction_3.all_tasks_done.notify_all()
                        q_Pico_Direction_3.unfinished_tasks = 0
                        q_Pico_Direction_3.mutex.release()
                        q_Pico_Direction_3.put(Direction_Zebro_3)
                        
                    print(PicoZebro_3)
                    print(Direction_Zebro_3)
                    #Picture = 9                                            # This has to be 9 for going to the next step for the last Zebro for every other one does not need to be assigned
                    Writing = ("Main","Global", "Leds_off")                 # Making sure all leds are turned off
                    q_Control_Serial_Write.put((1, Writing), block=True, timeout=None) # Turn leds of again
                    time.sleep(2)
                    print("Turning LEd 1 on")
                    Writing = ("Main","Global", "Led1_on")            
                    q_Control_Serial_Write.put((1, Writing), block=True, timeout=None) # Turn led 1 on for following all the Pico Zebro's
                    time.sleep(3)
                    Writing = ("Main","Global", "Led2_on")            
                    q_Control_Serial_Write.put((1, Writing), block=True, timeout=None) # Turn led 1 on for following all the Pico Zebro's
                    time.sleep(3)
                    Writing = ("Main","Global", "Led3_on")            
                    q_Control_Serial_Write.put((1, Writing), block=True, timeout=None) # Turn led 1 on for following all the Pico Zebro's
                    time.sleep(3)
                    print("MAIN RELEASE SERIAL LOCK")
                    
                    if q_Control_Uart_Main.empty() == False: #empty it so the pico can write again and the main will stop using the Uart
                        q_Control_Uart_Main.mutex.acquire()
                        q_Control_Uart_Main.queue.clear()
                        q_Control_Uart_Main.all_tasks_done.notify_all()
                        q_Control_Uart_Main.unfinished_tasks = 0
                        q_Control_Uart_Main.mutex.release()
                        
                    # Release Condition Serial Write. (Now movement can start.)
                    Picture_1_start_time = time.time() # Take current time so the main reset at Picture 1 every 10 mins

        if Picture == 9:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)                  # Take a gray picture
            #cv2.imwrite("gray.jpg",gray)
            blurred = cv2.GaussianBlur(gray, (11, 11), 0)                   # Blur image for noise reduction
            # threshold the image to reveal light regions in the
            # blurred image
            thresh = cv2.threshold(blurred, 225, 250, cv2.THRESH_BINARY)[1]
            # perform a series of dilations to remove
            # any small blobs of noise from the thresholded image
            thresh = cv2.dilate(thresh, None, iterations=1)
            thresh = cv2.dilate(thresh, None, iterations=3)
            # find the contours in the mask, then sort them from left to right
            cv2.imwrite("graywew.jpg",thresh)
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if imutils.is_cv2() else cnts[1]
            try:
                cnts = contours.sort_contours(cnts)[0]
            except ValueError:                                              # In case there are no lights on which means their are no leds or contours
                pass
                print("There are no zebros")
            
            Old_Direction_Pico_1 = Direction_Zebro_1
            Old_Zebro_1_Middle_x = Zebro_1_Middle_x
            Old_Zebro_1_Middle_y = Zebro_1_Middle_y
            
            Old_Direction_Pico_2 = Direction_Zebro_2
            Old_Zebro_2_Middle_x = Zebro_2_Middle_x
            Old_Zebro_2_Middle_y = Zebro_2_Middle_y

            Old_Direction_Pico_3 = Direction_Zebro_3
            Old_Zebro_3_Middle_x = Zebro_3_Middle_x
            Old_Zebro_3_Middle_y = Zebro_3_Middle_y
            
            # loop over the contours
            Leds = []
            Zebro_1_Leds = []
            Zebro_2_Leds = []
            Zebro_3_Leds = []
            for (i, c) in enumerate(cnts):
                # draw the bright spot on the image
                (x, y, w, h) = cv2.boundingRect(c)                          # For finding the x and y of the leds
                Old_Zebro_1_Middle_x_pos = Old_Zebro_1_Middle_x + 200
                Old_Zebro_1_Middle_x_neg = Old_Zebro_1_Middle_x - 200
                Old_Zebro_1_Middle_y_pos = Old_Zebro_1_Middle_y + 200
                Old_Zebro_1_Middle_y_neg = Old_Zebro_1_Middle_y - 200

                Old_Zebro_2_Middle_x_pos = Old_Zebro_2_Middle_x + 200
                Old_Zebro_2_Middle_x_neg = Old_Zebro_2_Middle_x - 200
                Old_Zebro_2_Middle_y_pos = Old_Zebro_2_Middle_y + 200
                Old_Zebro_2_Middle_y_neg = Old_Zebro_2_Middle_y - 200

                Old_Zebro_3_Middle_x_pos = Old_Zebro_3_Middle_x + 200
                Old_Zebro_3_Middle_x_neg = Old_Zebro_3_Middle_x - 200
                Old_Zebro_3_Middle_y_pos = Old_Zebro_3_Middle_y + 200
                Old_Zebro_3_Middle_y_neg = Old_Zebro_3_Middle_y - 200
                
                if (x < Old_Zebro_1_Middle_x_pos) and (x > Old_Zebro_1_Middle_x_neg) and (y < Old_Zebro_1_Middle_y_pos) and (y > Old_Zebro_1_Middle_y_neg):
                    Zebro_1_Led = [x,y]
                    Zebro_1_Leds.append(Zebro_1_Led)
                if (x < Old_Zebro_2_Middle_x_pos) and (x > Old_Zebro_2_Middle_x_neg) and (y < Old_Zebro_2_Middle_y_pos) and (y > Old_Zebro_2_Middle_y_neg):
                    Zebro_2_Led = [x,y]
                    Zebro_2_Leds.append(Zebro_2_Led)
                if (x < Old_Zebro_3_Middle_x_pos) and (x > Old_Zebro_3_Middle_x_neg) and (y < Old_Zebro_3_Middle_y_pos) and (y > Old_Zebro_3_Middle_y_neg):
                    Zebro_3_Led = [x,y]
                    Zebro_3_Leds.append(Zebro_3_Led)
                Led = [x,y]
                Leds.append(Led)
            for Zebros_1 in range(3):
                Blocking_Zebro = []                                         # Here will be the blocked Directions in
                if Zebros_1 == 0:
                    for Testing_i in Zebro_1_Leds:
                        for Testing_y in Zebro_1_Leds:
                            Delta_X = abs(Testing_i[0] - Testing_y[0])
                            Delta_Y = abs(Testing_i[1] - Testing_y[1])
                            Distance = math.sqrt((Delta_X*Delta_X) + (Delta_Y*Delta_Y))
                            if (Distance > 28) and (Distance <= 38):
                                Found_Led_1_1 = Testing_i
                                Found_Led_1_2 = Testing_y
                                Found_Led_2_1 = Testing_i
                                Found_Led_2_2 = Testing_y
                            if (Distance > 38) and (Distance <= 49):
                                Found_Led_2_3 = Testing_i
                                Found_Led_2_4 = Testing_y
                                Found_Led_3_1 = Testing_i
                                Found_Led_3_2 = Testing_y
                            if (Distance > 49) and (Distance <= 60):
                                Found_Led_1_3 = Testing_i
                                Found_Led_1_4 = Testing_y
                                Found_Led_3_3 = Testing_i
                                Found_Led_3_4 = Testing_y
                                
                    if Found_Led_1_1 == Found_Led_1_2:
                        Led_1 = Found_Led_1_1
                    elif Found_Led_1_1 == Found_Led_1_3:
                        Led_1 = Found_Led_1_1
                    elif Found_Led_1_1 == Found_Led_1_4:
                        Led_1 = Found_Led_1_1
                    elif Found_Led_1_2 == Found_Led_1_3:
                        Led_1 = Found_Led_1_2
                    elif Found_Led_1_2 == Found_Led_1_4:
                        Led_1 = Found_Led_1_2
                    elif Found_Led_1_3 == Found_Led_1_4:
                        Led_1 = Found_Led_1_3

                    if Found_Led_2_1 == Found_Led_2_2:
                        Led_2 = Found_Led_2_1
                    elif Found_Led_2_1 == Found_Led_2_3:
                        Led_2 = Found_Led_2_1
                    elif Found_Led_2_1 == Found_Led_2_4:
                        Led_2 = Found_Led_2_1
                    elif Found_Led_2_2 == Found_Led_2_3:
                        Led_2 = Found_Led_2_2
                    elif Found_Led_2_2 == Found_Led_2_4:
                        Led_2 = Found_Led_2_2
                    elif Found_Led_2_3 == Found_Led_2_4:
                        Led_2 = Found_Led_2_3

                    if Found_Led_3_1 == Found_Led_3_2:
                        Led_3 = Found_Led_3_1
                    elif Found_Led_3_1 == Found_Led_3_3:
                        Led_3 = Found_Led_3_1
                    elif Found_Led_3_1 == Found_Led_3_4:
                        Led_3 = Found_Led_3_1
                    elif Found_Led_3_2 == Found_Led_3_3:
                        Led_3 = Found_Led_3_2
                    elif Found_Led_3_2 == Found_Led_3_4:
                        Led_3 = Found_Led_3_2
                    elif Found_Led_3_3 == Found_Led_3_4:
                        Led_3 = Found_Led_3_3
                        
                    (Zebro_Middle_x,Zebro_Middle_y,Direction, Angle) = Find_Orientation(Led_1[0],Led_3[0],Led_1[1],Led_3[1])
                    Zebro_1_Middle_x = Zebro_Middle_x
                    Zebro_1_Middle_y = Zebro_Middle_y     
                    Direction_Zebro_1 = Direction
                    if (Zebro_1_Middle_x == 0) or (Zebro_1_Middle_y == 0):
                        Zebro_1_Middle_x = Old_Zebro_1_Middle_x
                        Zebro_1_Middle_y = Old_Zebro_1_Middle_y
                elif Zebros_1 == 1:
                    for Testing_i in Zebro_2_Leds:
                        for Testing_y in Zebro_2_Leds:
                            Delta_X = abs(Testing_i[0] - Testing_y[0])
                            Delta_Y = abs(Testing_i[1] - Testing_y[1])
                            Distance = math.sqrt((Delta_X*Delta_X) + (Delta_Y*Delta_Y))
                            if (Distance > 28) and (Distance <= 38):
                                Found_Led_1_1 = Testing_i
                                Found_Led_1_2 = Testing_y
                                Found_Led_2_1 = Testing_i
                                Found_Led_2_2 = Testing_y
                            if (Distance > 38) and (Distance <= 49):
                                Found_Led_2_3 = Testing_i
                                Found_Led_2_4 = Testing_y
                                Found_Led_3_1 = Testing_i
                                Found_Led_3_2 = Testing_y
                            if (Distance > 49) and (Distance <= 60):
                                Found_Led_1_3 = Testing_i
                                Found_Led_1_4 = Testing_y
                                Found_Led_3_3 = Testing_i
                                Found_Led_3_4 = Testing_y  
                    if Found_Led_1_1 == Found_Led_1_2:
                        Led_1 = Found_Led_1_1
                    elif Found_Led_1_1 == Found_Led_1_3:
                        Led_1 = Found_Led_1_1
                    elif Found_Led_1_1 == Found_Led_1_4:
                        Led_1 = Found_Led_1_1
                    elif Found_Led_1_2 == Found_Led_1_3:
                        Led_1 = Found_Led_1_2
                    elif Found_Led_1_2 == Found_Led_1_4:
                        Led_1 = Found_Led_1_2
                    elif Found_Led_1_3 == Found_Led_1_4:
                        Led_1 = Found_Led_1_3

                    if Found_Led_2_1 == Found_Led_2_2:
                        Led_2 = Found_Led_2_1
                    elif Found_Led_2_1 == Found_Led_2_3:
                        Led_2 = Found_Led_2_1
                    elif Found_Led_2_1 == Found_Led_2_4:
                        Led_2 = Found_Led_2_1
                    elif Found_Led_2_2 == Found_Led_2_3:
                        Led_2 = Found_Led_2_2
                    elif Found_Led_2_2 == Found_Led_2_4:
                        Led_2 = Found_Led_2_2
                    elif Found_Led_2_3 == Found_Led_2_4:
                        Led_2 = Found_Led_2_3

                    if Found_Led_3_1 == Found_Led_3_2:
                        Led_3 = Found_Led_3_1
                    elif Found_Led_3_1 == Found_Led_3_3:
                        Led_3 = Found_Led_3_1
                    elif Found_Led_3_1 == Found_Led_3_4:
                        Led_3 = Found_Led_3_1
                    elif Found_Led_3_2 == Found_Led_3_3:
                        Led_3 = Found_Led_3_2
                    elif Found_Led_3_2 == Found_Led_3_4:
                        Led_3 = Found_Led_3_2
                    elif Found_Led_3_3 == Found_Led_3_4:
                        Led_3 = Found_Led_3_3
                        
                    (Zebro_Middle_x,Zebro_Middle_y,Direction, Angle) = Find_Orientation(Led_1[0],Led_3[0],Led_1[1],Led_3[1])
                    Zebro_2_Middle_x = Zebro_Middle_x
                    Zebro_2_Middle_y = Zebro_Middle_y     
                    Direction_Zebro_2 = Direction
                    if (Zebro_2_Middle_x == 0) or (Zebro_2_Middle_y == 0):
                        Zebro_2_Middle_x = Old_Zebro_2_Middle_x
                        Zebro_2_Middle_y = Old_Zebro_2_Middle_y

                elif Zebros_1 == 2:
                    for Testing_i in Zebro_3_Leds:
                        for Testing_y in Zebro_3_Leds:
                            Delta_X = abs(Testing_i[0] - Testing_y[0])
                            Delta_Y = abs(Testing_i[1] - Testing_y[1])
                            Distance = math.sqrt((Delta_X*Delta_X) + (Delta_Y*Delta_Y))
                            if (Distance > 28) and (Distance <= 38):
                                Found_Led_1_1 = Testing_i
                                Found_Led_1_2 = Testing_y
                                Found_Led_2_1 = Testing_i
                                Found_Led_2_2 = Testing_y
                            if (Distance > 38) and (Distance <= 49):
                                Found_Led_2_3 = Testing_i
                                Found_Led_2_4 = Testing_y
                                Found_Led_3_1 = Testing_i
                                Found_Led_3_2 = Testing_y
                            if (Distance > 49) and (Distance <= 60):
                                Found_Led_1_3 = Testing_i
                                Found_Led_1_4 = Testing_y
                                Found_Led_3_3 = Testing_i
                                Found_Led_3_4 = Testing_y  
                    if Found_Led_1_1 == Found_Led_1_2:
                        Led_1 = Found_Led_1_1
                    elif Found_Led_1_1 == Found_Led_1_3:
                        Led_1 = Found_Led_1_1
                    elif Found_Led_1_1 == Found_Led_1_4:
                        Led_1 = Found_Led_1_1
                    elif Found_Led_1_2 == Found_Led_1_3:
                        Led_1 = Found_Led_1_2
                    elif Found_Led_1_2 == Found_Led_1_4:
                        Led_1 = Found_Led_1_2
                    elif Found_Led_1_3 == Found_Led_1_4:
                        Led_1 = Found_Led_1_3

                    if Found_Led_2_1 == Found_Led_2_2:
                        Led_2 = Found_Led_2_1
                    elif Found_Led_2_1 == Found_Led_2_3:
                        Led_2 = Found_Led_2_1
                    elif Found_Led_2_1 == Found_Led_2_4:
                        Led_2 = Found_Led_2_1
                    elif Found_Led_2_2 == Found_Led_2_3:
                        Led_2 = Found_Led_2_2
                    elif Found_Led_2_2 == Found_Led_2_4:
                        Led_2 = Found_Led_2_2
                    elif Found_Led_2_3 == Found_Led_2_4:
                        Led_2 = Found_Led_2_3

                    if Found_Led_3_1 == Found_Led_3_2:
                        Led_3 = Found_Led_3_1
                    elif Found_Led_3_1 == Found_Led_3_3:
                        Led_3 = Found_Led_3_1
                    elif Found_Led_3_1 == Found_Led_3_4:
                        Led_3 = Found_Led_3_1
                    elif Found_Led_3_2 == Found_Led_3_3:
                        Led_3 = Found_Led_3_2
                    elif Found_Led_3_2 == Found_Led_3_4:
                        Led_3 = Found_Led_3_2
                    elif Found_Led_3_3 == Found_Led_3_4:
                        Led_3 = Found_Led_3_3
                        
                    (Zebro_Middle_x,Zebro_Middle_y,Direction, Angle) = Find_Orientation(Led_1[0],Led_3[0],Led_1[1],Led_3[1])
                    Zebro_3_Middle_x = Zebro_Middle_x
                    Zebro_3_Middle_y = Zebro_Middle_y     
                    Direction_Zebro_3 = Direction
                    if (Zebro_3_Middle_x == 0) or (Zebro_3_Middle_y == 0):
                        Zebro_3_Middle_x = Old_Zebro_3_Middle_x
                        Zebro_3_Middle_y = Old_Zebro_3_Middle_y
                        
            for Zebros in range(3):
                if Zebros == 0:
                    Blocking_Zebro = Block.Block_6(Zebro_1_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x,
                                                   Zebro_1_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y)
                    
                    Zebro_1_Middle_x = Zebro_1_Middle_x
                    Zebro_1_Middle_y = Zebro_1_Middle_y
                    PicoZebro_1 = [Zebro_1_Middle_x , Zebro_1_Middle_y, Blocking_Zebro] 
                    print(Direction_Zebro_1)
                    print(PicoZebro_1)
                    print("debug")
                    if q_PicoZebro_1.empty() == True:                       # if the queue is empty fill it
                        q_PicoZebro_1.put(PicoZebro_1)
                    elif q_PicoZebro_1.empty() == False:                    # else empty it before filling it again with the next data. of the Pico Zebro 
                        q_PicoZebro_1.mutex.acquire()                       # which could happen condsidering this could happen faster than the Pico Control thread could use these values
                        q_PicoZebro_1.queue.clear()
                        q_PicoZebro_1.all_tasks_done.notify_all()
                        q_PicoZebro_1.unfinished_tasks = 0
                        q_PicoZebro_1.mutex.release()
                        q_PicoZebro_1.put(PicoZebro_1)
                    # once it is determined if finding Direction leve works this can be done:    
                    if q_Pico_Direction_1.empty() == True:                  # if the queue is empty fill it
                        q_Pico_Direction_1.put(Direction_Zebro_1)
                    elif q_Pico_Direction_1.empty() == False:               # else empty it before filling it again with the next data.
                        q_Pico_Direction_1.mutex.acquire()                  # Which is the current direction of the Pico Zebro
                        q_Pico_Direction_1.queue.clear()
                        q_Pico_Direction_1.all_tasks_done.notify_all()
                        q_Pico_Direction_1.unfinished_tasks = 0
                        q_Pico_Direction_1.mutex.release()
                        q_Pico_Direction_1.put(Direction_Zebro_1)
                        
                elif Zebros == 1:
                    Blocking_Zebro = Block.Block_6(Zebro_1_Middle_x, Zebro_2_Middle_x, Zebro_3_Middle_x,
                                                   Zebro_1_Middle_y, Zebro_2_Middle_y, Zebro_3_Middle_y)
                    Zebro_2_Middle_x = Zebro_2_Middle_x
                    Zebro_2_Middle_y = Zebro_2_Middle_y
                    PicoZebro_2 = [Zebro_2_Middle_x , Zebro_2_Middle_y, Blocking_Zebro] 
                    print(Direction_Zebro_2)
                    print(PicoZebro_2)
                    print("debug")
                    if q_PicoZebro_2.empty() == True:                       # if the queue is empty fill it
                        q_PicoZebro_2.put(PicoZebro_2)
                    elif q_PicoZebro_2.empty() == False:                    # else empty it before filling it again with the next data. of the Pico Zebro 
                        q_PicoZebro_2.mutex.acquire()                       # which could happen condsidering this could happen faster than the Pico Control thread could use these values
                        q_PicoZebro_2.queue.clear()
                        q_PicoZebro_2.all_tasks_done.notify_all()
                        q_PicoZebro_2.unfinished_tasks = 0
                        q_PicoZebro_2.mutex.release()
                        q_PicoZebro_2.put(PicoZebro_2)
                    # once it is determined if finding Direction leve works this can be done:    
                    if q_Pico_Direction_2.empty() == True:                  # if the queue is empty fill it
                        q_Pico_Direction_2.put(Direction_Zebro_2)
                    elif q_Pico_Direction_2.empty() == False:               # else empty it before filling it again with the next data.
                        q_Pico_Direction_2.mutex.acquire()                  # Which is the current direction of the Pico Zebro
                        q_Pico_Direction_2.queue.clear()
                        q_Pico_Direction_2.all_tasks_done.notify_all()
                        q_Pico_Direction_2.unfinished_tasks = 0
                        q_Pico_Direction_2.mutex.release()
                        q_Pico_Direction_2.put(Direction_Zebro_2)

                if Zebros == 2:
                    Blocking_Zebro = Block.Block_6(Zebro_3_Middle_x, Zebro_2_Middle_x, Zebro_1_Middle_x,
                                                   Zebro_3_Middle_y, Zebro_2_Middle_y, Zebro_1_Middle_y)
                    
                    Zebro_3_Middle_x = Zebro_3_Middle_x
                    Zebro_3_Middle_y = Zebro_3_Middle_y
                    PicoZebro_3 = [Zebro_3_Middle_x , Zebro_3_Middle_y, Blocking_Zebro] 
                    print(Direction_Zebro_3)
                    print(PicoZebro_3)
                    print("debug")
                    if q_PicoZebro_3.empty() == True:                       # if the queue is empty fill it
                        q_PicoZebro_3.put(PicoZebro_3)
                    elif q_PicoZebro_3.empty() == False:                    # else empty it before filling it again with the next data. of the Pico Zebro 
                        q_PicoZebro_3.mutex.acquire()                       # which could happen condsidering this could happen faster than the Pico Control thread could use these values
                        q_PicoZebro_3.queue.clear()
                        q_PicoZebro_3.all_tasks_done.notify_all()
                        q_PicoZebro_3.unfinished_tasks = 0
                        q_PicoZebro_3.mutex.release()
                        q_PicoZebro_3.put(PicoZebro_3)
                    # once it is determined if finding Direction leve works this can be done:    
                    if q_Pico_Direction_3.empty() == True:                  # if the queue is empty fill it
                        q_Pico_Direction_3.put(Direction_Zebro_3)
                    elif q_Pico_Direction_3.empty() == False:               # else empty it before filling it again with the next data.
                        q_Pico_Direction_3.mutex.acquire()                  # Which is the current direction of the Pico Zebro
                        q_Pico_Direction_3.queue.clear()
                        q_Pico_Direction_3.all_tasks_done.notify_all()
                        q_Pico_Direction_3.unfinished_tasks = 0
                        q_Pico_Direction_3.mutex.release()
                        q_Pico_Direction_3.put(Direction_Zebro_3)
                    
            Picture = 8                                                     # Making sure this steps repeats itself untill 10 mins = 600 secibds has passed
            
            if ((time.time() - Picture_1_start_time) > 600):                # Check if 10 mins has passed
                Picture = 0                                                 # Restart code and redetermine which Pico Zebro is which 
                print(Picture)
                Picture_1_start_time = time.time()
                print("Restarting program reinit")
                print((time.time() - Picture_1_start_time))
                pass
        # By doing it like this in steps it would not be the case with the frame is already taken before the led is turned on but only after wards
        Picture = Picture + 1                                               # Go to the next step after taking a new frame
        
        # show the frame
        key = cv2.waitKey(1) & 0xFF

        #clear the stream in preparation of the next frame
        rawCapture.truncate(0)

        # if the 'q' key was pressed, break from the loop                   # END of program when someone presse 1 on the cv2.imshow
        if key == ord("q"):
            # cleanup the camera and close any open windows
            print("Ending program")
            arduino.close()
            #ser.close()
            cv2.destroyAllWindows()
            break

# Call this function before anything else!
def initialize_serial():
    global arduino
    global connectedArray
    global lastCommand

    # Scan for all available ports
    allPorts = serial.tools.list_ports.comports()                           # Get all the available ports on the system
    usablePorts = [
        port[0]
            for port in allPorts
                if port[2] != 'n/a' and port[2].find("2341") != -1          # Filter out all non-arduino and empty items
    ]
    
    if len(usablePorts) == 0:                                               # Check if there are usable ports
        print("ARDUINO ERROR: ARDUINO_NOT_FOUND")                           # Print error message
        exit();                                                             # !!!!!!!!! Exit the program because we cant do anything without communicating with the Pico Zebros
        
    # Initalize some variables
    lastCommand = [0, 0, 0, 0, 255]                                         # For the first getState so that there wont be an error (zebroID, read(0) or write(1), address, value)
    connectedArray = bytearray(
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]                           # Just initialize this so you wont have to check for the array to be filled
    ) 

    # Setup the Serial interface with the first found port
    arduino = serial.Serial()                                               # Get a serial object to work with
    arduino.baudrate = 38400                                                # 38400 is a limitation by the BLE module (locked in firmware, and firmware update could fix this)
    arduino.port = usablePorts[0]                                           # '/dev/ttyUSB0' or 'COM9'
    arduino.open()                                                          # Open the connection, this throws an error if the device is in use
    print("ARDUINO FOUND AT: ", usablePorts[0])
    
    getResult()                                                             # Wait for arduino to initialize

    # Force blocking wait for the arduino to be done with processing data
def getResult():
    global lastCommand
    status = arduino.read()                                                 # This command is blocking till you get a result
    time.sleep(0.01)                                                        # Sleep for the next command to be accurate
    data_left = arduino.inWaiting()                                         # Get the waiting amount of bytes in the buffer
    if (status != b"\x00" and status != b"\xff" and
            status != 1 and lastCommand[0] != 20):                          # Check if the first buffer number is everything else than M_OK(0) or M_END_MESSAGE(255)
        # Display an error (please implement this to your likings)
        try:
            errorMessage = ["M_OK", "M_ERROR", "M_ERROR_NOT_CONNECTED", "M_ERROR_BUFFER_OVERFLOW", "M_ERROR_BUFFER_EMPTY", "M_ERROR_UNKNOWN_COMMAND"]
            print("ARDUINO ERROR: ", status, "(" + errorMessage[int.from_bytes(status,byteorder='big', signed=False)] + ")", lastCommand) 
        except IndexError:
            print("ARDUINO ERROR: ", status, "(M_ERROR_UNKNOWN)", lastCommand)
            
    return status + arduino.read(data_left)

if __name__ == '__main__':
    #Serial connection init 
    initialize_serial()
    time.sleep(3)
    getConnected()                                                  # Update the list with connected devices every frame
    time.sleep(2)
    q_Control_Uart_Main = queue.PriorityQueue(maxsize=1) # This is a 1 or 0 Determined by the main.
    
    q_Control_Serial_Write = queue.PriorityQueue(maxsize=1) # In here is the data for serial Write.
    #q_Control_Serial_Write[0] = Which Device/thread is writing
    #q_Control_Serial_Write[1] = To which Device is writing
    #q_Control_Serial_Write[2] = Wat the data is
    
    q_Data_is_Send = queue.PriorityQueue(maxsize=1)

    # All Queue objects Constructor for a FIFO queue
    # These Queue objects are only data obtained by main loop and read by Pico Zebro loops.
    q_PicoZebro_1 = queue.Queue(maxsize=1) #This is a list with in it [Zebro_1_Middle_x , Zebro_1_Middle_y, Blocking_Zebro] etc for every zebro.
    q_PicoZebro_2 = queue.Queue(maxsize=1) #This is a list with in it [Zebro_1_Middle_x , Zebro_1_Middle_y, Blocking_Zebro] etc for every zebro.
    # With a maximum of 1 list. so maxsize = 1.

    #In here will be the direection. Only at the start the main will put something in here afterwards for 10 mins the Zebro thread needs to put himself something in there with guessing.
    q_Pico_Direction_1 = queue.Queue(maxsize=1) # With a maximum of 1 list. so maxsize = 1. etc for every zebro
    q_Pico_Direction_2 = queue.Queue(maxsize=1) # With a maximum of 1 list. so maxsize = 1. etc for every zebro

    #If higher Precision with direction is required
    q_Pico_Angle_1 = queue.Queue(maxsize=1) # With a maximum of 1 list. so maxsize = 1.
    q_Pico_Angle_2 = queue.Queue(maxsize=1) # With a maximum of 1 list. so maxsize = 1.

    #All Pico Zebro Names 1 - 20
    Pico_N1 = "Pico_N1"
    Pico_N2 = "Pico_N2"

    UART_Thread_1 = UART_Thread(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main) # This call on the UArt thread will be the same no matter how many Pico's there are
    UART_Thread_1.setName('UART_Thread')

    Check_Connected_thread_1 = Check_Connected_thread(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main)
    Check_Connected_thread_1.setName("Check_Connected_thread")
    
    # Start all Pico Zebro Threads.
    # For every pico Thread new names need to be made and then called like this with the name
    Pico_Zebro_1 = Control_Zebro_Thread(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main,Pico_N1,q_PicoZebro_1,q_Pico_Direction_1,q_Pico_Angle_1)
    Pico_Zebro_1.setName('Pico_Zebro_1')
    Pico_Zebro_2 = Control_Zebro_Thread(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main,Pico_N2,q_PicoZebro_2,q_Pico_Direction_2,q_Pico_Angle_2)
    Pico_Zebro_2.setName('Pico_Zebro_2')

    # In the main every Pico value needs to be set So the more Pico the more values you have to give with the main.
    main(q_Control_Serial_Write,q_Data_is_Send,q_Control_Uart_Main,q_PicoZebro_1, q_PicoZebro_2,
         q_Pico_Direction_1, q_Pico_Direction_2,
         q_Pico_Angle_1, q_Pico_Angle_2)

