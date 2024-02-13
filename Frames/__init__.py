from .home import HomeFrame
from .vectorizer import VectorizerFrame
from .listener import ListenerFrame
from tkinter import ttk

def drawFrames(master: ttk.Notebook):

    homeframe = HomeFrame(master)
    homeframe.config(background='white')
    master.add(homeframe, text='Home')

    vecframe = VectorizerFrame(master)
    vecframe.config(background='white')
    master.add(vecframe, text='Vectorizer')

    lisframe = ListenerFrame(master)
    lisframe.config(background='white')
    master.add(lisframe, text='Listener')