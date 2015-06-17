# Imports
import cv2

# Read image
img = cv2.imread("images/example/example.jpg")

# Convert to grayscale and apply thresholding
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, th = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Find moments
M = cv2.moments(th, True)

print M

# Find Hu invariant moments
Hu = cv2.HuMoments(M)

print Hu
