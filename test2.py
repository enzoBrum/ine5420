from tkinter import *

class MyList(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_propagate(False)

        self.canvas = Canvas(self)
        self.canvas.grid(row=0, column=0, sticky="news")

        self.scroll_bar = Scrollbar(self, orient=VERTICAL, command = self.canvas.yview)
        self.scroll_bar.grid(row=0, column=1, sticky='ns')
        self.canvas.config(yscrollcommand = self.scroll_bar.set)
        
        self.internal_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.internal_frame, anchor='nw')

        self.__build()
        self.internal_frame.update_idletasks()

        self.config(width=300,height=300)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def __build(self):
        for i in range(300): Label(self.internal_frame, text = "Olá Mundo! Pela %i vez..." % i).pack()

window = Tk()
my_list = MyList(window)

window.mainloop()