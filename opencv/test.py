
import sys
import numpy as np
import cv2


class InnerContour:
    topLeft = (sys.maxsize, sys.maxsize)
    bottomLeft = (0, sys.maxsize)
    topRight = (sys.maxsize, 0)
    bottomRight = (0, 0)

    def calculateContour(self, contours):
        for contour in contours:
            x = contour.x
            y = contour.y
            if x < topLeft.x:
                pass
        pass


def contourIsOnEdge(contours):
    for cont in contours: 
        print("cont: ", cont)
        x = cont.item(0, 0)
        y = cont.item(0, 1)
        if x <= 5 or y <= 5:
            return True
    
    return False

# img = cv2.imread("text.png")
img = cv2.imread("lq_sui.jpg")
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Creating kernel 
kernel = np.ones((1, 1), np.uint8) 
# Using cv2.erode() method  
imgray = cv2.erode(imgray, kernel) 

size = 10
imgray = cv2.bilateralFilter(imgray, size, size * 2, size / 2)

_, threshold = cv2.threshold(imgray, 127, 255, 0) 
contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

height, width, channels = img.shape
print("img: ", height, width, channels)
print("len: ", len(contours))
# print(hierarchy)


cnt = contours[0]
M = cv2.moments(cnt)
# print(M)

minArea = 100.0
drawContours = []
allContours = []
for contour in contours:
    area = cv2.contourArea(contour)
    # print("area: ", area) 
    if area >= minArea:
        print("area: ", area)
        drawContours.append(contour)
        if contourIsOnEdge(contour):
            continue

        for cnt in contour:
            allContours.append(cnt.tolist())
        # print("contour: ", contour)
        # cv2.drawContours(img, [contour], 0, (0, 0,255), 3)

# print(allContours)
allContours = np.array(allContours)
# define main island contour approx. and hull
perimeter = cv2.arcLength(allContours,True)
epsilon = 0.01*cv2.arcLength(allContours,True)
approx = cv2.approxPolyDP(allContours,epsilon,True)
hull = cv2.convexHull(allContours)


cv2.drawContours(img, drawContours, -1, (0, 0,255), 3)
# cv2.drawContours(img, [allContours], 0, (0, 0,255), 3)

# cv2.drawContours(img, [approx], -1, (0, 0, 255), 3)
cv2.drawContours(img, [hull], -1, (0, 0, 255), 3)

cv2.imshow("image", img)
cv2.imshow("image gray", imgray)
cv2.waitKey(0)
cv2.destroyAllWindows()