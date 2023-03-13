try:
    from tkinter import *
except ImportError:
    from Tkinter import *
from PIL import ImageTk, Image
from time import sleep
from Air import Pump

class Window(Frame):
    inflate = False
    deflate = False
    pump = Pump(4, 100)
    depump = Pump(5,100)
    valuelist = [50, 75, 100, 125, 150, 175, 200]

    def __init__(self, master=None):
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
        self.speed = 100 #self.slider.get()
        print("Inflating: " + str(self.inflate))
        print("Speed: " + str(self.speed))

        if self.inflate:
            self.pump.runWithSpeed(self.speed)
        else:
            self.pump.stop()

    def setDeflate(self):
        assert (not self.inflate)
        self.deflate = not self.deflate
        self.speed = 100 #self.slider.get()

        print("Deflating: " + str(self.inflate))
        print("Speed: " + str(self.speed))

        if self.deflate:
            self.depump.runWithSpeed(self.speed)
        else:
            self.depump.stop()
