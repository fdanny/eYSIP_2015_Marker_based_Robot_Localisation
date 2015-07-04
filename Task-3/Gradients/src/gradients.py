#Import modules
import cv2
import numpy as np
import matplotlib.pyplot as plt

#Defining variables
scale = 1
delta = 0
ddepth = cv2.CV_64F

#Read the image
img = cv2.imread('keyboard.jpg')

'''
OpenCV represents RGB images as multi-dimensional NumPy arrays…but in reverse
order!This means that images are actually represented in BGR order rather than
RGB!
'''
#Convert to RGB
inp_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#Convert to grayscale
#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 

#Applying threshold
#ret, thresh = cv2.threshold(gray,127,255, cv2.THRESH_BINARY) 

# Gradient-X
grad_x = cv2.Sobel(img,ddepth,1,0,ksize = 3, scale = scale, delta = delta,borderType = cv2.BORDER_DEFAULT)

# Gradient-Y
grad_y = cv2.Sobel(img,ddepth,0,1,ksize = 3, scale = scale, delta = delta, borderType = cv2.BORDER_DEFAULT)

#Laplacian
lap = cv2.Laplacian(img,ddepth) 

# converting back to uint8
abs_grad_x = cv2.convertScaleAbs(grad_x)   
abs_grad_y = cv2.convertScaleAbs(grad_y)

#Finding the weighted mean
Sobel = cv2.addWeighted(grad_x,0.5,grad_y,0.5,0)

# Gradient-X
gra_x = cv2.Scharr(img,cv2.CV_16S,1,0)

# Gradient-Y
gra_y = cv2.Scharr(img,cv2.CV_16S,0,1)

ab_grad_x = cv2.convertScaleAbs(gra_x)   # converting back to uint8
ab_grad_y = cv2.convertScaleAbs(gra_y)

scharr = cv2.add(ab_grad_x,ab_grad_y)

#Plotting the images
plt.subplot(2,2,1),plt.imshow(inp_img,cmap = 'gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,2),plt.imshow(grad_x,cmap = 'gray')

plt.title('Sobel'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,3),plt.imshow(lap,cmap = 'gray')
plt.title('Laplacian'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,4),plt.imshow(scharr,cmap = 'gray')
plt.title('Scharr'), plt.xticks([]), plt.yticks([])

#Display the window
plt.show()
