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

MAX_PATH_LENGTH = 45
NAME_ENTRY_DEFAULT = ''
LABEL_ENTRY_DEFAULT = ''

class VectorizerFrame(Frame):

    def __init__(self, master,**kwargs):
        super().__init__(master, **kwargs)

        self.source_path = StringVar(self, 'C:/')
        self.dir_path = StringVar(self, 'C:/')
        self.append_data = BooleanVar(self, True)
        self.note_labels = BooleanVar(self, False)
        self.test_split = DoubleVar(self)
        self.draw()

    def browseRawFile(self):
        filename = ','.join(filedialog.askopenfilenames(initialdir = '/', title = 'Select File(s)', filetypes = (('csv files', '*.csv'),('all files', '*.*')))) 
        # Change label contents
        if len(filename)>MAX_PATH_LENGTH:
            self.raw_label.configure(text="..."+filename[-MAX_PATH_LENGTH:])
        else:
            self.raw_label.configure(text=filename)
        self.source_path.set(filename)

    def browseTargetDirectory(self):
        dirname = filedialog.askdirectory(initialdir= '/', title = 'Select Directory')
        # Change label contents
        if len(dirname)>MAX_PATH_LENGTH:
            self.dir_label.configure(text="..."+dirname[-MAX_PATH_LENGTH:])
        else:
            self.dir_label.configure(text=dirname)
        self.dir_path.set(dirname)

    def isValidFileName(self, filename):
        return not any(char in filename for char in ' \|/:*?"\'<>&%$@#()')

    def validateInput(self):
        msg = ""
        if self.source_path.get()[-4:] != '.csv':
            msg += '\nSelected source file is not a .csv file.'
        if not os.path.isfile(self.source_path.get()):
            msg += '\nSelected source file cannot be found.'
        if not os.path.isdir(self.dir_path.get()):
            msg += '\nTarget directory is not a valid directory.'
        if not self.isValidFileName(self.name_entry.get()):
            msg += '\nInvalid file name.'
        try:
            first = int(self.first_entry.get())
            if first < 0:
                msg += f'\nInvalid entry at Clip First: negative integer. Entered {first}'
        except:
            msg += f'\nInvalid entry at Clip First: invalid integer. Entered {first}'
        try:
            last = int(self.last_entry.get())
            if last < 0:
                msg += f'\nInvalid entry at Clip Last: negative integer. Entered {last}'
        except:
            msg += f'\nInvalid entry at Clip Last: invalid integer. Entered {last}'
        if msg == "":
            return True
        self.msg_label.configure(text="Error:"+msg, fg='red')

    def parseFiles(self):
        if self.validateInput():        
            msg = vectorize(source=self.source_path.get(),
                            dest=self.dir_path.get(),
                            name=self.name_entry.get(),
                            label=self.label_entry.get(),
                            note_labels=self.note_labels.get(),
                            append_data=self.append_data.get(),
                            test_split=self.test_split.get()/100,
                            cliphead=int(self.first_entry.get()),
                            cliptail=int(self.last_entry.get()))
            if msg == 'Success':
                self.msg_label.configure(text=msg, fg='green')
            else:
                self.msg_label.configure(text=msg, fg='red')

    def draw(self):
            #Build Panel
        row = 1

        Label(self, text='    ', bg='#FFFFFF').grid(row=row, column=0)
        row+=1

        self.msg_label = Label(self, text='Parse data on your EmotiBit\'s SD card into vectorized data ready for ML.', bg='#FFFFFF', bd=2, relief='solid', fg='black', wraplength=450, padx=10, pady=10)
        self.msg_label.grid(row=row, column=1, columnspan=4, sticky='nesw')
        row+=1

        Label(self, text='    ', bg='#FFFFFF').grid(row=row, column=0)
        row+=1

        Button(self, text='Vectorize', command=self.parseFiles, bg='#A6B6F7').grid(row=row, column=1, columnspan=4, sticky='nesw')
        row+=1

        Label(self, text='', bg='#FFFFFF').grid(row=row)
        row+=1

        Label(self, text='File to be parsed:', bg='#FFFFFF').grid(row=row, column=1)
        row+=1

        Button(self, text='Browse', command=self.browseRawFile).grid(row=row, column=4, sticky='nesw')
        self.raw_label = Label(self, text="/path/to/source/file", bg='#CCCCCC')
        self.raw_label.grid(row=row, column=1, columnspan=3, sticky='nesw')
        row+=1

        Label(self, text='', bg='#FFFFFF').grid(row=row)
        row+=1

        #Destination directory selector
        Label(self, text='Target directory', bg='#FFFFFF').grid(row=row, column=1)
        row+=1

        Button(self, text='Browse', command=self.browseTargetDirectory).grid(row=row, column=4, sticky='nesw')
        self.dir_label = Label(self, text="/path/to/directory", bg='#CCCCCC')
        self.dir_label.grid(row=row, column=1, columnspan=3, sticky='nesw')
        row+=1

        Label(self, text='', bg='#FFFFFF').grid(row=row)
        row+=1

        Checkbutton(self, text='Use Notes as Labels', bg='#FFFFFF', command=self.setvar('self.note_labels', not(self.note_labels.get())), variable=self.note_labels).grid(row=row, column=3)
        row+=1

        Label(self, text='Test split (%):', bg='#FFFFFF').grid(row=row, column=1, sticky='sw')
        self.split_scale = Scale(self, variable=self.test_split, from_=0, to_=100, orient='horizontal', background='white')
        self.split_scale.grid(row=row, column=2, columnspan=3, sticky='nesw')
        row+=1

        Label(self, text='', bg='#FFFFFF').grid(row=row)
        row+=1

        Label(self, text='Label:', bg='#FFFFFF').grid(row=row, column=1, sticky='w')
        self.label_entry = Entry(self, bd=1)
        self.label_entry.grid(row=row, column=2, columnspan=3, sticky='nesw')
        self.label_entry.insert(0, LABEL_ENTRY_DEFAULT)
        row+=1

        Label(self, text='Label data if not provided as note in raw file', bg='#FFFFFF').grid(row=row, column=1, columnspan=4, sticky='w')
        row+=1

        Label(self, text='', bg='#FFFFFF').grid(row=row)
        row+=1

        Label(self, text='Name:', bg="#FFFFFF").grid(row=row, column=1, sticky='w')
        self.name_entry = Entry(self, bd=1)
        self.name_entry.grid(row=row, column=2, columnspan=3, sticky='nesw')
        self.name_entry.insert(0, NAME_ENTRY_DEFAULT)
        row+=1

        Label(self, text='Name of the recording, uses timestamp if left empty.', bg='#FFFFFF').grid(row=row, column=1, columnspan=4, sticky='w')
        row+=1

        Label(self, text='', bg='#FFFFFF').grid(row=row)
        row+=1

        Label(self, text='Clip First', bg='#FFFFFF').grid(row=row, column=1)
        self.first_entry = Entry(self, bd=1)
        self.first_entry.grid(row=row, column=2)
        self.first_entry.insert(0, '0')
        Label(self, text='Clip Last', bg='#FFFFFF').grid(row=row, column=3)
        self.last_entry = Entry(self, bd=1)
        self.last_entry.grid(row=row, column=4)
        self.last_entry.insert(0, '0')
        row+=1

        Label(self, text='Clip the start and end of the parsed data.', bg='#FFFFFF').grid(row=row, column=1, columnspan=4, sticky='w')