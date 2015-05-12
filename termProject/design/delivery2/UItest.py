import threading
from Tkinter import *
import ImageTk
import time
import tkMessageBox
class UI(threading.Thread):
    def __init__(self, width, height, sock, queue, name):
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
        
  
    def translater(self):
        self.text = self.queue.get("coordinate",'No Pressed yet')
        self.card = self.queue.get("dealcard", [])
    
    def gainImagelist(self):
        self.img=[]
        self.imglocation=[]
        if self.card !=[]:
            num = len(self.card)
            for index in xrange(num):
                filename = "cards/" + self.card[index] + ".jpg"
                self.img += [ImageTk.PhotoImage(file = filename)]
                self.imglocation += [(self.margin+index*15,self.margin+(index+1)*15,420,550)]
        else:
            self.imgcard=ImageTk.PhotoImage(file = 'cards/card.jpg')
                
        
    def drawhandcard(self):
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
    def mousePressed(self, event):
        self.selectcard(event.x,event.y)
        #senddata='coordinate '+str((event.x,event.y))
        #self.sendClientdata(senddata)
    def redrawAll(self):
        self.canvas.delete(ALL)
        self.canvas.create_rectangle(0,0,self.width, self.height,fill='cyan')
        self.canvas.create_text(self.width/2,self.height/2, text=self.text)
        self.drawhandcard()
        self.canvas.create_image(100,200,image = self.imgcard,anchor = SW)
        self.canvas.create_image(100,210,image = self.imgcard,anchor = SW)
        self.canvas.create_image(700,200,image = self.imgcard,anchor = SW)
        self.canvas.create_image(700,210,image = self.imgcard,anchor = SW)
        self.canvas.create_window(300, 400, window=self.playing)
        self.canvas.create_window(400, 400, window=self.passing)
        
    def run(self):
        root = Tk()
        self.canvas = Canvas(root, width=self.width, height=self.height)
        root.resizable(width=FALSE, height=FALSE)
        self.canvas.create_rectangle(0,0,self.width, self.height,fill='cyan')
        self.canvas.pack()
        self.playing = Button(self.canvas, text="playcard")
        self.passing = Button(self.canvas, text="Pass")
        def mousePressedWrapper(event):
            self.mousePressed(event)
        root.bind("<Button-1>", mousePressedWrapper)
        def timerFiredWrapper():
            self.translater()
            self.gainImagelist()
            self.redrawAll()
            self.canvas.after(self.timerFiredDelay, timerFiredWrapper)
        timerFiredWrapper()
        root.mainloop()
 