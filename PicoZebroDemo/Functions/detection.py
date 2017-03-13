#!/usr/bin/env python
# TU Delft Pico Zebro Demo Detection Functions
# Writer: Martijn de Rooij
# Version 0.01
# Determing if green is sighted.

# Import the necessary packages
import numpy as np                      # Optimized library for numerical operations
import cv2                              # Include OpenCV library

class detection_functions:
    def __init__(self):
        pass

    def Green(self, image, output):
        kernel = np.ones((7,7),np.uint8)

        #closing = cv2.morphologyEx(output, cv2.MORPH_CLOSE, kernel)

        gray_green = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

        (_, cnts2, _) = cv2.findContours(gray_green.copy(), cv2.RETR_TREE,
                                    cv2.CHAIN_APPROX_SIMPLE)
        x = 0

        for c in cnts2:
            x1,y1,w1,h1 = cv2.boundingRect(c)
            if (w1 > 35) and (h1 > 35):
                x  = x + 1
                try:
                    cv2.rectangle(image,(x1-10,y1-10),(x1+w1+10,y1+h1+10),(0,255,0),2)
                    cv2.putText(image,'green Detected',(x1+w1+20,y1+h1+10),0,0.3,(0,255,0))

                    green_area = image[y1-10:y1+h1+10, x1-10:x1+w1+10]
                    cv2.imwrite("Pico_Zebro/Pico_Zebro_%d.jpg" % x, green_area)

                except IndexError:
                    pass
            else:
                pass
