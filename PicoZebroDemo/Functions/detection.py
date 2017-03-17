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
        #cv2.imwrite("image_Green.jpg", mask_green)

        gray_green = cv2.cvtColor(mask_green, cv2.COLOR_BGR2GRAY)

        (_, cnts2, _) = cv2.findContours(gray_green.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_NONE)
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
            #elif Pico_Zebro_Found == 11:
                #print("TO MANY ZEBROS")
        PZ = [Pico_Zebro_0, Pico_Zebro_1, Pico_Zebro_2, Pico_Zebro_3, Pico_Zebro_4,
              Pico_Zebro_5, Pico_Zebro_6, Pico_Zebro_7, Pico_Zebro_8, Pico_Zebro_9]
        
        return PZ

    def auto_canny(self, image, sigma=0.33):
            # compute the median of the single channel pixel intensities
            v = np.median(image)
     
            # apply automatic Canny edge detection using the computed median
            lower = int(max(0, (1.0 - sigma) * v))
            upper = int(min(255, (1.0 + sigma) * v))
            edged = cv2.Canny(image, lower, upper)
     
            # return the edged image
            return edged

    def Filter_Green(self, image, image_filter, mask_green):
        
        image_filter = cv2.bilateralFilter(image_filter, 11, 50, 50)
        #image_green = cv2.bitwise_and(image_filter, image_filter, mask = mask_green)
        #image_filter2 = cv2.addWeighted(image_green,0.8,image_filter,0.2,0)

        #image_filter = self.auto_canny(image_green)

        image_filter = cv2.Canny(image_filter, 15, 210)

        cv2.imshow("filter", image_filter)
        cv2.imwrite("image_Filter.jpg", image_filter)
        
        (_, cnts2, _) = cv2.findContours(image_filter.copy(), cv2.RETR_TREE,
                                    cv2.CHAIN_APPROX_NONE)
        cnts2 = sorted(cnts2, key = cv2.contourArea, reverse = True)#[:100]
        screenCnt = None
        # loop over our contours
        for c in cnts2:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            #cv2.drawContours(image, [c], -1, (255, 0, 255), -1)
             
            # if our approximated contour has four points, then
            # we can assume that we have found our screen
            if len(approx) == 4:
                screenCnt = approx
                break
        cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 5)
        cv2.imshow("Rectangles?", image)
        cv2.imwrite("Found_Zebro_Filter_green.jpg", image)

        return 0#PZ#green_area

