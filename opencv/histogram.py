
import sys
import numpy as np
import cv2
import copy 

from matplotlib import pyplot as plt


def r_c(hist ):
    Ng = 255
    tc = 255
    index = 0

    while index <= tc and index <= Ng:
        bck_sum = 0
        hist_sum_bck = 0
        fr_sum = 0
        hist_sum_fr = 0
        b = 0 
        f = 0
               
        for i in range(0, index+1):
            bck_sum += i * hist[i][0]
            hist_sum_bck += hist[i][0]
            
        for j in range(index+1, Ng+1):
            fr_sum += j * hist[j][0]
            hist_sum_fr += hist[j][0]

        try:
            b = (bck_sum / hist_sum_bck)   
            f = (fr_sum / hist_sum_fr)
        
            if hist_sum_bck == 0.0 : 
                raise ZeroDivisionError  
            if hist_sum_fr == 0.0:
                raise ZeroDivisionError 
        except ZeroDivisionError:
            index += 1
            continue

        tc = (b  + f) // 2 

        index += 1
        
    return tc


def findHistPeaks(hist):
    #Convert histogram to simple list
    hist = [val[0] for val in hist]

    #Generate a list of indices
    indices = list(range(0, 256))

    #Descending sort-by-key with histogram value as key
    s = [(x,y) for y,x in sorted(zip(hist,indices), reverse=True)]

    #Index of highest peak in histogram
    index_of_highest_peak = s[0][0]

    #Index of second highest peak in histogram
    index_of_second_highest_peak = s[1][0]

    return (index_of_highest_peak, index_of_second_highest_peak)

### load image and grayscale it
# img = cv2.imread("text.png")
img = cv2.imread("zht_bu.jpg")
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

### translate into 2D array
# plt.hist(img.ravel(),256,[0,256])
# plt.show()
histogram_img = cv2.calcHist([img],[0],None,[256],[0,256])
# histogram_img.resize(histogram_img.size)

# thr = int(r_c(histogram_img))
print("peaks:", findHistPeaks(histogram_img))

# dst = cv2.equalizeHist(imgray)
plt.plot(histogram_img)
plt.show()

# cv2.imshow("hist", histogram_img)
# cv2.imshow('Source image', img)
# cv2.imshow('Equalized Image', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()