
#Import modules
import cv2
import numpy as np
import matplotlib.pyplot as plt

#Read the image
im = cv2.imread('road3.jpg')
img = im.copy()
im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

#Convert to grayscale
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
       
#Applying filters
blur = cv2.GaussianBlur(gray,(5,5),0)
      
#Applying Canny edge detection
edges = cv2.Canny(blur,220,150,apertureSize = 3)

#Applying Hough's tranforms
lines = cv2.HoughLines(edges,1,np.pi/180,90,10)

for rho,theta in lines[0]:
   a = np.cos(theta)
   b = np.sin(theta)
   x0 = a*rho
   y0 = b*rho
   x1 = int(x0 + 1000*(-b))
   y1 = int(y0 + 1000*(a))
   x2 = int(x0 - 1000*(-b))
   y2 = int(y0 - 1000*(a))

   cv2.line(img,(x1,y1),(x2,y2),(255,0,0),2)
        
plt.subplot(121),plt.title('Original'),plt.imshow(im)
plt.subplot(122),plt.title('Hough'),plt.imshow(img)
plt.show()
