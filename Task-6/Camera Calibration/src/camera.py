#Imports
import cv2
import numpy as np

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)
objp = objp * 26

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

vd = cv2.VideoCapture(0)
i = 0
while(True):

    ret, img = vd.read()
    cv2.imshow("Video cap", img)
    

    inp = cv2.waitKey(1)
    
    if inp == 115: #If input is 's'
        cv2.imwrite(str(i)+".jpg",img)
        i = i + 1
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (9,6), None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)

            cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners)

            # Draw and display the corners
            cv2.drawChessboardCorners(img, (9,6), corners, ret)
            if ret == True:
                cv2.imshow('img',img)
                cv2.waitKey(500)

    elif inp == 27: break


ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints,
                                                   imgpoints, gray.shape[::-1],
                                                   None,None)



print "Camera calibration matrix\n\n", mtx
np.save('cam_broke_mtx', mtx)
np.save('cam_broke_dist', dist)

cv2.destroyAllWindows()

