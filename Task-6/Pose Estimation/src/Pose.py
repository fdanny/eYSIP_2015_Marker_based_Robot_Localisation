'''Pose estimation of a marker'''

import numpy as np
import cv2
import math

cap = cv2.VideoCapture(0)

#Press space when marker is in front of the camera
while True:
    ret, img = cap.read()
    cv2.imshow("img",img)
    if cv2.waitKey(1) == 32:
        cv2.imwrite("Marker_sample.jpg", img)
        break

def Points(img_name):
    i = 0
    aruco_points = []
    img1 = cv2.imread(img_name)
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray1, 175,255, cv2.THRESH_BINARY_INV+ cv2.THRESH_OTSU)
    kernel = np.ones((5,5), np.uint8)
    open1 = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
    median1 = cv2.medianBlur(open1, 5)
    c1, h1 = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in c1:
        k = cv2.isContourConvex(c)     #Check for convexity, removes unwanted curved contours
        if k == True:
            i = i +1
            continue
        elif k == False:
            e2 = 0.1*cv2.arcLength(c, True)
            a2 = cv2.approxPolyDP(c, e2, True)
            print "a2 = ", a2, "\n", "e2 =", e2
            if len(a2)== 4:
                x = a2[0,0,1]-a2[2,0,1] 
                y = a2[2,0,0]-a2[0,0,0]
                if x < 0:
                    x = x * (-1)      #Converting to unsigned int
                if y < 0:
                    y = y * (-1)      #Converting to unsigned int

                if  30 < e2 < 100:              #45-60cm
                    print "Contour Id : ",i,"length of array =", len(a2), "\n""\n", a2
                    print x-y
                    if -15 < x-y < 15:  # Without tilt
                        aruco_points = a2
                        cv2.drawContours(img1, c1, i, (0,255,0), 2)
                        cv2.imshow('img',img1)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        return aruco_points, '1'
                    elif -70 < x-y < 65:  #with tilt
                        aruco_points = a2
                        cv2.drawContours(img1, c1, i, (0,255,0), 2)
                        cv2.imshow('img',img1)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        return aruco_points, '1'
                    
                    
                elif 15 < e2 < 30:   # 60-100 | tilted
                    print "Contour Id : ",i,"length of array =", len(a2), "\n""\n", a2
                    print x-y
                    if -25 < x-y < 25:   #tilted 
                        aruco_points = a2
                        cv2.drawContours(img1, c1, i, (0,255,0), 2)
                        cv2.imshow('img',img1)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        return aruco_points, '2'
                    elif -60 < x-y < 60:
                        aruco_points = a2
                        cv2.drawContours(img1, c1, i, (0,255,0), 2)
                        cv2.imshow('img',img1)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        return aruco_points, '1'
                        
                elif 100 < x-y < 220:
                    print "Contour Id : ",i,"length of array =", len(a2), "\n""\n", a2
                    print x-y
                    if -10 < x-y < 10:
                        aruco_points = a2
                        cv2.drawContours(img1, c1, i, (0,255,0), 2)
                        cv2.imshow('img',img1)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        return aruco_points, '1'
                    else:
                        aruco_points = a2
                        cv2.drawContours(img1, c1, i, (0,255,0), 2)
                        cv2.imshow('img',img1)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        return aruco_points, '2'
                    
        i = i +1
                        
    if aruco_points == []:
        return '-1', '-1'
            

def Perspective(aruco_points,img_name):
    img = cv2.imread(img_name)
    a1 = aruco_points
    print aruco_points
    lx = -999
    ly = -999
    sx = 999
    sy = 999
    for i in range(0,4):
        if a1[i,0,0] > lx :
            lx = a1[i,0,0]
    print lx

    for i in range(0,4):
        if a1[i,0,0] < sx:
            sx = a1[i,0,0]
    print sx 

    for i in range(0,4):
        if a1[i,0,1] > ly:
            ly = a1[i,0,1]
    print ly
    for i in range(0,4):
        if a1[i,0,1] < sy:
            sy = a1[i,0,1]
    print sy

    pts1 = np.float32([[sx,sy],[sx,ly],[lx,ly],[lx,sy]])
    pts2 = np.float32([[0,0],[0,300],[300,300],[300,0]])
    print pts1
    print pts2
    return pts1



def crop(aruco_points,img_name):
    img = cv2.imread(img_name)
    a1 = aruco_points
    print aruco_points
    pts1 = np.float32([a1[0,0],a1[1,0],a1[2,0],a1[3,0]])
    pts2 = np.float32([[0,0],[0,300],[300,300],[300,0]])
    print pts1
    print pts2
    return pts1



# Prepare object points
objp = np.zeros((1*4,3), np.float32)

objp[1,1] = 1
objp[2,0] = 1
objp[2,1] = 1
objp[3,0] = 1

objp = objp * (600/9.0)
print objp

img = "Marker_sample.jpg"
pts, flag = Points(img)
if flag == '1':
    imgp = Perspective(pts, img)
elif flag == '2':
    imgp = crop(pts, img)
elif flag == '-1':
    quit()
    
print "Image points\n\n", imgp


mtx = np.load('matrix.npy')
dist = np.load('distortion.npy')

rvec, tvec, inliers = cv2.solvePnPRansac(objp, imgp, mtx, dist)
print "Rvec\n", rvec
print "\nTvec", tvec


dst, jacobian = cv2.Rodrigues(rvec)
x = tvec[0][0]
y = tvec[2][0]
t = (math.asin(-dst[0][2]))

print "X", x, "Y", y, "Angle", t
print "90-t", (math.pi/2) - t
Rx = y * (math.cos((math.pi/2) - t))
Ry = y * (math.sin((math.pi/2) - t))


print "rx", Rx, "ry", Ry
