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

    def add_wireframe(self, points, name, color, fill_polygon):
        self.root.event_generate(
            Events.ADD_SHAPE,
            data=json.dumps(
                {
                    "type": "wireframe",
                    "points": list(points),
                    "name": name,
                    "color": color,
                    "fill": fill_polygon,
                }
            ),
        )

    def add_curve2d(self, points, name, color, points_per_segment):
        self.root.event_generate(
            Events.ADD_SHAPE,
            data=json.dumps(
                {
                    "type": "curve2d",
                    "points": list(points),
                    "name": name,
                    "color": color,
                    "points_per_segment": points_per_segment,
                }
            ),
        )

    def create_widget(self, root: ttk.Frame):
        self.frame = Toplevel(root)
        self.frame.title("Add Object")

        shape_frame = ttk.Frame(self.frame)
        shape_frame.grid(row=4, columnspan=3, rowspan=10, padx=10, pady=5)

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
        options = ["Select a shape", "Point", "Line", "Wireframe", "Curve2D"]
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
        ).grid(row=60, columnspan=2, padx=10, pady=5)

    def __add_selected_object(
        self, type_obj: str, name: str, color: str, shape_frame: ttk.Frame
    ):
        row = 4 if type_obj == "Line" else 2
        column = 0 if type_obj in ("Wireframe", "Curve2D") else 1
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
                self.add_wireframe(
                    eval(f"[{points}]"), name, color, self.fill_polygon.get()
                )
            elif type_obj == "Curve2D":
                points_frame: ttk.Frame = shape_frame.winfo_children()[0]
                num_points_frame: ttk.Frame = shape_frame.winfo_children()[1]

                num_points = int(num_points_frame.winfo_children()[1].get())
                points = eval(f"[{points_frame.winfo_children()[2].get()}]")

                self.add_curve2d(points, name, color, num_points)
        except:
            from traceback import print_exc

            print_exc()
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

            self.fill_polygon = StringVar()
            ttk.Checkbutton(
                shape_frame,
                text="Fill Wireframe",
                onvalue="True",
                offvalue="False",
                variable=self.fill_polygon,
            ).grid(row=2, column=0)
        elif type_obj == "Curve2D":

            points_frame = ttk.Frame(shape_frame, padding="5 5 5 5")
            num_points_frame = ttk.Frame(shape_frame, padding="5 5 5 5")

            points_frame.grid(row=0, column=0)
            num_points_frame.grid(row=8, column=0, sticky="SW")
            ttk.Label(
                points_frame,
                text=(
                    "Give the points in exactly format: (x1, y1), (x2, y2), (x3,y3), (x4, y4), (x5, y5), (x6, y6), (x7, y7), (x8, y8) ...\n"
                    "The first set of 4 points defines a bezier curve, where (x1, y1) and (x4, y4) are the curve's begin/end and (x2, y2), (x3, y3) are it's Control points\n"
                    "The following sets of 3 points defines a bezier curve where the start is the end of the previous curve and the third point is it's end.\n"
                    "The first and second points are it's Control points.\n"
                    "For example: (x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5), (x6, y6), (x7, y7) describes two continuous curves.\n"
                    "Curve 1: begins at (x1, y1), ends at (x4, y4). Control points are (x2, y2) and (x3, y3)\n"
                    "Curve 2: begins at (x4, y4), ends at (x7, y7). Control points are (x5, y5) and (x6, y6)."
                ),
            ).grid(
                row=0, column=0, padx=10, pady=30, sticky="NW", rowspan=7, columnspan=7
            )

            ttk.Label(points_frame, text="Points: ").grid(row=8, column=0, sticky="W")
            entry_curve = ttk.Entry(points_frame)
            entry_curve.grid(row=8, column=1, sticky="W")

            ttk.Label(num_points_frame, text="Number of points: ").grid(
                row=6, column=0, sticky="WS"
            )
            num_points = ttk.Entry(num_points_frame)
            num_points.grid(row=6, column=7, sticky="ES")
