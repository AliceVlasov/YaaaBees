from tkinter import *
from PIL import ImageTk, Image
from time import sleep
from Air import Pump
from Cube_Controller import Cube_Controller

class Window(Frame):
    inflate = False
    deflate = False
    valuelist = []

    def __init__(self, master=None):
        # Setup controller for hardware
        self.controller = Cube_Controller(self.gui_safety_stop)
        self.isSafetyOn = True
        self.pouch_name = "cube"
        self.selected = IntVar()
        self.size = 0
        self.pouches = {
            0: "cube",
            1: "left_leg",
            2: "left_thigh",
        }

        shift = 0
        xshift = shift
        yshift = shift

        # Window settings 
        Frame.__init__(self, master)     
        self.master = master
        self.master.wm_title("User Interface")
        #self.master.attributes("-fullscreen", True) # Uncomment to make it fullscreen.
        self.master.geometry("800x480") # Uncomment to test it in the dimensions of the R.Pi dimensions. 
        self.master.resizable(False, False)

        # Background image of the body. 
        img = ImageTk.PhotoImage(Image.open("media/cube.png"))
        #logo = ImageTk.PhotoImage(Image.open("media/logo.png"))
        lab = Label(self.master, image=img)
        #log = Label(self.master, image=logo)
        #log.place(x=100, y=40)
        lab.place(x=0+xshift, y=-45+yshift, relwidth=1, relheight=1)

        # Widget can take all window
        self.pack(fill=BOTH, expand=1)

        text = Text(self.master, height=8, width=30, font=('Verdana', 10))
        text.insert(INSERT, self.pouch_name + " selected")
        text.place(x=280+xshift, y=320+yshift)

        self.text = text

        # Create the inflate/deflate buttons.
        activateButton = Button(self.master, text="Activate", command=self.activatePump, bg="firebrick", fg="white")
        resetButton = Button(self.master, text="Reset", command=self.resetPouch, bg="firebrick", fg="white")
        inflateButton = Button(self.master, text="Inflate", command=self.setInflate, bg="navy", fg="white")
        deflateButton = Button(self.master, text="Deflate", command=self.setDeflate, bg="navy", fg="white")

        # Create the pouch selection buttons. 
        # left_leg = Radiobutton(self.master, text="left_leg", variable=self.selected, value=1, command=self.setSelection)
        # left_thigh = Radiobutton(self.master, text="left_thigh", variable=self.selected, value=2, command=self.setSelection)
    
        gscale = Scale(self.master, cursor="dot", from_=self.controller.get_pouch_size_range()[0], to=self.controller.get_pouch_size_range()[1], orient=HORIZONTAL, command=self.valuecheck)
        self.scale = gscale
        self.size = gscale.get()

        # Place all the buttons. 
        activateButton.place(x=135+xshift, y=160+yshift, height=60, width=60)
        resetButton.place(x=205+xshift, y=160+yshift, height=60, width=60)
        inflateButton.place(x=535+xshift, y=160+yshift, height=60, width=60)
        deflateButton.place(x=605+xshift, y=160+yshift, height=60, width=60)

        self.activateButton = activateButton
        self.resetButton = resetButton
        self.inflateButton = inflateButton
        self.deflateButton = deflateButton

        gscale.place(x=135+xshift, y=100+yshift, height=40, width=140)

        self.master.mainloop()

    # Value check for the stepped slider functionality. 
    def valuecheck(self, value: int):
        #newvalue = min(self.valuelist, key=lambda x:abs(x-float(value)))
        self.size = value

    def write(self, input: str):
        self.text.delete('1.0', END)
        self.text.insert(INSERT, input)

    # Brings the pouch to a given size. 
    def activatePump(self):
        # Ensure that we aren't deflating already.
        print("__SIGNAL RECEIVED")
        pouch_size = self.size
        self.write("Cube size set to {0}".format(pouch_size))

        self.disableAll() # self.disableButton(self.activateButton)
        self.controller.inflate_to_size(int(pouch_size))
        self.enableAll() # self.enableButton(self.activateButton, self.activateButton["bg"], self.activateButton["bg"])

    # Deflates the pouch.
    def resetPouch(self):
        self.write("Resetting")
        self.disableAll() # self.disableButton(self.resetButton)
        self.controller.reset_pouch()
        self.enableAll() # self.enableButton(self.resetButton, self.activateButton["bg"], self.activateButton["bg"])
        self.write("Reset to initial size")
        # Inflates the pouch. 
    def setInflate(self):
        # Ensure that we aren't deflating already.
        print(self.size)
        if (not self.deflate):                
            self.inflate = not self.inflate
            print("Inflating: " + str(self.inflate))

            if self.inflate:
                self.disableButton(self.activateButton)
                self.disableButton(self.resetButton)
                self.disableButton(self.deflateButton)
                self.write("Inflating")
                self.controller.start_inflate(self.isSafetyOn)
            else:
                self.enableButton(self.activateButton, "firebrick", "white")
                self.enableButton(self.resetButton, "firebrick", "white")
                self.enableButton(self.deflateButton, "navy", "white")
                self.write("Stopped inflating")
                self.controller.stop_inflate(self.isSafetyOn)
        else: 
            self.write("Cannot inflate and deflate at the same time.")

    # Deflates the pouch.
    def setDeflate(self):
        # Ensure that we aren't inflating already.
        if (not self.inflate):
            if (self.inflateButton["state"] == DISABLED):
                self.enableButton(self.inflateButton, "navy", "white")
            self.deflate = not self.deflate

            print("Deflating: " + str(self.deflate))

            if self.deflate:
                self.disableButton(self.activateButton)
                self.disableButton(self.resetButton)
                self.disableButton(self.inflateButton)
                self.write("Deflating")
                self.controller.start_deflate(self.isSafetyOn)
            else:
                self.enableButton(self.activateButton, "firebrick", "white")
                self.enableButton(self.resetButton, "firebrick", "white")
                self.enableButton(self.inflateButton, "navy", "white")
                self.write("Stopped deflating")
                self.controller.stop_deflate(self.isSafetyOn)
        else: 
            self.write("Cannot inflate and deflate at the same time.")

    def disableButton(self, button: Button):
        button.config(state=DISABLED, bg="#ffffff", fg="#000000")
        button.update()

    def enableButton(self, button: Button, color: str, text_color: str):
        button.update()
        button.config(state=NORMAL, bg=color, fg=text_color)

    def disableAll(self):
        self.disableButton(self.activateButton)
        self.disableButton(self.resetButton)
        self.disableButton(self.inflateButton)
        self.disableButton(self.deflateButton)

    def enableAll(self):
        self.enableButton(self.activateButton, "firebrick", "white")
        self.enableButton(self.resetButton, "firebrick", "white")
        self.enableButton(self.inflateButton, "navy", "white")
        self.enableButton(self.deflateButton, "navy", "white")

    def gui_safety_stop(self):
        self.enableAll()
        if (self.inflate):
            self.disableButton(self.inflateButton)
            self.inflate = False
            self.write("Maximum inflation capacity reached.")
        elif (self.deflate):
            self.disableButton(self.deflateButton)
            self.deflate = False
            self.write("Maximum deflation capacity reached.")

    def cleanup(self):
        """
            Make sure setup is neutralised before shutting down
        """
        self.controller.cleanup()