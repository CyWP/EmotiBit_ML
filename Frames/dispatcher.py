from tkinter import (filedialog,
                     Button,
                     Checkbutton,
                     Label,
                     Entry,
                     StringVar,
                     BooleanVar,
                     DoubleVar,
                     IntVar,
                     Scale,
                     Frame,
                     ttk)
from Utils.dispatcher import OSCRelay
from taskmanager import TaskManager
import asyncio
import traceback

class DispatcherFrame(Frame):
    
    def __init__(self, master, **kwargs):

        super().__init__(master, **kwargs)

        self.relay = OSCRelay()
        self.draw()

    def dispatch(self):
        try:
            task = asyncio.create_task(self.relay.dispatch(int(self.in_port.get())))
            TaskManager.register_task(task)  # Register the task with TaskManager
            self.msg_label.configure(text=f'Relaying OSC data from port {self.in_port.get()}')
            self.dispatch_button.configure(text='Stop', command=self.stop_dispatch, bg='#F7A6B6')
        except Exception as e:
            self.msg_label.configure(text=str(e), fg='#FF0000')
            print(traceback.format_exc())

    def stop_dispatch(self):
        try:
            task = asyncio.create_task(self.relay.stop_dispatch())
            TaskManager.register_task(task)  # Register the task with TaskManager
            self.msg_label.configure(text='Relay Stopped')
            self.dispatch_button.configure(text='Dispatch', command=self.dispatch, bg='#A6B6F7')
        except Exception as e:
            self.msg_label.configure(text=str(e), fg='#FF0000')
            print(traceback.format_exc())

    def add_client(self):
        try:
            self.relay.add_client(ip=self.out_ip.get(), port=int(self.out_port.get()))
        except Exception as e:
            self.msg_label.configure(text=e)
        self.draw()

    def remove_client(self, index):
        try:
            self.relay.remove_client(index)
        except Exception as e:
            self.msg_label.configure(text=e)
        self.draw()

    def draw(self):

        row = 0

        Label(self, text='    ', bg='#FFFFFF').grid(row=row, column=0)
        row+=1

        self.msg_label = Label(self, text='Relay EmotiBit messages to multiple endpoints.', bg='#FFFFFF', bd=2, relief='solid', fg='black', wraplength=450, padx=10, pady=10, width=64)
        self.msg_label.grid(row=row, column=1, columnspan=4, sticky='nesw')
        row+=1

        Label(self, text='    ', bg='#FFFFFF').grid(row=row, column=0)
        row+=1

        Label(self, text='In Port:', bg='#FFFFFF').grid(row=row, column=1, sticky='nsw')
        self.in_port = Entry(self, bd=1)
        self.in_port.grid(row=row, column=1, sticky='nes')
        self.in_port.insert(0, '12345')
        self.dispatch_button = Button(self, text='Dispatch', command=self.dispatch, bg='#A6B6F7', padx=10)
        self.dispatch_button.grid(row=row, column=2, columnspan=3, sticky='nesw')
        row+=1

        Label(self, text='    ', bg='#FFFFFF').grid(row=row, column=0)
        row+=1

        Label(self, text='Add Relay', bg='#FFFFFF').grid(row=row, column=1, columnspan=1, sticky='nesw')
        row+=1
        Label(self, text='Relayed IP:', bg='#FFFFFF').grid(row=row, column=1, sticky='nsw')
        self.out_ip = Entry(self, bd=1)
        self.out_ip.grid(row=row, column=1, columnspan=2, sticky='nes')
        Label(self, text='Port:', bg='#FFFFFF').grid(row=row, column=3, sticky='nsw')
        self.out_port = Entry(self, bd=1)
        self.out_port.grid(row=row, column=3, sticky='nes')
        Button(self, text='Add', command=self.add_client).grid(row=row, column=4, sticky='nesw')
        row+=1

        Label(self, text='    ', bg='#FFFFFF').grid(row=row, column=0)
        row+=1

        Label(self, text='Relay Addresses', bg='#FFFFFF').grid(row=row, column=1, columnspan=1, sticky='nesw')
        row+=1
        self.clientlist = Frame(self, background='#FFFFFF', relief='solid', borderwidth=2, height=40)
        self.clientlist.grid(row=row, column=1, columnspan=4, sticky='nesw', ipadx=2, ipady=2)
        Label(self.clientlist, text='', bg='#FFFFFF').grid(row=0, column=0, columnspan=2, sticky='nes')

        for i, client in enumerate(self.relay.get_clients()):
            Label(self.clientlist, text=f'Ip {client[0]} @ port {client[1]}', bg='#FFFFFF').grid(row=i//3+1, column=i%3*3, columnspan=2, sticky='nes')
            Button(self.clientlist, text='-', command=lambda index=i: self.remove_client(index)).grid(row=i//3+1, column=i%3*3+2, sticky='nes')