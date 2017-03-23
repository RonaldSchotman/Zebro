#!/usr/bin/env python3

###########################################################################
# POOT
# The Zebro Project
# Delft University of Technology
# 2016
#
# Filename: pootControl.py
#
# Description:
# Tool to use as an ad-hoc locomotive controller for the Zebro
# It interfaces a buspirate that injects commands on to the ZebroBus.
# And yes, I know that busy loping is not the most elegant solution for
# this control loop, but tight deadlines are tight. Feel free to implement
# something with threads or something ;)
#
# Authors:
# Piet De Vaere -- Piet@DeVae.re
###########################################################################

import curses
import datetime
import serial
import time
from collections import deque

class BusPirate:
    def __init__(self, port = "/dev/ttyUSB1", baud = 115200):
        self.serial = serial.Serial(port, baud, timeout = 0)
        self.serial.write(b'#\n') # reset the BusPirate
        time.sleep(0.1) # wait a second
        self.serial.write(b'm\n4\n3\n') # set mode to i2c at 100kHz
        time.sleep(0.1) # wait a second
        self.serial.write(b'W\n') #enable power supplies
        time.sleep(0.1) # wait a second
        self.read_buffer = ""
        
    def get_data(self):
        while(True):
            new_data = self.serial.read(1)
            if len(new_data) == 0 or new_data == b'\n':
                break
            self.read_buffer = self.read_buffer + new_data.decode("ascii")
        if new_data == b'\n':
            return_string = self.read_buffer
            self.read_buffer = ""
            return return_string
        else:
            return None
        
    def transmit_command(self, command):
        self.serial.write(command.get_sequence_bytes())            
        self.serial.write(b'\n')            
      
    def transmit_bytes(self, data):
        self.serial.write(data)
        self.serial.write(b'\n')


class SerialDisplay:
    def __init__(self, screen, size = 1000):
        self.screen = screen
        self.text_buffer = deque(maxlen = size)
        
    def add_line(self, line):
        self.text_buffer.appendleft(line)
        
    def get_data_from_bus_pirate(self, buspirate):
        while(True):
            serial_data = buspirate.get_data()
            if not serial_data:
                return
            self.add_line(serial_data)

        
    def draw(self):
        size = self.screen.getmaxyx()
        
        self.screen.erase()
        
        # put the fancy header
        self.screen.addstr(0,0,'Poot BusPirate Monitor',
                           curses.A_REVERSE)
        self.screen.chgat(-1, curses.A_REVERSE)
        
        self.screen.addstr(size[0]-1,0,"Type '?' or '/' for a list of commands", 
                           curses.A_REVERSE)
        self.screen.chgat(-1, curses.A_REVERSE)
        
        self.screen.move(1,0)
        for line_nr in range(len(self.text_buffer)):
            position = size[0] - 2  - line_nr
            
            if position <= 0:
                break

            self.screen.addstr(position, 0, self.text_buffer[line_nr])
        
        stdscr.refresh()    

class Command:
    def __init__(self, sequence, key, description):
        self.sequence = sequence
        self.key = key
        self.description = description
        
    def get_sequence(self):
        return self.sequence
    
    def get_sequence_bytes(self):
        return bytes(self.sequence, 'ascii')
    
    def get_description(self):
        return self.description
    
    def get_key(self):
        return self.key
    
    def __repr__(self):
        string = "{}: {}"
        string = string.format(self.key, self.description)
        return string
    
class CommandCollection:
    def __init__(self):
        self.commands = []
        
    def add_command(self, command):
        self.commands.append(command)
        
    def add_new_command(self, sequence, key, description):
        new_command = Command(sequence, key, description)
        self.add_command(new_command)
        
    def find_command_by_key(self, key):
        for command in self.commands:
            if command.get_key() == key:
                return command
        return None
    
    def add_commands_to_screen(self, screen):
        screen.add_line('='*20)
        screen.add_line('List of commands')
        screen.add_line('')
        for command in self.commands:
            screen.add_line(str(command))
        screen.add_line('='*20)
        
    def add_commands_and_sequence_to_screen(self, screen):
        screen.add_line('='*20)
        screen.add_line('List of commands with sequences')
        screen.add_line('')
        for command in self.commands:
            screen.add_line(str(command))
            screen.add_line('    ' + command.get_sequence())
        screen.add_line('='*20)
            

  
def main(stdscr):
    bus_pirate = BusPirate();
    display = SerialDisplay(stdscr)
    commands = CommandCollection()
    commands.add_new_command("[1 2 3]", "a", "Go forward")
    commands.add_new_command("[a b c]", "k", "Just a another demo")
    commands.add_new_command("[0x00 22 0x12]", 'e', "Reset emergency_stop")

    #print(bus_pirate.get_data())
    
    last_time_update = datetime.datetime.now()
    time_sync_counter = 0

    while(True):
        display.get_data_from_bus_pirate(bus_pirate)


        # process commands received from user        
        try:
            input_char = stdscr.getkey()
        except curses.error:
            pass
        else:
            if input_char == '?':
                commands.add_commands_to_screen(display)
            if input_char == '/':
                commands.add_commands_and_sequence_to_screen(display)
            
            command = commands.find_command_by_key(input_char)
            if command:
                bus_pirate.transmit_command(command)
  
        current_time = datetime.datetime.now()
   
        #send periodic timing ticks
        if  current_time >= last_time_update + datetime.timedelta(seconds = 1):
            command = "[0x00 18 {}]".format(time_sync_counter)
            command = bytes(command, "ascii")
            bus_pirate.transmit_bytes(command)
            last_time_update = current_time
            time_sync_counter = (time_sync_counter + 1) % 256
       
        current_time = datetime.datetime.now()
        timedelta_to_next_update = current_time - last_time_update
        seconds_to_next_update = timedelta_to_next_update.total_seconds()
        
        if(seconds_to_next_update > 0.1):
            time.sleep(0.1)
        else:
            pass
       
        
        display.draw()
    
    
if __name__ == "__main__":
    stdscr = curses.initscr()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.keypad(1)
    stdscr.scrollok(1)
    stdscr.timeout(0)
    try:
        main(stdscr)
    finally:
        curses.nocbreak()
        curses.curs_set(1)
        stdscr.keypad(0)
        curses.echo()
        curses.endwin()
    #curses.wrapper(main)


