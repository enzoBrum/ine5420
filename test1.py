import tkinter as tk


def callback():
    detail = {1}
    print("detail: %s" % detail)
    print(type(dict(detail)))


def create_custom_event():
    root.event_generate("<<Custom>>")


root = tk.Tk()

button = tk.Button(root, text="click me", command=create_custom_event)
button.pack(side="top", padx=20, pady=20)

cmd = root.register(callback)
root.tk.call("bind", root, "<<Custom>>", cmd + " %d")

root.mainloop()
