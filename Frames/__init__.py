from .vectorizer import VectorizerFrame
from tkinter import ttk

def drawFrames(master: ttk.Notebook):
    vecframe = VectorizerFrame(master)
    vecframe.pack(fill='both', expand=True)
    master.add(vecframe, text='Vectorizer')