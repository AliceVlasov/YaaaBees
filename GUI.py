from tkinter import *
from time import sleep

class Window(Frame):
    inflate = False

    def __init__(self, master=None):
        Frame.__init__(self, master)     
        self.master = master
        

        # widget can take all window
        self.pack(fill=BOTH, expand=1)

        # create button, link it to clickExitButton()
        inflateButton = Button(self, text="Inflate", command=self.setInflate, bg="firebrick", fg="white")

        # place button at centre
        inflateButton.place(x=80, y=50, height=100, width=160)

    def clickExitButton(self):
        exit()

    def setInflate(self):
        self.inflate = not self.inflate
        print(self.inflate)

    def holdInflateButton(self):
        if self.inflate == True:
            print("asdwdc")