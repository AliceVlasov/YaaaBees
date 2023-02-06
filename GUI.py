from Tkinter import *
from time import sleep
from Air import Pump

class Window(Frame):
    inflate = False
    pump = Pump(1, 50)

    def __init__(self, master=None):
        Frame.__init__(self, master)     
        self.master = master
        
        # widget can take all window
        self.pack(fill=BOTH, expand=1)

        # create button, link it to clickExitButton()
        inflateButton = Button(self, text="Inflate", command=self.setInflate, bg="firebrick", fg="white")
        w = Scale(self.master, from_=50, to=100, orient=HORIZONTAL)
        w.pack()
        self.slider = w

        # place button at centre
        inflateButton.place(x=80, y=50, height=100, width=160)

    def clickExitButton(self):
        exit()

    def setInflate(self):
        self.inflate = not self.inflate
        self.speed = self.slider.get()
        print("Inflating: " + str(self.inflate))
        print("Speed: " + str(self.speed))

        if self.inflate:
            self.pump.runWithSpeed(self.speed)
        else:
            self.pump.stop()

    def holdInflateButton(self):
        if self.inflate == True:
            print("asdwdc")
