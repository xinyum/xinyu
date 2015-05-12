import socket
import threading
import select
import sys
from UI import UI

class Converter(object):
    @staticmethod
    def run(soc, recvdata, queue):
        comlist = recvdata.split()
        commandname = comlist.pop(0)
        if commandname == 'gamestart':
            gameWindow = UI(900,600, soc, queue, comlist[0],comlist[1],comlist[2])
            gameWindow.start()
            queue[commandname] = comlist
            return queue
        elif commandname == 'dealcard':
            templist=queue.get(commandname,[])
            templist+=comlist
            queue[commandname]= templist
            return queue
        elif commandname == 'cardplay':
            if comlist[1] == queue['gamestart'][0]:
                for card in comlist[2:]:
                    queue['dealcard'].remove(card)
                if len(comlist)==2:
                    comlist+=['pass']
                queue['mycardplay'] = comlist[1:]
                queue['myremain'] = int(comlist[0])
            elif comlist[1] == queue['gamestart'][1]:
                if len(comlist)==2:
                    comlist+=['pass']
                queue['leftcardplay'] = comlist[1:]
                queue['leftremain'] = int(comlist[0])
            elif comlist[1] == queue['gamestart'][2]:
                if len(comlist)==2:
                    comlist+=['pass']
                queue['rightcardplay'] = comlist[1:]
                queue['rightremain'] = int(comlist[0])
            return queue
        elif commandname =='roundover':
            if comlist ==['True']:
                queue['mycardplay']=[]
                queue['rightcardplay']=[]
                queue['leftcardplay']=[]
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
                    
                    self.queue=Converter.run(soc, recvdata, self.queue)
                    
                except:
                    sys.exit()
 
class Client(object):
    def __init__(self, ip, queue):
        TCP_PORT = 50005
        self.clisock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clisock.connect((ip, TCP_PORT))
        self.receiver = Receiver(self.clisock, queue)
        self.receiver.start()