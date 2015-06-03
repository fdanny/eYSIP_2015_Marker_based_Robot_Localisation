import cv2
import matplotlib.pyplot as plt

img = cv2.imread("example.jpg")
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

ret, th = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

cv2.imshow("Binary",th)

distance = cv2.distanceTransform(th, cv2.cv.CV_DIST_L2,5)

plot = plt.imshow(distance)
plot.set_cmap('bone')
plt.colorbar()
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
