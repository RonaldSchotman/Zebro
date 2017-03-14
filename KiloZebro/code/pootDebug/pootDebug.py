#!/usr/bin/env python3

###########################################################################
# POOT
# The Zebro Project
# Delft University of Technology
# 2016
#
# Filename: pootDebug.py
#
# Description:
# Debug tool for use with the POOT leg module.
# It receives the debug information transmitten over the UART of the
# leg module. If provided, it will use the vref.h header file to
# label the debug information
#
# Authors:
# Piet De Vaere -- Piet@DeVae.re
###########################################################################

import serial
import curses
import datetime
import csv
import argparse
import socket
from collections import deque

"""
This is the main class, it manages the screen, writes to the logfile ...
"""
class Debugger:
    vregs_label_start = "#define VREGS_"
    vregs_name_definitions_start = "/* BEGIN FIELD NAME DEFINITIONS */"
    vregs_name_definitions_end = "/* END FIELD NAME DEFINITIONS */"
    
    def __init__(self,
                    screen,                 # ncurses screen
                    serial_port,            # serial port the leg module is connected to
                    baudrate,               # baud rate
                    view_data,              # list of register to be viewed
                    legend_file,            # path to vregs.h file
                    write_log,              # when True we write to disk
                    udp_ip,                 # ip to send udp packages to
                    udp_port,               # port to send udp packages to
                    history_depth,          # how many packages to keep in memory
                    align_value = [0xFF, 0x45, 0x12, 0xEA, 0x4B],     # sequence used to find the beginning of a frame
                    package_length = 261):  # length of a frame
    
        self.screen = screen
        self.screen.nodelay(True)
        self.align_value = align_value
        self.package_length = package_length
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.write_log = write_log
        self.history = deque(maxlen = history_depth)
        if udp_ip and udp_port:
            self.udp_enabled = True
            self.udp_socket = UdpSocket(udp_ip, udp_port)
        else:
            self.udp_enabled = False
            self.udp_socket = None
        self.serial = SerialInterface(  port_name = self.serial_port,
                                        baudrate = self.baudrate,
                                        package_length = self.package_length,
                                        align_value = self.align_value);
        self.generate_legend(legend_file)
        self.view_data = view_data
        self.log = None
        self.log_writer = None

    """
    Transmit a serial data package over UDP
    """
    def send_over_udp(self, serial_data):
        if self.udp_enabled and self.udp_socket:
            self.udp_socket.send_package(serial_data)

    """
    Parse the vregs.h file and extract the register labels from them
    """
    def generate_legend(self, legend_file):
        self.legend = [""] * self.package_length
        
        try:
            vregs = open(legend_file)
        except:
            print ("niet gelukt")
            return
        
        line = vregs.readline().strip()
        while(line != self.vregs_name_definitions_start):
            line = vregs.readline().strip()
        
        for line in vregs:
            line = line.strip()
            if line == self.vregs_name_definitions_end:
                return
            if line.startswith(self.vregs_label_start):
                line = line[len(self.vregs_label_start):]
                line = line.split()
                label = line[0]
                index = int(line[1])
                self.legend[index] = label
            
    """
    Start the debugger.
    Read the serial port and write data to screen and to disk
    """  
    def start(self):
        self.serial.open()
        if self.write_log:
            self.open_log()
            
        while(True):
            serial_data = self.serial.read_package()
            self.display(serial_data)
            self.write_log_line(serial_data)
            self.send_over_udp(serial_data)
            self.history.append(serial_data)
            
            # see if the user has pushed a key, and process it
            try:
                key = self.screen.getch()
            except:
                pass
            else:
                # in the event of a screen resize
                if key == curses.KEY_RESIZE:
                    # prevent ncurses from crashing on screen resize
                    self.screen.clear()
                elif key == ord('q'):
                    # exit gracefully
                    self.close_log()
                    break;
                elif key == ord('u'):
                    self.udp_enabled = True
                elif key == ord('y'):
                    self.udp_enabled = False
                elif key == ord(' '):
                    if not self.write_log:
                        self.write_log = True
                        self.open_log()
                    
    """
    Generate the log file name, and open it for writing
    """
    def open_log(self):
        self.log_file = "POOT_debug_log_" + \
            datetime.datetime.now().isoformat().replace(':','-').replace('.','-') + \
            ".csv"
        try:
            self.log = open(self.log_file, 'w')
        except:
            pass
        else:
            self.log_writer = csv.writer(self.log)
            self.write_log_header()
            self.write_history_to_log()
            
    def write_history_to_log(self):
        for package in self.history:
            self.write_log_line(package)
    """
    close the log file
    """
    def close_log(self):    
        if self.log == None:
            self.log_writer == None
            
        else:
            self.log.close()    
            self.log = None
            self.log_writer = None
    """
    Write a line of data to the logfile
    """        
    def write_log_line(self, serial_data):
        if (self.log_writer == None) or (self.log == None):
            return
        
        log_data = []
        log_data.append(serial_data.get_time().isoformat())
        for entry in serial_data:
            log_data.append(entry)
        
        self.log_writer.writerow(log_data)
   
    """
    Write the header information to the logfile.
    This includes register numbers and lables
    """
    def write_log_header(self):
        index_data = [""] + list(range(self.package_length))
        header_data = ["time"] + self.legend
        
        self.log_writer.writerow(index_data)
        self.log_writer.writerow(header_data)
    
    """
    Put the received data on the screen
    """
    def display(self, serial_data):
        total_width = 3 + 1 + 20 + 1 + 3 + 2
        screen_size = self.screen.getmaxyx()
            
        self.screen.addstr(0,0, serial_data.get_time().isoformat())
        self.screen.addstr(0, total_width - 1, "|")
            
        y_cursor = 1
        x_cursor = 0
        for index in range(self.package_length):
            if (self.view_data == None) or (index in self.view_data):
                self.screen.addstr(y_cursor, x_cursor, self.line_to_string(index, serial_data[index]))
                y_cursor = y_cursor + 1
                if y_cursor >= self.screen.getmaxyx()[0]:
                    x_cursor = x_cursor + total_width
                    y_cursor = 0
                if x_cursor + total_width >= self.screen.getmaxyx()[1]:
                    break
        
        if(self.screen.getmaxyx == screen_size):
            self.screen.refresh()
              
    """
    generate the display  text for a single register entry         
    """
    def line_to_string(self, index, data):
        legend_text = self.legend[index]
        print_string = "{0:<3} {2:<3} {1:<20} |"
        print_string = print_string.format(index, legend_text, data)
        return print_string
            
        
        
"""
class to interface the serial port, and to allign the frames
"""
class SerialInterface:
    def __init__(self, port_name, baudrate, package_length, align_value):
        self.port = serial.Serial()
        self.port.baudrate = baudrate
        self.port.port = port_name
        self.package_length = package_length
        self.align_value = align_value
    
    """
    Open the serial port
    """ 
    def open(self):
        self.port.open()
        self.align();

    """
    Align the receiver (that's us)  with the frames from the leg module
    """
    def align(self):
        state = 0
        sequence_steps = len(self.align_value)
        
        serial_data = self.port.read()[0];
        print(serial_data)
        while(state < sequence_steps):
            if serial_data == self.align_value[state]:
                state = state + 1
            else:
                state = 0;
            if state >= sequence_steps:
                return    
            serial_data = self.port.read()[0]
            print(serial_data)
    
    """
    Check if the package is alligned
    """  
    def check_for_align(self, data_package):
        for i in range(len(self.align_value)):
            if self.align_value[-(i+1)] != data_package[-(i+1)]:
                return False
        return True

    """
    Read a package from the leg module
    """
    def read_package(self):
        serial_package = self.port.read(self.package_length)
        # if the alignment is wrong, re-align, and read again
        if not self.check_for_align(serial_package):
            self.align()
            return self.read_package()

        return SerialPackage(serial_package)

"""
Wrapper class for a serial data frame
"""
class SerialPackage:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.size = len(raw_data)
        self.timestamp = datetime.datetime.now()
    
    """
    Get the time at which this packet was received
    """     
    def get_time(self):
        return self.timestamp
        
    def __getitem__(self, index):
        return self.raw_data[index]
        
    def __iter__(self):
        return iter(self.raw_data)
        
    def get_raw_data(self):
        return self.raw_data

    def display(self):
        for i in range(self.size):
            print_string = "{:>3} {}"
            print_string = print_string.format(i, self.raw_data[i])
            print(print_string)
"""
Wrapper class for a UDP socket used to transmit serial data packages
"""   
class UdpSocket:
    def __init__(self, ip, port):
        self.port = port
        self.ip = ip
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    """
    Transmit a serial data package over this udp socket
    """
    def send_package(self, serial_package):
        self.sock.sendto(serial_package.get_raw_data(), (self.ip, self.port))

def main(stdscr, args):
    curses.curs_set(0)
    debugger = Debugger(
            screen = stdscr,
            serial_port = args.serial_port,
            baudrate = args.baud_rate,
            view_data = args.view_data,
            legend_file = args.legend_file,
            udp_ip = args.udp_ip,
            udp_port = args.udp_port,
            history_depth = args.history_depth,
            write_log = args.write_log)
    debugger.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="Receive and decode debug info from a zebro leg module.",
            epilog = \
            """ q: exit | u: enable UDP transmitions |
                y: disable UDP transmitions | space: start writing log file""",
            add_help = True)
    parser.add_argument("-p", "--port",
            default = "/dev/ttyUSB2",
            help = "The serial port to read from",
            dest = "serial_port")
    parser.add_argument("-b", "--baud",
            default = 2000000,
            type = int,
            help = "The baud rate of the serial port",
            dest = "baud_rate")
    parser.add_argument("-i", "--history-depth",
            default = 10000,
            type = int,
            help = "The number of past data packages to keep in memory",
            dest = "history_depth")
    parser.add_argument("-l", "--legend",
            default = "vregs.h",
            help = "Path the the vregs.h header file",
            dest = "legend_file")
    parser.add_argument("-d", "--to-disk",
            action = "store_true",
            default = False,
            help = "write logfile to disk",
            dest = "write_log")
    parser.add_argument("-u", "--udp-port",
            default = 5000,
            type = int,
            help = "port to forward UDP pacakges to",
            dest = "udp_port")
    parser.add_argument("-t", "--udp-ip",
            default = "127.0.0.1",
            help = "ip to forward UDP pacakges to",
            dest = "udp_ip")
    parser.add_argument("-r", "--register",
            action = "append",
            default = None,
            type = int,
            help = "Only watch a subset of virtual registers",
            dest = "view_data")
    args = parser.parse_args()
    
    curses.wrapper(main, args)
    
