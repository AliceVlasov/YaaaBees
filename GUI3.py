from tkinter import *
from PIL import ImageTk, Image
from time import sleep
from Air import Pump
from Safe_Controller import Safe_Controller

class Window(Frame):
    inflate = False
    deflate = False

    def __init__(self, master=None):
        # Window settings 
        Frame.__init__(self, master)     
        self.master = master
        self.master.wm_title("User Interface")
        #self.master.attributes("-fullscreen", True) # Uncomment to make it fullscreen.
        self.master.geometry("800x480") # Uncomment to test it in the dimensions of the R.Pi dimensions. 
        self.master.resizable(False, False)

        # Setup controller for hardware
        self.controller = Safe_Controller()
        self.pouch_name = "left_thigh"
        self.selected = IntVar()
        self.slider = {
            "left_leg": self.controller.get_pouch_size_range("left_leg")[0],
            "left_thigh": self.controller.get_pouch_size_range("left_thigh")[0]
        }
        # For updating the selection labels' sizes.
        self.textvars = {
            "left_leg": StringVar(self.master, "left_leg: " + str(self.slider["left_leg"])), 
            "left_thigh": StringVar(self.master, "left_thigh: " + str(self.slider["left_thigh"])),
        }
        self.pouches = {
            1: "left_leg",
            2: "left_thigh",
        }

        shift = 0
        xshift = shift
        yshift = shift

        # Widget can take all window
        self.pack(fill=BOTH, expand=1)

        # Background image of the body. 
        img = ImageTk.PhotoImage(Image.open("media/body3.png"))
        lab = Label(self.master, image=img)
        lab.place(x=0+xshift, y=-40+yshift, relwidth=1, relheight=1)

        # Textbox 
        text = Text(self.master, height=2, width=30, font=('Verdana', 10))
        text.insert(INSERT, self.pouch_name + " selected")
        text.place(x=525+xshift, y=100+yshift)

        self.text = text

        # Create the inflate/deflate buttons.
        inflateButton = Button(self.master, text="Activate", command=self.activatePump, bg="firebrick", fg="white")
        deflateButton = Button(self.master, text="Reset", command=self.resetPouch, bg="firebrick", fg="white")

        # Create the pouch selection buttons. 
        left_leg = Radiobutton(self.master, textvariable=self.textvars["left_leg"], variable=self.selected, value=1, command=self.setSelection)
        left_thigh = Radiobutton(self.master, textvariable=self.textvars["left_thigh"], variable=self.selected, value=2, command=self.setSelection)
        
        # Set default selection to left_thigh
        self.selected.set(2)
    
        # Slider label
        slider_label = Label(self.master, text="circumference in cm")
        slider_label.place(x=495+xshift, y=378+yshift)

        # Slider 
        legal_min, legal_max = self.controller.get_pouch_size_range("left_thigh")
        gscale = Scale(self.master, cursor="dot", from_=legal_min, to=legal_max, orient=HORIZONTAL) #, command=self.valuecheck)
        self.scale = gscale
        self.slider[self.pouch_name] = gscale.get()
        gscale.place(x=500+xshift, y=400+yshift, height=40, width=100)

        # Place all the buttons. 
        inflateButton.place(x=340+xshift, y=400+yshift, height=60, width=60)
        deflateButton.place(x=400+xshift, y=400+yshift, height=60, width=60)
        left_leg.place(x=430+xshift, y=320+yshift)
        left_thigh.place(x=440+xshift, y=240+yshift)

        self.activateButton = inflateButton
        self.resetButton = deflateButton

        self.master.mainloop()

    # Writes the given input to the textbox. 
    def write(self, input: str):
        self.text.delete('1.0', END)
        self.text.insert(INSERT, input)

    # Selection of the pouch using Radiobuttons. 
    def setSelection(self):
        self.pouch_name = self.pouches[self.selected.get()]
        self.write(self.pouch_name + " selected")
        legal_min, legal_max = self.controller.get_pouch_size_range(self.pouch_name)
        self.scale["from"] = legal_min
        self.scale["to"] = legal_max
        # newvalues = []
        # for i in range(legal_min, legal_max):
        #     newvalues.append(i)
        # self.slider[self.pouch_name] = self.scale.get()
        self.scale.set(self.slider[self.pouch_name])

    # Brings the pouch to a given size. 
    def activatePump(self):
        # Ensure that we aren't deflating already.
        print("__SIGNAL RECEIVED")
        pouch_size = self.scale.get()
        self.write("{0} to size {1}".format(self.pouch_name, pouch_size))
        
        self.disableButton(self.activateButton)
        self.disableButton(self.resetButton)
        self.controller.inflate_pouch_to_size(self.pouch_name, int(pouch_size))
        self.enableButton(self.activateButton)
        self.enableButton(self.resetButton)

        self.slider[self.pouch_name] = pouch_size
        self.textvars[self.pouch_name].set(self.pouch_name + ": " + str(self.slider[self.pouch_name]))
        print(self.slider)

    # Deflates the pouch.
    def resetPouch(self):
        self.write("Resetting the pouch")
        self.disableButton(self.resetButton)
        self.disableButton(self.activateButton)
        self.controller.reset_pouch(self.pouch_name)
        self.enableButton(self.resetButton)
        self.enableButton(self.activateButton)

        self.scale.set(self.scale["from"])
        self.slider[self.pouch_name] = int(self.scale["from"])
        self.textvars[self.pouch_name].set(self.pouch_name + ": " + str(self.slider[self.pouch_name]))
        print(self.slider)

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