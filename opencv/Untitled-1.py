
import cv2
import numpy as np

img = cv2.imread("0031.jpg")
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(imgray,50,150, apertureSize = 3)

cv2.imshow("canny", edges)
lines = cv2.HoughLines(edges,1,np.pi/180,200)

minLineLength = 100
maxLineGap = 10
lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)

if lines is not None and  lines.any():
    print("len: ", len(lines), "\nlines:", lines)
if lines is not None and   lines.any() and len(lines) != 0:
    for line in lines:
        # rho,theta = line[0]
        x1,y1,x2,y2 = line[0]
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
        # a = np.cos(theta)
        # b = np.sin(theta)
        # x0 = a*rho
        # y0 = b*rho
        # x1 = int(x0 + 1000*(-b))
        # y1 = int(y0 + 1000*(a))
        # x2 = int(x0 - 1000*(-b))
        # y2 = int(y0 - 1000*(a))

        # cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

    # cv2.imwrite('houghlines3.jpg',img)
    cv2.imshow("img", img)

cv2.waitKey(0)
cv2.destroyAllWindows()
