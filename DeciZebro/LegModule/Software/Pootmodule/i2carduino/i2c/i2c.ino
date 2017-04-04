// Wire Master Reader
// by Nicholas Zambetti <http://www.zambetti.com>

// Demonstrates use of the Wire library
// Reads data from an I2C/TWI slave device
// Refer to the "Wire Slave Sender" example for use with this

// Created 29 March 2006

// This example code is in the public domain.

#include <stdint.h>
#include <Wire.h>

void setup() {
  Wire.begin();        // join i2c bus (address optional for master)
  Serial.begin(9600);  // start serial for output
}

uint8_t sync_counter_address = 18;
uint8_t sync_counter= 0;

uint8_t motion_address = 32;
uint8_t motion[5] = {1,0,0,0,0};

void loop() {
  Wire.beginTransmission(0);  // transmit to general call address
  Wire.write(sync_counter_address);
  Wire.write(sync_counter);           
  Wire.endTransmission();     // stop transmitting
  
  Wire.beginTransmission(0);  // transmit to device #8
  Wire.write(motion_address); 
  Wire.write(motion, 5);        
  Wire.endTransmission();     // stop transmitting
  delay(950);
  sync_counter++;
}
