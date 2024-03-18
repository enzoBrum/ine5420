from tkinter import *
from tkinter import ttk




root = Tk()
root.title("Feet to Meters")
root.geometry("800x800")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

subframe = ttk.Frame(root, padding="3 3 12 12")

ttk.Label(mainframe, text="Showing Frame 1").grid(column=1, row=1)
ttk.Label(subframe, text="Showing Frame 2").grid(column=1, row=1)
ttk.Label(mainframe, text="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA").grid(column=2, row=1)
ttk.Label(subframe, text="BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB").grid(column=2, row=1)
def foo():
    mainframe.grid_forget()
    subframe.grid(column=0, row=0, sticky=(N,W,E,S))

def bar():
    subframe.grid_forget()
    mainframe.grid(column=0, row=0, sticky=(N,W,E,S))

ttk.Button(mainframe, text="Hide Frame 1", command=foo).grid(column=1, row=2)
ttk.Button(subframe, text="Hide Frame 2", command=bar).grid(column=1, row=2)

root.mainloop()
