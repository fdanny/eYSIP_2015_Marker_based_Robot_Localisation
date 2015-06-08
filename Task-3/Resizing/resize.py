#Import OpenCV, numpy and matplotlib
import numpy
import cv2
import matplotlib.pyplot as plt


#Read the image
img = cv2.imread('lion.jpg')

'''
OpenCV represents RGB images as multi-dimensional NumPy arrays…but in reverse
order!This means that images are actually represented in BGR order rather than
RGB!
'''
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   #Convert to RGB

#Resize()
res = cv2.resize(img,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_LINEAR)

plt.figure(0)     #Create a new window
plt.subplot(121),plt.imshow(img), plt.title('Original')
plt.subplot(122), plt.imshow(res), plt.title('Resized')

plt.show()        #Display the image

