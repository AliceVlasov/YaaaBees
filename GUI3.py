try:
    from tkinter import *
except ImportError:
    from Tkinter import *
from PIL import ImageTk, Image
from time import sleep
from Air import Pump
from Safe_Controller import Safe_Controller

class Window(Frame):
    inflate = False
    deflate = False
    valuelist = [1, 2, 3, 4, 5, 6]

    def __init__(self, master=None):
        # Setup controller for hardware
        self.controller = Safe_Controller()
        self.pouch_name = "cube"
        self.selected = IntVar()
        self.slider = {
            "cube": 0,
            "left_leg": 1,
            "left_thigh": 1
        }
        self.pouches = {
            1: "left_leg",
            2: "left_thigh",
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
        img = ImageTk.PhotoImage(Image.open("media/body3.png"))
        logo = ImageTk.PhotoImage(Image.open("media/logo.png"))
        lab = Label(self.master, image=img)
        log = Label(self.master, image=logo)
        log.place(x=100, y=40)
        lab.place(x=0, y=-40, relwidth=1, relheight=1)

        text = Text(self.master, height=2, width=30, font=('Verdana', 10))
        text.insert(INSERT, self.pouch_name + " selected")
        text.place(x=525, y=100)

        self.text = text

        # Create the inflate/deflate buttons.
        inflateButton = Button(self.master, text="Activate", command=self.activatePump, bg="firebrick", fg="white")
        deflateButton = Button(self.master, text="Reset", command=self.resetPouch, bg="white", fg="black")
        #self.disableButton(deflateButton)

        # Create the pouch selection buttons. 
        left_leg = Radiobutton(self.master, text="left_leg", variable=self.selected, value=1, command=self.setSelection)
        left_thigh = Radiobutton(self.master, text="left_thigh", variable=self.selected, value=2, command=self.setSelection)
    
        gscale = Scale(self.master, cursor="dot", from_=1, to=6, orient=HORIZONTAL, command=self.valuecheck)
        self.scale = gscale
        self.slider[self.pouch_name] = gscale.get()

        # Place all the buttons. 
        inflateButton.place(x=340, y=400, height=60, width=60)
        deflateButton.place(x=400, y=400, height=60, width=60)
        left_leg.place(x=430, y=320)
        left_thigh.place(x=440, y=240)

        self.activateButton = inflateButton
        self.resetButton = deflateButton

        gscale.place(x=500, y=400, height=40, width=100)

        self.master.mainloop()

    # Value check for the stepped slider functionality. 
    def valuecheck(self, value: int):
        newvalue = min(self.valuelist, key=lambda x:abs(x-float(value)))
        self.slider[self.pouch_name] = newvalue

    def write(self, input: str):
        self.text.delete('1.0', END)
        self.text.insert(INSERT, input)

    # Selection of the pouch using Radiobuttons. 
    def setSelection(self):
        self.pouch_name = self.pouches[self.selected.get()]
        self.slider[self.pouch_name] = self.scale.get()
        self.write(self.pouch_name + " selected")
        legal_min, legal_max = self.controller.get_pouch_size_range(self.pouch_name)
        self.scale["from"] = legal_min
        self.scale["to"] = legal_max

    # Brings the pouch to a given size. 
    def activatePump(self):
        # Ensure that we aren't deflating already.
        print("__SIGNAL RECEIVED")
        pouch_size = self.slider[self.pouch_name]
        self.write("{0} to size {1}".format(self.pouch_name, pouch_size))
        self.disableButton(self.activateButton)
        self.controller.inflate_pouch_to_size(self.pouch_name, pouch_size)
        #self.activateButton.update()
        self.enableButton(self.activateButton)

    # Deflates the pouch.
    def resetPouch(self):
        # Ensure that we aren't inflating already.
        self.controller.reset_pouch(self.pouch_name) 
    
    def disableButton(self, button: Button):
        button.config(state=DISABLED, bg="#ffffff", fg="#000000")
        button.update()

    def enableButton(self, button: Button):
        button.update()
        button.config(state=NORMAL, bg="firebrick", fg="white")

    def cleanup(self):
        """
            Make sure setup is neutralised before shutting down
        """
        self.controller.cleanup()