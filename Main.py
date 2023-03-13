try:
    from tkinter import *
except ImportError:
    from Tkinter import *
from GUI2 import Window
from PIL import ImageTk, Image

root = Tk()

app = Window(root)
app.cleanup()
#root.wm_title("Tkinter button")
#root.attributes("-fullscreen", True)
#root.resizable(False, False)
#root.mainloop()