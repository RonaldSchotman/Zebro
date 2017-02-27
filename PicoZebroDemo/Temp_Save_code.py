    g = sum(sum(mask_green))

    # blue
    for(lower,upper) in blue:
            lower = np.array(lower,dtype=np.uint8)
            upper = np.array(upper,dtype=np.uint8)
    # the mask    
    mask = cv2.inRange(hsv,lower,upper)
    b = sum(sum(mask))

    #red
    for(lower,upper) in red:
            lower = np.array(lower,dtype=np.uint8)
            upper = np.array(upper,dtype=np.uint8) 
    # the mask 
    mask = cv2.inRange(hsv,lower,upper)
    r = sum(sum(mask))

    #yellow	
    for(lower,upper) in yellow:
            lower = np.array(lower,dtype=np.uint8)
            upper = np.array(upper,dtype=np.uint8) 
    # the mask 
    mask = cv2.inRange(hsv,lower,upper)
    y = sum(sum(mask))

    if b < 1000 and r < 1000 and y < 1000 and g < 1000:
        pass 
    else:
        if b > r and b > g and b >y:
            pass 
        elif r > g and r > y:
            pass 
        elif y > g:
            pass 
        else:
            pass # print ("block green")

    # For Finding rectangles
    
    # make image gray for finding rectangles
    # convert the image to grayscale, blur it slightly,
    # and threshold it
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

    # find contours in the thresholded image and initialize the
    # shape detector
    (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:    
        rect = cv2.boundingRect(c)
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        
        if len(approx) == 4:
            if rect[2] < 100 or rect[3] < 100: continue
            x,y,w,h = rect
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(image,'Moth Detected',(x+w+10,y+h),0,0.3,(0,255,0))
        else:
            pass
        

    # convert the image to grayscale, blur it slightly,
    # and threshold it
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
 
    # find contours in the thresholded image and initialize the
    # shape detector
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    
    # loop over conturs for finding rectangles.
    for c in cnts:
        M = cv2.moments(c)
        # shape using only the contour
        shape = functions_shape.detect(c)
        if shape == "rectangle":
            M = cv2.moments(c)
            if (M["m00"] == 0):
                M["m00"]=1
            cX = int((M["m10"] / M["m00"]) * ratio)
            cY = int((M["m01"] / M["m00"]) * ratio)
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 255, 255), 2)


    

        # if no contours were found, return None
        if len(cnts) == 0:
            pass

        # if the shape has 4 vertices, it is either a square or
        # a rectangle
        elif len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            
            if ar >= 0.95 and ar <= 1.05:
                cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            
            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

                    M = cv2.moments(c)
        # initialize the shape name and approximate the contour
        area = cv2.contourArea(c)
        if area < 10000:
           cnts.remove(c)
        else:
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
       
    approx = cv2.approxPolyDP(cn, 0.02 * cv2.arcLength(cn, True), True)

    def is_contour_bad(self, c):
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        
        # the contour is 'bad' if it is not a rectangle
        return not len(approx) == 4

    # function from pyimagesearch for finding barcodes (works for qr codes.
    def detect(self, image):
        # convert the image to grayscale, blur it slightly,
        # and threshold it
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

        # find contours in the thresholded image and initialize the
        # shape detector
        (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts:
            # initialize the shape name and approximate the contour
            shape = "unidentified"
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)

            # if no contours were found, return None
            if len(cnts) == 0:
                return None

            # if the shape has 4 vertices, it is either a square or
            # a rectangle
            elif len(approx) == 4:
                # compute the bounding box of the contour and use the
                # bounding box to compute the aspect ratio
                (x, y, w, h) = cv2.boundingRect(approx)
                ar = w / float(h)

                box = c
 
                # a square will have an aspect ratio that is approximately
                # equal to one, otherwise, the shape is a rectangle
                shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

        # return the bounding box of the rectangle
        return box
            
    def detect_shape(self, c):
        # initialize the shape name and approximate the contour
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        # if the shape is a triangle, it will have 3 vertices
        if len(approx) == 3:
            shape = "triangle"
 
        # if the shape has 4 vertices, it is either a square or
        # a rectangle
        elif len(approx) == 4:
        # compute the bounding box of the contour and use the
        # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
 
            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
 
        # if the shape is a pentagon, it will have 5 vertices
        elif len(approx) == 5:
            shape = "pentagon"
                                          
        # if the shape is a hexagon, it will have 6 vertices
        elif len(approx) == 6:
            shape = "hexagon"                                    
 
        # otherwise, we assume the shape is a circle
        else:
            shape = "circle"

        # return the name of the shape
        return shape
    
