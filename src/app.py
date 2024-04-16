from functools import wraps
import json
from tkinter import E, N, S, Tk, W, ttk
import traceback
from typing import Callable

import numpy as np
import sv_ttk

from descritor_obj import DescritorOBJ
from display_file import DisplayFile
from event import Events
from interface import Viewport, Window
from shape import Line, Point, Shape, Wireframe
from transformations import center, rotate, scale, translation
from vector3 import Vector3
from widgets import ShapeListbox, WindowControls

VIEWPORT_DIMENSION = (600, 600)
GEOMETRY = "1000x1000"
PROGRAM_NAME = "sistema básico de CG 2D"


class App:
    window: Window
    viewport: Viewport
    display_file: DisplayFile
    root: Tk
    frame: ttk.Frame
    selected_shape: Shape | None
    selected_shape_old_color: str
    shape_listbox: ShapeListbox
    window_controls: WindowControls

    def redraw_viewport(func):
        @wraps(func)
        def wrapper(self: "App", *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.viewport.draw(self.window, self.display_file)
            return result

        return wrapper

    def bind_event(
        self, callback: Callable[[str | None], None], event: str, has_data: bool = True
    ):
        if not has_data:
            self.root.bind(event, callback)
        else:
            # tkinter does not handle events that send data.
            # see: https://stackoverflow.com/a/41912425
            self.root.call(
                "bind", str(self.root), event, self.root.register(callback) + " %d"
            )

    @redraw_viewport
    def add_shape(self, data: str):
        try:
            data = json.loads(data)

            points = [Vector3(x, y) for x, y in data["points"]]
            name = data["name"]

            idx = 1
            while (
                self.display_file.get_shape_by_id(f"{data['type'].title()}[{name}]")
                is not None
            ):
                if name.endswith(f"-{idx-1}"):
                    name = name.replace(f"-{idx-1}", f"-{idx}")
                else:
                    name += f"-{idx}"
                idx += 1

            color = data["color"]
            shape = None
            match data["type"]:
                case "point":
                    shape = Point(points[0], name, color)
                case "line":
                    shape = Line.from_vector3(*points, name, color)
                case "wireframe":
                    shape = Wireframe.from_vector3(
                        points,
                        data["fill"].lower() == "true",
                        name,
                        color,
                    )

            print(f"Added shape: {shape}")
            self.display_file.append(shape)
            self.shape_listbox.shapes_str_var.set(self.display_file._shapes)
        except:
            traceback.print_exc()

    def save_shapes(self, filename):
        if self.selected_shape:
            self.selected_shape.color = self.selected_shape_old_color
        DescritorOBJ.save(
            self.display_file, self.shape_listbox.add_object.color_hex_name, filename
        )

        if self.selected_shape:
            self.selected_shape.color = "gold"

    @redraw_viewport
    def load_shapes(self, filename):
        self.display_file, hex_color_names = DescritorOBJ.load(filename)

        names_color_hex = {
            name: color_hex for color_hex, name in hex_color_names.items()
        }
        self.shape_listbox.add_object.color_hex_name |= names_color_hex
        self.shape_listbox.shapes_str_var.set(self.display_file._shapes)
        self.window.reset()

    @redraw_viewport
    def rotate_window(self, e):
        rotate(
            float(self.window_controls.window_step.get()),
            Vector3(*center(self.window.points)),
            self.window.points,
        )

    @redraw_viewport
    def move_window(self, direction: str):
        self.window.move(
            direction.upper(), float(self.window_controls.window_step.get())
        )

    @redraw_viewport
    def zoom(self, factor: str):
        self.window.zoom(
            1 if factor == "+" else -1, float(self.window_controls.window_step.get())
        )

    @redraw_viewport
    def translation(self, direction: str):
        old_cx, old_cy = center(self.selected_shape.points)
        xvar = float(self.window_controls.xvar.get())
        yvar = float(self.window_controls.yvar.get())
        using_object_center = abs(old_cx - xvar) < 1e-6 and abs(old_cy - yvar) < 1e-6

        vup = [
            self.window.points[3].x - self.window.points[0].x,
            self.window.points[3].y - self.window.points[0].y,
            1,
        ]

        vup_normalized = np.array(vup) / np.linalg.norm(vup)

        step = 10
        if direction == "R":
            displacement_vector = np.cross(vup_normalized, [0, 0, 1]) * step
        elif direction == "L":
            displacement_vector = -np.cross(vup_normalized, [0, 0, 1]) * step
        # Up and Down dont need np.cross
        elif direction == "U":
            displacement_vector = vup_normalized * step
        else:
            displacement_vector = -vup_normalized * step


        displacement_vector = Vector3.from_array(displacement_vector)
        points = self.selected_shape.points
        for i in range(len(self.selected_shape.points)):
            points[i] += displacement_vector

        if using_object_center:
            new_cx, new_cy = center(self.selected_shape.points)
            self.window_controls.xvar.set(new_cx)
            self.window_controls.yvar.set(new_cy)

    @redraw_viewport
    def scale(self, factor: str):
        scale(1.2 if factor == "+" else 0.8, self.selected_shape.points)

    @redraw_viewport
    def rotate(self, data: str):
        data = json.loads(data)
        rotate(
            data["degree"], Vector3(data["x"], data["y"], 1), self.selected_shape.points
        )

    @redraw_viewport
    def clear_selected_shape(self, e):
        if self.selected_shape:
            self.selected_shape.color = self.selected_shape_old_color
            self.selected_shape = None
            self.window_controls.xvar.set(0)
            self.window_controls.yvar.set(0)

    @redraw_viewport
    def update_selected_shape(self, selected_shape_id: str):
        if self.selected_shape:
            self.selected_shape.color = self.selected_shape_old_color

        self.selected_shape = self.display_file.get_shape_by_id(selected_shape_id)
        self.selected_shape_old_color = self.selected_shape.color
        print("Color: %s" % self.selected_shape_old_color)
        self.selected_shape.color = "gold"

        cx, cy = center(self.selected_shape.points)
        self.window_controls.xvar.set(cx)
        self.window_controls.yvar.set(cy)

        print(f"Selected shape: {self.selected_shape}")

    @redraw_viewport
    def change_line_clipping(self, alg: str):
        print(f"Mudando algoritmo de clipping para {alg}")
        Line.clipping_function = alg

    def __create_viewport_and_log(self):
        viewport_frame = ttk.Frame(self.frame, padding="12 -3 12 12")
        viewport_frame.grid(column=1, row=0)

        ttk.Label(viewport_frame, text="Viewport").grid(column=0, row=0, sticky="w")

        self.viewport = Viewport(
            Vector3(0, 0),
            Vector3(VIEWPORT_DIMENSION[0], VIEWPORT_DIMENSION[1]),
            viewport_frame,
            "#ffffff",
        )

        self.viewport.canvas.grid(column=0, row=1)

    def __create_left_menu(self):
        menu_frame = ttk.Frame(
            self.frame, padding="12 -3 12 12", border=3, borderwidth=3, relief="groove"
        )
        menu_frame.grid(column=0, row=0)

        ttk.Label(menu_frame, text="Menu de Funções").grid(column=0, row=0, sticky="n")

        self.shape_listbox = ShapeListbox(
            menu_frame,
            column=0,
            row=2,
        )

        self.window_controls = WindowControls(
            menu_frame,
            column=0,
            row=4,
        )

    def __bind_events(self):
        self.bind_event(self.move_window, Events.MOVE_WINDOW, True)
        self.bind_event(self.zoom, Events.ZOOM, True)
        self.bind_event(self.rotate_window, Events.ROTATE_WINDOW, False)
        self.bind_event(self.translation, Events.MOVE_SHAPE, True)
        self.bind_event(self.scale, Events.SCALE_SHAPE, True)
        self.bind_event(self.rotate, Events.ROTATE_SHAPE, True)
        self.bind_event(self.update_selected_shape, Events.SELECT_SHAPE, True)
        self.bind_event(self.clear_selected_shape, Events.CLEAR_SHAPE_SELECTION, False)
        self.bind_event(self.add_shape, Events.ADD_SHAPE, True)
        self.bind_event(self.save_shapes, Events.SAVE_SHAPES, True)
        self.bind_event(self.load_shapes, Events.LOAD_SHAPES, True)
        self.bind_event(
            self.change_line_clipping, Events.CHANGE_CLIPPING_ALGORITHM, True
        )

    def __init__(self):
        self.root = Tk()
        self.root.title(PROGRAM_NAME)
        self.root.geometry(GEOMETRY)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.selected_shape = None
        self.window = Window(
            Vector3(10, 10),
            Vector3(VIEWPORT_DIMENSION[0] - 10, VIEWPORT_DIMENSION[1] - 10),
        )
        self.frame = ttk.Frame(self.root, padding="3 3 12 12")
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.display_file = DisplayFile()

        self.__create_left_menu()
        self.__create_viewport_and_log()
        self.__bind_events()

        # self.add_shape(
        #    json.dumps(
        #        {
        #            "type": "line",
        #            "points": [(100, 100), (500, 500)],
        #            "name": "Foo",
        #            "color": self.shape_listbox.add_object.color_hex_name["blue"],
        #        }
        #    )
        # )
        self.add_shape(
            json.dumps(
                {
                    "type": "wireframe",
                    "points": [(0, 500), (100, 600), (150, 500)],
                    "name": "Bar-1",
                    "color": self.shape_listbox.add_object.color_hex_name["red"],
                    "fill": "false",
                }
            )
        )
        self.add_shape(
            json.dumps(
                {
                    "type": "wireframe",
                    "points": [(0, 0), (100, 100), (150, 0)],
                    "name": "Bar",
                    "color": self.shape_listbox.add_object.color_hex_name["red"],
                    "fill": "True",
                }
            )
        )

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
