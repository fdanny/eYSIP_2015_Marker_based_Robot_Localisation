# Imports
import cv2
import numpy as np

# Read image
img = cv2.imread("music.jpg",0)

# Create structuring element
kernel = np.ones((5,5),np.uint8)

# Dilate image
dilation = cv2.dilate(img,kernel,iterations = 1)

# Show image
cv2.imshow("Dilated image",dilation)

# Save image
cv2.imwrite("Dilated music.jpg",dilation)

cv2.waitKey(0)
cv2.destroyAllWindows()
