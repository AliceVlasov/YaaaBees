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
        # Setup controller for hardware
        self.controller = Controller()
        self.pouch_name = "cube"
        self.selected = IntVar()
        self.pouches = {
            0: "cube",
            1: "left_leg",
            2: "left_thight",
            3: "thick+sleeve",
            4: "cylinder_sleeve",
            5: "thiccc thigh"
        }
        
        # Window settings 
        Frame.__init__(self, master)     
        self.master = master
        self.master.wm_title("User Interface")
        #self.master.attributes("-fullscreen", True) # Uncomment to make it fullscreen.
        self.master.geometry("800x480") # Uncomment to test it in the dimensions of the R.Pi dimensions. 
        self.master.resizable(False, False)

        # Widget can take all window
        self.pack(fill=BOTH, expand=1)

        # Background image of the body. 
        img= ImageTk.PhotoImage(Image.open("media/body3.png"))
        lab = Label(self.master, image=img)
        lab.pack()
        lab.place(x=0, y=-40, relwidth=1, relheight=1)

        # Create the inflate/deflate buttons.
        inflateButton = Button(self.master, text="Inflate", command=self.setInflate, bg="firebrick", fg="white")
        deflateButton = Button(self.master, text="Deflate", command=self.setDeflate, bg="firebrick", fg="white")
        
        # Create the pouch selection buttons. 
        cube = Radiobutton(self.master, text="cube", variable=self.selected, value=0, command=self.setSelection)
        left_leg = Radiobutton(self.master, text="left_leg", variable=self.selected, value=1, command=self.setSelection)
        left_thigh = Radiobutton(self.master, text="left_thigh", variable=self.selected, value=2, command=self.setSelection)
        thick_sleeve = Radiobutton(self.master, text="thick_sleeve", variable=self.selected, value=3, command=self.setSelection)
        cylinder_sleeve = Radiobutton(self.master, text="cylinder_sleeve", variable=self.selected, value=4, command=self.setSelection)
        thiccc_thigh = Radiobutton(self.master, text="thiccc_thigh", variable=self.selected, value=5, command=self.setSelection)
        
        #scale = Scale(self.master, cursor="dot", from_=50, to=200, orient=HORIZONTAL, command=self.valuecheck, tickinterval=50)
        #self.slider = scale

        # Place all the buttons. 
        inflateButton.place(x=340, y=400, height=60, width=60)
        deflateButton.place(x=400, y=400, height=60, width=60)
        cube.place(x=480, y=380)
        left_leg.place(x=430, y=320)
        left_thigh.place(x=440, y=240)
        thick_sleeve.place(x=480, y=400)
        cylinder_sleeve.place(x=480, y=420)
        thiccc_thigh.place(x=480, y=440)
        #scale.place(x=350, y=260, height=75, width=160)

        self.master.mainloop()

    # Value check for the stepped slider functionality. 
    def valuecheck(self, value):
        newvalue = min(self.valuelist, key=lambda x:abs(x-float(value)))
        self.slider.set(newvalue)

    # Selection of the pouch using Radiobuttons. 
    def setSelection(self):
        self.pouch_name = self.pouches[self.selected.get()]
        print(self.pouch_name)

    # Inflates the pouch. 
    def setInflate(self):
        assert (not self.deflate)
        self.inflate = not self.inflate
        print("Inflating: " + str(self.inflate))

        if self.inflate:
            self.controller.inflate_pouch(self.pouch_name)
        else:
            self.controller.stop_inflate()

    # Deflates the pouch.
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