import cv2
import numpy as np
#from matplotlib import pyplot as plt

# global variables used in functions

global low_th
global high_th
global img

# callback for 'low' trackbar
def low_threshold(x):
    low_th = x
    high_th = cv2.getTrackbarPos('high', 'canny')
    
    edges = cv2.Canny(img, x, high_th)
    cv2.imshow('canny', edges)

# callback for 'high' trackbar
def high_threshold(x):
    high_th = x
    low_th = cv2.getTrackbarPos('low', 'canny')
   
    edges = cv2.Canny(img, low_th, x)
    cv2.imshow('canny', edges)   


#reading image 
img = cv2.imread('../images/castle.jpg',0)
cv2.imshow('original', img)

#creating the window for opencv
cv2.namedWindow('canny')

#creating trackbar for low and high thresholds
cv2.createTrackbar('low','canny',0,255,low_threshold)
cv2.createTrackbar('high','canny',0,255,high_threshold)


#setting the trackbar position
low_th = 100
high_th = 200
cv2.setTrackbarPos('low','canny',low_th)
cv2.setTrackbarPos('high','canny',high_th)


#canny edge detection
edges = cv2.Canny(img,low_th,high_th)
cv2.imshow('canny', edges)


#escape sequence
if ((cv2.waitKey(0) & 0xFF) == 27):
    cv2.destroyAllWindows()
