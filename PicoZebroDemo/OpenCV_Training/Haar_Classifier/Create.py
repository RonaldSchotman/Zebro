import cv2
import numpy as np
import os

#opencv_createsamples -img pico_zebro_v1_50_50.jpg -bg bg.txt -info info/info.lst -pngoutput info -maxxangle 0.5 -maxyangle 0.5 -maxzangle 0.5 -num 1000

#import numpy as np
#import cv2
Pico_zebro_cascade = cv2.CascadeClassifier('data/cascade.xml')
#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
img = cv2.imread('Picture.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

Pico_zebro = Pico_zebro_cascade.detectMultiScale(gray, 1.3, 5)
for (x,y,w,h) in Pico_zebro:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
cv2.imwrite('Haar_classifier_Result1.jpg', img)
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
