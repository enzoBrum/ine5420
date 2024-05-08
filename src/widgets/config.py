from math import radians
from tkinter import ttk
from tkinter import StringVar

from event import Events
from vector3 import Vector3


class Configuration:
    root: ttk.Frame
    frame: ttk.Frame
    __move_step: StringVar
    __rotation_axis: StringVar
    __scale_step: StringVar
    __zoom_step: StringVar
    __rotation_degree: StringVar
    move_window_or_shape: StringVar
    window_rotation: StringVar
    __clipping_algorithm: StringVar

    def __init__(
        self,
        root: ttk.Frame,
        column: int,
        row: int,
    ):
        self.root = root
        self.frame = ttk.Frame(root, padding="15 10 10 10", border=3, borderwidth=3, relief="flat")
        self.frame.grid(row=row, column=column, sticky="NSWE")

        self.__move_step = StringVar(value="10.0")
        self.__rotation_axis = StringVar(value="(10, 10, 10)")
        self.__scale_step = StringVar(value="1.2")
        self.__zoom_step = StringVar(value="10.0")
        self.__rotation_degree = StringVar(value="10.0")

        ttk.Label(self.frame, text="Move Step: ").grid(column=0, row=0, pady=(60, 3), sticky="W")
        ttk.Entry(self.frame, textvariable=self.__move_step).grid(column=1, row=0, pady=(70, 3), sticky="W")

        ttk.Label(self.frame, text="Scale Step: ").grid(column=0, row=1, pady=3, sticky="W")
        ttk.Entry(self.frame, textvariable=self.__scale_step).grid(column=1, row=1, pady=3, sticky="W")

        ttk.Label(self.frame, text="Zoom Step: ").grid(column=0, row=1, pady=3, sticky="W")
        ttk.Entry(self.frame, textvariable=self.__zoom_step).grid(column=1, row=2, pady=3, sticky="W")

        ttk.Label(self.frame, text="Rotation Axis: ").grid(column=0, row=3, pady=3, sticky="W")
        ttk.Entry(self.frame, textvariable=self.__rotation_axis).grid(column=1, row=3, pady=3, sticky="W")

        ttk.Label(self.frame, text="Rotation Degrees: ").grid(column=0, row=4, pady=3, sticky="W")
        ttk.Entry(self.frame, textvariable=self.__rotation_degree).grid(column=1, row=4, pady=3, sticky="W")

        ttk.Separator(self.frame, orient="horizontal").grid(row=5, column=0, ipadx=200, columnspan=2, pady=(20, 20))

        ttk.Label(self.frame, text="Clipping Algorithm").grid(column=0, row=6, pady=3, sticky="W")

        cohen = "cohen-sutherland"
        liang = "liang-barsky"
        self.__clipping_algorithm = StringVar(value=cohen)
        ttk.Radiobutton(
            self.frame,
            text=cohen,
            value=cohen,
            variable=self.__clipping_algorithm,
            command=lambda: self.frame.event_generate(Events.CHANGE_CLIPPING_ALGORITHM, data="cohen"),
        ).grid(column=0, row=7, pady=3, sticky="W")
        ttk.Radiobutton(
            self.frame,
            text=liang,
            value=liang,
            variable=self.__clipping_algorithm,
            command=lambda: self.frame.event_generate(Events.CHANGE_CLIPPING_ALGORITHM, data="liang"),
        ).grid(column=0, row=8, pady=3, sticky="W")

        ttk.Separator(self.frame, orient="horizontal").grid(row=9, column=0, ipadx=200, columnspan=2, pady=(20, 20))

        ttk.Label(self.frame, text="Movement").grid(column=0, row=10, pady=3, sticky="W")

        self.move_window_or_shape = StringVar(value="WINDOW")
        ttk.Radiobutton(
            self.frame,
            text="window",
            value="WINDOW",
            variable=self.move_window_or_shape,
            command=lambda: self.frame.event_generate(Events.CHANGE_MOVE, data="WINDOW"),
        ).grid(column=0, row=11, pady=3, sticky="W")
        ttk.Radiobutton(
            self.frame,
            text="shape",
            value="SHAPE",
            variable=self.move_window_or_shape,
            command=lambda: self.frame.event_generate(Events.CHANGE_MOVE, data="SHAPE"),
        ).grid(column=0, row=12, pady=3, sticky="W")

        ttk.Separator(self.frame, orient="horizontal").grid(row=13, column=0, ipadx=200, columnspan=2, pady=(20, 20))

        ttk.Label(self.frame, text="Window Rotation").grid(row=14, column=0, pady=3, sticky="W")
        self.window_rotation = StringVar(value="axis")
        ttk.Radiobutton(
            self.frame,
            text="Around Axis",
            value="axis",
            variable=self.window_rotation,
        ).grid(column=0, row=15, pady=3, sticky="W")
        ttk.Radiobutton(
            self.frame,
            text="Around itself vertically",
            value="vertical",
            variable=self.window_rotation,
        ).grid(column=0, row=16, pady=3, sticky="W")
        ttk.Radiobutton(
            self.frame,
            text="Around itself horizontally",
            value="horizontal",
            variable=self.window_rotation,
        ).grid(column=0, row=17, pady=3, sticky="W")
        ttk.Radiobutton(
            self.frame,
            text="Around VPN",
            value="vpn",
            variable=self.window_rotation,
        ).grid(column=0, row=18, pady=3, sticky="W")

    @property
    def rotation_axis(self) -> Vector3:
        axis = self.__rotation_axis.get().strip()[1:-1]  # ignora () e []

        return Vector3.from_array([float(x) for x in axis.split(",")])

    @property
    def move_step(self) -> float:
        return float(self.__move_step.get())

    @property
    def scale_step(self) -> float:
        return float(self.__scale_step.get())

    @property
    def zoom_step(self) -> float:
        return float(self.__zoom_step.get())

    @property
    def rotation_rad(self) -> float:
        return radians(float(self.__rotation_degree.get()))
