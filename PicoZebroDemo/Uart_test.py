#!/usr/bin/env python
import serial

ser = serial.Serial(
 # port='/dev/serial0',
  port='/dev/ttyS0',
  baudrate = 9600,
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS,
  timeout=1
)

#print (("Serial is open: " + (ser.isOpen())))

print ("Now Writing")
ser.write(b"This is a test")

print ("Did write, now read")
x = ser.readline()
#x.decode('utf-8')
print(x)
#print ("got '" + x + "'")

ser.close()
