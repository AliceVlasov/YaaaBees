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
            "left_leg": 1,
            "left_thigh": 1
        }
        self.pouches = {
            0: "cube",
            1: "left_leg",
            2: "left_thigh",
            3: "thick_sleeve",
            4: "cylinder_sleeve",
            5: "thiccc_thigh"
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

        # Create the inflate/deflate buttons.
        inflateButton = Button(self.master, text="Inflate", command=self.setInflate, bg="firebrick", fg="white")
        deflateButton = Button(self.master, text="Deflate", command=self.setDeflate, bg="firebrick", fg="white")
        self.disableButton(deflateButton)

        # Create the pouch selection buttons. 
        cube = Radiobutton(self.master, text="cube", variable=self.selected, value=0, command=self.setSelection)
        left_leg = Radiobutton(self.master, text="left_leg", variable=self.selected, value=1, command=self.setSelection)
        left_thigh = Radiobutton(self.master, text="left_thigh", variable=self.selected, value=2, command=self.setSelection)
        thick_sleeve = Radiobutton(self.master, text="thick_sleeve", variable=self.selected, value=3, command=self.setSelection)
        cylinder_sleeve = Radiobutton(self.master, text="cylinder_sleeve", variable=self.selected, value=4, command=self.setSelection)
        #thiccc_thigh = Radiobutton(self.master, text="thiccc_thigh", variable=self.selected, value=5, command=self.setSelection)
        reset = Radiobutton(self.master, text="reset (still the thigh)", variable=self.selected, value=5, command=self.setSelection)
        
        gscale = Scale(self.master, cursor="dot", from_=1, to=6, orient=HORIZONTAL, command=self.valuecheck)
        self.scale = gscale
        self.slider[self.pouch_name] = gscale.get()

        text = Text(self.master, height=2, width=30, font=('Verdana', 10))
        text.insert(INSERT, self.pouch_name + " selected")
        text.place(x=525, y=100)

        self.text = text

        # Place all the buttons. 
        inflateButton.place(x=340, y=400, height=60, width=60)
        deflateButton.place(x=400, y=400, height=60, width=60)
        cube.place(x=480, y=380)
        left_leg.place(x=430, y=320)
        left_thigh.place(x=440, y=240)
        thick_sleeve.place(x=480, y=400)
        cylinder_sleeve.place(x=480, y=420)
        reset.place(x=480, y=440)

        gscale.place(x=500, y=305, height=40, width=100)

        self.master.mainloop()

    # Value check for the stepped slider functionality. 
    def valuecheck(self, value):
        newvalue = min(self.valuelist, key=lambda x:abs(x-float(value)))
        self.slider[self.pouch_name] = newvalue

    # Selection of the pouch using Radiobuttons. 
    def setSelection(self):
        self.pouch_name = self.pouches[self.selected.get()]
        self.slider[self.pouch_name] = self.scale.get()
        print(self.pouch_name)
        self.text.delete('1.0', END)
        self.text.insert(INSERT, self.pouch_name + " selected")

    def disableButton(self, button: Button):
        button["state"] = DISABLED
        button["bg"] = "#ffffff"
        button["fg"] = "#000000"

    # Inflates the pouch. 
    def setInflate(self):
        # Ensure that we aren't deflating already.
        print(self.slider)
        assert (not self.deflate)

        if not self.inflate:
            success = self.controller.inflate_pouch(self.pouch_name)
        else:
            success = self.controller.stop_inflate()
        
        if success:
            self.inflate = not self.inflate

    # Deflates the pouch.
    def setDeflate(self):
        # Ensure that we aren't inflating already.
        assert (not self.inflate)

        if not self.deflate:
            success = self.controller.deflate_pouch(self.pouch_name)
        else:
            success = self.controller.stop_deflate()
        
        if success:
            self.deflate = not self.deflate
    
    def safetyStop(self):
        #TODO for enes: here we can trigger a popup to display for a few seconds saying something like "pouch inflated/deflated to maximum", depending on whether inflate is true or false
        if self.inflate:
            self.inflate = not self.inflate
        elif self.deflate:
            self.deflate = not self.deflate
        else:
            print("Error: safety stop triggered when no pouch is inflating or deflating!")
    
    def cleanup(self):
        """
            Make sure setup is neutralised before shutting down
        """
        self.controller.cleanup()