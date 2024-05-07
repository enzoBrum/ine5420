import json
from tkinter import ttk
from tkinter import StringVar
from typing import Literal

from event import Events


class MovementControls:
    root: ttk.Frame
    frame: ttk.Frame
    _moving: Literal["SHAPE", "WINDOW"]
    _text_button_increase: StringVar
    _text_button_decrease: StringVar

    def __init__(
        self,
        root: ttk.Frame,
        column: int,
        row: int,
    ):
        self.root = root
        self.frame = ttk.Frame(root, padding="15 10 10 10", border=3, borderwidth=3, relief="flat")
        self.frame.grid(row=row, column=column, sticky="NSWE")
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self._moving = "WINDOW"

        ttk.Button(
            self.frame,
            text="Move Up",
            command=lambda: self.root.event_generate(Events.MOVE_WINDOW if self._moving == "WINDOW" else Events.MOVE_SHAPE, data="U"),
        ).grid(column=1, row=0, sticky="s", pady=(40, 3))
        ttk.Button(
            self.frame,
            text="Move Left",
            command=lambda: self.root.event_generate(Events.MOVE_WINDOW if self._moving == "WINDOW" else Events.MOVE_SHAPE, data="L"),
        ).grid(
            column=0,
            row=1,
            sticky="w",
            padx=(0, 3), 
            pady=(3, 40),
            rowspan=2
        )
        ttk.Button(
            self.frame,
            text="Move Right",
            command=lambda: self.root.event_generate(Events.MOVE_WINDOW if self._moving == "WINDOW" else Events.MOVE_SHAPE, data="R"),
        ).grid(column=2, row=1, sticky="e", padx=(3, 0), pady=(3, 40), rowspan=2)
        ttk.Button(
            self.frame,
            text="Move Down",
            command=lambda: self.root.event_generate(Events.MOVE_WINDOW if self._moving == "WINDOW" else Events.MOVE_SHAPE, data="D"),
        ).grid(column=1, row=1, padx=3, pady=(3, 40), rowspan=2)


        self._text_button_increase = StringVar(value="Zoom In")
        self._text_button_decrease = StringVar(value="Zoom Out")
        ttk.Button(
            self.frame,
            textvariable=self._text_button_increase,
            command=lambda: self.root.event_generate(Events.ZOOM if self._moving == "WINDOW" else Events.SCALE_SHAPE, data="+"),
        ).grid(column=0, row=3)
        ttk.Button(
            self.frame,
            textvariable=self._text_button_decrease,
            command=lambda: self.root.event_generate(Events.ZOOM if self._moving == "WINDOW" else Events.SCALE_SHAPE, data="-"),
        ).grid(column=1, row=3)
        ttk.Button(
            self.frame,
            text="Rotate",
            command=lambda: self.root.event_generate(Events.ROTATE_WINDOW if self._moving == "WINDOW" else Events.ROTATE_SHAPE),
        ).grid(column=2, row=3)

    @property
    def moving(self) -> str:
        return self._moving

    @moving.setter
    def moving(self, new_value: str) -> str:
        self._moving = new_value

        match self._moving:
            case "SHAPE":
                self._text_button_decrease.set("Decrease Size")
                self._text_button_increase.set("Increase Size")
            case "WINDOW":
                self._text_button_decrease.set("Zoom Out")
                self._text_button_increase.set("Zoom In")

