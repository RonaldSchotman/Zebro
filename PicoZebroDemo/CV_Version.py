import cv2
print(cv2.__version__)

print("---------------------")
if (cv2.ocl.haveOpenCL()):
    print("OpenCL available")
else:
    print("OpenCL not available")
print("---------------------")

