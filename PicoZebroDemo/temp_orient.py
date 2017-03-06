# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:37:13 2017

@author: Martijn
"""

import serial
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import math
import numpy as np

# Function: Routine to get Distance between two points
# Description: Given 2 points, the function returns the distance
def distance(p,q):
    return math.sqrt(math.pow(math.fabs(p[0]-q[0]),2)+math.pow(math.fabs(p[1]-q[1]),2))

# Function: Perpendicular Distance of a Point J from line formed by Points L and M; Equation of the line ax+by+c=0
# Description: Given 3 points, the function derives the line quation of the first two points,
# calculates and returns the perpendicular distance of the the 3rd point from this line.
def lineEquation(l,m,j):
    a = -((m[1] - l[1])/(m[0] - l[0]))
    b = 1.0
    c = (((m[1] - l[1])/(m[0] - l[0]))*l[0]) - l[1]
    try:
        pdist = (a*j[0]+(b*j[1])+c)/math.sqrt((a*a)+(b*b))
    except:
        return 0
    else:
        return pdist

# Function: Slope of a line by two Points L and M on it; Slope of line, S = (x1 -x2) / (y1- y2)
# Description: Function returns the slope of the line formed by given 2 points, the alignement flag
# indicates the line is vertical and the slope is infinity.
def lineSlope(l,m):
    dx = m[0] - l[0]
    dy = m[1] - l[1]
    if dy != 0:
        align = 1
        dxy = dy/dx
        return dxy,align
    else:
        align = 0
        dxy = 0.0
        return dxy,align

#obtain squares and only observe those:
def getSquares(contours,cid):
    x,y,w,h= cv2.boundingRect(contours[cid])
    return x,y,w,h

# Function: Compare a point if it more far than previously recorded
# farthest distance Description: Farthest Point detection using
# reference point and baseline distance
def updateCorner(p,ref,baseline,corner):
    temp_dist = distance(p,ref)
    if temp_dist > baseline:
        baseline = temp_dist
        corner = p
    return baseline,corner

# Function: Routine to calculate 4 Corners of the Marker in Image Space using Region partitioning
# Theory: OpenCV Contours stores all points that describe it and these points lie the perimeter of the polygon.
#	The below function chooses the farthest points of the polygon since they form the vertices of that polygon,
#	exactly the points we are looking for. To choose the farthest point, the polygon is divided/partitioned into
#	4 regions equal regions using bounding box. Distance algorithm is applied between the centre of bounding box
#	every contour point in that region, the farthest point is deemed as the vertex of that region. Calculating
#	for all 4 regions we obtain the 4 corners of the polygon ( - quadrilateral).

def getVertices(contours,cid,slope,quad):
    M0 = (0.0,0.0)
    M1 = (0.0,0.0)
    M2 = (0.0,0.0)
    M3 = (0.0,0.0)
    x,y,w,h = cv2.boundingRect(contours[cid])
    A = (x,y)
    B = (x+w,y)
    C = (x+w,h+y)
    D = (x,y+h)
    W = ((A[0]+B[0])/2,A[1])
    X = (B[0],(B[1]+C[1])/2)
    Y = ((C[0]+D[0])/2,C[1])
    Z = (D[0],(D[1]+A[1])/2)
    dmax = []
    for i in range(4):
        dmax.append(0.0)
    pd1 = 0.0
    pd2 = 0.0
    if(slope > 5 or slope < -5 ):
        for i in range(len(contours[cid])):
            pd1 = lineEquation(C,A,contours[cid][i])
            pd2 = lineEquation(B,D,contours[cid][i])
            if(pd1 >= 0.0 and pd2 > 0.0):
                dmax[1],M1 = updateCorner(contours[cid][i],W,dmax[1],M1)
            elif(pd1 > 0.0 and pd2 <= 0):
                dmax[2],M2 = updateCorner(contours[cid][i],X,dmax[2],M2)
            elif(pd1 <= 0.0 and pd2 < 0.0):
                dmax[3],M3 = updateCorner(contours[cid][i],Y,dmax[3],M3)
            elif(pd1 < 0 and pd2 >= 0.0):
                dmax[0],M0 = updateCorner(contours[cid][i],Z,dmax[0],M0)
            else:
                continue
    else:
        halfx = (A[0]+B[0])/2
        halfy = (A[1]+D[1])/2
        for i in range(len(contours[cid])):
            if(contours[cid][i][0][0]<halfx and contours[cid][i][0][1]<=halfy):
                dmax[2],M0 = updateCorner(contours[cid][i][0],C,dmax[2],M0)
            elif(contours[cid][i][0][0]>=halfx and contours[cid][i][0][1]<halfy):
                dmax[3],M1 = updateCorner(contours[cid][i][0],D,dmax[3],M1)
            elif(contours[cid][i][0][0]>halfx and contours[cid][i][0][1]>=halfy):
                dmax[0],M2 = updateCorner(contours[cid][i][0],A,dmax[0],M2)
            elif(contours[cid][i][0][0]<=halfx and contours[cid][i][0][1]>halfy):
                dmax[1],M3 = updateCorner(contours[cid][i][0],B,dmax[1],M3)
    quad.append(M0)
    quad.append(M1)
    quad.append(M2)
    quad.append(M3)
    return quad

# Function: Sequence the Corners wrt to the orientation of the QR Code
def updateCornerOr(orientation,IN):
    if orientation == 0:
        M0 = IN[0]
        M1 = IN[1]
        M2 = IN[2]
        M3 = IN[3]
    elif orientation == 1:
        M0 = IN[1]
        M1 = IN[2]
        M2 = IN[3]
        M3 = IN[0]
    elif orientation == 2:
        M0 = IN[2]
        M1 = IN[3]
        M2 = IN[0]
        M3 = IN[1]
    elif orientation == 3:
        M0 = IN[3]
        M1 = IN[0]
        M2 = IN[1]
        M3 = IN[2]

    OUT = []
    OUT.append(M0)
    OUT.append(M1)
    OUT.append(M2)
    OUT.append(M3)

    return OUT

#cross points
def cross(v1,v2):
    cr = v1[0]*v2[1] - v1[1]*v2[0]
    return cr

# Function: Get the Intersection Point of the lines formed by sets of two points
def getIntersection(a1,a2,b1,b2,intersection):
    p = a1
    q = b1
    r = (a2[0]-a1[0],a2[1]-a1[1])
    s = (b2[0]-b1[0],b2[1]-b1[1])
    if cross(r,s) == 0:
        return False, intersection
    t = cross((q[0]-p[0],q[1]-p[1]),s)/float(cross(r,s))
    intersection = (int(p[0]+(t*r[0])),int(p[1]+(t*r[1])))
    return True,intersection

camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 32
rawCapture = PiRGBArray(camera,size=(640,480))
time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture,format="bgr",use_video_port=True):
    image = frame.array
    #show the image
    #wait until some key is pressed to procced

    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Convert Image captured from Image Input to GrayScale
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

        AB = distance(mc[A],mc[B])
        BC = distance(mc[B],mc[C])
        AC = distance(mc[A],mc[C])

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
        dist = lineEquation(mc[median1],mc[median2],mc[outlier])

        # Also calculate the slope of the longest side
        slope,align = lineSlope(mc[median1],mc[median2])


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
            tempL = getVertices(contours,top,slope,tempL)
            tempM = getVertices(contours,right,slope,tempM)
            tempO = getVertices(contours,bottom,slope,tempO)
            L = updateCornerOr(orientation,tempL)
            M = updateCornerOr(orientation,tempM)
            O = updateCornerOr(orientation,tempO)

            iflag,N = getIntersection(M[1],M[2],O[3],O[2],N)

            src.append(L[0])
            src.append(M[1])
            src.append(N)
            src.append(O[3])

            #Draw contours on the image
            cv2.drawContours(image,contours,top,(255,0,0),2)
            cv2.drawContours(image,contours,right,(0,255,0),2)
            cv2.drawContours(image,contours,bottom,(0,0,255),2)

        # Show the Orientation of the QR Code wrt to 2D Image Space
        if(orientation == 0):
            cv2.putText(image,'North',(20,30),0,0.3,(0,255,0))
        elif(orientation == 1):
            cv2.putText(image,'East',(20,30),0,0.3,(0,255,0))
        elif(orientation == 2):
            cv2.putText(image,'South',(20,30),0,0.3,(0,255,0))
        elif(orientation == 3):
            cv2.putText(image,'West',(20,30),0,0.3,(0,255,0))

    cv2.imshow("rect",image)
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == ord("q"):
        break
