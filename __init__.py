import tkinter as tk
from tkinter import ttk
from Frames import drawFrames

if __name__=="__main__":

    root = tk.Tk()

    root.title("EmotiBit ML Tools")
    root.iconbitmap('icon.ico')
    root.minsize(520, 560)  # width, height
    root.maxsize(600, 600)
    root.geometry('500x160+25+25')  # width x height + x + y
    root.config(bg='#FFFFFF')

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)
    drawFrames(notebook)

    root.mainloop()