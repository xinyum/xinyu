import socket
import threading
import select

import random
from UI import UI

myUI = UI(300,300)
myUI.start()

SERVER_IP = "127.0.0.1"
TCP1_PORT = 5005

clisock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clisock.connect((SERVER_IP, TCP1_PORT))
oldtext=''
#print 'Connection address:', addr
#servsock=clisock.getpeername()
while True:
    text = myUI.sendtextout()
    if text != oldtext:
        clisock.send(text)
        data = clisock.recv(1024)
    myUI.changetext(data)
    text = oldtext
clisock.close()





