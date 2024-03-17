import tkinter as tk

# --- functions ---

def toggle_text():

    if btn['text'] == 'Show':
        btn['text']  = 'Hide'
        frame.grid(row=6, column=0, sticky='we')
    else:
        btn['text'] = 'Show'
        frame.grid_forget()

# --- main ---

root = tk.Tk()

some_list = ['A', 'B', 'C']

frame = tk.Frame(root)
frame.columnconfigure(0, weight=1) # resise column

for i, item in enumerate(some_list):
    b = tk.Button(frame, text=item)
    b.grid(row=i, column=0, sticky='we')

btn = tk.Button(root, text='Show', command=toggle_text)
btn.grid(row=5, column=0, sticky='w')

root.mainloop()