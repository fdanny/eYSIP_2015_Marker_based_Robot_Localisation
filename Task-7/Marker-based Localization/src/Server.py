"""
This code receives and maps points

Authors: Niharika Jayanthi, Dheeraj Kamath
Project: Marker-based Localization
Mentor: Sanam Shakya

Main functions: draw_arena(), draw_marker(), draw_robot()
                getCoordinates(), get_socket()

Global variables: arena_length, arena_breadth, s, host, port, room_width

"""
import socket
import cv2
from matplotlib import pyplot as plt
import numpy as np
import math


#Define Globals

arena_length=600
arena_breadth=600

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 7000
s.bind((host, port))
s.listen(2)

room_width = 1160


#Helper functions

def draw_arena(img1):
    """
    * Function Name:	draw_arena
    * Input:		Image to be drawn in
    * Output:		Modified image with arena drawn
    * Logic:		The arena lines are drawn one at a time, with a distance
                        of 50 units separating them.
    * Example Call:	draw_arena(image)
    """
    # Draw a diagonal blue line with thickness of 5 px
    row_width = 50
    col_width =  50

    #print arena_length/50
    for i in range(0, arena_length/row_width):
        cv2.line(img1,(row_width,0),(row_width,arena_length),(0,0,0),1)
        cv2.line(img1,(0,col_width),(arena_breadth,col_width),(0,0,0),1)
        row_width=row_width+50
        col_width=col_width+50
    
    
def draw_marker(id, img1):
    """
    * Function Name:	draw_marker
    * Input:		Marker ID, image to be drawn in
    * Output:		Returns 1 if valid marker is drawn. Else, it returns -1.
    * Logic:		The marker id is checked for validity. If marker is
                        valid, it draws in fixed position and returns 1. Else,
                        it returns -1.
    * Example Call:	draw_marker(65, image)
    """
    marker_width = 50
    marker_length = 50
    
    font = cv2.FONT_HERSHEY_SIMPLEX

    if id == 65:
        x = 0
        y = 0
    elif id == 250:
        x = 550
        y = 0
    elif id == 796:
        x = 0
        y = 550
    elif id == 500:
        x = 550
        y = 550
    else:
        return '-1'
    
    cv2.rectangle(img1,(x,y),(x+marker_width,y+marker_length),(255,0,0,10),-1)
    cv2.putText(img1,'#'+str(id),(x+10,y+30), font, 0.5,(0,0,0),1)

    return 1


def draw_robot(x, y, theta_radian, img1):
    """
    * Function Name:	draw_robot()
    * Input:		x,y coordinates of the robot's position in map, angle
                        of inclination(theta) and image to be drawn in.
    * Output:		Modified image with the robot drawn in it and result is
                        displayed.
    * Logic:		The end point of the line is found by calculating a
                        rotation matrix and translating it. The robot is then
                        drawn as a circle and the line on the robot depicts
                        its orientation.
    * Example Call:	draw_robot(250, 250, 45, image)
    """
    radius = 20
    
    rotation_matrix= [[np.cos(theta_radian), -np.sin(theta_radian)],
                      [np.sin(theta_radian), np.cos(theta_radian)]]
    R = np.array(rotation_matrix)
    xy = [[radius],[0]]
    xy = np.array(xy)
    rotated_xy = np.dot(R,xy)

    translation = [[x],[y]]
    translation = np.array(translation)
    trans_xy = rotated_xy + translation

    #Convert from floating point to integers
    x = int(x)
    y = int(y)
    
    cv2.circle(img1,(x,y), radius, (0,0,255), -1)

    cv2.line(img1,(x,y),(trans_xy[0],trans_xy[1]),(0,0,0),2)
    cv2.imshow("Position", img1)
    cv2.waitKey(1000)


def getCoordinates(x, y, t, mID):
    """
    * Function Name:	getCoordinates
    * Input:		x, y coordinates of point, angle t, marker ID
    * Output:		Returns new values of x, y and t.
    * Logic:		It compares the marker ID to a valid list of markers,
                        whose position in a room is already known to us and
                        returns the values of x,y and t according to the ID.
    * Example Call:	getCoordinates(125, 235, 45, 500)
    """

    if mID == 65:
        return x, y, 3*math.pi/2 - abs(t)
    elif mID == 796:
        return x, 550 - y, math.pi/2 + abs(t)
    elif mID == 500:
        return 550 - x, 550 - y, math.pi/2 - abs(t)
    elif mID == 250:
        return 550 - x, y, 3 * math.pi/2 + abs(t)
    else:
        print "Marker doen't match!"
        return 0, 0, 0



def get_socket():
    """
    * Function Name:	get_socket
    * Input:		-
    * Output:		-
    * Logic:		This function creates a TCP socket and receives
                        information from the client. This information includes
                        x, y coordinates of a marker, the angle t(calculated
                        with sine inverse), angle t1 (calculated as cosine
                        inverse) and the marker ID detected. These values are
                        passed to getCoordinates, which returns the x,y
                        values scaled to virtual map. Then, the marker/arena and
                        robot is drawn.
    * Example Call:	get_socket()
    """
    global s, first_msg, arena_M, cur_x, cur_y

    c, addr = s.accept()

    while True:
        msg = c.recv(100)
        print "Message received is", msg
        
        try:
            if msg == 'q':
                print "End of messages.\n"
                break

            x, y, t, t1, m_id = msg.split()
            x = float(x)
            y = float(y)
            t = float(t)
            t1 = float(t1)
            m_id = int(m_id)

            x = 600 * (x/room_width)
            y = 600 * (y/room_width)
            
            Rx = abs(y * math.cos(math.pi/2 - t))
            Ry = abs(y * math.sin(math.pi/2 - t))
            img_arena = arena_M.copy()
            ret = draw_marker(m_id, arena_M)
            if ret == '-1':
                print "Marker not recognised."
                
            print "X", x, "Y", y, "T", t, "T1", t1, "mID", m_id

            print "Rx", Rx, "Ry", Ry

            mx, my, t = getCoordinates(Rx, Ry, t, m_id)

            if (mx,my,t) == (0,0,0):
                print "Invalid coordinates"
                continue
            arena_copy = arena_M.copy()
            draw_robot(mx, my, t, arena_copy)
            
        except ValueError:
            print "Bad message!\n"
            break

# Create a black image
img = np.ones((arena_length,arena_breadth,4), np.uint8)*245
#img2 = np.ones((arena_length,arena_breadth,4), np.uint8)*255

draw_arena(img)
arena_M = img
get_socket()
s.close()

#cv2.imshow("Map", arena_M)
cv2.waitKey(0)
cv2.destroyAllWindows()
                                
