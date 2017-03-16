#!/usr/bin/env python
# TU Delft Pico Zebro Demo Threading Functions
# Writer: Martijn de Rooij
# Version 0.01
# Creating and killing of threads when necessary

# Import the necessary packages
import numpy as np                      # Optimized library for numerical operations
import cv2                              # Include OpenCV library
import threading                        # Liibrary for threads.

global PZ1 = 1

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

class threading_functions:
    def __init__(self):
        pass

    def printit(self):
        threading.Timer(5.0, self.printit).start()
        print ("Hello, World!")
        PZ = PZ1
        print(PZ)
