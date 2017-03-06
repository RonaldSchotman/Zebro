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
import math

class functions_orient:
    def __init__(self):
        pass

    # Function: Routine to get Distance between two points
    # Description: Given 2 points, the function returns the distance
    def distance(self, p,q):
        return math.sqrt(math.pow(math.fabs(p[0]-q[0]),2)+math.pow(math.fabs(p[1]-q[1]),2))

    # Function: Perpendicular Distance of a Point J from line formed by Points L and M; Equation of the line ax+by+c=0
    # Description: Given 3 points, the function derives the line quation of the first two points,
    # calculates and returns the perpendicular distance of the the 3rd point from this line.
    def lineEquation(self, l,m,j):
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
    def lineSlope(self, l,m):
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
    def getSquares(self, contours,cid):
        x,y,w,h= cv2.boundingRect(contours[cid])
        return x,y,w,h

    # Function: Compare a point if it more far than previously recorded
    # farthest distance Description: Farthest Point detection using
    # reference point and baseline distance
    def updateCorner(self, p,ref,baseline,corner):
        temp_dist = self.distance(p,ref)
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

    def getVertices(self, contours,cid,slope,quad):
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
                pd1 = self.lineEquation(C,A,contours[cid][i])
                pd2 = self.lineEquation(B,D,contours[cid][i])
                if(pd1 >= 0.0 and pd2 > 0.0):
                    dmax[1],M1 = self.updateCorner(contours[cid][i],W,dmax[1],M1)
                elif(pd1 > 0.0 and pd2 <= 0):
                    dmax[2],M2 = self.updateCorner(contours[cid][i],X,dmax[2],M2)
                elif(pd1 <= 0.0 and pd2 < 0.0):
                    dmax[3],M3 = self.updateCorner(contours[cid][i],Y,dmax[3],M3)
                elif(pd1 < 0 and pd2 >= 0.0):
                    dmax[0],M0 = self.updateCorner(contours[cid][i],Z,dmax[0],M0)
                else:
                    continue
        else:
            halfx = (A[0]+B[0])/2
            halfy = (A[1]+D[1])/2
            for i in range(len(contours[cid])):
                if(contours[cid][i][0][0]<halfx and contours[cid][i][0][1]<=halfy):
                    dmax[2],M0 = self.updateCorner(contours[cid][i][0],C,dmax[2],M0)
                elif(contours[cid][i][0][0]>=halfx and contours[cid][i][0][1]<halfy):
                    dmax[3],M1 = self.updateCorner(contours[cid][i][0],D,dmax[3],M1)
                elif(contours[cid][i][0][0]>halfx and contours[cid][i][0][1]>=halfy):
                    dmax[0],M2 = self.updateCorner(contours[cid][i][0],A,dmax[0],M2)
                elif(contours[cid][i][0][0]<=halfx and contours[cid][i][0][1]>halfy):
                    dmax[1],M3 = self.updateCorner(contours[cid][i][0],B,dmax[1],M3)
        quad.append(M0)
        quad.append(M1)
        quad.append(M2)
        quad.append(M3)
        return quad

    # Function: Sequence the Corners wrt to the orientation of the QR Code
    def updateCornerOr(self, orientation,IN):
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
    def cross(self, v1,v2):
        cr = v1[0]*v2[1] - v1[1]*v2[0]
        return cr

    # Function: Get the Intersection Point of the lines formed by sets of two points
    def getIntersection(self, a1,a2,b1,b2,intersection):
        p = a1
        q = b1
        r = (a2[0]-a1[0],a2[1]-a1[1])
        s = (b2[0]-b1[0],b2[1]-b1[1])
        if self.cross(r,s) == 0:
            return False, intersection
        t = self.cross((q[0]-p[0],q[1]-p[1]),s)/float(self.cross(r,s))
        intersection = (int(p[0]+(t*r[0])),int(p[1]+(t*r[1])))
        return True,intersection

