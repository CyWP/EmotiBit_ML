#Just the UI stuff
from tkinter import (filedialog,
                     Button,
                     Checkbutton,
                     Label,
                     Entry,
                     StringVar,
                     IntVar,
                     BooleanVar,
                     DoubleVar,
                     Scale,
                     Frame,
                     ttk)
from Utils.listener import start_listening_server
import os

class ListenerFrame(Frame):

    def __init__(self, master,**kwargs):

        super().__init__(master, **kwargs)

        self.custom_port = BooleanVar(self, False)
        self.port = IntVar(self, 12345)
        self.period = DoubleVar(self, 0.1)

        self.draw()

    def draw(self):

        row = 1

        Label(self, text='    ', bg='#FFFFFF').grid(row=row, column=0)
        row+=1

