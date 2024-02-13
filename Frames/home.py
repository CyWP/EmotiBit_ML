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
from PIL import Image, ImageTk
from Utils.vectorizer import vectorize
import os

class HomeFrame(Frame):

    def __init__(self, master,**kwargs):
        super().__init__(master, **kwargs)
        self.draw()

    def draw(self):
        self.image = ImageTk.PhotoImage(Image.open("./logo.png"))

        self.photo = Label(self, image=self.image)
        self.photo.pack(side='top', fill='both', expand=True)