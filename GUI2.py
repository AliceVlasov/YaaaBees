try:
    from tkinter import *
except ImportError:
    from Tkinter import *
from PIL import ImageTk, Image
from time import sleep
from Air import Pump
from Controller import Controller

class Window(Frame):
    inflate = False
    deflate = False
    valuelist = [50, 75, 100, 125, 150, 175, 200]

    def __init__(self, master=None):
        #setup controller for hardware
        self.controller = Controller()
        self.pouch_name = "cube"
        
        Frame.__init__(self, master)     
        self.master = master
        self.master.wm_title("Tkinter button")
        #self.master.attributes("-fullscreen", True)
        self.master.geometry("800x480")
        self.master.resizable(False, False)

        # widget can take all window
        self.pack(fill=BOTH, expand=1)

        img= ImageTk.PhotoImage(Image.open("media/body.png"))
        lab = Label(self.master, image=img)
        lab.pack()
        lab.place(x=0, y=0, relwidth=1, relheight=1)

        # create the button and the scale, link it to clickExitButton()
        inflateButton = Button(self.master, text="Inflate", command=self.setInflate, bg="firebrick", fg="white")
        deflateButton = Button(self.master, text="Deflate", command=self.setDeflate, bg="firebrick", fg="white")
        scale = Scale(self.master, cursor="dot", from_=50, to=200, orient=HORIZONTAL, command=self.valuecheck, tickinterval=50)
        self.slider = scale

        inflateButton.place(x=440, y=340, height=60, width=60)
        deflateButton.place(x=500, y=340, height=60, width=60)
        scale.place(x=350, y=260, height=75, width=160)
        print("wadsd")
        self.master.mainloop()

    def valuecheck(self, value):
        newvalue = min(self.valuelist, key=lambda x:abs(x-float(value)))
        self.slider.set(newvalue)

    def clickExitButton(self):
        exit()

    def setInflate(self):
        assert (not self.deflate)
        self.inflate = not self.inflate
        print("Inflating: " + str(self.inflate))

        if self.inflate:
            self.controller.inflate_pouch(self.pouch_name)
        else:
            self.controller.stop_inflate()

    def setDeflate(self):
        assert (not self.inflate)
        self.deflate = not self.deflate

        print("Deflating: " + str(self.inflate))

        if self.deflate:
            self.controller.deflate_pouch(self.pouch_name)
        else:
            self.controller.stop_deflate()
    
    def cleanup(self):
        """
            Make sure setup is neutralised before shutting down
        """
        self.controller.cleanup()