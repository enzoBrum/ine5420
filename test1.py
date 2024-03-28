import tkinter as tk
import random

def click_handler(event):
    event.widget.itemconfigure("current", fill="white")

root = tk.Tk()
canvas = tk.Canvas(root, bg="bisque", width=400, height=400)
canvas.pack(fill="both", expand=True)

canvas.bind("<1>", click_handler)
for i in range(100):
    x = random.randint(0, 350)
    y = random.randint(0, 350)
    color = random.choice(("red", "orange", "green", "blue"))
    width = random.randint(25, 50)
    height = random.randint(25, 50)
    canvas.create_rectangle(x, y, x+width, y+height, fill=color)

root.mainloop()
