#!/usr/bin/env python
# TU Delft Pico Zebro Demo Detection Functions
# Writer: Martijn de Rooij
# Version 0.01
# Calibration Functions

# Import the necessary packages
import numpy as np                      # Optimized library for numerical operations
import cv2                              # Include OpenCV library

class calibration_functions:
    def __init__(self):
        pass

    #Calibration of gamma level
    def adjust_gamma(self, image, gamma):
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
                          for i in np.arange(0,256)]).astype("uint8")
        return cv2.LUT(image, table)
    
    #Calibration of light level
    def calibrate_light(self, image):
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l,a,b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(2,2))
        cl = clahe.apply(l)
        limg = cv2.merge((cl,a,b))
        #final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
