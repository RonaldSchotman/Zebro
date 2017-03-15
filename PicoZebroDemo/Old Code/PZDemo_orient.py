#!/usr/bin/env python
# TU Delft Pico Zebro Demo
# Writer: Martijn de Rooij
# Version 0.02
# From live video find green and put a rectangle around it.
# This is step 1 for finding and recognizing the Pico zebro.
# The needs to be done from 170 cm
# version 0.01 works from 45 cm partly

# Python 3 compat
from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass

# import the functions
from Functions.functions_shape import functions_shape
from Functions.functions_orient import functions_orient

# import the necessary packages
from picamera.array import PiRGBArray   # Pi camera Libary capture BGR video
from picamera import PiCamera           # PiCamera liberary
import time                             # For real time video (using openCV)
import numpy as np                      # Optimized library for numerical operations
import cv2                              # Include OpenCV library (Most important one)

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (1280, 720)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(1280, 720))

#Standard hsv color values. These are obtained through code converter.py
green = [([40,40,55],[92,150,255])] #=green

# allow the camera to warmup (So this is only during start up once).
time.sleep(0.1)

funct = functions_shape()
orient = functions_orient()

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the NumPy array representing the image, the initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array

    #For finding the PicoZebro's
    # making light levels less invuential
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l,a,b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(2,2))
    cl = clahe.apply(l)
    limg = cv2.merge((cl,a,b))
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    #adjusting Gamma level if highly needed
    adjusted = funct.adjust_gamma(final, 1)
    
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
    cv2.imshow("HSV green visable  ", output)

    # Use current frame image and hsv green value to find 2 largest
    # green contours, draw rectangle around them and put them in image
    funct.Find_draw(image, output)

    #From here pn out it is orientation testing.
    Zebro_image= cv2.imread("Pico/tests1.jpg", 1)
    Zebro_gray = cv2.cvtColor(Zebro_image, cv2.COLOR_BGR2GRAY)
    
    Zebro_height, Zebro_width = Zebro_image.shape[:2]
    Zebro_res = cv2.resize(Zebro_image, (200, 200),interpolation = cv2.INTER_CUBIC)
    Zebro_gray = cv2.cvtColor(Zebro_res, cv2.COLOR_BGR2GRAY)
    Zebro_edges = cv2.Canny(Zebro_gray, 50, 200)
    cv2.imshow("Zebro_edges", Zebro_edges)
    cv2.imshow("Zebro_res", Zebro_res)

    Testing = cv2.imread("Pico/tests1.jpg", 0)

    height, width = Testing.shape[:2]
    res = cv2.resize(Testing, (100, 100),interpolation = cv2.INTER_CUBIC)
    cv2.imwrite("Pico/testing5.jpg", res)

    gaussian_1 = cv2.GaussianBlur(res, (15,15), 3)
    unshapr_image = cv2.addWeighted(res, 1.55, gaussian_1, 0, 0, res)
    hist_eq = cv2.equalizeHist(unshapr_image)

    cv2.imwrite("Pico/testing2.jpg", hist_eq)

    qr_image= cv2.imread("Pico/testing2.jpg", 1)
    
    

    image_gray = cv2.cvtColor(qr_image, cv2.COLOR_BGR2GRAY) # Convert Image captured from Image Input to GrayScale
    edges = cv2.Canny(image_gray,100,200,3)      # Apply Canny edge detection on the gray image
    (_,contours,hierarchy) = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # Find contours with hierarchy

 # Get Moments for all Contours and the mass centers
    mu = []
    mc = []
    mark = 0
    for x in range(0,len(contours)):
        mu.append(cv2.moments(contours[x]))

    for m in mu:
        if m['m00'] != 0:
            mc.append((m['m10']/m['m00'],m['m01']/m['m00']))
        else:
            mc.append((0,0))

    # Start processing the contour data

    # Find Three repeatedly enclosed contours A,B,C
    # NOTE: 1. Contour enclosing other contours is assumed to be the three Alignment markings of the QR code.
    # 2. Alternately, the Ratio of areas of the "concentric" squares can also be used for identifying base Alignment markers.
    # The below demonstrates the first method
        
    for x in range(0,len(contours)):

        #approx = cv2.approxPolyDP(x, 0.04 * cv2.arcLength(x, True), True)
        #if (len(approx) == 4):
        k = x
        c = 0
        while(hierarchy[0][k][2] != -1):
            k = hierarchy[0][k][2]
            c = c + 1
        if hierarchy[0][k][2] != -1:
            c = c + 1

        if c >= 5:
            if mark == 0:
                A = x
            elif mark == 1:  # i.e., A is already found, assign current contour to B
                B = x
            elif mark == 2:  # i.e., A and B are already found, assign current contour to C
                C = x
            mark = mark+1

    if (mark > 2):
        # Ensure we have (atleast 3; namely A,B,C) 'Alignment Markers' discovered
        # We have found the 3 markers for the QR code; Now we need to determine which of them are 'top', 'right' and 'bottom' markers

        # Determining the 'top' marker
        # Vertex of the triangle NOT involved in the longest side is the 'outlier'

        AB = orient.distance(mc[A],mc[B])
        BC = orient.distance(mc[B],mc[C])
        AC = orient.distance(mc[A],mc[C])

        if(AB>BC and AB>AC):
            outlier = C
            median1 = A
            median2 = B
        elif(AC>AB and AC>BC):
            outlier = B
            median1 = A
            median2 = C
        elif(BC>AB and BC>AC):
            outlier = A
            median1 = B
            median2 = C

        top = outlier # The obvious choice

        # Get the Perpendicular distance of the outlier from the longest side
        dist = orient.lineEquation(mc[median1],mc[median2],mc[outlier])

        # Also calculate the slope of the longest side
        slope,align = orient.lineSlope(mc[median1],mc[median2])


        # Now that we have the orientation of the line formed median1 & median2 and we also have the position of the outlier w.r.t. the line
        # Determine the 'right' and 'bottom' markers
        if align == 0:
            bottom = median1
            right = median2
        elif(slope < 0 and dist < 0): #Orientation - North
            bottom = median1
            right = median2
            orientation = 0
        elif(slope > 0 and dist < 0): #Orientation - East
            right = median1
            bottom = median2
            orientation = 1
        elif(slope < 0 and dist > 0): #Orientation - South
            right = median1
            bottom = median2
            orientation = 2
        elif(slope > 0 and dist > 0): #Orientation - West
            bottom = median1
            right = median2
            orientation = 3
                        
        #To ensure any unintended values do not sneak up when QR code is not present
        areatop = 0.0
        arearight = 0.0
        areabottom = 0.0
        if(top < len(contours) and right < len(contours) and bottom < len(contours) and cv2.contourArea(contours[top]) > 10 and cv2.contourArea(contours[right]) > 10 and cv2.contourArea(contours[bottom]) > 10):
            tempL = []
            tempM = []
            tempO = []
            # src - Source Points basically the 4 end co-ordinates of the overlay image
            # dst - Destination Points to transform overlay image

            src = []
            N = (0,0)
            tempL = orient.getVertices(contours,top,slope,tempL)
            tempM = orient.getVertices(contours,right,slope,tempM)
            tempO = orient.getVertices(contours,bottom,slope,tempO)
            L = orient.updateCornerOr(orientation,tempL)
            M = orient.updateCornerOr(orientation,tempM)
            O = orient.updateCornerOr(orientation,tempO)

            iflag,N = orient.getIntersection(M[1],M[2],O[3],O[2],N)

            src.append(L[0])
            src.append(M[1])
            src.append(N)
            src.append(O[3])

            #Draw contours on the image
            cv2.drawContours(qr_image,contours,top,(255,0,0),2)
            cv2.drawContours(qr_image,contours,right,(0,255,0),2)
            cv2.drawContours(qr_image,contours,bottom,(0,0,255),2)

        # Show the Orientation of the QR Code wrt to 2D Image Space
        if(orientation == 0):
            cv2.putText(qr_image,'North',(20,30),0,0.3,(0,255,0))
        elif(orientation == 1):
            cv2.putText(qr_image,'East',(20,30),0,0.3,(0,255,0))
        elif(orientation == 2):
            cv2.putText(qr_image,'South',(20,30),0,0.3,(0,255,0))
        elif(orientation == 3):
            cv2.putText(qr_image,'West',(20,30),0,0.3,(0,255,0))

    cv2.imwrite("Pico/rect2.jpg",qr_image)

    Timetest = time.strftime("%d-%m-%Y")
    # Show the current view
    cv2.imshow("original %s" % Timetest,image)

    # show the frame
    key = cv2.waitKey(1) & 0xFF

    #clear the stream in preparation of the next frame
    rawCapture.truncate(0)

    # if the 'q' key was pressed, break from the loop
    if key == ord("q"):
        # cleanup the camera and close any open windows
        cv2.destroyAllWindows()
        break
