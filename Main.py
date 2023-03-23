try:
    from tkinter import *
except ImportError:
    from Tkinter import *
from GUI3 import Window
from PIL import ImageTk, Image

root = Tk()

app = Window(root)
app.cleanup()