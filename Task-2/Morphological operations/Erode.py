# Imports
import cv2
import numpy as np

# Read image
img = cv2.imread("music.jpg",0)

# Create structuring element
kernel = np.ones((5,5),np.uint8)

# Erode image
erosion = cv2.erode(img,kernel,iterations = 1)

# Show Image
cv2.imshow("Eroded image",erosion)

# Save image
cv2.imwrite("Eroded music.jpg",erosion)

cv2.waitKey(0)
cv2.destroyAllWindows()
