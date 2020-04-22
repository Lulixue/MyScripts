
import numpy as np
import cv2

# img = cv2.imread("text.png")
img = cv2.imread("df_bu.jpg")
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, threshold = cv2.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

height, width, channels = img.shape
print("img: ", height, width, channels)
print("len: ", len(contours))
# print(hierarchy)


cnt = contours[0]
M = cv2.moments(cnt)
# print(M)

minArea = 20.0
drawContours = []
for contour in contours:
    area = cv2.contourArea(contour)
    # print("area: ", area)
    if area >= minArea:
        drawContours.append(contour)
        # cv2.drawContours(img, [contour], 0, (0, 0,255), 3)



cv2.imshow("image", img)
cv2.imshow("image gray", imgray)
cv2.waitKey(0)
cv2.destroyAllWindows()