import socket


TCP_IP = '192.168.1.101'
TCP_PORT = 5005
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

#MESSAGE = "Hello, World!"
#MESSAGE = raw_input("->")
MESSAGE = "x,y,alpha,id,0"
while MESSAGE != 'q':
    s.send(MESSAGE)
    data = s.recv(BUFFER_SIZE)
    print "received data:", data
    MESSAGE = raw_input("->")
s.close()


