#!/usr/bin/env python3

###########################################################################
# POOT
# The Zebro Project
# Delft University of Technology
# 2016
#
# Filename: pootPlot.py
#
# Description:
# Debug tool for use with the POOT leg module.
# Should be used in concunction with pootDebug.py
# This script received debug packages from the leg module over UDP
# It then plots the requested fields in real time.
# pootDebug.py can received the debug packages over UART and forward them
# UDP
#
# Authors:
# Piet De Vaere -- Piet@DeVae.re
###########################################################################

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import socket
from collections import deque
import random
import sys
import argparse

"""
Main class for the plotter application
"""
class UdpPlotter:
    buffersize = 4096
    vregs_label_start = "#define VREGS_"
    vregs_name_definitions_start = "/* BEGIN FIELD NAME DEFINITIONS */"
    vregs_name_definitions_end = "/* END FIELD NAME DEFINITIONS */"
    package_length = 261

    def __init__(self,
            udp_port,       # port to receive udp packages from
            udp_ip,         # ip to accect udp packages from
            columns,        # number of columns in the plotting window
            refresh_rate,   # time between data refreshes [ms]
            legend_file,    # path to the vregs.h file
            fields,         # array of fields to plot
            length):        # number of samples to store and show
        self.generate_legend(legend_file)
        self.fields = fields
        self.length = length
        self.udp_port = udp_port
        self.udp_ip = udp_ip
        self.data = {}
        self.window = None
        self.columns = columns
        self.refresh_rate = refresh_rate
        for field in self.fields:
            container = deque(maxlen = self.length)
            self.data[field] = container
        self.init_socket()
        self.plot()
        self.set_timer()
        self.generate_window()
        self.plotting = True
        self.window.keyPressEvent = self.process_keypress

    """
    Process keypresses generated in the plotting window
    """
    def process_keypress(self, event):
        arrow_key_delta = 1000
        if event.key() == QtCore.Qt.Key_Left:
            if self.length > arrow_key_delta:
                self.resize (self.length - arrow_key_delta)
        elif event.key() == QtCore.Qt.Key_Right:
            self.resize (self.length + arrow_key_delta)
        elif event.key() == QtCore.Qt.Key_Q:
            sys.exit(0)
        elif event.key() == QtCore.Qt.Key_Space:
            self.plotting = not self.plotting

    """
    Change the number of samples that are stored and displayed
    """
    def resize(self, new_length):
        for field in self.data:
            new_deque = deque(maxlen = new_length)
            new_deque.extend(self.data[field])
            while(len(new_deque) != new_length):
                if len(new_deque) == 0:
                    break
                new_deque.appendleft(new_deque[0])
            self.data[field] = new_deque
        self.length = new_length
        
    """
    Initialise UDP socket used to receive the data packages.
    """
    def init_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.udp_ip, self.udp_port))
        self.sock.settimeout(0.0)

    """
    Get all data that arrived over UDP since the last time this
    function was called
    """
    def get_data_from_socket(self):
        while True:
            try:
                rawdata = self.sock.recv(self.buffersize)
            except BlockingIOError:
                return
            self.add_data(rawdata)

    """
    Add the following data package to the history
    """
    def add_data(self, rawdata):
        for field in self.fields:
            if len(self.data[field]) == 0:
                for counter in range(self.length):
                    self.data[field].append(rawdata[field])

            else:
                 self.data[field].append(rawdata[field])
    
    """
    Parse the vregs.h file and extract the register labels from them
    """
    def generate_legend(self, legend_file):
        self.legend = [""] * self.package_length

        try:
            vregs = open(legend_file)
        except:
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
    Create the plotting window
    """
    def generate_window(self):
        self.window  = pg.GraphicsWindow()
        self.plots = {}
        row = 0
        column = 0
        for field in self.fields:
            title_text = "{} --- {}".format(field, self.legend[field])
            plot = self.window.addPlot(row, column, title = title_text)
            self.plots[field] = plot
            # if column == self.columns - 1:
            #     row = row + 1
            column = (column + 1) % self.columns
    """
    Draw the plots in the plotting window
    """
    def plot(self):
        if self.window == None:
            self.generate_window()
        for field in self.fields:
            try:
                self.plots[field].plot(self.data[field], clear = True)
            except NameError:
                pass
    
    """
    Configure the timer used for periodicly redrawing the plots
    """
    def set_timer(self):
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(self.refresh_rate)

    """
    Called by the timer.
    Fetches new data and plots it
    """
    def update(self):
        self.get_data_from_socket()
        if self.plotting:
            self.plot() 

    """
    Start the application
    """
    def run(self):
        self.plot()
        pg.QtGui.QApplication.exec_()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="Recieve debug data from leg module over UDP and plot it",
            epilog = \
            """ q: exit | <- : plot fewer samples |
                -> : plot more samples | space: pause plots""",
            add_help = True)
    parser.add_argument('fields',
            type=int,
            nargs='+',
            help='vregs field to plot')
    parser.add_argument("-p", "--port",
            default = 5000,
            type = int,
            help = "port to receive UDP packages on",
            dest = "udp_port")
    parser.add_argument("-i", "--ip",
            default = "0.0.0.0",
            help = "ip receive UDP packages from",
            dest = "udp_ip")
    parser.add_argument("-c", "--columns",
            default = None,
            type = int,
            help = "Number of columns in plotting window",
            dest = "columns")
    parser.add_argument("-r", "--refresh-rate",
            default = 20,
            type = int,
            help = "number of [ms] between plot updates",
            dest = "refresh_rate")
    parser.add_argument("-l", "--legend",
            default = "vregs.h",
            help = "Path the the vregs.h header file",
            dest = "legend_file")     
    parser.add_argument("-s", "--plot-size",
            default = 3000,
            type = int,
            help = "number of samples to show on the plot",
            dest = "length")

    args = parser.parse_args()

    plotter = UdpPlotter(
        udp_port = args.udp_port,
        udp_ip = args.udp_ip,
        columns = args.columns,
        refresh_rate = args.refresh_rate,
        legend_file = args.legend_file,
        fields = args.fields,
        length = args.length)
    
    plotter.run()
