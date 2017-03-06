    cv2.imshow("Zebro_s", Zebro_edges)

    #Function for finding larges contour in image Zebro
    (_,contours2,hierarchy2) = cv2.findContours(Zebro_edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # Find contours with hierarchy
    areaArray = []

    cv2.drawContours(Zebro_edges, contours2, -1, (255, 0,0 ), 1)
    cv2.imshow("Zebro_edges", Zebro_edges)
    
    for i, c in enumerate(contours2):
        area = cv2.contourArea(c)
        areaArray.append(area)
        [vx,vy,x,y] = cv2.fitLine(contours2[0], cv2.DIST_L2,0,1,1)
        lefty = int((-x*vy/vx)+y)
        righty = int(((200-x)*vy/vx)+y)
        cv2.line(Zebro_edges, (200-1,righty),(0,lefty),(0,255,255),2)

    cv2.imshow("Zebro_lines", Zebro_edges)

    minLineLength = 20
    lines = cv2.HoughLinesP(image = Zebro_edges, rho=0.5, theta = np.pi/180, threshold = 20,
                            lines=np.array([]),minLineLength=minLineLength,maxLineGap=100)

    a,b,c = lines.shape
    for i in range(a):
        cv2.line(Zebro_res, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]),
                 (0,0,255), 3, cv2.LINE_AA)

    cv2.imshow("Zebro_res ",Zebro_res)

    Zebro_template = cv2.imread("Pico/fourdots2.jpg", 1)

    Zebro_height, Zebro_width = Zebro_image.shape[:2]
    Zebro_template_height, Zebro_template_width = Zebro_template.shape[:2]
    result_size = [ s[0] - s[1] + 1 for s in zip([Zebro_height, Zebro_width], [Zebro_template_height, Zebro_template_width]) ]

    #result = cv2.createImage(result_size, cv.IPL_DEPTH_32F, 1)

    result = cv2.matchTemplate(image, Zebro_template, cv2.TM_CCORR)

    min_val, Max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    cv2.imshow("Zeres", result)

    ret, thresh = cv2.threshold(Zebro_gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel,iterations=2)

    sure_bg = cv2.dilate(opening,kernel,iterations=3)

    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.7*dist_transform.max(),255,0)

    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)

    cv2.imshow("unknown", sure_bg)

black = [([0,0,0],[0,0,40])] #=black
white = [([0,0,0],[0,0,255])] #=white

    Zebro_image= cv2.imread("Pico/rect.jpg", 1)

    # color in cube is hsv values for easier detection of green.
    black_hsv = cv2.cvtColor(Zebro_image, cv2.COLOR_BGR2HSV)

    #green the important color
    for(black_lower,black_upper) in black:
            black_lower = np.array(black_lower,dtype=np.uint8)
            black_upper = np.array(black_upper,dtype=np.uint8) 
    # the mask 
    mask_black = cv2.inRange(black_hsv,black_lower,black_upper)

    #green the important color
    for(white_lower,white_upper) in white:
            white_lower = np.array(white_lower,dtype=np.uint8)
            white_upper = np.array(white_upper,dtype=np.uint8) 
    # the mask 
    mask_white = cv2.inRange(black_hsv,white_lower,white_upper)

    Black_white_out = cv2.bitwise_and(Zebro_image, Zebro_image, mask = mask_white)
    cv2.imshow("HSV white mask", mask_white)
    cv2.imshow("HSV white", Black_white_out)

    #Function for finding larges contour in image
    image_gray2 = cv2.cvtColor(qr2_image, cv2.COLOR_BGR2GRAY) # Convert Image captured from Image Input to GrayScale
    edges2 = cv2.Canny(image_gray2,100,200,3)      # Apply Canny edge detection on the gray image
    (_,contours2,hierarchy2) = cv2.findContours(edges2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # Find contours with hierarchy
    areaArray = []
    for i, c in enumerate(contours2):
        area = cv2.contourArea(c)
        areaArray.append(area)
    #first sort the array by area
 
    sorteddata = sorted(zip(areaArray, contours2), key=lambda x: x[0], reverse=True)

    #find the nth largest contour [n-1][1], in this case 1
    try:
        largestcontour = sorteddata[0][1]
        #draw it
        x, y, w, h = cv2.boundingRect(largestcontour)
        appelkoek = qr2_image[y:y+h, x:x+w]
        cv2.rectangle(qr2_image, (x, y), (x+w, y+h), (0,255,0), 2)
        cv2.imwrite("Pico/testing.jpg", appelkoek)

    except IndexError:
        pass


        while True:        
            i = 0
            for c in contours2:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.04 * peri, True)
                if i == 1:
                    break
     
                # if the shape has 4 vertices, it is either a square or
                # a rectangle
                if len(approx) == 4:
                # compute the bounding box of the contour and use the
                # bounding box to compute the aspect ratio
                    (x, y, w, h) = cv2.boundingRect(approx)
                    ar = w / float(h)
     
                    # a square will have an aspect ratio that is approximately
                    # equal to one, otherwise, the shape is a rectangle
                    if ar >= 0.95 and ar <= 1.05:
                        break
                i = i + 1


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
    
