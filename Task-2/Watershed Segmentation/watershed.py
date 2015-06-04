#import opencvn numpy and matplotlib
import numpy as np               
import cv2
from matplotlib import pyplot as plt

#Reading the image
img = cv2.imread('water_coins.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)        #Conversion to gray scale
ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)   #thresholding

cv2.imshow("Otsu", thresh)

# noise removal
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

# sure background area
sure_bg = cv2.dilate(opening,kernel,iterations=3)


# Finding sure foreground area
dist_transform = cv2.distanceTransform(opening,cv2.cv.CV_DIST_L2,5)
ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

# Finding unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)

cv2.imshow("Sure bg", sure_bg)
cv2.imshow("Sure fg",sure_fg)
cv2.imshow("unknown",unknown)

#Marker Labelling
contours, hierarchy = cv2.findContours(sure_fg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

#Creating a numpy array for markers and converting the image to 32 bit using dtype paramter
marker = np.zeros((gray.shape[0], gray.shape[1]),dtype = np.int32)

marker = np.int32(sure_fg) + np.int32(sure_bg)

for id in range(len(contours)):
                cv2.drawContours(marker,contours,id,id+2, -1)

marker = marker + 1
marker[unknown==255] = 0

"""
# Marker labelling
ret, markers = cv2.connectedComponents(sure_fg)

# Add one to all labels so that sure background is not 0, but 1
markers = markers+1

# Now, mark the region of unknown with zero
markers[unknown==255] = 0
"""

cv2.watershed(img, marker)
img[marker==-1]=(0,0,255)

cv2.imshow('watershed', img)

#To display using colormap
imgplt = plt.imshow(marker)
plt.colorbar()               #Creates a bar of colors
plt.show()                   #Displays the windows

cv2.waitKey(0)
cv2.destroyAllWindows()       #Destroys all windows
