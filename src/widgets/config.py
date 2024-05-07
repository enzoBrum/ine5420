from tkinter import ttk
from tkinter import StringVar

from event import Events


class Configuration:
    root: ttk.Frame
    frame: ttk.Frame
    window_step: StringVar
    rotation_axis: StringVar
    scale_step: StringVar
    __clipping_algorithm: StringVar
    __move_window_or_shape: StringVar
    __window_rotation: StringVar

    def __init__(
        self,
        root: ttk.Frame,
        column: int,
        row: int,
    ):
        self.root = root
        self.frame = ttk.Frame(root, padding="15 10 10 10", border=3, borderwidth=3, relief="flat")
        self.frame.grid(row=row, column=column, sticky="NSWE")

        self.window_step = StringVar(value="10.0")
        self.rotation_axis = StringVar(value="(10, 10, 10)")
        self.scale_step = StringVar(value="10.0")

        ttk.Label(self.frame, text="Move Step: ").grid(column=0, row=0, pady=(60,3), sticky="W")
        ttk.Entry(self.frame, textvariable=self.window_step).grid(column=1, row=0, pady=(70,3), sticky="W")

        ttk.Label(self.frame, text="Scale Step: ").grid(column=0, row=1, pady=3, sticky="W")
        ttk.Entry(self.frame, textvariable=self.scale_step).grid(column=1, row=1, pady=3, sticky="W")

        ttk.Label(self.frame, text="Rotation Axis").grid(column=0, row=2, pady=3, sticky="W")
        ttk.Entry(self.frame, textvariable=self.scale_step).grid(column=1, row=2, pady=3, sticky="W")

        ttk.Separator(self.frame, orient="horizontal").grid(row=3, column=0, ipadx=200, columnspan=2, pady=(20, 20))


        ttk.Label(self.frame, text="Clipping Algorithm").grid(column=0, row=4, pady=3, sticky="W")

        cohen = "cohen-sutherland"
        liang = "liang-barsky"
        self.__clipping_algorithm = StringVar(value=cohen)
        ttk.Radiobutton(
            self.frame,
            text=cohen,
            value=cohen,
            variable=self.__clipping_algorithm,
            command=lambda: self.frame.event_generate(Events.CHANGE_CLIPPING_ALGORITHM, data="cohen"),
        ).grid(column=0, row=5, pady=3, sticky="W")
        ttk.Radiobutton(
            self.frame,
            text=liang,
            value=liang,
            variable=self.__clipping_algorithm,
            command=lambda: self.frame.event_generate(Events.CHANGE_CLIPPING_ALGORITHM, data="liang"),
        ).grid(column=0, row=6, pady=3, sticky="W")

        ttk.Separator(self.frame, orient="horizontal").grid(row=7, column=0, ipadx=200, columnspan=2, pady=(20, 20))

        ttk.Label(self.frame, text="Movement").grid(column=0, row=8, pady=3, sticky="W")
    
        self.__move_window_or_shape = StringVar(value="window")
        ttk.Radiobutton(
            self.frame,
            text="window",
            value="window",
            variable=self.__move_window_or_shape,
            command=lambda: self.frame.event_generate(Events.CHANGE_MOVE, data="window"),
        ).grid(column=0, row=9, pady=3, sticky="W")
        ttk.Radiobutton(
            self.frame,
            text="shape",
            value="shape",
            variable=self.__move_window_or_shape,
            command=lambda: self.frame.event_generate(Events.CHANGE_MOVE, data="shape"),
        ).grid(column=0, row=10, pady=3, sticky="W")


        ttk.Separator(self.frame, orient="horizontal").grid(row=11, column=0, ipadx=200, columnspan=2, pady=(20, 20))

        ttk.Label(self.frame, text="Window Rotation").grid(row=12, column=0, pady=3, sticky="W")
        self.__window_rotation = StringVar(value="axis")
        ttk.Radiobutton(
            self.frame,
            text="Around Axis",
            value="axis",
            variable=self.__window_rotation,
            command=lambda: self.frame.event_generate(Events.CHANGE_MOVE, data="axis"),
        ).grid(column=0, row=13, pady=3, sticky="W")
        ttk.Radiobutton(
            self.frame,
            text="Around itself vertically",
            value="vertical",
            variable=self.__window_rotation,
            command=lambda: self.frame.event_generate(Events.CHANGE_MOVE, data="vertical"),
        ).grid(column=0, row=14, pady=3, sticky="W")
        ttk.Radiobutton(
            self.frame,
            text="Around itself horizontally",
            value="horizontal",
            variable=self.__window_rotation,
            command=lambda: self.frame.event_generate(Events.CHANGE_MOVE, data="horizontal"),
        ).grid(column=0, row=15, pady=3, sticky="W")
        ttk.Radiobutton(
            self.frame,
            text="Around VPN",
            value="vpn",
            variable=self.__window_rotation,
            command=lambda: self.frame.event_generate(Events.CHANGE_MOVE, data="vpn"),
        ).grid(column=0, row=16, pady=3, sticky="W")
