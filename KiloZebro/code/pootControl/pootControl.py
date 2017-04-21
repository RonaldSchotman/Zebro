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

FORWARD = 0
BACKWARD = 1

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
        self.open_log()

    def open_log(self):
        self.log_file = "POOT_buspirate_log_" + \
            datetime.datetime.now().isoformat().replace(':','-')\
            .replace('.','-') + ".txt"
        try:
            self.log = open(self.log_file, 'w')
        except:
            self.log = None

    def write_log_line(self, line):
        if not self.log:
            return

        log_line = line
        if len(log_line) == 0 or log_line[-1] != '\n':
            log_line = log_line + '\n'
        self.log.write(log_line)

    def add_line(self, line):
        self.text_buffer.appendleft(line)
        if self.log:
            self.write_log_line(line)

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
        key = self.key
        if key == " ":
            key = "SPACE"
        string = "{: <10}: {}"
        string = string.format(key, self.description)
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
            
def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

@static_vars(position=0) 
def main(stdscr):
    bus_pirate = BusPirate();
    display = SerialDisplay(stdscr)
    commands = CommandCollection()
    commands.add_new_command("[0x00 30 1 0 0 0 0 0 0 1]", "c", 'Calibrate Encoders')
    commands.add_new_command("[0x00 30 255 0 0 0 0 0 0 1]", " ", 'Stop all')
    commands.add_new_command("[0x00 22 0x12]", 'e', "Reset emergency_stop")
    # commands.add_new_command("[0x00 30 7 0 120 1 0 0]", "d", "Debug Command")

    #print(bus_pirate.get_data())
    
    last_time_update = datetime.datetime.now()
    time_sync_counter = 0
    position_control_kp = 0
    current_control_kp = 0
    position_control_ki = 0
    current_control_ki = 0
    position_control_kd = 0

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
            if input_char == 'c':
                command = commands.find_command_by_key(input_char)
            if input_char == 'e':
                command = commands.find_command_by_key(input_char)
            if input_char == ' ':
                command = commands.find_command_by_key(input_char)                

            if input_char == 'y':
                if (current_control_kp<255):
                    current_control_kp += 1
                command = Command("[0x00 50 {0}]".format(current_control_kp), "y", 'Increase kp current control')
            if input_char == 'h':
                if (current_control_kp>0):
                    current_control_kp -= 1
                command = Command("[0x00 50 {0}]".format(current_control_kp), "h", 'Decrease kp current control')
            if input_char == 'u':
                if (current_control_ki<255):
                    current_control_ki += 1
                command = Command("[0x00 51 {0}]".format(current_control_ki), "u", 'Increase ki current control')
            if input_char == 'j':
                if (current_control_ki>0):
                    current_control_ki -= 1
                command = Command("[0x00 51 {0}]".format(current_control_ki), "j", 'Decrease ki current control')

            if input_char == 'i':
                if (position_control_kp<255):
                    position_control_kp += 1
                command = Command("[0x00 145 {0}]".format(position_control_kp), "i", 'Increase kp position control')
            if input_char == 'k':
                if (position_control_kp>0):
                    position_control_kp -= 1
                command = Command("[0x00 145 {0}]".format(position_control_kp), "k", 'Decrease kp position control')
            if input_char == 'o':
                if (position_control_ki<255):
                    position_control_ki += 1
                command = Command("[0x00 146 {0}]".format(position_control_ki), "o", 'Increase ki position control')
            if input_char == 'l':
                if (position_control_ki>0):
                    position_control_ki -= 1
                command = Command("[0x00 146 {0}]".format(position_control_ki), "l", 'Decrease ki position control')
            if input_char == 'p':
                if (position_control_kd<255):
                    position_control_kd += 1
                command = Command("[0x00 147 {0}]".format(position_control_kd), "p", 'Increase kd position control')
            if input_char == ';':
                if (position_control_kd>0):
                    position_control_kd -= 1
                command = Command("[0x00 147 {0}]".format(position_control_kd), ";", 'Decrease kd position control')

            if input_char == 'w':
                main.position = (main.position + 10)%910
                position_a = (main.position >> 8) & 0xff
                position_b = main.position & 0xff
                time_a = time_sync_counter
                time_b = 50
                command = Command("[0x00 30 2 {0} {1} {2} {3} 1 0 1]".format(position_a, position_b, time_a, time_b), "w", 'walk forward')
            if input_char == 's':
                main.position = (main.position + 900)%910
                position_a = (main.position >> 8) & 0xff
                position_b = main.position & 0xff
                time_a = time_sync_counter
                time_b = 50
                command = Command("[0x00 30 3 {0} {1} {2} {3} 1 0 1]".format(position_a, position_b, time_a, time_b), "s", 'walk backward')
            if input_char == 'z':
                position = 610
                position_a = (main.position >> 8) & 0xff
                position_b = main.position & 0xff
                time_a = time_sync_counter + 1
                time_b = 0
                command = Command("[0x00 30 2 {0} {1} {2} {3} 1 0 1]".format(position_a, position_b, time_a, time_b), "z", 'stand up')


            if command:
                bus_pirate.transmit_command(command)
  
        current_time = datetime.datetime.now()
   
        #send periodic timing ticks
        if  current_time >= last_time_update + datetime.timedelta(seconds = 1):
            command = "[0x00 11 {}]".format(time_sync_counter)
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


