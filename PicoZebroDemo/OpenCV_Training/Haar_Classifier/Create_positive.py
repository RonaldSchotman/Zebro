import cv2
import numpy as np
import os

img = cv2.imread("Pico_zebro_v3.png")
rows,cols = img.shape[:2]

while True:
    Angles = 360
    Points = 10
    for i in range(Points):
        #print(i)
        
        pts1 = np.float32([[5,5],[40,5],[5,20]])
        pts2 = np.float32([[5,5],[40,5],[5,20+i]])

        M = cv2.getAffineTransform(pts1,pts2)
        #M = cv2.getRotationMatrix2D((cols/2,rows/2),i,1)
        dst = cv2.warpAffine(img,M,(cols,rows))
        cv2.imshow("Pico_Zebro_New",dst)
        cv2.imwrite("pos/Turned_Pico_Affine_7%s.jpg" %i,dst)
    
    
    # show the frame
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key was pressed, break from the loop
    if key == ord("q"):
        # cleanup the camera and close any open windows
        cv2.destroyAllWindows()
        break
