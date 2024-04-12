from .home import HomeFrame
from .vectorizer import VectorizerFrame
from .dispatcher import DispatcherFrame
from .writer import WriterFrame
from tkinter import ttk

def drawFrames(master: ttk.Notebook):

    homeframe = HomeFrame(master)
    homeframe.config(background='white')
    master.add(homeframe, text='Home')

    vecframe = VectorizerFrame(master)
    vecframe.config(background='white')
    master.add(vecframe, text='Vectorizer')

    disframe = DispatcherFrame(master)
    disframe.config(background='white')
    master.add(disframe, text='Dispatcher', sticky='nesw')

    wrtframe = WriterFrame(master)
    wrtframe.config(background='white')
    master.add(wrtframe, text='Writer', sticky='nesw')