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
from Utils.writer import OSCSV
from taskmanager import TaskManager
import asyncio
import traceback

MAX_PATH_LENGTH = 45

class WriterFrame(Frame):
    
    def __init__(self, master, **kwargs):

        super().__init__(master, **kwargs)
        self.writer = OSCSV()
        self.dir_path = StringVar(self, 'C:/')
        self.draw()

    def write(self):
        try:
            task = asyncio.create_task(self.writer.write(dest=self.dir_path.get(),
                                                         name=self.active_cls.get(),
                                                         preset=self.data_preset.get(),
                                                         port=int(self.in_port.get()),
                                                         frequency=int(self.frequency.get())))
            TaskManager.register_task(task)  # Register the task with TaskManager
            self.msg_label.configure(text=f'Writing OSC data from port {self.in_port.get()}')
            self.write_button.configure(text='Stop', command=self.stop_writing, bg='#F7A6B6')
        except Exception as e:
            self.msg_label.configure(text=str(e), fg='#FF0000')
            print(traceback.format_exc())

    def stop_writing(self):
        try:
            task = asyncio.create_task(self.writer.stop_writing())
            TaskManager.register_task(task)  # Register the task with TaskManager
            self.msg_label.configure(text='Writer Stopped')
            self.write_button.configure(text='Write to Class', command=self.write, bg='#A6B6F7')
        except Exception as e:
            self.msg_label.configure(text=str(e), fg='#FF0000')
            print(traceback.format_exc())

    def browseTargetDirectory(self):
        dirname = filedialog.askdirectory(initialdir= '/', title = 'Select Directory')
        # Change label contents
        if len(dirname)>MAX_PATH_LENGTH:
            self.dir_label.configure(text="..."+dirname[-MAX_PATH_LENGTH:])
        else:
            self.dir_label.configure(text=dirname)
        self.dir_path.set(dirname)

    def add_class(self):
        try:
            self.writer.add_class(self.name_entry.get())
        except Exception as e:
            self.msg_label.configure(text=e)
        self.draw()

    def remove_class(self, index):
        try:
            self.writer.remove_class(index)
        except Exception as e:
            self.msg_label.configure(text=e)
        self.draw()

    def draw(self):

        row = 0

        Label(self, text='    ', bg='#FFFFFF').grid(row=row, column=0)
        row+=1

        self.msg_label = Label(self, text='Record and classify live data.', bg='#FFFFFF', bd=2, relief='solid', fg='black', wraplength=450, padx=10, pady=10, width=64)
        self.msg_label.grid(row=row, column=1, columnspan=4, sticky='nesw')
        row+=1

        Label(self, text='    ', bg='#FFFFFF').grid(row=row, column=0)
        row+=1

        self.write_button = Button(self, text='Write to Class', command=self.write, bg='#A6B6F7', padx=10)
        self.write_button.grid(row=row, column=1, columnspan=4, sticky='nesw')
        row+=1

        Label(self, text='Class', bg='#ffffff').grid(row=row, column=1)
        self.active_cls = ttk.Combobox(self, values=self.writer.get_classes(), state='readonly')
        self.active_cls.grid(row=row, column=2, sticky='nesw')

        Label(self, text='Use Data:', bg='#FFFFFF').grid(row=row, column=3, sticky='nesw')
        self.data_preset = ttk.Combobox(self, values=OSCSV.get_presets(), state='readonly')
        self.data_preset.grid(row=row, column=4, sticky='nesw')
        self.data_preset.current(0)
        row+=1

        Label(self, text='In Port:', bg='#FFFFFF').grid(row=row, column=1, sticky='nesw')
        self.in_port = Entry(self, bd=1)
        self.in_port.grid(row=row, column=2, sticky='nesw')
        self.in_port.insert(0, '12345')

        Label(self, text='Max Freq:', bg='#FFFFFF').grid(row=row, column=3, sticky='nesw')
        self.frequency = Entry(self, bd=1)
        self.frequency.grid(row=row, column=4, sticky='nesw')
        self.frequency.insert(0, '30')
        row+=1

        Label(self, text='    ', bg='#FFFFFF').grid(row=row, column=0)
        row+=1

        #Destination directory selector
        Label(self, text='Target directory', bg='#FFFFFF').grid(row=row, column=1)
        row+=1

        Button(self, text='Browse', command=self.browseTargetDirectory).grid(row=row, column=4, sticky='nesw')
        self.dir_label = Label(self, text="/path/to/directory", bg='#CCCCCC')
        self.dir_label.grid(row=row, column=1, columnspan=3, sticky='nesw')
        row+=1

        Label(self, text='    ', bg='#FFFFFF').grid(row=row, column=0)
        row+=1

        self.name_entry = Entry(self, bd=1)
        self.name_entry.grid(row=row, column=1, columnspan=3, sticky='nesw')
        Button(self, text='Add Class', command=self.add_class).grid(row=row, column=4, columnspan=1, sticky='nesw')
        row += 1

        Label(self, text='    ', bg='#FFFFFF').grid(row=row, column=0)
        row+=1

        Label(self, text='Classes', bg='#FFFFFF').grid(row=row, column=1, sticky='w')
        row+=1

        self.rowconfigure(index=(row, row+1), weight=0)
        self.rowconfigure(index=row+2, weight=1)
        cls_frame = Frame(self, background='#FFFFFF', relief='solid', borderwidth=2, height=40)
        cls_frame.grid(row=row, rowspan=3, column=1, columnspan=4, sticky='nesw')
        cls_frame.columnconfigure(index=(0, 1, 2, 3, 4, 5), weight=1)
        for i, cls in enumerate(self.writer.get_classes()):
            Button(cls_frame, text='-', command=lambda index=i: self.remove_class(index)).grid(row=i//2, column=(i%2)*3)
            Label(cls_frame, text=cls).grid(row=i//2, column=(i%2)*3+1, columnspan=2)