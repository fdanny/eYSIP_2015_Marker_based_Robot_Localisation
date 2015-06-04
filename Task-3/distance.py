# Import cv2 and matplotlib
import cv2
import matplotlib.pyplot as plt

# Read image and convert it to grayscale
img = cv2.imread("example.jpg")
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# Convert to binary image using thresholding
ret, th = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Perform distance transformation
distance = cv2.distanceTransform(th, cv2.cv.CV_DIST_L2,5)

# Create new window
plt.figure(0)

# Plot grayscale image on 1st plot
plt.subplot(121)
plot = plt.imshow(gray)
plot.set_cmap('bone')

# Plot distance transformed image on 2nd plot
plt.subplot(122)
plot = plt.imshow(distance)
plot.set_cmap('bone')

# Display window
plt.show()

