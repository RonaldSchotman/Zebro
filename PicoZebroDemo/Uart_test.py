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

print (("Serial is open: {0}".format(ser.isOpen())))

print ("Now Writing")
Test = "This is a test"

Test = Test.encode('utf-8')
print(Test)
ser.write(Test)
x = ser.readline()

print ("Did write, now read")
x = x.decode('utf-8')
print(x)
print ("got '{0}'  Test".format(x))

ser.close()
