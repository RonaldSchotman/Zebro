#!/usr/bin/env python
# TU Delft Pico Zebro Demo
# OCR, but, with SVM instead of kNN. OpenCV Machine Learning
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
        
affine_flags = cv2.WARP_INVERSE_MAP|cv2.INTER_LINEAR

## Detect keypoints and compute descriptors for train images
def deskew(img):
    m = cv2.moments(img)
    if abs(m['mu02']) < 1e-2:
        return img.copy()
    skew = m['mu11']/m['mu02']
    M = np.float32([[1, skew, -0.5*SZ*skew], [0, 1, 0]])
    img = cv2.warpAffine(img,M,(SZ, SZ),flags=affine_flags)
    return img

def hog(img):
    gx = cv2.Sobel(img, cv2.CV_32F, 1, 0)
    gy = cv2.Sobel(img, cv2.CV_32F, 0, 1)
    mag, ang = cv2.cartToPolar(gx, gy)
    bins = np.int32(bin_n*ang/(2*np.pi))    # quantizing binvalues in (0...16)
    bin_cells = bins[:10,:10], bins[10:,:10], bins[:10,10:], bins[10:,10:]
    mag_cells = mag[:10,:10], mag[10:,:10], mag[:10,10:], mag[10:,10:]
    hists = [np.bincount(b.ravel(), m.ravel(), bin_n) for b, m in zip(bin_cells, mag_cells)]
    hist = np.hstack(hists)     # hist is a 64 bit vector
    return hist

for file in files:
    ima = cv2.imread(file)
    print (file)
    gray=cv2.cvtColor(ima,cv2.COLOR_BGR2GRAY)
    kpts, des = sift.detectAndCompute(gray, None) #sift = cv2.xfeatures2d.SIFT_create()
    kp_train.append(kpts)
    dsc_train.append(des)

deskewed = [map(deskew,row) for row in train_cells]
hogdata = [map(hog,row) for row in deskewed]
trainData = np.float32(hogdata).reshape(-1,64)
responses = np.float32(np.repeat(np.arange(10),250)[:,np.newaxis])

svm = cv2.ml.SVM_create()
svm.setKernel(cv2.ml.SVM_LINEAR)
svm.setType(cv2.ml.SVM_C_SVC)
svm.setC(2.67)
svm.setGamma(5.383)
svm.train(trainData, cv2.ml.ROW_SAMPLE, responses)
svm.save('svm_data.dat')

