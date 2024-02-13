#Just the UI stuff
from tkinter import (Tk, 
                     filedialog,
                     Button,
                     Checkbutton,
                     Label,
                     Entry,
                     StringVar,
                     BooleanVar,
                     ttk)
from Utils.vectorizer import vectorize
import os

MAX_PATH_LENGTH = 45
NAME_ENTRY_DEFAULT = ''
LABEL_ENTRY_DEFAULT = ''

class VectorizerFrame(ttk.Frame):

    def __init__(self, master, **kwargs):
        super().__init__()
        self.root = master
        root = self.root

        self.source_path = StringVar(root, 'C:/')
        self.dir_path = StringVar(root, 'C:/')
        self.derive_data=BooleanVar(root, True)
        self.note_labels = BooleanVar(root, False)

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
                            derive=self.derive_data.get(),
                            label=self.label_entry.get(),
                            note_labels=self.note_labels.get(),
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

        self.msg_label = Label(self, text='Use this program to parse output from your EmotiBit into a vectorized one destined for machine learning.', bg='#FFFFFF', bd=2, relief='solid', fg='black', wraplength=450, padx=10, pady=10)
        self.msg_label.grid(row=row, column=1, columnspan=4, sticky='nesw')
        row+=1

        Label(self, text='    ', bg='#FFFFFF').grid(row=row, column=0)
        row+=1

        Button(self, text='Vectorize', command=self.parseFiles, bg='#A6B6F7').grid(row=row, column=1, columnspan=4, sticky='nesw')
        row+=1

        Checkbutton(self, text='Derive data', bg='#FFFFFF', command=self.setvar('derive_data', not(self.derive_data.get())), variable=self.derive_data).grid(row=row, column=1)
        Checkbutton(self, text='Use Notes as Labels', bg='#FFFFFF', command=self.setvar('note_labels', not(self.note_labels.get())), variable=self.note_labels).grid(row=row, column=3)
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
        Label(self, text='Target directory:', bg='#FFFFFF').grid(row=row, column=1)
        row+=1

        Button(self, text='Browse', command=self.browseTargetDirectory).grid(row=row, column=4, sticky='nesw')
        self.dir_label = Label(self, text="/path/to/directory", bg='#CCCCCC')
        self.dir_label.grid(row=row, column=1, columnspan=3, sticky='nesw')
        row+=1

        Label(self, text='', bg='#FFFFFF').grid(row=row)
        row+=1

        Label(self, text='File name:', bg="#FFFFFF").grid(row=row, column=1, sticky='w')
        self.name_entry = Entry(self, bd=1)
        self.name_entry.grid(row=row, column=2, columnspan=3, sticky='nesw')
        self.name_entry.insert(0, NAME_ENTRY_DEFAULT)
        row+=1

        Label(self, text='Do not add extensions or spaces.', bg='#FFFFFF').grid(row=row, column=1, columnspan=4, sticky='w')
        row+=1

        Label(self, text='', bg='#FFFFFF').grid(row=row)
        row+=1

        Label(self, text='Label data:', bg='#FFFFFF').grid(row=row, column=1, sticky='w')
        self.label_entry = Entry(self, bd=1)
        self.label_entry.grid(row=row, column=2, columnspan=3, sticky='nesw')
        self.label_entry.insert(0, LABEL_ENTRY_DEFAULT)
        row+=1

        Label(self, text='(Optional) Enter a label name for data in the file.', bg='#FFFFFF').grid(row=row, column=1, columnspan=4, sticky='w')
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