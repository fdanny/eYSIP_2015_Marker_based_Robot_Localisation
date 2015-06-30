import numpy as np
import cv2
from matplotlib import pyplot as plt

arena_length=600
arena_breadth=600
# Create a black image
img1 = np.ones((arena_length,arena_breadth,4), np.uint8)*245
img2 = np.ones((arena_length,arena_breadth,4), np.uint8)*255


def draw_arena():
    # Draw a diagonal blue line with thickness of 5 px
    row_width = 50
    col_width =  50

    print arena_length/50
    for i in range(0, arena_length/row_width):
        cv2.line(img1,(row_width,0),(row_width,arena_length),(0,0,0),1)
        cv2.line(img1,(0,col_width),(arena_breadth,col_width),(0,0,0),1)
        row_width=row_width+50
        col_width=col_width+50
#def markers(x, y, id):
    
    
def draw_marker(x,y,id):
    marker_width = 50
    marker_length = 50
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    cv2.rectangle(img1,(x,y),(x+marker_width,y+marker_length),(255,0,0,10),-1)
    cv2.putText(img1,'#'+str(id),(x+10,y+30), font, 0.5,(0,0,0),1)


def draw_robot(x,y,theta):
    radius = 20
    
    
    theta_radian = theta*np.pi/180
    
    rotation_matrix= [[np.cos(theta_radian), -np.sin(theta_radian)],[np.sin(theta_radian), np.cos(theta_radian)]]
    R = np.array(rotation_matrix)
    xy = [[radius],[0]]
    xy = np.array(xy)
    rotated_xy = np.dot(R,xy)

    translation = [[x],[y]]
    translation = np.array(translation)
    trans_xy = rotated_xy+ translation

    cv2.circle(img1,(x,y), radius, (0,0,255), -1)

    cv2.line(img1,(x,y),(trans_xy[0],trans_xy[1]),(0,0,0),2)
    #transformed_xy = 
    print xy
    print trans_xy
    print rotation_matrix
    print rotated_xy
    
    
    
draw_arena()
draw_marker(50,50,31)
draw_marker(250,250,50)
draw_robot(150,150,45)


rows,cols,_ = img1.shape

#M = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
#dst = cv2.warpAffine(img1,M,(cols,rows))



#dst = cv2.addWeighted(img1,0.5,img2,0.5,0)
#plt.imshow(dst, cmap = 'jet', interpolation = 'bicubic')
#plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
#plt.show()
cv2.imshow('arena', img1)

cv2.waitKey(0)
cv2.destroyAllWindows()
