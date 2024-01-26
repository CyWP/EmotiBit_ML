#Just the UI stuff
from tkinter import (Tk, 
                     filedialog,
                     Button,
                     Checkbutton,
                     Label,
                     Entry,
                     StringVar,
                     BooleanVar,)
from csvutils import vectorize
import os

MAX_PATH_LENGTH = 45
NAME_ENTRY_DEFAULT = ''
LABEL_ENTRY_DEFAULT = ''

root = Tk()

source_path = StringVar(root, 'C:/')
dir_path = StringVar(root, 'C:/')
derive_data=BooleanVar(root, True)
rename_source = BooleanVar(root, False)

def browseRawFile():
    filename = ','.join(filedialog.askopenfilenames(initialdir = '/', title = 'Select File(s)', filetypes = (('csv files', '*.csv'),('all files', '*.*')))) 
    # Change label contents
    if len(filename)>MAX_PATH_LENGTH:
        raw_label.configure(text="..."+filename[-MAX_PATH_LENGTH:])
    else:
        raw_label.configure(text=filename)
    source_path.set(filename)

def browseTargetDirectory():
    dirname = filedialog.askdirectory(initialdir= '/', title = 'Select Directory')
    # Change label contents
    if len(dirname)>MAX_PATH_LENGTH:
        dir_label.configure(text="..."+dirname[-MAX_PATH_LENGTH:])
    else:
        dir_label.configure(text=dirname)
    dir_path.set(dirname)

def isValidFileName(filename):
    return not any(char in filename for char in ' \|/:*?"\'<>&%$@#()')

def validateInput():
    msg = ""
    if source_path.get()[-4:] != '.csv':
        msg += '\nSelected source file is not a .csv file.'
    if not os.path.isfile(source_path.get()):
        msg += '\nSelected source file cannot be found.'
    if not os.path.isdir(dir_path.get()):
        msg += '\nTarget directory is not a valid directory.'
    if not isValidFileName(name_entry.get()):
        msg += '\nInvalid file name.'
    try:
        first = int(first_entry.get())
        if first < 0:
            msg += '\nInvalid entry at Clip First: negative integer.'
    except:
        msg += '\nInvalid entry at Clip First: invalid integer.'
    try:
        last = int(last_entry.get())
        if last < 0:
            msg += '\nInvalid entry at Clip Last: negative integer.'
    except:
        msg += '\nInvalid entry at Clip Last: invalid integer.'
    if msg == "":
        return True
    msg_label.configure(text="Error:"+msg, fg='red')

def parseFiles():
    if validateInput():        
        msg = vectorize(source=source_path.get(),
                        dest=f'{dir_path.get()}/{name_entry.get()}.csv',
                        derive=derive_data.get(),
                        label=label_entry.get(),
                        cliphead=int(first_entry.get()),
                        cliptail=int(last_entry.get()))
        if msg == 'Success':
            msg_label.configure(text=msg, fg='green')
        else:
            msg_label.configure(text=msg, fg='red')

if __name__=='__main__':
        #Build Panel
    row = 1
    root.title('EmotiBit Data Vectorizer')
    root.minsize(520, 500)  # width, height
    root.maxsize(600, 600)
    root.geometry('500x160+25+25')  # width x height + x + y
    root.config(bg='#FFFFFF')

    Label(root, text='    ', bg='#FFFFFF').grid(row=row, column=0)
    row+=1

    msg_label = Label(root, text='Use this program to parse output from your EmotiBit into a vectorized one destined for machine learning.', bg='#FFFFFF', bd=2, relief='solid', fg='black', wraplength=450, padx=10, pady=10)
    msg_label.grid(row=row, column=1, columnspan=4, sticky='nesw')
    row+=1

    Label(root, text='    ', bg='#FFFFFF').grid(row=row, column=0)
    row+=1

    Button(root, text='Vectorize', command=parseFiles, bg='#A6B6F7').grid(row=row, column=1, columnspan=4, sticky='nesw')
    row+=1

    Checkbutton(root, text='Derive data', bg='#FFFFFF', command=root.setvar('derive_data', not(derive_data.get())), variable=derive_data).grid(row=row, column=1)
    Checkbutton(root, text='Rename Source', bg='#FFFFFF', command=root.setvar('rename_source', not(rename_source.get())), variable=rename_source).grid(row=row, column=3)
    row+=1

    Label(root, text='', bg='#FFFFFF').grid(row=row)
    row+=1

    Label(root, text='File to be parsed:', bg='#FFFFFF').grid(row=row, column=1)
    row+=1

    Button(root, text='Browse', command=browseRawFile).grid(row=row, column=4, sticky='nesw')
    raw_label = Label(root, text="/path/to/source/file", bg='#CCCCCC')
    raw_label.grid(row=row, column=1, columnspan=3, sticky='nesw')
    row+=1

    Label(root, text='', bg='#FFFFFF').grid(row=row)
    row+=1

    #Destination directory selector
    Label(root, text='Target directory:', bg='#FFFFFF').grid(row=row, column=1)
    row+=1

    Button(root, text='Browse', command=browseTargetDirectory).grid(row=row, column=4, sticky='nesw')
    dir_label = Label(root, text="/path/to/directory", bg='#CCCCCC')
    dir_label.grid(row=row, column=1, columnspan=3, sticky='nesw')
    row+=1

    Label(root, text='', bg='#FFFFFF').grid(row=row)
    row+=1

    Label(root, text='File name:', bg="#FFFFFF").grid(row=row, column=1, sticky='w')
    name_entry = Entry(root, bd=1)
    name_entry.grid(row=row, column=2, columnspan=3, sticky='nesw')
    name_entry.insert(0, NAME_ENTRY_DEFAULT)
    row+=1

    Label(root, text='Do not add extensions or spaces.', bg='#FFFFFF').grid(row=row, column=1, columnspan=4, sticky='w')
    row+=1

    Label(root, text='', bg='#FFFFFF').grid(row=row)
    row+=1

    Label(root, text='Label data:', bg='#FFFFFF').grid(row=row, column=1, sticky='w')
    label_entry = Entry(root, bd=1)
    label_entry.grid(row=row, column=2, columnspan=3, sticky='nesw')
    label_entry.insert(0, LABEL_ENTRY_DEFAULT)
    row+=1

    Label(root, text='(Optional) Enter a label name for data in the file.', bg='#FFFFFF').grid(row=row, column=1, columnspan=4, sticky='w')
    row+=1

    Label(root, text='', bg='#FFFFFF').grid(row=row)
    row+=1

    Label(root, text='Clip First', bg='#FFFFFF').grid(row=row, column=1)
    first_entry = Entry(root, bd=1)
    first_entry.grid(row=row, column=2)
    first_entry.insert(0, '0')
    Label(root, text='Clip Last', bg='#FFFFFF').grid(row=row, column=3)
    last_entry = Entry(root, bd=1)
    last_entry.grid(row=row, column=4)
    last_entry.insert(0, '0')
    row+=1

    Label(root, text='Clip the start and end of the parsed data.', bg='#FFFFFF').grid(row=row, column=1, columnspan=4, sticky='w')

    root.mainloop()