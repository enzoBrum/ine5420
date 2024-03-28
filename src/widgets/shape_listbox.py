from tkinter import Event, ttk, Listbox, N, S, E, W
from typing import Callable
from interface import Window
from display_file import DisplayFile
from shape import Shape

from .add_object import AddObject

class ShapeListbox:
    root: ttk.Frame
    listbox: Listbox
    display_file: DisplayFile
    redraw_viewport_callback: Callable[[], None]
    selected_shape: Shape | None
    selected_shape_old_color: str | None    
    add_object: AddObject
    

    def __init__(self, root: ttk.Frame, display_file: DisplayFile, redraw_viewport_callback: Callable, column: int, row: int):
        self.display_file = display_file
        self.redraw_viewport_callback = redraw_viewport_callback
        self.add_object = AddObject(display_file, redraw_viewport_callback)
        self.selected_shape = None
        self.selected_shape_old_color = None
        self.create_widgets(root, column, row)


    def create_widgets(self, root: ttk.Frame, column: int, row: int):
        ttk.Label(root, text="Objetos").grid(column=0, row=1, sticky="w")
        self.listbox = Listbox(
            root,
            height=12,
            width=24,
            borderwidth=3,
            listvariable=self.display_file.shapes_str_var,
            highlightbackground="black",
            highlightthickness=1,
        )
        self.listbox.grid(column=column, row=row, sticky=(N, S, E, W))
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(column=column + 1, row=row, sticky=(N, S, W))
        self.listbox.configure(yscrollcommand=scrollbar.set)
        self.listbox.bind("<<ListboxSelect>>", self.__update_selected_shape)
        
        button_frame = ttk.Frame(root)
        button_frame.grid(column=0, row=3)
        ttk.Button(button_frame, text="Add Object", command=lambda: self.add_object.create_widget(root)).grid(
            column=0, row=0
        )
        ttk.Button(button_frame, text="Clear Selection", command=lambda: self.__update_selected_shape(None)).grid(
            column=1, row=0, sticky="w"
        )

    def __update_selected_shape(self, event: Event):
        if self.selected_shape:
            self.selected_shape.color = self.selected_shape_old_color

        if event is not None:
            index = event.widget.curselection()
            if index:
                self.selected_shape = self.display_file.get_shape_by_id(event.widget.get(index[0]))
                self.selected_shape_old_color = self.selected_shape.color
                self.selected_shape.color = "gold"
            else:
                self.selected_shape.color = self.selected_shape_old_color
                self.selected_shape = None

        self.listbox.event_generate("<<ChangedSelectedShape>>", data=self.selected_shape)
        print(f"Selected shape: {self.selected_shape}")
        
        self.redraw_viewport_callback()