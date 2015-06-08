#Import OpenCV and Numpy
import numpy as np
import cv2
import matplotlib.pyplot as plt

#Read the image
img = cv2.imread('pepper.png')

'''
OpenCV represents RGB images as multi-dimensional NumPy arrays…but in reverse
order!This means that images are actually represented in BGR order rather than
RGB!
'''
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   #Coverting from bgr to rgb


# Do the processing
blur = cv2.GaussianBlur(img,(5,5),0)


plt.figure(0)       # Create a new window

plt.subplot(121),plt.imshow(img), plt.title('Original')
plt.xticks([]), plt.yticks([])      #Removing ticks

plt.subplot(122),plt.imshow(blur), plt.title('Gaussian')
plt.xticks([]), plt.yticks([])

plt.show()          #Display the window


# Close and exit
cv2.waitKey(0)
cv2.destroyAllWindows()

