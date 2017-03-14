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

    def Green(self, image, image_green):
        kernel = np.ones((8,8),np.uint8)

        mask_green = cv2.morphologyEx(image_green, cv2.MORPH_CLOSE, kernel)
        mask_green = cv2.dilate(mask_green, None, iterations=1)
        cv2.imshow("mask_green",mask_green)

        gray_green = cv2.cvtColor(mask_green, cv2.COLOR_BGR2GRAY)

        (_, cnts2, _) = cv2.findContours(gray_green.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
        Pico_Zebro_Found = 0
        
        Pico_Zebro_0 = 0
        green_area = image[0:0+0, 0:0+0]
        Pico_Zebro_1 = 0
        Pico_Zebro_2 = 0
        Pico_Zebro_3 = 0
        Pico_Zebro_4 = 0
        Pico_Zebro_5 = 0
        Pico_Zebro_6 = 0
        Pico_Zebro_7 = 0
        Pico_Zebro_8 = 0
        Pico_Zebro_9 = 0
        
        for c in cnts2:
            x1,y1,w1,h1 = cv2.boundingRect(c)
            if (w1 > 35) and (h1 > 35):
                Pico_Zebro_Found  = Pico_Zebro_Found + 1
                try:
                    cv2.rectangle(image,(x1-40,y1-40),(x1+w1+40,y1+h1+40),(0,255,0),2)
                    cv2.putText(image,'green Detected',(x1+w1+50,y1+h1+40),0,0.3,(0,255,0))

                    #green_area = image[y1-10:y1+h1+10, x1-10:x1+w1+10]
                    #cv2.imwrite("Pico_Zebro/Pico_Zebro_%d.jpg" % Pico_Zebro_Found, green_area)
                except IndexError:
                    pass
            else:
                pass

            if Pico_Zebro_Found == 0:
                Pico_Zebro_0 = 0
                Pico_Zebro_1 = 0
                Pico_Zebro_2 = 0
                Pico_Zebro_3 = 0
                Pico_Zebro_4 = 0
                Pico_Zebro_5 = 0
                Pico_Zebro_6 = 0
                Pico_Zebro_7 = 0
                Pico_Zebro_8 = 0
                Pico_Zebro_9 = 0
            elif Pico_Zebro_Found == 1:
                green_area = image[y1-20:y1+h1+20, x1-20:x1+w1+20]
                Pico_Zebro_0 = 1
            elif Pico_Zebro_Found == 2:
                Pico_Zebro_1 = 1
            elif Pico_Zebro_Found == 3:
                Pico_Zebro_2 = 1
            elif Pico_Zebro_Found == 4:
                Pico_Zebro_3 = 1
            elif Pico_Zebro_Found == 5:
                Pico_Zebro_4 = 1
            elif Pico_Zebro_Found == 6:
                Pico_Zebro_5 = 1
            elif Pico_Zebro_Found == 7:
                Pico_Zebro_6 = 1
            elif Pico_Zebro_Found == 8:
                Pico_Zebro_7 = 1
            elif Pico_Zebro_Found == 9:
                Pico_Zebro_8 = 1
            elif Pico_Zebro_Found == 10:
                Pico_Zebro_9 = 1
            elif Pico_Zebro_Found == 11:
                print("TO MANY ZEBROS")
        PZ = [Pico_Zebro_0, Pico_Zebro_1, Pico_Zebro_2, Pico_Zebro_3, Pico_Zebro_4,
              Pico_Zebro_5, Pico_Zebro_6, Pico_Zebro_7, Pico_Zebro_8, Pico_Zebro_9]
        
        return green_area
