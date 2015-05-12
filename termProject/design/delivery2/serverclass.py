import socket
import select
import random
import time

class Logic(object):
    def __init__(self,playerlist):
        self.allcards = ['0802','0304','0401','1201','0403','1002','0604','1102',
                         '0301','0501','0902','0504','0601','1402','0603','1401',
                         '1701','0701','0503','0704','1202','0803','1503','0804',
                         '0901','0502','1001','0903','0904','1003','1004','1302',
                         '1101','0302','0402','0702','1104','0303','1203','1204',
                         '1301','1601','1303','0602','1304','1403','1404','0404',
                         '1501','1103','1502','0703','0801','1504']
        self.playerlist = playerlist
        self.linkPlayers(playerlist)

    class Round(object):
        def __init__(self, player, cardsPlayed):
            self.roundMax = cardsPlayed
            self.roundPass = []
            self.turn = player.next
            self.maxtype=cardtype(self.roundMax)
        
        def playcards(self, player, cardsPlayed):
            cardtype=cardtype(cardsPlayed)
            if self.islegal(cardtype,maxtype,cardsPlayed)==True:
                player.playcard(cardsPlayed)
            
            
        def islegal(self, cardtype, cardsPlayed):
            if cardtype == self.maxtype:
                if cardsPlayed[-1][0:2]<= self.roundMax[-1][0:2]:
                    return False
                else: return True
            else:
                if cardtype=='bomb':
                    return True
                else: return False
        
            
        def cardtype(cards):
            cardnum=len(cards)
            if cardnum == 1:
                cardtype='one'
                return cardtype
            elif cardnum == 2 and cards[0][0:2]==cards[1][0:2]:
                cardtype='two'
                return cardtype
            elif cardnum == 4:
                if (cards[0][0:2]==cards[1][0:2]):
                    if cards[1][0:2]==cards[2][0:2] and cards[2][0:2]==cards[3][0:2]:
                        cardtype='bomb'
                        return cardtype
                    elif (abs(int(cards[1][0:2])-int(cards[2][0:2]))==1):
                        cardtype='sister'
                        return cardtype
            elif cardnum == 5 :
                if (cards[0][0:2]==cards[1][0:2]):
                    if  ((cards[1][0:2]==cards[2][0:2] and cards[3][0:2]==cards[4][0:2])
                        or(cards[3][0:2]==cards[4][0:2] and cards[2][0:2]==cards[3][0:2])):
                        cardtype = 'fullhouse'
                        return cardtype
                
                else:
                    for index in cardnum-1:
                        if abs(int(cards[index][0:2])-int(cards[index+1][0:2]))!=1:
                            return False
                    cardtype= 'row5'
                    return cardtype
            elif cardnum >5:
                for index in cardnum-1:
                        if abs(int(cards[index][0:2])-int(cards[index+1][0:2]))!=1:
                            return False
                cardtype= 'row'+str(cardnum)
                return cardtype
            else:
                return False
        
            
            
    def linkPlayers(self, playerlist):
        playerlist[0].next = playerlist[1]
        playerlist[1].next = playerlist[2]
        playerlist[2].next = playerlist[0]
        
        
    def randomPickcards(self):
        cards = random.choice(self.allcards)
        self.allcards.remove(cards)
        return cards
    
    def playercardsstore(self, player,cards):
        player.handcards.append(cards)
    
    def dealcard(self):
        while len(self.allcards) != 0:
            for player in self.playerlist:
                cards = self.randomPickcards()
                self.playercardsstore(player, cards)
  
  
class Player(object):
    def __init__(self, sock, name):
        self.sock = sock
        self.name = name
        self.handcards=[]
        self.next = None
        
    def playcard(self,cardlist):
        for card in cardlist:
            if card not in self.handcards:
                return False
        for card in cardlist:
            self.handcards.remove(card)
        return True
        
        
class CustomerCommu(object):
    def __init__(self,servsock,readlist,writelist):
        self.readlist = readlist
        self.writelist = writelist
        self.servsock =servsock
 
 
    def doselectmodule(self):
        while True:
            (readable, writable, exceptional) = select.select(self.readlist, [], [])
            for soc in readable:
                if soc == self.servsock:
                    newsock, (remhost, remport) = soc.accept()
                    self.readlist.append( newsock )
                    self.writelist.append( newsock )
                    self.sendSolveddata('playernum ' + str(len(self.writelist)))
                    if len(self.writelist) == 3:
                        time.sleep(5)
                        name = 'A'
                        playerlist=[]
                        for gamesoc in self.writelist:
                            try:
                                gamesoc.send('gamestart '+ name)
                                playerlist.append(Player(gamesoc, name))
                                name = chr(ord(name)+1)
                            except:
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
                    
                else:
                    try:
                        recvdata = soc.recv(1024)
                        senddata = recvdata
                        self.sendSolveddata(senddata)
                    except:
                        soc.close
                        self.readlist.remove(soc)
                        self.writelist.remove(soc)
    
    def sendSolveddata(self,senddata):
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


