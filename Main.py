from Tkinter import *
from GUI import Window

root = Tk()
app = Window(root)
root.wm_title("Tkinter button")
root.geometry("320x200")
root.resizable(False, False)
root.mainloop()