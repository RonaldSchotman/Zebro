#!/usr/bin/env python
# TU Delft Pico Zebro Demo
# Writer: Martijn de Rooij
# Version 0.01
# Determing the shape

# Python 3 compat
from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass

# Import the necessary packages
import numpy as np                      # Optimized library for numerical operations
import cv2                              # Include OpenCV library

class functions_shape:
    def __init__(self):
        pass

    
    def adjust_gamma(self, image, gamma):
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
                          for i in np.arange(0,256)]).astype("uint8")
        return cv2.LUT(image, table)

    def Find_draw(self, image, output):
        kernel = np.ones((7,7),np.uint8)

        closing = cv2.morphologyEx(output, cv2.MORPH_CLOSE, kernel)

        gray_green = cv2.cvtColor(closing, cv2.COLOR_BGR2GRAY)

        (_, cnts2, _) = cv2.findContours(gray_green.copy(), cv2.RETR_TREE,
                                    cv2.CHAIN_APPROX_SIMPLE)
        x = 0

        for c in cnts2:
            x1,y1,w1,h1 = cv2.boundingRect(c)
            if (w1 > 25) and (h1 > 25): #(x1 > 550) and (y1 > 150) and (w1 > 500) and (h1 > 120)
                # if resolution = 1280, 720 do 25 by 25 for w1 and h1
                # if resolution = 1920, 1080 do 101 by 101 for w1 and h1
                x  = x + 1
                try:
                    cv2.rectangle(image,(x1-20,y1-20),(x1+w1+20,y1+h1+20),(0,255,0),2)
                    cv2.putText(image,'green Detected',(x1+w1+30,y1+h1+20),0,0.3,(0,255,0))

                    green_area = image[y1-20:y1+h1+20, x1-20:x1+w1+20]
                    cv2.imwrite("Pico/tests%d.jpg" % x, green_area)

                except IndexError:
                    pass
            else:
                pass

    #Do This function only the first time to determine values for Find_Draw:            
    def Find_draw_largest(self, image, output):
        kernel = np.ones((7,7),np.uint8)

        closing = cv2.morphologyEx(output, cv2.MORPH_CLOSE, kernel)
        opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

        gray_green = cv2.cvtColor(closing, cv2.COLOR_BGR2GRAY)

        (_, cnts2, _) = cv2.findContours(gray_green.copy(), cv2.RETR_TREE,
                                    cv2.CHAIN_APPROX_SIMPLE)

        areaArray = []
        for i, c in enumerate(cnts2):
            area = cv2.contourArea(c)
            areaArray.append(area)

        #first sort the array by area
        sorteddata = sorted(zip(areaArray, cnts2), key=lambda x: x[0], reverse=True)

        #find the nth largest contour [n-1][1], in this case 1
        try:
            largestcontour = sorteddata[0][1]

            #draw it
            x, y, w, h = cv2.boundingRect(largestcontour)
            print (w,h)
            
            appelkoek = image[y:y+h, x:x+w]
            cv2.imwrite("appelkoek2.jpg", appelkoek)
            cv2.rectangle(image, (x, y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(image,'GROEN JAHOOR',(x+w+10,y+h),0,0.3,(0,255,0))

        except IndexError:
            pass        


