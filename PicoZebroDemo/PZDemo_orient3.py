#!/usr/bin/env python
# TU Delft Pico Zebro Demo
# PZ_DEMO Orientation determination. (This code is for determing the orientation of the Pico Zebro.)
# Writer: Martijn de Rooij
# Version 0.03

# Everything is being tested from 120 cm

# Till now ALL steps are NOT giving satisfactory results. Sometimes they work sometimes they dont.

# Step 1 Pico Zebro Demo
# From live video find green and put a rectangle around it.
#   This is done as follows:
#   Step 1 is initialize the camera. (This determines how many green pixels will be seen)
#   Step 2 Determine the upper and lower levels in HSV for green.
#   HSV = https://henrydangprg.com/2016/06/26/color-detection-in-python-with-opencv/
#   Step 3 Capture video feed from Pi Camera in frames.
#   Step 4 Try to calibrate acording to lightlevel in test area.
#   Step 5 Create mask for determing if area is green
#   Step 6 Use function Find and draw green     (RESOLUTION MATTERS ALOT FOR THIS FUNCTION)
#   For more information about this function see functions_shape.py in the map Functions

# Step 2 Pico Zebro Demo
# In the found rectangle from step 1 find the QR code
#   This is done as follows:
#   Step 1 Take rectangle and resize the obtained images to a set size.
#   Step 2 This images in Canny contours detection
#   Step 3 Hope that the found largest contour is the one you want
#   This is because the size for w and h must be set otherwise the possibilities for finding bigger or smaller
#   largest contours is to big.

# Step 3 Pico Zebro Demo
# In the found QR code image figure out orientation
#   Step 1 Determine what black and white are in HSV values
#   Step 2 Find both black and white in the image
#   Step 3 Add them together
#   Step 4 Find from this the largest contour
#   (This is always the wanted one or the entire picture if somehting went wrong)
#   Step 5 Use functions cv2.minArea react for determing W and H from the QR code also the turned angle
#   (if it is not 0 or -90)
#   Step 6 make a smaller rectangle and from those four points determine if pixel is black or white
#   If pixel is white then you can easiliy determine orientation with rect[2] and which pixel was white


# Python 3 compatability
from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass

# import the functions
from Functions.functions_shape import functions_shape

# import the necessary packages
from picamera.array import PiRGBArray   # Pi camera Libary capture BGR video
from picamera import PiCamera           # PiCamera liberary
import time                             # For real time video (using openCV)
import numpy as np                      # Optimized library for numerical operations
import cv2                              # Include OpenCV library (Most important one)

# STEP 1

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (1920, 1088) #1920, 1088 #1280, 720 #1600, 912
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(1920, 1088))

#Standard hsv color values. These are obtained through code converter.py
green = [([40,33,40],[92,153,255])] #=green
black = [([0,0,0],[179,255,90])] #=black
white = [([0,0,230],[179,255,255])] #=white

white2 = [([0,0,110],[179,255,255])] #=white2
white3 = [([200,200,200],[255,255,255])] #white bgr for testing purposes
white4 = (200,255)


# allow the camera to warmup (So this is only during start up once).
time.sleep(0.1)

# Debug variable for doing someting just once in the code 
Do_once = 1

funct = functions_shape()

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the NumPy array representing the image, the initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array

# For finding the PicoZebro's
    
    # Making light levels less invluential
    # It takes the RGB it sees and adapts the light level of it
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l,a,b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(2,2))
    cl = clahe.apply(l)
    limg = cv2.merge((cl,a,b))
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    # Adjusting Gamma level if highly needed 1 means nothing changes
    adjusted = funct.adjust_gamma(final, 0.75)
    
    # color in cube is hsv values for easier detection of green.
    hsv = cv2.cvtColor(adjusted, cv2.COLOR_BGR2HSV)

    #green the important color
    for(lower,upper) in green:
            lower = np.array(lower,dtype=np.uint8)
            upper = np.array(upper,dtype=np.uint8) 
    # the mask 
    mask_green = cv2.inRange(hsv,lower,upper)

    #Show the green and the current view
    output = cv2.bitwise_and(adjusted, adjusted, mask = mask_green)
    #cv2.imshow("HSV green visable  ", output)

    # Use current frame image and hsv green value to find 2 largest
    # green contours, draw rectangle around them and put them in image
    funct.Find_draw(image, output)


#STEP 2
#code for finding Qr code in picoZebro image 1.

    #From here pn out it is orientation testing.
    Zebro_image = cv2.imread("Pico/tests1.jpg", 1)
    try:
        Zebro_height, Zebro_width = Zebro_image.shape[:2]
        Zebro_res = cv2.resize(Zebro_image, (200, 200),interpolation = cv2.INTER_CUBIC)
        
        #adjusting Gamma level if highly needed
        Zebro_adjust_gamma = funct.adjust_gamma(Zebro_res, 1)

        # Turn image into gray for finding contours.
        Zebro_gray = cv2.cvtColor(Zebro_adjust_gamma, cv2.COLOR_BGR2GRAY)

        Zebro_kernel= np.ones((3,3),np.uint8)
        Zebro_erosion = cv2.erode(Zebro_gray,Zebro_kernel, iterations=1) 
            
        Zebro_edges = cv2.Canny(Zebro_erosion, 100, 200, apertureSize = 3)
#Debugging
        cv2.imshow("edges Zebro",Zebro_edges)

        #Function for finding larges contour in image Zebro
        (_,contours2,hierarchy2) = cv2.findContours(Zebro_edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # Find contours with hierarchy
        areaArray = []
        
        for i, c in enumerate(contours2):
            area = cv2.contourArea(c)
            areaArray.append(area)
        sorteddata = sorted(zip(areaArray, contours2), key=lambda x: x[0], reverse=True)

        try:
            largestcontour = sorteddata[0][1]
            x, y, w, h = cv2.boundingRect(largestcontour)
            # After random testing these where the values that kind of worked for area for QR
            # This still isn't perfect
            #if w > 33 and h >33 and w < 70 and h < 70:     For 1280, 720
            if w > 20 and h > 20 and w < 65 and h < 75:
                #print(w,h)
                y = y-20
                x = x-20
                h=h+30
                w=w+30
                QR_CODE = Zebro_res[y:y+h, x:x+w]
                cv2.imshow("QR_CODE LargestContour", QR_CODE)
                cv2.imwrite("Pico/QR_CODE.jpg", QR_CODE)
        except IndexError:
            pass
    except AttributeError:
        pass

# STEP 3
# From here on out it is determing angle and with that direction

    # Pre found images for now for testing
    QR_image = cv2.imread("Pico/QR_CODE2.jpg", 1)

    # Making light levels less invluential
    # It takes the RGB it sees and adapts the light level of it
    QR_lab = cv2.cvtColor(QR_image, cv2.COLOR_BGR2LAB)
    QR_l,QR_a,QR_b = cv2.split(QR_lab)
    QR_clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(1,1))
    QR_cl = QR_clahe.apply(QR_l)
    QR_limg = cv2.merge((QR_cl,QR_a,QR_b))
    QR_final = cv2.cvtColor(QR_limg, cv2.COLOR_LAB2BGR)

    accumMask = np.zeros(QR_image.shape[:2], dtype="uint8")

    #adjusting Gamma level if highly needed
    QR_adjust_gamma = funct.adjust_gamma(QR_final, 1)

    # Converts to gray for better results
#   QR_gray = cv2.cvtColor(QR_adjust_gamma, cv2.COLOR_BGR2GRAY)

    # color in cube is hsv values for easier detection of green.
    QR_hsv = cv2.cvtColor(QR_adjust_gamma, cv2.COLOR_BGR2HSV)

    kernel_erode = np.ones((3,3),np.uint8)
    kernel_dilate = np.ones((4,4),np.uint8)
    kernel_closing = np.ones((4,4),np.uint8)

    # Detecting Black in QR code
    for(lower,upper) in black:
            lower = np.array(lower,dtype=np.uint8)
            upper = np.array(upper,dtype=np.uint8)
    mask_QR_black = cv2.inRange(QR_hsv,lower,upper)
    mask_QR_black = cv2.erode(mask_QR_black, kernel_erode, iterations=2)
    mask_QR_black = cv2.dilate(mask_QR_black, kernel_dilate, iterations=1)

#debugging
    cv2.imshow("mask_QR_black",mask_QR_black)
    # Detecting White in QR code
    for(lower,upper) in white:
            lower = np.array(lower,dtype=np.uint8)
            upper = np.array(upper,dtype=np.uint8)
    mask_QR_white = cv2.inRange(QR_hsv,lower,upper)
    
    mask_QR_white = cv2.erode(mask_QR_white, kernel_erode, iterations=2)
    mask_QR_white = cv2.dilate(mask_QR_white, kernel_dilate, iterations=1)

    #debugging
    cv2.imshow("mask_QR_white",mask_QR_white)
    cv2.imwrite("Pico/White_MASK.jpg", mask_QR_white)

    #Add White and black mask together
    accumMask = cv2.addWeighted(mask_QR_white,1,mask_QR_black,1,0)
#debugging
    cv2.imshow("accumMask",accumMask)
    #accumMask = cv2.bitwise_not(accumMask)
    
    #Finding largest contour in black and white image     
    mask_QR = cv2.erode(accumMask, None, iterations=1)
    mask_QR = cv2.dilate(mask_QR, None, iterations=2)
    mask_QR_closing = cv2.morphologyEx(mask_QR, cv2.MORPH_CLOSE, None)

    cv2.imshow("mask_QR_closing",mask_QR_closing)

    # Finds contours
    im2, cnts, hierarchy = cv2.findContours(mask_QR_closing.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    areaArray_QR = []
    
    for i, c_QR in enumerate(cnts):
        area_QR = cv2.contourArea(c_QR)
        areaArray_QR.append(area_QR)
        
    sorteddata_QR = sorted(zip(areaArray_QR, cnts), key=lambda x: x[0], reverse=True)

    MASK_WR = cv2.imread("Pico/White_MASK.jpg")

    Mask_image = np.zeros(MASK_WR.shape[:2], dtype="uint8")

    Mask_image = cv2.addWeighted(MASK_WR,1,QR_image,0.01,1)

    cv2.imshow("Mask_image", Mask_image)

    # Draws contours
    try:
        largestcontour_QR = sorteddata_QR[0][1]
        ## BEGIN - draw rotated rectangle
        rect = cv2.minAreaRect(largestcontour_QR)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        
        P_W, P_H = rect[1]
        P_W_New = int(P_W*0.65)
        P_H_New = int(P_H*0.65)
        rect_new = (rect[0]),(P_W_New,P_H_New),rect[2]
        box_new = cv2.boxPoints(rect_new)
        box_new = np.int0(cv2.boxPoints(rect_new))
        
        P_W_Pixel = int(P_W*0.15)
        P_H_Pixel = int(P_H*0.15)
        
        Pixel0 = (box_new[0,0],box_new[0,1])
        Pixel1 = (box_new[1,0],box_new[1,1])
        Pixel2 = (box_new[2,0],box_new[2,1])
        Pixel3 = (box_new[3,0],box_new[3,1])
        
        QR_square_0 = (Pixel0),(P_W_Pixel,P_H_Pixel),rect[2]
        QR_square_1 = (Pixel1),(P_W_Pixel,P_H_Pixel),rect[2]
        QR_square_2 = (Pixel2),(P_W_Pixel,P_H_Pixel),rect[2]
        QR_square_3 = (Pixel3),(P_W_Pixel,P_H_Pixel),rect[2]
        
        QR_square_0_test = np.int0(cv2.boxPoints(QR_square_0))
        QR_square_1_test = np.int0(cv2.boxPoints(QR_square_1))
        QR_square_2_test = np.int0(cv2.boxPoints(QR_square_2))
        QR_square_3_test = np.int0(cv2.boxPoints(QR_square_3))
        
        if abs(rect[2]) <= 45:
            QR_y_0 = (np.asscalar(np.uint16(QR_square_0_test[1,1])))
            QR_x_0 = (np.asscalar(np.uint16(QR_square_0_test[1,0])))
            QR_y_1 = (np.asscalar(np.uint16(QR_square_1_test[1,1])))
            QR_x_1 = (np.asscalar(np.uint16(QR_square_1_test[1,0])))
            QR_y_2 = (np.asscalar(np.uint16(QR_square_2_test[1,1])))
            QR_x_2 = (np.asscalar(np.uint16(QR_square_2_test[1,0])))
            QR_y_3 = (np.asscalar(np.uint16(QR_square_3_test[1,1])))
            QR_x_3 = (np.asscalar(np.uint16(QR_square_3_test[1,0])))
        elif abs(rect[2]) > 45:
            QR_y_0 = (np.asscalar(np.uint16(QR_square_0_test[2,1])))
            QR_x_0 = (np.asscalar(np.uint16(QR_square_0_test[2,0])))
            QR_y_1 = (np.asscalar(np.uint16(QR_square_1_test[2,1])))
            QR_x_1 = (np.asscalar(np.uint16(QR_square_1_test[2,0])))
            QR_y_2 = (np.asscalar(np.uint16(QR_square_2_test[2,1])))
            QR_x_2 = (np.asscalar(np.uint16(QR_square_2_test[2,0])))
            QR_y_3 = (np.asscalar(np.uint16(QR_square_3_test[2,1])))
            QR_x_3 = (np.asscalar(np.uint16(QR_square_3_test[2,0])))

            
        QR_Area_Orientation_0 = QR_image[QR_y_0:QR_y_0+P_H_Pixel,QR_x_0:QR_x_0+P_W_Pixel]
        QR_Area_Orientation_1 = QR_image[QR_y_1:QR_y_1+P_H_Pixel,QR_x_1:QR_x_1+P_W_Pixel]
        QR_Area_Orientation_2 = QR_image[QR_y_2:QR_y_2+P_H_Pixel,QR_x_2:QR_x_2+P_W_Pixel]
        QR_Area_Orientation_3 = QR_image[QR_y_3:QR_y_3+P_H_Pixel,QR_x_3:QR_x_3+P_W_Pixel]

    #From here
        #QR_Area_Orientation_0 = cv2.resize(QR_Area_Orientation_0, (200, 200),interpolation = cv2.INTER_CUBIC)
        #cv2.imshow("QR_Area_Orientation_0", QR_Area_Orientation_0)
        
        QR_Orientation_hsv_0 = cv2.cvtColor(QR_Area_Orientation_0, cv2.COLOR_BGR2GRAY)

        ret,QR_Orientation_hsv_0 = cv2.threshold(QR_Orientation_hsv_0,127,255,cv2.THRESH_BINARY)
        QR_Orientation_hsv_0 = cv2.cvtColor(QR_Orientation_hsv_0, cv2.COLOR_GRAY2BGR)
        QR_Orientation_hsv_0 = cv2.cvtColor(QR_Orientation_hsv_0, cv2.COLOR_BGR2HSV)

        #QR_Orientation_hsv_0 = cv2.cvtColor(QR_Area_Orientation_0, cv2.COLOR_BGR2HSV)

        #QR_Orientation_hsv_0 = cv2.bitwise_not(QR_Orientation_hsv_0)

        QR_Orientation_hsv_1 = cv2.cvtColor(QR_Area_Orientation_1, cv2.COLOR_BGR2GRAY)
        QR_Orientation_hsv_1 = cv2.cvtColor(QR_Area_Orientation_1, cv2.COLOR_BGR2HSV)
        #QR_Orientation_hsv_1 = cv2.bitwise_not(QR_Orientation_hsv_1)
        QR_Orientation_hsv_2 = cv2.cvtColor(QR_Area_Orientation_2, cv2.COLOR_BGR2GRAY)
        QR_Orientation_hsv_2 = cv2.cvtColor(QR_Area_Orientation_2, cv2.COLOR_BGR2HSV)
        #QR_Orientation_hsv_2 = cv2.bitwise_not(QR_Orientation_hsv_2)
        QR_Orientation_hsv_3 = cv2.cvtColor(QR_Area_Orientation_3, cv2.COLOR_BGR2GRAY)
        QR_Orientation_hsv_3 = cv2.cvtColor(QR_Area_Orientation_3, cv2.COLOR_BGR2HSV)
        #QR_Orientation_hsv_3 = cv2.bitwise_not(QR_Orientation_hsv_3)


        for(lower,upper) in white2:
            lower = np.array(lower,dtype=np.uint8)
            upper = np.array(upper,dtype=np.uint8)

        white_pixel0 = cv2.inRange(QR_Orientation_hsv_0,lower,upper)
        white_pixel1 = cv2.inRange(QR_Orientation_hsv_1,lower,upper)
        white_pixel2 = cv2.inRange(QR_Orientation_hsv_2,lower,upper)
        white_pixel3 = cv2.inRange(QR_Orientation_hsv_3,lower,upper)

    # TO here it is going wrong. Only here for step 3. I dont know what just the amount of white is not correct here

        if Do_once ==1:
            print(abs(rect[2]))
            print("Found White on pixel 0")
            white_pixel0 = cv2.countNonZero(white_pixel0)
            print(white_pixel0)
            print("Found White on pixel 1")
            white_pixel1 = cv2.countNonZero(white_pixel1)
            print(white_pixel1)
            print("Found White on pixel 2")
            white_pixel2 = cv2.countNonZero(white_pixel2)
            print(white_pixel2)
            print("Found White on pixel 3")
            white_pixel3 = cv2.countNonZero(white_pixel3)
            print(white_pixel3)

            if white_pixel0 > white_pixel1 and white_pixel0 > white_pixel2 and white_pixel0 > white_pixel3:
                degree = abs(rect[2])
                print("PIXEL 000000")
                print (degree)
            if white_pixel1 > white_pixel0 and white_pixel1 > white_pixel2 and white_pixel1 > white_pixel3:
                degree = 270 + abs(rect[2])
                print("PIXEL 1111111")
                print (degree)
            if white_pixel2 > white_pixel0 and white_pixel2 > white_pixel1 and white_pixel2 > white_pixel3:
                degree = 180 + abs(rect[2])
                print("PIXEL 22222222")
                print (degree)
            if white_pixel3 > white_pixel0 and white_pixel3 > white_pixel1 and white_pixel3 > white_pixel2:
                degree = 90 + abs(rect[2])
                print("PIXEL 33333333")
                print (degree)
            
            Do_once = 2
 
        #draw both cantours. The one around the QR code and the one were the white pixel is determined out of.
        #cv2.drawContours(QR_image,[box],0,(0,191,255),2)
        cv2.drawContours(QR_image,[QR_square_0_test],0,(0,191,0),2)
        cv2.drawContours(QR_image,[QR_square_1_test],0,(0,191,0),2)
        cv2.drawContours(QR_image,[QR_square_2_test],0,(0,191,0),2)
        cv2.drawContours(QR_image,[QR_square_3_test],0,(0,191,0),2)
        # Draw a diagonal blue line with thickness of 2 px for checking where white pixel is.
        cv2.line(QR_image,(box_new[0,0],box_new[0,1]),(box_new[2,0],box_new[2,1]),(255,191,0),2)
        cv2.line(QR_image,(QR_square_0_test[0,0],QR_square_0_test[0,1]),(QR_square_0_test[2,0],QR_square_0_test[2,1]),(255,191,0),2)
        cv2.line(QR_image,(QR_square_1_test[0,0],QR_square_1_test[0,1]),(QR_square_1_test[2,0],QR_square_1_test[2,1]),(255,191,0),2)
        cv2.line(QR_image,(QR_square_2_test[0,0],QR_square_2_test[0,1]),(QR_square_2_test[2,0],QR_square_2_test[2,1]),(255,191,0),2)
        cv2.line(QR_image,(QR_square_3_test[0,0],QR_square_3_test[0,1]),(QR_square_3_test[2,0],QR_square_3_test[2,1]),(255,191,0),2)

        ## END - draw rotated rectangle
    except IndexError:
        print(IndexError)
        pass
    
#    cv2.imshow('sdsdsdasada', thresh1)
    cv2.imshow('outout QR code', QR_image)

#Show current vieuw of camera

    # Take current day
    Timetest = time.strftime("%d-%m-%Y")
    # Show the current view for debugging
    #cv2.imshow("original %s" % Timetest,image)

    # show the frame
    key = cv2.waitKey(1) & 0xFF

    #clear the stream in preparation of the next frame
    rawCapture.truncate(0)

    # if the 'q' key was pressed, break from the loop
    if key == ord("q"):
        # cleanup the camera and close any open windows
        cv2.destroyAllWindows()
        break
