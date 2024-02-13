#Just the UI stuff
from tkinter import (filedialog,
                     Button,
                     Checkbutton,
                     Label,
                     Entry,
                     StringVar,
                     BooleanVar,
                     DoubleVar,
                     Scale,
                     Frame,
                     ttk)
from Utils.vectorizer import vectorize
import os

class ListenerFrame(Frame):

    def __init__(self, master,**kwargs):
        super().__init__(master, **kwargs)