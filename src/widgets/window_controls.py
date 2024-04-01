import json
from tkinter import ttk

from tkinter import StringVar
from event import Events


class WindowControls:
    root: ttk.Frame
    frame: ttk.Frame
    window_step: StringVar
    xvar: StringVar
    yvar: StringVar

    def __init__(
        self,
        root: ttk.Frame,
        column: int,
        row: int,
    ):
        self.root = root
        self.frame = ttk.Frame(
            root, padding="12 -3 12 12", border=3, borderwidth=3, relief="groove"
        )

        self.frame.grid(column=column, row=row, sticky="nswe", pady=12)
        self.frame.grid_columnconfigure(0, weight=1)
        self.window_step = StringVar(value=str(10.0))

        ttk.Label(self.frame, text="Window").grid(column=0, row=0, sticky="nw")

        ttk.Label(self.frame, text="Passo:").grid(column=0, row=1, sticky="w")

        ttk.Entry(self.frame, textvariable=self.window_step).grid(
            column=1, row=1, sticky="w"
        )

        move_controls_frame = ttk.Frame(self.frame, padding="3 30 3 3")
        move_controls_frame.grid(column=0, row=2, columnspan=2, rowspan=2)
        ttk.Button(
            move_controls_frame,
            text="Up",
            command=lambda: self.root.event_generate(Events.MOVE_WINDOW, data="U"),
        ).grid(column=1, row=0, sticky="ns")
        ttk.Button(
            move_controls_frame,
            text="Left",
            command=lambda: self.root.event_generate(Events.MOVE_WINDOW, data="L"),
        ).grid(
            column=0,
            row=1,
            sticky="w",
        )
        ttk.Button(
            move_controls_frame,
            text="Right",
            command=lambda: self.root.event_generate(Events.MOVE_WINDOW, data="R"),
        ).grid(column=2, row=1, sticky="e")
        ttk.Button(
            move_controls_frame,
            text="Down",
            command=lambda: self.root.event_generate(Events.MOVE_WINDOW, data="D"),
        ).grid(column=1, row=1)

        zoom_controls = ttk.Frame(self.frame, padding="3 30 3 3")
        zoom_controls.grid(column=0, row=4, columnspan=2)
        ttk.Button(
            zoom_controls,
            text="In",
            command=lambda: self.root.event_generate(Events.ZOOM, data="+"),
        ).grid(column=0, row=3)
        ttk.Button(
            zoom_controls,
            text="Out",
            command=lambda: self.root.event_generate(Events.ZOOM, data="-"),
        ).grid(column=1, row=3)
        ttk.Button(
            zoom_controls,
            text="Rotate",
            command=lambda: self.root.event_generate(Events.ROTATE_WINDOW),
        ).grid(column=2, row=3)

        move_object_frame = ttk.Frame(self.frame, padding="3 30 3 3")
        move_object_frame.grid(column=0, row=5, columnspan=1)
        ttk.Label(move_object_frame, text="Object Translation:").grid(
            row=0, column=0, padx=5
        )
        ttk.Button(
            move_object_frame,
            text="Up",
            command=lambda: self.root.event_generate(Events.MOVE_SHAPE, data="U"),
        ).grid(row=1, column=2, sticky="ns")
        ttk.Button(
            move_object_frame,
            text="Left",
            command=lambda: self.root.event_generate(Events.MOVE_SHAPE, data="L"),
        ).grid(
            row=2,
            column=1,
            sticky="w",
        )
        ttk.Button(
            move_object_frame,
            text="Right",
            command=lambda: self.root.event_generate(Events.MOVE_SHAPE, data="R"),
        ).grid(row=2, column=3, sticky="e")
        ttk.Button(
            move_object_frame,
            text="Down",
            command=lambda: self.root.event_generate(Events.MOVE_SHAPE, data="D"),
        ).grid(row=2, column=2)

        scale_frame = ttk.Frame(self.frame, padding="3 30 3 3")
        scale_frame.grid(column=0, row=7, columnspan=1)
        ttk.Label(scale_frame, text="Object Scale:").grid(row=0, column=0, padx=7)
        ttk.Button(
            scale_frame,
            text="+",
            command=lambda: self.root.event_generate(Events.SCALE_SHAPE, data="+"),
        ).grid(row=0, column=1)
        ttk.Button(
            scale_frame,
            text="-",
            command=lambda: self.root.event_generate(Events.SCALE_SHAPE, data="-"),
        ).grid(row=0, column=2)

        object_rotation_frame = ttk.Frame(
            self.frame,
            padding="10 -3 10 10",
            border=3,
            borderwidth=3,
            relief="groove",
        )
        object_rotation_frame.grid(column=0, row=9, pady=12)
        ttk.Label(object_rotation_frame, text="Rotation").grid(
            row=0, column=0, sticky="n"
        )
        ttk.Label(object_rotation_frame, text="Degree:").grid(row=1, column=0)

        degree_var = StringVar(value="45")
        degree = ttk.Entry(object_rotation_frame, width=10, textvariable=degree_var)
        degree.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(object_rotation_frame, text="Rotation point:").grid(row=2, column=0)

        ttk.Label(object_rotation_frame, text="X:").grid(row=3, column=0)

        self.xvar = StringVar(object_rotation_frame)
        self.xvar.set(0)
        entry_x = ttk.Entry(object_rotation_frame, textvariable=self.xvar, width=10)
        entry_x.grid(row=3, column=1)

        ttk.Label(object_rotation_frame, text="Y:").grid(row=4, column=0)
        self.yvar = StringVar(object_rotation_frame)
        self.yvar.set(0)
        entry_y = ttk.Entry(object_rotation_frame, textvariable=self.yvar, width=10)
        entry_y.grid(row=4, column=1)

        ttk.Button(
            object_rotation_frame,
            text="Rotate",
            command=lambda: self.root.event_generate(
                Events.ROTATE_SHAPE,
                data=json.dumps(
                    {
                        "degree": float(degree_var.get()),
                        "x": float(self.xvar.get()),
                        "y": float(self.yvar.get()),
                    }
                ),
            ),
        ).grid(row=5, column=0)
