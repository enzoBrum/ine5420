from fileinput import filename
from tkinter import E, Event, Listbox, N, S, StringVar, Tk, W, filedialog, ttk
from typing import Callable

from display_file import DisplayFile
from event import Events
from shape import Shape

from .add_object import AddObject


class ShapeListbox:
    root: ttk.Frame
    listbox: Listbox
    add_object: AddObject
    shapes_str_var: StringVar

    def __init__(
        self,
        root: ttk.Frame,
        column: int,
        row: int,
    ):
        self.root = root
        self.add_object = AddObject(self.root)
        self.shapes_str_var = StringVar()

        ttk.Label(root, text="Objetos").grid(column=0, row=1, sticky="w")
        self.listbox = Listbox(
            root,
            height=12,
            width=24,
            borderwidth=3,
            listvariable=self.shapes_str_var,
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
        ttk.Button(
            button_frame,
            text="Add Object",
            command=lambda: self.add_object.create_widget(self.root),
        ).grid(column=0, row=0)
        ttk.Button(
            button_frame,
            text="Clear Selection",
            command=lambda: self.__update_selected_shape(None, clear_selection=True),
        ).grid(column=1, row=0, sticky="w")
        ttk.Button(button_frame, text="Save", command=self.save_shapes).grid(
            column=0, row=1
        )
        ttk.Button(button_frame, text="Load", command=self.load_shapes).grid(
            column=1, row=1, sticky="w"
        )

    def __update_selected_shape(self, event: Event, clear_selection: bool = False):
        if clear_selection:
            self.root.event_generate(Events.CLEAR_SHAPE_SELECTION)
            return

        index = event.widget.curselection()
        if index:
            self.root.event_generate(
                Events.SELECT_SHAPE, data=event.widget.get(index[0])
            )

    def save_shapes(self):
        filename = filedialog.asksaveasfilename(
            filetypes=[("Wavefront Object", "*.obj")]
        )
        if filename:
            self.root.event_generate(Events.SAVE_SHAPES, data=filename)

    def load_shapes(self):
        filename = filedialog.askopenfilename(filetypes=[("Wavefront Object", "*.obj")])
        if filename:
            self.root.event_generate(Events.LOAD_SHAPES, data=filename)
