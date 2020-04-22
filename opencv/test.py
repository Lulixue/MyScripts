
import sys
import numpy as np
import cv2
import copy

class InnerContour:
    topLeft = (sys.maxsize, sys.maxsize)
    bottomLeft = (0, sys.maxsize)
    topRight = (sys.maxsize, 0)
    bottomRight = (0, 0)
    minX = sys.maxsize
    minY = sys.maxsize
    maxX = 0 
    maxY = 0

    def __init__(self, contours):
        for contour in contours:
            x = contour.item(0, 0)
            y = contour.item(0, 1)
            if x < self.minX:
                self.minX = x
            if x > self.maxX:
                self.maxX = x
            if y < self.minY: 
                self.minY = y
            if y > self.maxY:
                self.maxY = y
        pass


def contourIsOnEdge(contours):
    for cont in contours: 
        print("cont: ", cont)
        x = cont.item(0, 0)
        y = cont.item(0, 1)
        if x <= 5 or y <= 5:
            return True
    
    return False


### load image and grayscale it
# img = cv2.imread("text.png")
img = cv2.imread("cz_bu.jpg")
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


### erode image
# cv2.imshow("before erode", imgray)
# # Creating kernel 
# kernel = np.ones((1, 1), np.uint8) 
# # Using cv2.erode() method  
# imgray = cv2.erode(imgray, kernel) 
# cv2.imshow("after erode", imgray)

### blur image
size = 10
imgray = cv2.bilateralFilter(imgray, size, size * 2, size / 2)

### threshold 
_, threshold = cv2.threshold(imgray, 127, 255, 0) 
contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

height, width, channels = img.shape
print("img: ", height, width, channels)
print("len: ", len(contours)) 

### all contours together
minArea = 100.0
drawContours = []
allContours = []
for contour in contours:
    area = cv2.contourArea(contour) 
    if area >= minArea: 
        drawContours.append(contour)
        if contourIsOnEdge(contour):
            continue

        for cnt in contour:
            allContours.append(cnt.tolist()) 

rows,cols = img.shape[:2]
### draw fitting line
# i = 0
# for cnt in drawContours:
#     image = copy.copy(img)
#     border = InnerContour(cnt)
#     [vx,vy,x,y] = cv2.fitLine(cnt, cv2.DIST_L2,0,0.01,0.01)
#     lefty = int((-x*vy/vx) + y)
#     righty = int(((cols-x)*vy/vx)+y)
    

#     cv2.drawContours(image, [cnt], 0, (0, 0,255), 3)
#     cv2.line(image,(cols-1,righty),(0,lefty),(0,255,0),2)
#     # cv2.line(image,(int(vx),int(vy)),(int(x), int(y)),(0,255,0),2) 
#     title = "image" + str(i)
#     cv2.imshow(title, image)
#     i += 1
 

### draw image outline
allContours = np.array(allContours)
# define main island contour approx. and hull
perimeter = cv2.arcLength(allContours,True)
epsilon = 0.01*cv2.arcLength(allContours,True)
approx = cv2.approxPolyDP(allContours,epsilon,True)
hull = cv2.convexHull(allContours)

print("hull: ", hull)
cv2.drawContours(img, drawContours, -1, (0, 0,255), 3)
# cv2.drawContours(img, [allContours], 0, (0, 0,255), 3)

# cv2.drawContours(img, [approx], -1, (0, 0, 255), 3)
cv2.drawContours(img, [hull], -1, (255, 255, 255), 3)


### crop contour
i = 0
for cnt in drawContours:
    rc = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rc) 
    box = np.int0(box)
    # cv2.drawContours(img, [box],0,(0,0,255),2)
    print(rc)  
    pts = box.tolist()

    print(pts)
    # crop
    # img_crop = img[pts[1][1]:pts[0][1], pts[1][0]:pts[2][0]] 
                       
    title = "crop" + str(i)
    i+=1  
    # cv2.imshow(title, img_crop)

### draw centroid
M = cv2.moments(hull) 

# calculate x,y coordinate of center
cX = int(M["m10"] / M["m00"])
cY = int(M["m01"] / M["m00"])

# put text and highlight the center
cv2.circle(img, (cX, cY), 5, (255, 255, 255), -1)
# cv2.putText(img, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)



cv2.imshow("image", img)
cv2.imshow("image gray", imgray)
cv2.waitKey(0)
cv2.destroyAllWindows()