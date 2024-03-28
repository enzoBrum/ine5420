from tkinter import ttk
from typing import Callable
from interface import Window

class WindowControls:
    window: Window
    root: ttk.Frame
    frame: ttk.Frame
    redraw_viewport_callback: Callable[[], None]

    def __init__(self, root: ttk.Frame, window: Window, redraw_viewport_callback: Callable, column: int, row: int):
        self.window = window
        self.redraw_viewport_callback = redraw_viewport_callback

        self.create_widgets(root, column, row)

    def create_widgets(self, root: ttk.Frame, column: int, row: int):
        self.frame = ttk.Frame(
            root, padding="12 -3 12 12", border=3, borderwidth=3, relief="groove"
        )

        self.frame.grid(column=column, row=row, sticky="nswe", pady=12)
        self.frame.grid_columnconfigure(0, weight=1)

        ttk.Label(self.frame, text="Window").grid(
            column=0, row=4, sticky="nw"
        )

        ttk.Label(self.frame, text="Passo:").grid(column=0, row=5, sticky="w")

        ttk.Entry(self.frame, textvariable=self.window.step_var).grid(
            column=1, row=5, sticky="w"
        )

        move_controls_frame = ttk.Frame(self.frame, padding="3 30 3 3")
        move_controls_frame.grid(column=0, row=6, columnspan=2, rowspan=2)
        ttk.Button(move_controls_frame, text="Up", command=self.move_up).grid(
            column=1, row=0, sticky="ns"
        )
        ttk.Button(move_controls_frame, text="Left", command=self.move_left).grid(
            column=0,
            row=1,
            sticky="w",
        )
        ttk.Button(move_controls_frame, text="Right", command=self.move_right).grid(
            column=2, row=1, sticky="e"
        )
        ttk.Button(move_controls_frame, text="Down", command=self.move_down).grid(
            column=1, row=1
        )

        zoom_controls = ttk.Frame(self.frame, padding="3 30 3 3")
        zoom_controls.grid(column=0, row=8, columnspan=2)
        ttk.Button(zoom_controls, text="In", command=self.zoom_in).grid(column=0, row=3)
        ttk.Button(zoom_controls, text="Out", command=self.zoom_out).grid(
            column=1, row=3
        )

    def zoom_out(self):
        self.window.zoom(-1)
        self.redraw_viewport_callback()

    def zoom_in(self):
        self.window.zoom(1)
        self.redraw_viewport_callback()


    def move_left(self):
        self.window.move("L")
        self.redraw_viewport_callback()

    def move_right(self):
        self.window.move("R")
        self.redraw_viewport_callback()

    def move_up(self):
        self.window.move("U")
        self.redraw_viewport_callback()

    def move_down(self):
        self.window.move("D")
        self.redraw_viewport_callback()
    
    
