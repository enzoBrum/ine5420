import json
from tkinter import Frame, StringVar, Toplevel, ttk
from typing import Callable

from display_file import DisplayFile
from event import Events
from shape import Line, Point, Wireframe
from vector3 import Vector3


class AddObject:
    frame: Toplevel
    root: Frame
    color_hex_name: dict[str, str] = {
        "black": "#000000",
        "red": "#ff0000",
        "green": "#00ff00",
        "blue": "#0000ff",
        "orange": "#FFA500",
        "pink": "#FFC0CB",
        "purple": "#800080",
        "gray": "#808080",
    }

    def __init__(self, root: Frame):
        self.frame = None
        self.root = root

    def add_point(self, x, y, name, color):
        self.root.event_generate(
            Events.ADD_SHAPE,
            data=json.dumps(
                {"type": "point", "points": [(x, y)], "name": name, "color": color}
            ),
        )

    def add_line(self, x1, y1, x2, y2, name, color):
        self.root.event_generate(
            Events.ADD_SHAPE,
            data=json.dumps(
                {
                    "type": "line",
                    "points": [(x1, y1), (x2, y2)],
                    "name": name,
                    "color": color,
                }
            ),
        )

    def add_wireframe(self, points, name, color):
        self.root.event_generate(
            Events.ADD_SHAPE,
            data=json.dumps(
                {
                    "type": "wireframe",
                    "points": list(points),
                    "name": name,
                    "color": color,
                }
            ),
        )

    def create_widget(self, root: ttk.Frame):
        self.frame = Toplevel(root)
        self.frame.title("Add Object")

        shape_frame = ttk.Frame(self.frame)
        shape_frame.grid(row=4, columnspan=2, padx=10, pady=5)

        ttk.Label(self.frame, text="Object Name:").grid(
            row=0, column=0, padx=10, pady=5
        )
        entry_name = ttk.Entry(self.frame)
        entry_name.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.frame, text="Color:").grid(row=1, column=0, padx=10, pady=5)
        entry_color = ttk.Entry(self.frame)
        entry_color.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.frame, text="Shape:").grid(row=2, column=0, padx=10, pady=5)
        type_var = StringVar(self.frame)
        options = ["Select a shape", "Point", "Line", "Wireframe"]
        ttk.OptionMenu(
            self.frame,
            type_var,
            *options,
            command=lambda selection: self.__update_shape_frame(
                shape_frame, type_var.get()
            ),
        ).grid(row=2, column=1, padx=10, pady=5)

        ttk.Button(
            self.frame,
            text="Add",
            command=lambda: self.__add_selected_object(
                type_var.get(), entry_name.get(), entry_color.get(), shape_frame
            ),
        ).grid(row=6, columnspan=2, padx=10, pady=5)

    def __add_selected_object(
        self, type_obj: str, name: str, color: str, shape_frame: ttk.Frame
    ):
        row = 4 if type_obj == "Line" else 2
        column = 0 if type_obj == "Wireframe" else 1
        if name == "":
            ttk.Label(shape_frame, text="Digit a name.").grid(row=row, column=column)
            return

        if color not in self.color_hex_name and (
            color[0] != "#" or len(color) != 7
        ):  #  len(color) é 7, se a cor for hexadecimal
            ttk.Label(
                shape_frame,
                text=f'Digit an available color: {", ".join(self.color_hex_name.keys())}\nOr use a hex value, like: #00ff0f',
            ).grid(row=row, column=column)
            return

        if color[0] != "#":
            color = self.color_hex_name[color]
        else:
            self.color_hex_name[color] = color

        try:
            if type_obj == "Point":
                x = float(shape_frame.winfo_children()[1].get())
                y = float(shape_frame.winfo_children()[3].get())
                self.add_point(x, y, name, color)
            elif type_obj == "Line":
                x1 = float(shape_frame.winfo_children()[1].get())
                y1 = float(shape_frame.winfo_children()[3].get())
                x2 = float(shape_frame.winfo_children()[5].get())
                y2 = float(shape_frame.winfo_children()[7].get())
                self.add_line(x1, y1, x2, y2, name, color)
            elif type_obj == "Wireframe":
                points = str(shape_frame.winfo_children()[1].get())
                self.add_wireframe(eval(f"[{points}]"), name, color)
        except:
            error_message = (
                "X's and Y's must be a number."
                if type_obj in ["Line", "Point"]
                else "Format is incorrect or X's and Y's are not a number."
            )
            ttk.Label(shape_frame, text=error_message).grid(row=row, column=column)

        self.__update_shape_frame(shape_frame, type_obj)

    def __update_shape_frame(self, shape_frame: ttk.Frame, type_obj: str):
        for widget in shape_frame.winfo_children():
            widget.destroy()

        if type_obj == "Point":
            ttk.Label(shape_frame, text="X:").grid(row=0, column=0, padx=5, pady=5)
            entry_x = ttk.Entry(shape_frame)
            entry_x.grid(row=0, column=1, padx=5, pady=5)

            ttk.Label(shape_frame, text="Y:").grid(row=1, column=0, padx=5, pady=5)
            entry_y = ttk.Entry(shape_frame)
            entry_y.grid(row=1, column=1, padx=5, pady=5)
        elif type_obj == "Line":
            ttk.Label(shape_frame, text="X1:").grid(row=0, column=0, padx=5, pady=5)
            entry_x1 = ttk.Entry(shape_frame)
            entry_x1.grid(row=0, column=1, padx=5, pady=5)

            ttk.Label(shape_frame, text="Y1:").grid(row=1, column=0, padx=5, pady=5)
            entry_y1 = ttk.Entry(shape_frame)
            entry_y1.grid(row=1, column=1, padx=5, pady=5)

            ttk.Label(shape_frame, text="X2:").grid(row=2, column=0, padx=5, pady=5)
            entry_x2 = ttk.Entry(shape_frame)
            entry_x2.grid(row=2, column=1, padx=5, pady=5)

            ttk.Label(shape_frame, text="Y2:").grid(row=3, column=0, padx=5, pady=5)
            entry_y2 = ttk.Entry(shape_frame)
            entry_y2.grid(row=3, column=1, padx=5, pady=5)
        elif type_obj == "Wireframe":
            ttk.Label(
                shape_frame,
                text="Give the points in exactly format: (x1, y1), (x2, y2), (x3,y3) ...",
            ).grid(row=0, column=0, padx=5, pady=5)
            entry_points = ttk.Entry(shape_frame)
            entry_points.grid(row=1, column=0, padx=5, pady=5)
