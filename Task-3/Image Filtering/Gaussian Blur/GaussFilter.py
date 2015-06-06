#Import OpenCV and Numpy
import numpy
import cv2

#Read the image
img = cv2.imread('pepper.png')

# Do the processing
blur = cv2.GaussianBlur(img,(5,5),0)

# Show the image
cv2.imshow('Gaussian',blur)
cv2.imshow('Original',img)

# Close and exit
cv2.waitKey(0)
cv2.destroyAllWindows()

