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
import webbrowser

class HomeFrame(Frame):

    def __init__(self, master,**kwargs):
        super().__init__(master, **kwargs)
        self.draw()

    def draw(self):
        self.image = ImageTk.PhotoImage(Image.open("./logo.png"))

        Button(self, text='Documentation', height=3, bg='#A6B6F7', command=self.open_docs).pack(side='top', fill='x', expand=True)
        self.photo = Label(self, image=self.image)
        self.photo.pack(side='top', fill='both', expand=True)

    def open_docs(self):
        webbrowser.open('https://github.com/CyWP/EmotiBit_ML')