import threading
from Tkinter import *
import ImageTk
import time
import tkMessageBox


class UI(threading.Thread):
    def __init__(self, width, height, sock, queue, name, leftplayername, rightplayername):
        super(UI, self).__init__()
        self.width = width
        self.height = height
        self.sock = sock
        self.queue = queue
        self.margin = 200
        self.card =[]
        self.name = name
        self.timerFiredDelay = 500
        self.select=[]
        self.leftname = leftplayername
        self.rightname = rightplayername
        self.errotext = ''
 
    def translater(self):
        #translate the command and passing it into class variable
        self.card = self.queue.get("dealcard", [])
        self.turn = self.queue.get("turn",False)
        self.message = self.queue.get("errmessage", [])
        self.play = self.queue.get("mycardplay", [])
        self.leftplay = self.queue.get("leftcardplay", [])
        self.rightplay = self.queue.get("rightcardplay", [])
        self.myremain = self.queue.get("myremain", 18)
        self.rightremain = self.queue.get("rightremain", 18)
        self.leftremain = self.queue.get("leftremain", 18)
        self.winner = self.queue.get("win",None)
        self.roundover = self.queue.get("roundover",False)
    
    def gainImagelist(self):
        #get the image list for loading picture
        self.playimg = []
        self.leftimg = []
        self.rightimg = []
        self.img =[]
        self.imglocation=[]
        if self.card !=[]:
            for index in xrange(len(self.card)):
                try:
                    filename = "cards/" + self.card[index] + ".jpg"
                except:
                    return
                self.img += [ImageTk.PhotoImage(file = filename)]
                self.imglocation += [(self.margin+index*15,self.margin+(index+1)*15,420,550)]
        else:
            self.imgcard=ImageTk.PhotoImage(file = 'cards/card.jpg')
        if self.play != []:
            if self.play[0] == self.name:
                num = len(self.play)
                for index in xrange(1,num):
                    filename = "cards/" + self.play[index] + ".jpg"
                    self.playimg += [ImageTk.PhotoImage(file = filename)]
        if self.leftplay != []:
            if self.leftplay[0] == self.leftname:
                num = len(self.leftplay)
                for index in xrange(1,num):
                    filename = "cards/" + self.leftplay[index] + ".jpg"
                    self.leftimg += [ImageTk.PhotoImage(file = filename)]
        if self.rightplay != []:
            if self.rightplay[0] == self.rightname:
                num = len(self.rightplay)
                for index in xrange(1,num):
                    filename = "cards/" + self.rightplay[index] + ".jpg"
                    self.rightimg += [ImageTk.PhotoImage(file = filename)] 
            
        
    def drawhandcard(self):
        #draw the hand card
        if self.img!=[]:
            num = len(self.img)
            for index in xrange(num):
                if index not in self.select:
                    self.canvas.create_image(self.imglocation[index][0],
                        self.imglocation[index][3],image = self.img[index],anchor = SW)
                else:
                    self.canvas.create_image(self.imglocation[index][0],
                        self.imglocation[index][3]-15,image = self.img[index],anchor = SW)
        else:
            self.canvas.create_image(self.margin,550,image = self.imgcard,anchor = SW)
    
    def drawplaycard(self):
        # draw the played card according to who play card.
        if self.playimg!=[]:
            num = len(self.playimg)
            for index in xrange(num):
                    self.canvas.create_image(300+index*15,380,
                                             image = self.playimg[index],anchor = SW)
        if self.leftimg!=[]:
            num = len(self.leftimg)
            for index in xrange(num):
                    self.canvas.create_image(200+index*15,200,
                                             image = self.leftimg[index],anchor = SW)
        if self.rightimg!=[]:
            num = len(self.rightimg)
            for index in xrange(num):
                    self.canvas.create_image(650+index*15,200,
                                             image = self.rightimg[index],anchor = SE)
        
    def selectcard(self,ex,ey):
        for (x0,x1,y0,y1) in self.imglocation:
            if ex>x0 and ex<x1 and ey>y0 and ey<y1:
                index=self.imglocation.index((x0,x1,y0,y1))
                
                if index in self.select:
                    self.select.remove(index)
                else:    
                    self.select += [index]
                
    def sendClientdata(self,senddata):
        self.sock.send(senddata)
    
    def converter(self,cardlist):
        cl=sorted(cardlist)
        cardstr=''
        for card in cl:
            cardstr+=card+' '
        senddata='wantplay '+cardstr
        return senddata
    
    def ButtonPlayingPressed(self):
        if self.turn == [self.name]:
            cardlist=[]
            for index in self.select:
                cardlist+=[self.card[index]]
            senddata=self.converter(cardlist)
            self.sendClientdata(senddata)
            self.select = []
            self.message=[]
            self.queue['errmessage']=[]
            
            
    def ButtonPassingPressed(self):
        if self.turn == [self.name]:
            self.sendClientdata('wantplay ')
            self.queue['errmessage']=[]
            
                    
    def mousePressed(self, event):
        self.selectcard(event.x,event.y)
    
    def wingame(self):
        self.canvas.create_text(self.width/2,self.height/2,text="You Win! :)",fill='red',font=20)
        self.canvas.create_window(self.width/2,self.height/2+100, window=self.restart)
    def losegame(self ):
        self.canvas.create_text(self.width/2,self.height/2,text="You Lose :(",fill='green',font=20)
        self.canvas.create_window(self.width/2,self.height/2+100, window=self.restart)
    
    
    def ButtonExitPressed(self):
        sys.exit(0)
        
    def redrawAll(self):
        self.canvas.delete(ALL)
        self.canvas.create_rectangle(0,0,self.width, self.height,fill='cyan')
        self.canvas.create_text(580,400, text="Waiting for Dealing Cards.",anchor=SW)
        self.canvas.create_text(580,420, text="Then using Mouse to click the card to choose card.",anchor=SW)
        self.canvas.create_text(580,440, text="Press buttons to play card or pass in your turn",anchor=SW)
        self.canvas.create_text(580,460, text="Remember: 3<4<5<6<7<8<9<10<J<Q<K<A<2<JockerA<JockerB",anchor=SW)
        self.canvas.create_text(580,480, text="You can play single(A), one pair(AA),two adjacent pairs(3344)",anchor=SW)
        self.canvas.create_text(580,500, text="Straight(56789), bomb(6666) or fullhouse(44433).",anchor=SW)
        self.canvas.create_text(580,520, text="bomb is larger than any other cardtype. ",anchor=SW)
        if self.winner!=None:
            if self.winner==[self.name]:
                self.wingame()
            if self.winner!=[self.name]:
                self.losegame()
        else:
            if self.message != [] and self.turn == [self.name]:
                if self.message[0] == 'inipass':self.errotext = 'Cannot Pass Now, please pick a card!'
                if self.message[0] == 'wrongtype': self.errotext = "Wrong Card Type!! Please choose again!"
                if self.message[0] == 'illegal': self.errotext = 'Not greater enough!! Please choose again!'
                if self.message[0] == 'card_store_erro': self.errotext = 'card load erro'
                self.canvas.create_text(self.width/2+300,self.height/2, text=self.errotext,fill='orange', font=5)
            self.canvas.create_text(300,580, text='player'+self.name, fill= 'purple',font=5)
            self.canvas.create_text(150,250, text='player'+self.leftname,fill= 'red',font=5)
            self.canvas.create_text(750,250, text='player'+self.rightname,fill= 'green',font=5)
            self.drawhandcard()
            self.drawplaycard()
            self.canvas.create_image(100,200,image = self.imgcard,anchor = SW)
            self.canvas.create_image(100,210,image = self.imgcard,anchor = SW)
            self.canvas.create_image(800,200,image = self.imgcard,anchor = SE)
            self.canvas.create_image(800,210,image = self.imgcard,anchor = SE)
            self.canvas.create_text(600,580, text="remain cards:%d"%self.myremain,fill='purple',font=5)
            self.canvas.create_text(150,270, text="remain cards:%d"%self.leftremain,fill='red',font=5)
            self.canvas.create_text(750,270, text="remain cards:%d"%self.rightremain,fill='green',font=5)
            self.canvas.create_window(300, 400, window=self.playing)
            self.canvas.create_window(400, 400, window=self.passing)
            if self.turn == [self.name]:
                self.canvas.create_text(self.width/2,580, text="it's your turn!",font=5,fill='brown')
            if self.turn == [self.leftname]:
                self.canvas.create_text(150,300, text="it's player%s's turn!"%self.leftname,font=5,fill='brown')
            if self.turn == [self.rightname]:
                self.canvas.create_text(750,300, text="it's player%s's turn!"%self.rightname,font=5,fill='brown')
            
        
    def run(self):
        self.root = Tk()
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.root.resizable(width=FALSE, height=FALSE)
        self.canvas.create_rectangle(0,0,self.width, self.height,fill='cyan')
        self.canvas.create_text(580,380, text="Waiting for Dealing Cards.",anchor=SW)
        self.canvas.create_text(580,400, text="Then using Mouse to click the card to choose card.",anchor=SW)
        self.canvas.create_text(580,420, text="Press buttons to play card or pass in your turn",anchor=SW)
        self.canvas.create_text(580,460, text="Remember: 3<4<5<6<7<8<9<10<J<Q<K<A<2<JockerA<JockerB",anchor=SW)
        self.canvas.create_text(580,480, text="You can play single(A), one pair(AA),two adjacent pairs(3344)",anchor=SW)
        self.canvas.create_text(580,500, text="Straight(56789), bomb(6666) or fullhouse(44433).",anchor=SW)
        self.canvas.create_text(580,520, text="bomb is larger than any other cardtype. ",anchor=SW)
        self.canvas.pack()
        self.playing = Button(self.canvas, text="playcard", command=self.ButtonPlayingPressed)
        self.passing = Button(self.canvas, text="Pass",command=self.ButtonPassingPressed)
        self.restart = Button(self.canvas, text="Exit Game", command=self.ButtonExitPressed)
        def mousePressedWrapper(event):
            self.mousePressed(event)
        self.root.bind("<Button-1>", mousePressedWrapper)
        def timerFiredWrapper():
            self.translater()
            self.gainImagelist()
            self.redrawAll()
            self.canvas.after(self.timerFiredDelay, timerFiredWrapper)
        timerFiredWrapper()
        self.root.mainloop()

