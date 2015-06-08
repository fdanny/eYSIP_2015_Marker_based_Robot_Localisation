#Import OpenCV, numpy and matplotlib
import numpy
import cv2
import matplotlib.pyplot as plt


#Read the image
img = cv2.imread('monalisa.jpg')


'''
OpenCV represents RGB images as multi-dimensional NumPy arrays…but in reverse
order!This means that images are actually represented in BGR order rather than
RGB!
'''
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   #Convert to RGB
    
#Resize()
res = cv2.resize(img,None,fx=0.2, fy=0.2, interpolation = cv2.INTER_LINEAR)
#cv2.imshow('res',res)

#Applying filters on image resized using resize()
r1_blur = cv2.medianBlur(res,5)

#Applying filters on original image
nr_blur = cv2.medianBlur(img,5)

#Downsizing the image
ds = cv2.pyrDown(img, 5)

#Applying filters on downsized image using pyrDown()
r2_blur = cv2.medianBlur(ds,5)


plt.figure("Compare")         #Create a new window
plt.subplot(221),plt.imshow(img), plt.title('Original image')
plt.xticks([]), plt.yticks([])
plt.subplot(222),plt.imshow(nr_blur),plt.title('Median Blur without resize')
plt.xticks([]), plt.yticks([])
plt.subplot(223),plt.imshow(r1_blur),plt.title('Median Blur after resize()')
plt.xticks([]), plt.yticks([])
plt.subplot(224),plt.imshow(r2_blur),plt.title('Median Blur after pyrDown()')
plt.xticks([]), plt.yticks([])
plt.show()
