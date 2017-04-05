import serial
import time
import serial.tools.list_ports;


# Call this function before anything else!
def initialize_serial():
    global arduino
    global connectedArray
    global lastCommand

    # Scan for all available ports
    allPorts = serial.tools.list_ports.comports()                   # Get all the available ports on the system
    usablePorts = [
        port[0]
            for port in allPorts
                if port[2] != 'n/a' and port[2].find("2341") != -1  # Filter out all non-arduino and empty items
    ]
    
    if len(usablePorts) == 0:                                       # Check if there are usable ports
        print("ARDUINO ERROR: ARDUINO_NOT_FOUND")                   # Print error message
        exit();                                                     # !!!!!!!!! Exit the program because we cant do anything. IMPLEMENT THIS IN BY YOUR OWN LIKINGS!!!!!!!!!
        
    # Initalize some variables
    lastCommand = [0, 0, 0, 0, 255]                                 # For the first getState so that there wont be an error (zebroID, read(0) or write(1), address, value)
    connectedArray = bytearray(
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]                   # Just initialize this so you wont have to check for the array to be filled
    ) 

    # Setup the Serial interface with the first found port
    arduino = serial.Serial()                                       # Get a serial object to work with
    arduino.baudrate = 38400                                        # 38400 is a limitation by the BLE module (locked in firmware, and firmware update could fix this)
    arduino.port = usablePorts[0]                                   # '/dev/ttyUSB0' or 'COM9'
    arduino.open()                                                  # Open the connection, this throws an error if the device is in use
    print("ARDUINO FOUND AT: ", usablePorts[0])
    
    getResult()                                                     # Wait for arduino to initialize


# Update the connectedArray array with the conencted state of all devices, array is 20 items long
def getConnected():
    global connectedArray
    global lastCommand
    msg = lastCommand = bytearray([20, 0, 0, 0, 255])               # The command for getting the list of connected devices
    arduino.write(msg)                                              # Write the command to the zebro through the arduino
    res = getResult()
    if res[-1] == 255 and len(res) == 22:
        connectedArray = res[1:]                                    # Remove the status byte from the front

# Force blocking wait for the arduino to be done with processing data
def getResult():
    global lastCommand
    status = arduino.read()                                         # This command is blocking till you get a result
    time.sleep(0.01)                                                # Sleep for the next command to be accurate
    data_left = arduino.inWaiting()                                 # Get the waiting amount of bytes in the buffer
    if (status != b"\x00" and status != b"\xff" and
            status != 1 and lastCommand[0] != 20):               # Check if the first buffer number is everything else than M_OK(0) or M_END_MESSAGE(255)
        # Display an error (please implement this to your likings)
        try:
            errorMessage = ["M_OK", "M_ERROR", "M_ERROR_NOT_CONNECTED", "M_ERROR_BUFFER_OVERFLOW", "M_ERROR_BUFFER_EMPTY", "M_ERROR_UNKNOWN_COMMAND"]
            print("ARDUINO ERROR: ", status, "(" + errorMessage[int.from_bytes(status,byteorder='big', signed=False)] + ")", lastCommand) 
        except IndexError:
            print("ARDUINO ERROR: ", status, "(M_ERROR_UNKNOWN)", lastCommand)
            
    return status + arduino.read(data_left)                         # return the whole buffer at once including the statusbyte

# Turn leds on a specific PicoZebro on or off (ledNr = 0 to 5)
# Values are stored like 0b00000RGB so sending a 7(0b111) will turn all colors of one led package on. 
def setLed(connectionID, ledNr, value):
    global lastCommand
    msg = lastCommand = bytearray([connectionID, 1, 33 + ledNr, value, 255])   # Adress 33(0x21) and up is for the leds
    arduino.write(msg)                                              # Write the command to the zebro through the arduino
    getResult()                                                     # Wait for the arduino to finish the command


# Set the movement of the PicoZebro. Changing this will not force the state, the Zebro will finish what it was doing before entering new state.
# Possible values{ 0: IDLE, 1: FORWARD, 2: BACKWARDS, 3: TURN_LEFT, 4: TURN_RIGHT }
def setMovement(connectionID, value):
    global lastCommand
    msg = lastCommand = bytearray([connectionID, 1, 32, value, 255])   # Adress 32(0x20) and up is for the movement states
    arduino.write(msg)                                              # Write the command to the zebro through the arduino
    print("setMovement:", getResult())                                                     # Wait for the arduino to finish the command


##########################################################
# This function is a preview how it could be implemented #
##########################################################
def previewTestCase():
    initialize_serial()

    # Infinite loop with turning 3 leds on and off (0 to and including 2)
    while 1:
        time.sleep(0.5)                                             # For demo purposes
        getConnected()                                              # Update the list with connected devices every now and then
        print("Connected Devices:",
            [i for (i,c) in enumerate(connectedArray)               # Print all connected devices
                if c == 1]
        )

        if connectedArray[0] == 1:                                  # Is the Zebro connected?
            for i in range(0, 3):                                   # Loop through 3 leds
                setLed(connectionID=0, ledNr=0, value=4)            # Set led top left front OFF(1) for connection 0
                setLed(connectionID=0, ledNr=1, value=4)            # Set led top left front OFF(1) for connection 0
                setLed(connectionID=0, ledNr=2, value=4)            # Set led top left front OFF(1) for connection 0
                setLed(connectionID=0, ledNr=3, value=4)            # Set led top left front OFF(1) for connection 0
                time.sleep(0.2)                                     # Wait some time to make it visible for the naked eye
                setLed(connectionID=0, ledNr=0, value=0)            # Set led top left front ON(0) for connection 0
                setLed(connectionID=0, ledNr=1, value=0)            # Set led top left front OFF(1) for connection 0
                setLed(connectionID=0, ledNr=2, value=0)            # Set led top left front OFF(1) for connection 0
                setLed(connectionID=0, ledNr=3, value=0)            # Set led top left front OFF(1) for connection 0

                time.sleep(0.2)                                     # Wait some time to make it visible for the naked eye
                

            setMovement(0, 1)
            time.sleep(5)
            setMovement(0, 0)
            time.sleep(5)
            setMovement(0, 3)
            time.sleep(5)
            setMovement(0, 0)
            time.sleep(5)
            setMovement(0, 4)
            time.sleep(5)
            #setMovement(0, 4)
            #time.sleep(5)
            setMovement(0, 0)
            time.sleep(5)
            
    arduino.close()                                                 # Somewhere, someday, sometime close the connection when done, unreachable statement.


# Execute the code
previewTestCase()
