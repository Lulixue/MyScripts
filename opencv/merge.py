
import sys
import numpy as np
import cv2
import copy


def resizeImage(img, dW, dH):
    h, w = img.shape[:2]
    deltaW = int(abs(w - dW)/2)
    deltaH = int(abs(h - dH)/2)
    return img[deltaH:(deltaH+dH), deltaW:(deltaW+dW)]


### load image and grayscale it
# img = cv2.imread("text.png")
img = cv2.imread("cz_bu.jpg")
img2 = cv2.imread("df_bu.jpg")
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

h1, w1 = img.shape[:2]
h2, w2 = img2.shape[:2]

dW = min(w1, w2)
dH = min(h1, h2)

img1 = resizeImage(img, dW, dH)
img3 = resizeImage(img2, dW , dH)

print("img1: ", img1.shape)
print("img3: ", img3.shape)
dst = cv2.addWeighted(img1,0.75,img3,0.25,0)
cv2.imshow('dst',dst)

cv2.waitKey(0)
cv2.destroyAllWindows()
exit()
