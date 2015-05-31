'''
***************************************************************************************
*
*                   IMAGE PROCESSING ( MASKING OPERATION )
*
*
*  TEAM MEMBERS : NIHARIKA JAYANTHI, DHEERAJ KAMATH
*  
*  MENTOR : SANAM SHAKYA
*
*  FILENAME : MASKING.PY
*
*  THEME : DEVELOP MODULES FOR IMAGE PROCESSING AND ROBOT LOCALISATION USING MARKERS
*
*  FUNCTIONS : cv2.inRange(), cv2.cvtColor(), cv2.bitwise_and(), cv2.threshold()
*
*  GLOBAL VARIABLES : NONE
*
***************************************************************************************
'''

#####################################################

import cv2                        #Import OpenCV
import numpy as np                #Import Numpy 


############ Reading the image ######################
img = cv2.imread('Rainbow-Gems.jpg')


############### Blue Mask ###########################
'''
* FUNCTION NAME  : cv2.inRange()
* INPUT          : Input is source image.
* OUTPUT         : A image in which the hsv values of the pixels lying in the defined range
                   will be extracted and displayed.
* LOGIC          : It displys only those values of the pixels which lie in the range specified
* EXAMPLE CALL   : mask = cv2.inRange(hsv, lower_range, upper_range)
* ADDITIONAL INFO: The HSV values are calculated by using a color pic tool. Refer the documentation
                   for further information.

'''
lower_blue = np.array([95,60,60])            #First set of Pixel values/ hsv values
upper_blue = np.array([150,255,255])         #Second set of Pixel values/ hsv values

'''
For masking we need a hsv image. Hence we use the function cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
This converts the source image to hsv.
'''

hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower_blue, upper_blue)
res = cv2.bitwise_and(img,img, mask = mask)       #It AND's the source image and the masked image to give the colored image 
cv2.imshow('res', res)

cv2.waitKey(5000)
cv2.destroyAllWindows()           




