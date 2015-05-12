import socket
import threading
import select
import sys
from UItest import UI
#from Converter import Converter

class Converter(object):
    @staticmethod
    def run(soc, recvdata, queue):
        comlist = recvdata.split(' ')
        commandname = comlist.pop(0)
        if commandname == 'gamestart':
            gameWindow = UI(800,600, soc, queue, comlist[0])
            gameWindow.start()
            return queue
        elif commandname == 'dealcard':
            templist=queue.get(commandname,[])
            templist+=comlist
            queue[commandname]= templist
            return queue
        else:
            queue[commandname] = comlist
            return queue


class Receiver(threading.Thread):
    def __init__(self, sock, queue):
        super(Receiver, self).__init__()
        self.list = [sock]
        self.queue = queue
        
        
    def run(self):
        while True:
            (readable, writable, exceptional) = select.select(self.list, [], [])
            for soc in readable:
                try:
                    recvdata = soc.recv(1024)
                    #print 'recvdata:',recvdata
                    self.queue=Converter.run(soc, recvdata, self.queue)
                    #print 'queue:',self.queue
                except:
                    sys.exit()
 
class Client(object):
    def __init__(self, ip, queue):
        TCP_PORT = 50005
        self.clisock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clisock.connect((ip, TCP_PORT))
        self.receiver = Receiver(self.clisock, queue)
        self.receiver.start()