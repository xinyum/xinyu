import socket
import select
import time
import random
from Logic import Player,Logic

class Conver(object):
    @staticmethod
    def run(gamelogic, player, recvdata):
        clinfo = recvdata.split()
        infoname = clinfo.pop(0)
        if infoname == 'wantplay':
            #if gamelogic.turn == player:
            (presend,sendtoplayer) = gamelogic.playdetermine(player, clinfo)
            print 'conver: ',(presend,sendtoplayer)
            if sendtoplayer == 'all':
                cards=''
                for card in clinfo:
                    cards += ' '+card
                presend = 'cardplay ' + str(len(player.handcards))+" "+player.name +  cards
            return (presend, sendtoplayer)

    @staticmethod
    def checkround(gamelogic):
        if gamelogic.checkroundover():
            return ('roundover True', 'all')
        return ('roundover False', 'all')

class CustomerCommu(object):
    def __init__(self,servsock,readlist,writelist):
        self.readlist = readlist
        self.writelist = writelist
        self.servsock = servsock
        
    def toclose(self):
        for soc in self.readlist:
            soc.close()

    def doselectmodule(self):
        while True:
            (readable, writable, exceptional) = select.select(self.readlist, [], [])
            for soc in readable:
                if soc == self.servsock:
                    newsock, (remhost, remport) = soc.accept()
                    self.readlist.append( newsock )
                    self.writelist.append( newsock )
                    self.sendToAll('playernum ' + str(len(self.writelist)))
                    if len(self.writelist) == 3:
                        time.sleep(4)
                        name = 'A' 
                        playerlist=[]
                        for gamesoc in self.writelist:
                            try:
                                if name=='A':
                                    gamesoc.send('gamestart '+ name+ ' B'+' C' )
                                elif name=='B':
                                    gamesoc.send('gamestart '+ name+ ' C'+' A' )
                                else:
                                    gamesoc.send('gamestart '+ name+ ' A'+' B' )
                                playerlist.append(Player(gamesoc, name))
                                name = chr(ord(name)+1)
                            except Exception, e:
                                print e
                                soc.close
                                self.readlist.remove(soc)
                                self.writelist.remove(soc)
                        gamelogic = Logic(playerlist)
                        gamelogic.dealcard()
                        time.sleep(3)
                        for i in xrange(len(playerlist[0].handcards)):
                            time.sleep(0.5)
                            for player in playerlist:
                                player.handcards.sort()
                                player.sock.send('dealcard '+ player.handcards[i])
                        time.sleep(1)
                        self.sendToAll('turn '+gamelogic.turn.name)
                else:
                    try:
                        recvdata = soc.recv(1024)
                        print 'recvdata',recvdata
                        player = gamelogic.getPlayer(soc)
                        (presend, sendtoplayer) = Conver.run(gamelogic, player, recvdata)
                        if sendtoplayer == 'all':
                            self.sendToAll(presend)
                        else:
                            sendtoplayer.sock.send(presend)
                        time.sleep(0.3)
                        (presend, sendtoplayer) = Conver.checkround(gamelogic)
                        if sendtoplayer == 'all':
                            self.sendToAll(presend)
                        time.sleep(0.3)
                        if gamelogic.isgameover == True:
                            self.sendToAll('win '+ player.name)
                            self.toclose()
                        else:
                            self.sendToAll('turn '+gamelogic.turn.name)
                            print 'turn ', gamelogic.turn.name
                    except Exception, e:
                        print e
                        soc.close
                        self.readlist.remove(soc)
                        self.writelist.remove(soc)

    def sendToAll(self, senddata):
        for soc in self.writelist:
            soc.send(senddata)
            print 'senddata:',senddata

class Server(object):
    def run(self):
        TCP1_IP = '' #listen to everyone
        TCP1_PORT = 50005 #my port
        servsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servsock.bind((TCP1_IP, TCP1_PORT))
        servsock.listen(5)
        readlist=[servsock]
        writelist=[]
        self.servercommu=CustomerCommu(servsock, readlist,writelist)
        self.servercommu.doselectmodule()

Server().run()

