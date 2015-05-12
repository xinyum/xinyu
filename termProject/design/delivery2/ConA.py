import threading
import tkMessageBox
from UItest import UI
from Tkinter import *
from clientclass import Client

class Connectbox(object):
    ip=''
    def __init__(self):
        self.width = 400
        self.height = 400
        self.timerFiredDelay=500
        self.players = 0
        self.queue = {}
    def loading(self):
        self.canvas.delete(ALL)
        self.canvas.create_rectangle(0,0,self.width, self.height,fill='orange')
        self.canvas.create_text(200,100,text='Please wait for other Players!')
        self.canvas.create_text(200,200,text='Already has %s Players!'%self.players)
        self.canvas.create_text(200,300,text='The Game will launch automatically when has 3 Players!')

    def Buttonpressed(self):
        Connectbox.ip=self.Input.get()
        try:
            self.client=Client('127.0.0.1',self.queue)
        except:
            tkMessageBox.showerror("Error", "Cannot connect %s: Server is not open"%Connectbox.ip)
            return
        self.loading()
        def timerFiredWrapper():
            if self.players < 3:
                players = self.queue.get('playernum',0)
                if players!=0:
                    self.players =int(players[0])
                else:
                    self.players=players
                self.loading()
                self.canvas.after(self.timerFiredDelay, timerFiredWrapper)
            else:
                self.root.destroy()       
        timerFiredWrapper()
        
    def run(self):
        self.root = Tk()
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.root.resizable(width=FALSE, height=FALSE)
        self.canvas.create_rectangle(0,0,self.width, self.height,fill='orange')
        self.b1 = Button(self.canvas, text="ConnectNow",command=self.Buttonpressed)
        self.canvas.create_window(200, 300, window=self.b1)
        self.Input=Entry(self.canvas)
        self.canvas.create_window(200, 200, window=self.Input)
        self.canvas.pack()
        self.root.mainloop()

star=Connectbox()
star.run()


