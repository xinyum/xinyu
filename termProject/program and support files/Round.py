class Round(object):
    #this class is the function determine each round if player's move is legal
    num = 0
    roundstore = [] 
    def __init__(self, player, cardsPlayed):
        self.roundMax = cardsPlayed
        self.roundPass = 0
        self.roundMaxPlayer = player
        self.now = player
        self.turn = player.next
        self.roundover = False
        Round.num += 1
        Round.roundstore += [self]
        self.maxtype = self.cardtype(self.roundMax)
  
    def inicard(self):
        #determine if the initial player want to play legal card
        if self.maxtype == 'wrongtype' :
            return 'wrongtype'
        elif self.maxtype == 'pass':
            return 'inipass'
        else:
            if self.now.playcard(self.roundMax) == True:
                return 'Truthy'
            else:return 'cardstoreerro'
        
    def playcards(self, player, cardsPlayed):
        #determine if player want to play legal card
        cardtype = self.cardtype(cardsPlayed)
        if cardtype == 'pass':
            self.roundPass += 1
            player.pas = True
            if self.roundPass >= 2:
                self.roundover = True  
            return 'Truthy'
        if cardtype == 'wrongtype':
            return 'wrongtype'
        else:
            if self.islegal(cardtype,cardsPlayed) == True:
                if player.playcard(cardsPlayed) == True:
                    return 'Truthy'
                else:
                    return 'cardstoreerro'
            else:
                if self.islegal(cardtype,cardsPlayed) == 'wrongtype':
                    return 'wrongtype'
                else: return 'illegal'
    def checkGameover(self,player):
        if player.handcards == []:
            return True
        else:
            return False
                
    def shiftrun(self, cardsPlayed):
        if cardsPlayed != []:
            self.roundMax = cardsPlayed
            self.maxtype = self.cardtype(cardsPlayed)
            self.roundMaxPlayer = self.now
        self.now = self.turn
        self.turn = self.turn.next
        if(self.now.pas): self.shiftrun([])
            
            
    def islegal(self, cardtype, cardsPlayed):
        if cardtype == self.maxtype:
            if cardtype != 'fullhouse':
                if cardsPlayed[-1][0:2] <= self.roundMax[-1][0:2]:
                    return False
                else: return True
            else:
                if cardsPlayed[-1][0:2] <= self.roundMax[-1][0:2]:
                    return False
                else: return True
        else:
            if cardtype=='bomb':
                return True
            else: return 'wrongtype'
        
            
    def cardtype(self, cards):
        cardnum=len(cards)
        if cardnum == 0:
            return 'pass'
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
                for index in xrange(cardnum-1):
                    if abs(int(cards[index][0:2])-int(cards[index+1][0:2]))!=1:
                        return 'wrongtype'
                cardtype= 'row5'
                return cardtype
        elif cardnum >5:
            for index in xrange(cardnum-1):
                if abs(int(cards[index][0:2])-int(cards[index+1][0:2]))!=1:
                    return 'wrongtype'
            cardtype= 'row'+str(cardnum)
            return cardtype
        else:
            return 'wrongtype'