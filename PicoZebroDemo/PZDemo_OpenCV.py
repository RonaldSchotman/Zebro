#!/usr/bin/env python
# TU Delft Pico Zebro Demo
# PZ_DEMO recognition determination. (This code is for recognizing Pico Zebro)
# Writer: Martijn de Rooij
# Version 0.03

# Everything is being tested from 120 cm height.

# Python 3 compatability
from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass

# import detection functions
from Functions.detection import detection_functions
from Functions.calibration import calibration_functions

Detect = detection_functions()
Calib = calibration_functions()

# import the necessary packages
from picamera.array import PiRGBArray   # Pi camera Libary capture BGR video
from picamera import PiCamera           # PiCamera liberary
import time                             # For real time video (using openCV)
import numpy as np                      # Optimized library for numerical operations
import cv2                              # Include OpenCV library (Most important one)

# Step 1 Calibration Camera

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (1648, 928)
camera.framerate = 5
rawCapture = PiRGBArray(camera, size=(1648, 928))

# allow the camera to warmup (So this is only during start up once).
time.sleep(0.5)

# Calibration Functions (They dont work yet)
#data = np.load('calibration_ouput_1.npz') # This Calibration File is not yet correct
#(ret, mtx, dist, rvecs, tvecs) = (data['ret'], data['mtx'], data['dist'], data['rvecs'], data['tvecs'])

#Standard hsv color values. 
green = [([40,33,40],[92,153,255])] #=green
black = [([0,30,0],[179,230,50])] #=black
white = [([0,0,220],[179,255,255])] #=white

white2 = [([0,0,220],[179,255,255])] #=white

Do_once = 1

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the NumPy array representing the image, the initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array

# Calibration
    #Calibrate Every Frame acording to calibration data
    #h,w = image.shape[:2]
    #(newcameramtx, roi) = cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
    # undistort
    #Undistort_image = cv2.undistort(image, data['mtx'], data['dist'], None, newcameramtx)
    # undistort V2
    #mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
    #dst = cv2.remap(image,mapx,mapy,cv2.INTER_LINEAR)

    # crop the image is not an option so show new image
    #cv2.imshow("Undistort_image" ,Undistort_image)

    #Use of calibrated image using data

    # Calibrate on light level
    image_light = Calib.calibrate_light(image)

    # Adjusting Gamma level if highly needed 1 means nothing changes
    image_gamma = Calib.adjust_gamma(image_light, 1)

    #Blur image for better detection
    image_blurred = cv2.GaussianBlur(image_gamma, (11, 11), 0)
    #image_blur = cv2.medianBlur(image_gamma, 5)

#Step 1 Detect Green (right now I am quite happy with how well this works, not perfect but good enough)
    #should  still return coordinates

    #USeless functions
    image_gray = cv2.cvtColor(image_blurred, cv2.COLOR_BGR2GRAY)

    #image_test = cv2.adaptiveThreshold(image_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                  #                     cv2.THRESH_BINARY,111,31)
    cv2.imwrite("Pico/image_test2.jpg", image_gray)
    #cv2.imshow("image_test", image_test)
    
    image_hsv = cv2.cvtColor(image_blurred, cv2.COLOR_BGR2HSV)

    #green the important color
    for(lower,upper) in green:
            lower = np.array(lower,dtype=np.uint8)
            upper = np.array(upper,dtype=np.uint8) 
    # the mask 
    mask_green = cv2.inRange(image_hsv,lower,upper)

    image_green = cv2.bitwise_and(image_blurred, image_blurred, mask = mask_green)

    Pico_Zebro = []
    Found_Zebro = Detect.Green(image, image_green)
    Pico_Zebro.append(Found_Zebro)    #HERE is in a array how many Zebro's are found (MAX 10)
    #print(Pico_Zebro)

#Step 2 Find QR code in detected green area
    try:
        #cv2.imshow("Pico_Zebro",Found_Zebro)
        Zebro_height, Zebro_width = Found_Zebro.shape[:2]
        
        if(Zebro_height == 0) or (Zebro_width == 0):
            Found_Zebro = cv2.imread("Pico/testing5.jpg", 1)
            Zebro_res = cv2.resize(Found_Zebro, (200, 200),interpolation = cv2.INTER_CUBIC)
        else:
            Zebro_res = cv2.resize(Found_Zebro, (200, 200),interpolation = cv2.INTER_CUBIC)
        
        #adjusting Gamma level if highly needed
        Zebro_adjust_gamma = Calib.adjust_gamma(Zebro_res, 1)

        Zebro_QR_Mask = np.zeros(Zebro_res.shape[:2], dtype="uint8")
        # color in cube is hsv values for easier detection of QR code
        Zebro_hsv = cv2.cvtColor(Zebro_adjust_gamma, cv2.COLOR_BGR2HSV)

        kernel_erode = np.ones((3,3),np.uint8)
        kernel_dilate = np.ones((3,3),np.uint8)
        kernel_closing = np.ones((3,3),np.uint8)

        # Detecting Black in Zebro image
        for(lower,upper) in black:
                lower = np.array(lower,dtype=np.uint8)
                upper = np.array(upper,dtype=np.uint8)
        Zebro_Black_Mask = cv2.inRange(Zebro_hsv,lower,upper)
        Zebro_Black_Mask = cv2.dilate(Zebro_Black_Mask, kernel_dilate, iterations=1)

        #cv2.imshow("Zebro_Black_Mask",Zebro_Black_Mask)

        # Detecting White in Zebro image
        for(lower,upper) in white:
                lower = np.array(lower,dtype=np.uint8)
                upper = np.array(upper,dtype=np.uint8)
        Zebro_White_Mask = cv2.inRange(Zebro_hsv,lower,upper)
        #Zebro_White_Mask = cv2.dilate(Zebro_White_Mask, kernel_dilate, iterations=1)

        #cv2.imshow("Zebro_White_Mask",Zebro_White_Mask)

        Zebro_QR_Mask = cv2.addWeighted(Zebro_Black_Mask,1,Zebro_White_Mask,1,0)
        Zebro_QR_Mask = cv2.dilate(Zebro_QR_Mask, kernel_dilate, iterations=1)
        Zebro_QR_Mask = cv2.morphologyEx(Zebro_QR_Mask, cv2.MORPH_CLOSE, kernel_closing)

        #Zebro_gray = cv2.cvtColor(Zebro_adjust_gamma, cv2.COLOR_BGR2GRAY)
        #cv2.imshow("Zebro_QR_Mask",Zebro_QR_Mask)

        Zebro_edges = cv2.Canny(Zebro_QR_Mask, 150, 250, apertureSize = 3)
        #cv2.imshow("edges Zebro",Zebro_edges)

        #Function for finding larges contour in image Zebro
        (_,contours2,_) = cv2.findContours(Zebro_edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE) # Find contours with hierarchy
        areaArray = []
        
        for i, c in enumerate(contours2):
            area = cv2.contourArea(c)
            areaArray.append(area)
            #cv2.drawContours(Zebro_res, [c], -1, (255,0,255), -1)

        sorteddata = sorted(zip(areaArray, contours2), key=lambda x: x[0], reverse=True)
        #cv2.imshow("resolution 200 200",Zebro_res)

        try:
            largestcontour = sorteddata[0][1]
            x, y, w, h = cv2.boundingRect(largestcontour)
            if w > 20 and h > 20:# and w < 100 and h < 100:
                #print(w,h)
                y = y-20
                x = x-20
                h=h+30
                w=w+30
                QR_CODE = Zebro_res[y:y+h, x:x+w]
                try:
                    #cv2.imshow("QR_CODE LargestContour", QR_CODE)
                    cv2.imwrite("Pico/QR_CODE.jpg", QR_CODE)
                except cv2.error as e:
                    pass
        except IndexError:
            pass
    except(AttributeError, TypeError, cv2.error) as e:
        pass

# STEP 3
# From here on out it is determing angle and with that direction

    # Pre found images for now for testing
    QR_image = cv2.imread("Pico/QR_CODE1.jpg", 1)

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
    QR_adjust_gamma = Calib.adjust_gamma(QR_final, 1)

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
    #cv2.imshow("mask_QR_black",mask_QR_black)
    # Detecting White in QR code
    for(lower,upper) in white:
            lower = np.array(lower,dtype=np.uint8)
            upper = np.array(upper,dtype=np.uint8)
    mask_QR_white = cv2.inRange(QR_hsv,lower,upper)
    
    mask_QR_white = cv2.erode(mask_QR_white, kernel_erode, iterations=2)
    mask_QR_white = cv2.dilate(mask_QR_white, kernel_dilate, iterations=1)

    #debugging
    #cv2.imshow("mask_QR_white",mask_QR_white)
    #cv2.imwrite("Pico/White_MASK.jpg", mask_QR_white)

    #Add White and black mask together
    accumMask = cv2.addWeighted(mask_QR_white,1,mask_QR_black,1,0)
#debugging
    #cv2.imshow("accumMask",accumMask)
    #accumMask = cv2.bitwise_not(accumMask)
    
    #Finding largest contour in black and white image     
    mask_QR = cv2.erode(accumMask, None, iterations=1)
    mask_QR = cv2.dilate(mask_QR, None, iterations=2)
    mask_QR_closing = cv2.morphologyEx(mask_QR, cv2.MORPH_CLOSE, None)

    #cv2.imshow("mask_QR_closing",mask_QR_closing)

    # Finds contours
    im2, cnts, hierarchy = cv2.findContours(mask_QR_closing.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    areaArray_QR = []
    
    for i, c_QR in enumerate(cnts):
        area_QR = cv2.contourArea(c_QR)
        areaArray_QR.append(area_QR)
        
    sorteddata_QR = sorted(zip(areaArray_QR, cnts), key=lambda x: x[0], reverse=True)

    #MASK_WR = cv2.imread("Pico/White_MASK.jpg")

    #Mask_image = np.zeros(MASK_WR.shape[:2], dtype="uint8")

    #Mask_image = cv2.addWeighted(MASK_WR,1,QR_image,0.01,1)

    #cv2.imshow("Mask_image", Mask_image)

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
        
        P_W_Pixel = int(P_W*0.20)
        P_H_Pixel = int(P_H*0.20)
        
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

        #QR_Area_Orientation_0 = cv2.resize(QR_Area_Orientation_0, (200, 200),interpolation = cv2.INTER_CUBIC)
        #cv2.imshow("QR_Area_Orientation_0", QR_Area_Orientation_0)
        
        #QR_Orientation_hsv_0 = cv2.cvtColor(QR_Area_Orientation_0, cv2.COLOR_BGR2GRAY)

        #ret,QR_Orientation_hsv_0 = cv2.threshold(QR_Orientation_hsv_0,127,255,cv2.THRESH_BINARY)
        #QR_Orientation_hsv_0 = cv2.cvtColor(QR_Orientation_hsv_0, cv2.COLOR_GRAY2BGR)
        #QR_Orientation_hsv_0 = cv2.cvtColor(QR_Orientation_hsv_0, cv2.COLOR_BGR2HSV)

        QR_Orientation_hsv_0 = cv2.cvtColor(QR_Area_Orientation_0, cv2.COLOR_BGR2HSV)

        #QR_Orientation_hsv_0 = cv2.bitwise_not(QR_Orientation_hsv_0)

        #QR_Orientation_hsv_1 = cv2.cvtColor(QR_Area_Orientation_1, cv2.COLOR_BGR2GRAY)
        QR_Orientation_hsv_1 = cv2.cvtColor(QR_Area_Orientation_1, cv2.COLOR_BGR2HSV)

        #QR_Orientation_hsv_2 = cv2.cvtColor(QR_Area_Orientation_2, cv2.COLOR_BGR2GRAY)
        QR_Orientation_hsv_2 = cv2.cvtColor(QR_Area_Orientation_2, cv2.COLOR_BGR2HSV)

        #QR_Orientation_hsv_3 = cv2.cvtColor(QR_Area_Orientation_3, cv2.COLOR_BGR2GRAY)
        QR_Orientation_hsv_3 = cv2.cvtColor(QR_Area_Orientation_3, cv2.COLOR_BGR2HSV)

        for(lower,upper) in white2:
            lower = np.array(lower,dtype=np.uint8)
            upper = np.array(upper,dtype=np.uint8)

        white_pixel0 = cv2.inRange(QR_Orientation_hsv_0,lower,upper)
        white_pixel1 = cv2.inRange(QR_Orientation_hsv_1,lower,upper)
        white_pixel2 = cv2.inRange(QR_Orientation_hsv_2,lower,upper)
        white_pixel3 = cv2.inRange(QR_Orientation_hsv_3,lower,upper)

    # TO here it is going wrong. Only here for step 3. I dont know what just the amount of white is not correct here
        white_pixel0 = cv2.countNonZero(white_pixel0)
        white_pixel1 = cv2.countNonZero(white_pixel1)
        white_pixel2 = cv2.countNonZero(white_pixel2)
        white_pixel3 = cv2.countNonZero(white_pixel3)

        if white_pixel0 > white_pixel1 and white_pixel0 > white_pixel2 and white_pixel0 > white_pixel3:
            degree = abs(rect[2])
            #print("PIXEL 0")
            #print (degree)
        if white_pixel1 > white_pixel0 and white_pixel1 > white_pixel2 and white_pixel1 > white_pixel3:
            degree = 270 + abs(rect[2])
            #print("PIXEL 1")
            #print (degree)
        if white_pixel2 > white_pixel0 and white_pixel2 > white_pixel1 and white_pixel2 > white_pixel3:
            degree = 180 + abs(rect[2])
            #print("PIXEL 2")
            #print (degree)
        if white_pixel3 > white_pixel0 and white_pixel3 > white_pixel1 and white_pixel3 > white_pixel2:
            degree = 90 + abs(rect[2])
            #print("PIXEL 3")
            #print (degree)
        
        if Do_once ==1:
            print(abs(rect[2]))
            print("Found White on pixel 0")
            #white_pixel0 = cv2.countNonZero(white_pixel0)
            print(white_pixel0)
            print("Found White on pixel 1")
            #white_pixel1 = cv2.countNonZero(white_pixel1)
            print(white_pixel1)
            print("Found White on pixel 2")
            #white_pixel2 = cv2.countNonZero(white_pixel2)
            print(white_pixel2)
            print("Found White on pixel 3")
            #white_pixel3 = cv2.countNonZero(white_pixel3)
            print(white_pixel3)

            if white_pixel0 > white_pixel1 and white_pixel0 > white_pixel2 and white_pixel0 > white_pixel3:
                degree = abs(rect[2])
                print("PIXEL 0")
                print (degree)
            if white_pixel1 > white_pixel0 and white_pixel1 > white_pixel2 and white_pixel1 > white_pixel3:
                degree = 270 + abs(rect[2])
                print("PIXEL 1")
                print (degree)
            if white_pixel2 > white_pixel0 and white_pixel2 > white_pixel1 and white_pixel2 > white_pixel3:
                degree = 180 + abs(rect[2])
                print("PIXEL 2")
                print (degree)
            if white_pixel3 > white_pixel0 and white_pixel3 > white_pixel1 and white_pixel3 > white_pixel2:
                degree = 90 + abs(rect[2])
                print("PIXEL 3")
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
    
# debugging
    #cv2.imshow('outout QR code', QR_image)
    
    #DEBUG CV2.IMSHOW
    #cv2.imshow("image_light" ,image_light)
    #cv2.imshow("image_gamma" ,image_gamma)
    # Take current day
    Timetest = time.strftime("%d-%m-%Y")
    # Show the current view for debugging
#    cv2.imshow("original %s" % Timetest,image)

    # show the frame
    key = cv2.waitKey(1) & 0xFF

    #clear the stream in preparation of the next frame
    rawCapture.truncate(0)

    # if the 'q' key was pressed, break from the loop
    if key == ord("q"):
        # cleanup the camera and close any open windows
        cv2.destroyAllWindows()
        break
