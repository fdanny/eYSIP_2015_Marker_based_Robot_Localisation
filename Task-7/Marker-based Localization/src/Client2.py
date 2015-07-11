"""
Code for localizing a robot with Aruco markers.

Authors: Niharika Jayanthi, Dheeraj Kamath
Project: Marker-based Localization
Mentor: Sanam Shakya

Main functions:

Global variables:

"""

#Imports

import cv2
import socket
import numpy as np
import math



#Global variables

MAX_MARKERS = 4

mark_detect = [0, 0, 0, 0]
    
objp = np.zeros((1*4,3), np.float32)

objp[1,1] = 1
objp[2,0] = 1
objp[2,1] = 1
objp[3,0] = 1

objp = objp * 105
#(700/9.605116)

count = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 7000

server_ip = '192.168.1.104'

s.connect((server_ip, port))
print "Connected to server"


#Helper functions

def is_aruco_present(img1):
    """
    * Function Name:	is_aruco_present
    * Input:		Image captured
    * Output:		Returns the set of corner points of the marker in the
                        image.
    * Logic:		Finds the contour having four points and compares properties to that of a square
                        to find the marker
    * Example Call:	is_aruco_present()
    """

    i = 0
    raw_points = []
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
                if  10 < e2 < 250:              #10cm - 200cm efficiency
                    print "Contour Id : ",i,"length of array =", len(a2), "\n""\n", a2
                    print x-y
                    if -75 < x-y < 75:  
                        raw_points = a2
                        cv2.drawContours(img1, c1, i, (0,255,0), 2)
                        cv2.imshow('img',img1)
                        cv2.waitKey(500)
                        cv2.destroyAllWindows()
                        return raw_points
            i = i + 1
                                                        
    if raw_points == []:
        return '-1'
            

def get_distance(x1,y1,x2,y2):
    """
    * Function Name:	get_distance
    * Input:		Points
    * Output:		Returns the distnce between two points
    * Logic:		Uses algebra to find the distance
    * Example Call:	get_distance(x, y, x1, y1)
    """
    distance = math.hypot(x2 - x1, y2 - y1)
    return distance

#### To resolve the occurence of points randomly which may tilt image in Perspective ######
def refined_points(approx):
    """
    * Function Name:	refined_points
    * Input:		Points
    * Output:		Corrects the randomness of points and the order
    * Logic:		The distance between the aruco_point and the point of the same type is least
    * Example Call:	get_distance(x, y, x1, y1)
    """
    x1 = approx[0][0][0]
    y1 = approx[0][0][1]
    x2 = approx[1][0][0]
    y2 = approx[1][0][1]
    x3 = approx[3][0][0]
    y3 = approx[3][0][1]
    x4 = approx[2][0][0]
    y4 = approx[2][0][1]
    aruco_points  = [(x1,y1),(x2,y2),(x3,y3),(x4,y4)]
    min_dist = 10000
    for i in aruco_points:
        x, y = i
        dist = get_distance(x,y,0,0)
        if dist < min_dist:
            min_dist = dist
            X1, Y1 = x, y
    min_dist = 10000
    for i in aruco_points:
        x,y = i
        dist = get_distance(x,y,0,480)
        if dist < min_dist:
            min_dist = dist
            X2,Y2 = x,y
    min_dist = 10000        
    for i in aruco_points:
        x,y = i
        dist = get_distance(x,y,540,0)
        if dist < min_dist:
            min_dist = dist
            X3,Y3 = x,y
    min_dist = 10000
    for i in aruco_points:
        x,y = i
        dist = get_distance(x,y,540,480)
        if dist < min_dist:
            min_dist = dist
            X4,Y4 = x,y
    points = ((X1,Y1),(X2, Y2), (X3, Y3), (X4, Y4))
    print "pts", points
    return points



def Perspective(aruco_points,img_name):
    """
    * Function Name:	Perspective
    * Input:		A numpy array with four points and name of an image
    * Output:		Returns the image after performing perspective transform
                        on it
    * Logic:		(FILL THIS PART)
    * Example Call:	Perspective(points, "Marker.jpg")
    """
    img = cv2.imread(img_name)
    a1 = aruco_points
    print aruco_points
    pts1 = np.float([a1[0,0], a1[1,0], a1[2,0], a1[3,0]])
    pts2 = np.float32([[0,0], [0,300], [300,300], [300,0]])
    print pts1
    print pts2
    M = cv2.getPerspectiveTransform(pts1,pts2)

    dst = cv2.warpPerspective(img,M,(300,300))
    per_img = dst.copy()
    cv2.imshow("Perspective",dst)
    cv2.waitKey(500)
    cv2.destroyAllWindows()
    resize = cv2.resize(per_img, (399,399), interpolation = cv2.INTER_CUBIC)
    #Grid box
    dx, dy = 57,57

    # Custom (rgb) grid color
    grid_color = [0,0,255]

    # Modify the image to include the grid
    resize[:,::dy,:] = grid_color
    resize[::dx,:,:] = grid_color
    aruco = resize[57:342, 57:342]
    cv2.imshow("grid",aruco)
    cv2.waitKey(500)
    cv2.destroyAllWindows()
    ret, thresh= cv2.threshold(aruco, 127,255, cv2.THRESH_BINARY)
    g2 = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    return g2, pts1






def findArucoID(marker_img):
    """
    * Function Name:	findArucoID
    * Input:		An image of Aruco marker.
    * Output:		Returns an integer value that represents the ID of the
                        Aruco marker
    * Logic:		The second and fourth columns from the Aruco marker are
                        analyzed. If the pixel value in the grid cell is 0
                        (black), it is taken as 0. If it is 255(white), it is
                        considered as 1. The binary number is generated by
                        reading in a top-bottom, left-right manner.
    * Example Call:	findArucoID(img)
    """

    height = 57
    width = 57
    ret_val = 0
    cv2.imshow("aruco", marker_img)
    cv2.waitKey(500)
    cv2.destroyAllWindows()
    for i in range(5):
        for y in (1, 3):
            px1 = marker_img[height*i + 29, y * width + width/2]
            if px1 == 255:
                val = 1
                #binary.append(val)
            else:
                val = 0
                #binary.append(val)
            ret_val = 2 * ret_val + val
    #print "Binary", binary, ret_val
    return ret_val


def sendPoints(x, y, t, t1, markerID):
    """
    * Function Name:	sendPoints
    * Input:		The (x,y) coordinates of a point, angle, t, which is the
                        rotation angle and the ID(integer) of the marker whose
                        points are being sent.
    * Output:		Sends a message to the server containing the information
                        from the input
    * Logic:		A TCP message is sent to the server through socket
                        programming.
    * Example Call:	sendPoints(269, 346, 1.11812, 34)
    """
    global s

    
    msg = str(x) + " " + str(y) + " " + str(t) + " "+str(t1) + " "+ str(markerID)
    print "message sent"
        

    s.send(msg)
    


def getProperties(points):
    """
    * Function Name:	getProperties
    * Input:		A set of four points of the corners of aruco markers.
                        These points can be obtained from is_aruco_present()
                        function.
    * Output:		-
    * Logic:		The Perspective-n-Point problem is solved by Ransac
                        algorithm. We obtain the translation and rotation
                        vectors through this function.
    * Example Call:	getProperties(points)
    """

    global objp
    
    # Arrays to store object points and image points from all the images.
    objpoints = objp
    print "OBJP", objpoints
    
    imgpoints = points

    #imgpoints = np.array(imgpoints)
    print "IMGP", imgpoints

    mtx = np.load('matrix.npy')
    dist = np.load('distortion.npy')

    rvec, tvec, inliers = cv2.solvePnPRansac(objpoints, imgpoints, mtx, dist)
    print "Rvec\n", rvec
    print "\nTvec", tvec

    x = tvec[0][0]
    y = tvec[2][0]

    dst, jacobian = cv2.Rodrigues(rvec)

    print "Rot Matrix", dst

    t = math.asin(-dst[0][2])
    t1 = math.acos(dst[0][0])

    return x, y, t, t1


def Video(True):
    """
    * Function Name:	Video
    * Input:		-
    * Output:	        Analyzes and detects markers till all markers are
                        detected.
    * Logic:		It runs through a infinite loop checking
                        every frame for markers. If marker is obtained,
                        it increments a count, else, next frame is analyzed.
                        This process is continued till all the markers are
                        detected.
    * Example Call:	Video(True)
    """
    global count,s, mark_detect
    cap = cv2.VideoCapture(1)

    while(True):
        ret, frame = cap.read()
        cv2.imshow("Video", frame)
        cv2.waitKey(500)
        raw_points = is_aruco_present(frame)
        #cv2.imshow("Captured", frame)
        if raw_points != '-1':
            img_name = "Marker.jpg"
            cv2.imwrite(img_name, frame)
            #count = count + 1
            aruco_points = refined_points(raw_points)
            p_img, pts = Perspective(aruco_points, img_name)
            m_id = findArucoID(p_img)
            if (m_id == 65 and mark_detect[0] == 0):
                mark_detect[0] = 1
            elif (m_id == 796 and mark_detect[1] == 0):
                mark_detect[1] = 1
            elif (m_id == 500 and mark_detect[2] == 0):
                mark_detect[2] = 1
            elif (m_id == 250 and mark_detect[3] == 0):
                mark_detect[3] = 1
            else:
                continue
            count = count + 1
            x, y, t, t1 = getProperties(pts)
            if (x == 0.0 and y == 0.0):
                count = count - 1
                if (m_id == 65 and mark_detect[0] == 1):
                    mark_detect[0] = 0
                elif (m_id == 796 and mark_detect[1] == 1):
                    mark_detect[1] = 0
                elif (m_id == 500 and mark_detect[2] == 1):
                    mark_detect[2] = 0
                elif (m_id == 250 and mark_detect[3] == 1):
                    mark_detect[3] = 0
                continue
                
            sendPoints(x, y, t, t1, m_id)
            print "X", x, "Y", y, "T", t, "T1", t1,  "ID", m_id
            if count == MAX_MARKERS:
                print "All detected"
                print "Closing connection"
                if cv2.waitKey(1) == 32: # Ascii for spacebar
                    s.send('q')
                break
                        
                    
            

    cap.release()
    cv2.waitKey(0)     # Escape sequence
    cv2.destroyAllWindows()

Video(True)
s.close()
