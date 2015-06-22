#Importing modules
import cv2
import numpy as np
import matplotlib.pyplot as plt

#Read the image from the camera
img1 = cv2.imread('heirarchy.png')
img2=   img1.copy()   #Using the same image by copying
img3 =  img1.copy()
img4 =  img1.copy()

#Converting to grayscale
gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

#Thesholding
ret,thresh = cv2.threshold(gray,200,255,0)

#Finding contours for each of them
contours1,heirarchy1 = cv2.findContours(thresh,cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
contours2, heirarchy2 = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
contours3,heirarchy3 = cv2.findContours(thresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours4, heirarchy4 = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#Drawing contours for all of them
cv2.drawContours(img1, contours1, -1, (0,255,0),1)
cv2.drawContours(img2, contours2, -1, (0,255,0),1)
cv2.drawContours(img3, contours3, -1, (0,255,0),1)
cv2.drawContours(img4, contours4, -1, (0,255,0),1)

#Printing their hierarchy/ order of relationship
print heirarchy1
print heirarchy2
print heirarchy3
print heirarchy4

#Plotting the image 
plt.subplot(221),plt.imshow(img1),plt.title("RETR_CCOMP")
plt.xticks([]),plt.yticks([])
plt.subplot(222),plt.imshow(img2),plt.title("RETR_LIST")
plt.xticks([]),plt.yticks([])
plt.subplot(223),plt.imshow(img3),plt.title("RETR_TREE")
plt.xticks([]),plt.yticks([])
plt.subplot(224),plt.imshow(img4),plt.title("RETR_EXTERNAL")
plt.xticks([]),plt.yticks([])
plt.show()


#Escape sequence
cv2.waitKey(0)
cv2.destroyAllWindows()
