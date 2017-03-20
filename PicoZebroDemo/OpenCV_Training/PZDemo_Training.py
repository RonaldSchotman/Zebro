#!/usr/bin/env python
# TU Delft Pico Zebro Demo
# PZ_DEMO Learner
# Writer: Martijn de Rooij
# Version 0.01

# Everything is being tested from 120 cm height.

# Python 3 compatability
from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass

# import the necessary packages
import time                             # For timing functions
import numpy as np                      # Optimized library for numerical operations
import cv2                              # Include OpenCV library (Most important one)
import os                               # Include easy file multi file reader

## Prepare images files
rootpath = 'Classifier_Pictures/'
files = []
for filedir, dirs, filess in os.walk(rootpath):
    for filename in filess:
        pathfile = os.path.join(filedir, filename)
        files.append(pathfile)

## Detect keypoints and compute descriptors for train images
kp_train = []
dsc_train = []
sift = cv2.xfeatures2d.SIFT_create()
for file in files:
    ima = cv2.imread(file)
    print (file)
    gray=cv2.cvtColor(ima,cv2.COLOR_BGR2GRAY)
    kpts, des = sift.detectAndCompute(gray, None) #sift = cv2.xfeatures2d.SIFT_create()
    kp_train.append(kpts)
    dsc_train.append(des)

dsc_train = np.array(dsc_train)
responses = np.arange(len(kp_train),dtype = np.float32)
knn = cv2.ml.KNearest_create()


