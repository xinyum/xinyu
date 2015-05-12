import socket
import select
#from Converter import Converter

class CustomerCommu(object):
    def __init__(self,servsock,readlist,writelist):
        self.readlist = readlist
        self.writelist = writelist
        self.servsock =servsock
        #self.conv = Converter()
 
    
    def doselectmodule(self):
        while True:
            (readable, writable, exceptional) = select.select(self.readlist, [], [])
            for soc in readable:
                if soc == self.servsock:
                    print "a"
                    newsock, (remhost, remport) = soc.accept()
                    self.readlist.append( newsock )
                    self.writelist.append( newsock )
                    print self.readlist
                else:
                    recvdata = soc.recv(1024)
                    if recvdata == '':
                        soc.close
                        self.readlist.remove(soc)
                        self.writelist.remove(soc)
                        continue
                    #senddata = self.conv.convert(recvdata)
                    senddata = recvdata
                    self.sendSolveddata(senddata)

    def sendSolveddata(self,senddata):
        #print self.writelist
        for soc in self.writelist:
            soc.send(senddata)
 
 
 

TCP1_IP = '' #listen to everyone
TCP1_PORT = 5005 #my port
servsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servsock.bind((TCP1_IP, TCP1_PORT))
servsock.listen(5)
readlist=[servsock]
writelist=[]
CustomerCommu(servsock, readlist,writelist).doselectmodule()





