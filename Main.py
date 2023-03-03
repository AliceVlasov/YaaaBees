try:
    from tkinter import *
except ImportError:
    from Tkinter import *
from GUI import Window

root = Tk()
app = Window(root)
root.wm_title("Tkinter button")
root.attributes("-fullscreen", True)
root.resizable(False, False)
root.mainloop()