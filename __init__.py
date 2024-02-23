import tkinter as tk
from tkinter import ttk
from Frames import drawFrames
import asyncio
from taskmanager import TaskManager  # Import your task manager module

root = tk.Tk()

async def main():

    root.title("EmotiBit ML Tools")
    root.iconbitmap('icon.ico')
    root.minsize(520, 560)  # width, height
    root.maxsize(600, 600)
    root.geometry('500x160+25+25')  # width x height + x + y
    root.config(bg='#FFFFFF')
    root.protocol("WM_DELETE_WINDOW", on_closing)

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)
    drawFrames(notebook)
    
    TaskManager.register_task(asyncio.create_task(tkinter_mainloop(root)))

    try:
        await asyncio.gather(TaskManager.run_tasks())
    except KeyboardInterrupt:
        pass
    finally:
        await TaskManager.cancel_tasks()

def on_closing():
    root.destroy()  # Close the Tkinter window
    # Cancel all tasks managed by TaskManager
    asyncio.create_task(cancel_all_tasks())

async def cancel_all_tasks():
    await TaskManager.cancel_tasks()
    
async def tkinter_mainloop(root):
    while True:
        root.update()
        await asyncio.sleep(0.01)  # Adjust sleep time as needed

if __name__ == "__main__":
    asyncio.run(main())