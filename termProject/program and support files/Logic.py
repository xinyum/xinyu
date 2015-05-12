import random
from Round import Round
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
        self.isgameover = False
        self.turn = random.choice(self.playerlist)
        
    def getPlayer(self,sock):
        for player in self.playerlist:
            if sock == player.sock:
                return player
    
    def checkroundover(self):
        if Round.num == 0:
            return False
        return Round.roundstore[Round.num-1].roundover

    def playdetermine(self, player, cardsPlayed):
        if Round.num == 0 or Round.roundstore[Round.num-1].roundover==True:
            roun=Round(player, cardsPlayed)
            if Round.roundstore[Round.num-1].inicard() != 'Truthy':
                if Round.roundstore[Round.num-1].inicard() == 'wrongtype': 
                    erromessage='errmessage '+'wrongtype'
                elif Round.roundstore[Round.num-1].inicard() == 'inipass':
                    erromessage='errmessage '+'inipass'
                elif Round.roundstore[Round.num-1].inicard() == 'cardstoreerro':
                    erromessage='errmessage '+'card_store_erro'
                Round.roundstore.pop(Round.num-1)
                Round.num -= 1
                return (erromessage, player) 
            else:
                if Round.roundstore[Round.num-1].checkGameover(player) == False:
                    for pl in self.playerlist:
                        pl.pas = False
                    Round.roundstore[Round.num-1].shiftrun(cardsPlayed)
                    self.turn = Round.roundstore[Round.num-1].now
                else:
                    self.isgameover = True
                return (cardsPlayed, 'all')
                    
        elif Round.roundstore[Round.num-1].roundover == False:
            if Round.roundstore[Round.num-1].playcards(player, cardsPlayed) != 'Truthy':
                if Round.roundstore[Round.num-1].playcards(player, cardsPlayed) == 'wrongtype':
                    erromessage = 'errmessage '+'wrongtype'
                elif Round.roundstore[Round.num-1].playcards(player, cardsPlayed) == 'illegal':
                    erromessage = 'errmessage '+'illegal'
                elif Round.roundstore[Round.num-1].playcards(player, cardsPlayed) == 'cardstoreerro':
                    erromessage='errmessage '+'card_store_erro'
                return (erromessage, player )
            else:
                if Round.roundstore[Round.num-1].checkGameover(player) == False:
                    Round.roundstore[Round.num-1].shiftrun(cardsPlayed)
                    self.turn = Round.roundstore[Round.num-1].now
                else:
                    self.isgameover = True
                return (cardsPlayed, 'all')
 
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
        self.pas = False
        self.name = name
        self.handcards=[]
        self.next = self
        
    def playcard(self,cardlist):
        for card in cardlist:
            if card not in self.handcards:
                return False
        for card in cardlist:
            self.handcards.remove(card)
        return True