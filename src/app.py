from functools import wraps
import json
from math import radians
from tkinter import E, N, S, Tk, W, ttk
import traceback
from typing import Callable

import numpy as np

from clipping import CohenSutherland, LiangBarsky
from descritor_obj import DescritorOBJ
from display_file import DisplayFile
from event import Events
from interface import Viewport, Window
from projections import parallel_projection, perspective_projection
from shape import (
    BSpline,
    BSpline3D,
    Curve2D,
    Curve3D,
    Line,
    Point,
    Point3D,
    Shape,
    Wireframe,
    Wireframe3D,
)
from transformations import Transformer3D
from vector3 import Vector3
from widgets import Configuration, MovementControls, ShapeListbox

VIEWPORT_DIMENSION = (800, 800)
GEOMETRY = "1280x1080"
PROGRAM_NAME = "sistema básico de CG 3D"


class App:
    window: Window
    viewport: Viewport
    display_file: DisplayFile
    root: Tk
    frame: ttk.Frame
    selected_shape: Shape | None
    selected_shape_old_color: str
    shape_listbox: ShapeListbox
    movement_controls: MovementControls
    configuration: Configuration
    animation_running: bool

    def redraw_viewport(func):
        @wraps(func)
        def wrapper(self: "App", *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.viewport.draw(self.window, self.display_file)
            return result

        return wrapper

    def bind_event(self, callback: Callable[[str | None], None], event: str, has_data: bool = True):
        if not has_data:
            self.root.bind(event, callback)
        else:
            # tkinter does not handle events that send data.
            # see: https://stackoverflow.com/a/41912425
            self.root.call("bind", str(self.root), event, self.root.register(callback) + " %d")

    @redraw_viewport
    def add_shape(self, data: str):
        try:
            data = json.loads(data)

            if "points" in data:
                points = [Vector3(*coords) for coords in data["points"]]
            elif "lines" in data:
                lines = [(Vector3(*a[0]), Vector3(*a[1])) for a in data["lines"]]
            name = data["name"]

            idx = 1
            while self.display_file.get_shape_by_id(f"{data['type'].title()}[{name}]") is not None:
                if name.endswith(f"-{idx-1}"):
                    name = name.replace(f"-{idx-1}", f"-{idx}")
                else:
                    name += f"-{idx}"
                idx += 1

            color = data["color"]
            shape = None
            match data["type"]:
                case "point":
                    shape = Point3D(points, name, color)
                case "line":
                    shape = Line(points, name, color)
                case "wireframe":
                    shape = Wireframe3D(lines, name, color)
                case "bspline":
                    shape = BSpline(
                        points,
                        name,
                        color,
                        int(data["points_per_segment"]),
                    )
                case "curve3d":
                    control_points = [(Vector3(*a)) for a in data["control_points"]]
                    shape = Curve3D(control_points, name, color, int(data["points_per_segment"]))
                case "bspline3d":
                    control_points = [[Vector3(*a) for a in line] for line in data["control_points"]]
                    shape = BSpline3D(control_points, name, color, int(data["points_per_segment"]))

            print(f"Added shape: {shape}")
            self.display_file.append(shape)
            self.shape_listbox.shapes_str_var.set(self.display_file._shapes)
        except:
            traceback.print_exc()

    def save_shapes(self, filename):
        if self.selected_shape:
            self.selected_shape.color = self.selected_shape_old_color
        DescritorOBJ.save(self.display_file, self.shape_listbox.add_object.color_hex_name, filename)

        if self.selected_shape:
            self.selected_shape.color = "gold"

    @redraw_viewport
    def load_shapes(self, filename):
        self.display_file.all_dirty()
        self.viewport.clean(self.display_file)
        self.display_file, hex_color_names = DescritorOBJ.load(filename)

        names_color_hex = {name: color_hex for color_hex, name in hex_color_names.items()}
        self.shape_listbox.add_object.color_hex_name |= names_color_hex
        self.shape_listbox.shapes_str_var.set(self.display_file._shapes)
        self.window.reset()

    @redraw_viewport
    def rotate_window(self, e):
        if self.animation_running and e is not True:
            return
        match self.configuration.window_rotation.get():
            case "horizontal":
                axis = "X"
            case "vertical":
                axis = "Y"
            case "vpn":
                axis = "Z"
            case "axis":
                axis = None
            case _:
                raise ValueError(f"Invalid window rotation. rotation: {self.configuration.window_rotation.get()}")

        if axis is not None:
            self.window.rotate(self.configuration.rotation_rad, axis)
        else:
            Transformer3D(self.window.points[:] + [self.window.vpn, self.window.vrp]).rotate(
                self.configuration.rotation_rad, self.configuration.rotation_axis
            ).apply()
        self.display_file.all_dirty()

        animate = self.configuration.animate_window_rotation.get() == "on"
        if animate:
            self.root.after(40, self.rotate_window, True)  # 40 ms --> 25 FPS
            self.animation_running = True
        elif self.animation_running:
            self.animation_running = False

    @redraw_viewport
    def move_window(self, direction: str):
        self.window.move(direction, self.configuration.move_step)
        self.display_file.all_dirty()

    @redraw_viewport
    def zoom(self, factor: str):
        self.window.zoom(1 if factor == "+" else -1, self.configuration.zoom_step)
        self.display_file.all_dirty()

    @redraw_viewport
    def translation(self, direction: str):
        self.selected_shape.dirty = True

        vup = [
            self.window.points[3].x - self.window.points[0].x,
            self.window.points[3].y - self.window.points[0].y,
            self.window.points[3].z - self.window.points[0].z,
        ]

        # Normalize vup to reduce the numerical error
        vup_normalized = np.array(vup) / np.linalg.norm(vup)

        step = self.configuration.move_step

        # np.cross returns a vector perpendicular to the normalized vup and [0, 0, 1]
        # the vector [0, 0, 1] is penpendicular to axes x and y, so np.cross return
        # a vector thats is pendicular to vup, x, y and is multiply by the scalar step
        # to give a sensation to a unique direction
        if direction == "R":
            displacement_vector = np.cross(vup_normalized, [0, 0, 1]) * step
        elif direction == "L":
            displacement_vector = -np.cross(vup_normalized, [0, 0, 1]) * step
        # Up and Down dont need np.cross
        elif direction == "U":
            displacement_vector = vup_normalized * step
        elif direction == "D":

            displacement_vector = -vup_normalized * step
        elif direction == "F":
            displacement_vector = [0, 0, step]
        else:
            displacement_vector = [0, 0, -step]

        # Apply the displacement_vector for window points
        for i in range(len(self.selected_shape.points)):
            self.selected_shape.points[i] += Vector3.from_array(displacement_vector)

        center = self.selected_shape.transformer.center(self.selected_shape.points)
        self.configuration.selected_shape_center = center

    @redraw_viewport
    def scale(self, factor: str):
        self.selected_shape.dirty = True

        step = self.configuration.scale_step if factor == "+" else 1 / self.configuration.scale_step

        self.selected_shape.transformer.scale(step).apply()
        center = self.selected_shape.transformer.center(self.selected_shape.points)
        self.configuration.selected_shape_center = center

    @redraw_viewport
    def rotate(self, e):
        self.selected_shape.dirty = True

        self.selected_shape.transformer.rotate(self.configuration.rotation_rad, self.configuration.rotation_axis).apply()
        center = self.selected_shape.transformer.center(self.selected_shape.points)
        self.configuration.selected_shape_center = center

    @redraw_viewport
    def clear_selected_shape(self, e):
        if self.selected_shape:
            self.selected_shape.dirty = True
            self.selected_shape.color = self.selected_shape_old_color
            self.selected_shape = None
            self.configuration.selected_shape_center = None

    @redraw_viewport
    def update_selected_shape(self, selected_shape_id: str):
        if self.selected_shape:
            self.selected_shape.color = self.selected_shape_old_color
            self.selected_shape.dirty = True

        self.selected_shape = self.display_file.get_shape_by_id(selected_shape_id)
        self.selected_shape.dirty = True
        self.selected_shape_old_color = self.selected_shape.color
        self.selected_shape.color = "gold"

        self.configuration.move_window_or_shape.set("SHAPE")
        self.movement_controls.set_moving("SHAPE")
        center = self.selected_shape.transformer.center(self.selected_shape.points)
        self.configuration.selected_shape_center = center

    @redraw_viewport
    def change_line_clipping(self, alg: str):
        print(f"Mudando algoritmo de clipping para {alg}")
        if alg == "cohen":
            Line.clipper = CohenSutherland
        else:
            Line.clipper = LiangBarsky
        self.display_file.all_dirty()

    @redraw_viewport
    def change_projection(self, proj: str):
        print(f"Mudando projeção para {proj}")
        if proj == "perspective":
            self.viewport.projection = perspective_projection
        else:
            self.viewport.projection = parallel_projection
        self.display_file.all_dirty()

    def __create_viewport_and_log(self):
        viewport_frame = ttk.Frame(self.frame, padding="12 -3 12 12")
        viewport_frame.grid(column=6, row=0)

        ttk.Label(viewport_frame, text="Viewport").grid(column=0, row=0, sticky="w")

        self.viewport = Viewport(
            Vector3(0, 0),
            Vector3(VIEWPORT_DIMENSION[0], VIEWPORT_DIMENSION[1]),
            viewport_frame,
            "#ffffff",
        )

        self.viewport.canvas.grid(column=0, row=1)

    def __create_left_menu(self):
        menu_frame = ttk.LabelFrame(self.frame, padding="12 -3 12 12", border=3, borderwidth=3, relief="groove", text="Function Menu")
        menu_frame.grid(column=0, row=0, sticky="NSEW", rowspan=20, columnspan=5)

        left_frame = ttk.Frame(menu_frame)
        left_frame.grid(row=0, column=0)

        right_frame = ttk.Frame(menu_frame)
        right_frame.grid(row=0, column=3)

        self.shape_listbox = ShapeListbox(
            left_frame,
            column=0,
            row=0,
        )

        self.movement_controls = MovementControls(left_frame, column=0, row=4)

        ttk.Separator(menu_frame, orient="vertical").grid(row=0, column=2, rowspan=3, ipady=400, ipadx=10, padx=(30, 10))

        self.configuration = Configuration(right_frame, column=3, row=2)

    def __bind_events(self):
        self.bind_event(lambda move: self.movement_controls.set_moving(move), Events.CHANGE_MOVE)
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
        self.bind_event(self.change_line_clipping, Events.CHANGE_CLIPPING_ALGORITHM, True)
        self.bind_event(self.change_projection, Events.CHANGE_PROJECTION, True)

    def __init__(self):
        self.root = Tk()
        self.root.title(PROGRAM_NAME)
        self.root.geometry(GEOMETRY)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.selected_shape = None
        self.window = Window(
            Vector3(-100, -100, -100),
            Vector3(VIEWPORT_DIMENSION[0], VIEWPORT_DIMENSION[1], -300),
        )
        self.frame = ttk.Frame(self.root, padding="3 3 12 12")
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        # self.frame.rowconfigure(0, weight=1)
        # self.frame.columnconfigure(0, weight=2)
        self.display_file = DisplayFile()
        self.animation_running = False

        self.__create_left_menu()
        self.__create_viewport_and_log()
        self.__bind_events()

        self.load_shapes("./cube_and_pyramid.obj")

        self.add_shape(
            json.dumps(
                {
                    "type": "curve3d",
                    "control_points": [
                        (0.0, 0.0, 100.0),
                        (50.0, 0.0, 125.0),
                        (100.0, 0.0, 125.0),
                        (150.0, 0.0, 100.0),
                        (0.0, 50.0, 125.0),
                        (50.0, 50.0, 175.0),
                        (100.0, 50.0, 175.0),
                        (150.0, 50.0, 125.0),
                        (0.0, 100.0, 125.0),
                        (50.0, 100.0, 175.0),
                        (100.0, 100.0, 175.0),
                        (150.0, 100.0, 125.0),
                        (0.0, 150.0, 100.0),
                        (50.0, 150.0, 125.0),
                        (100.0, 150.0, 125.0),
                        (150.0, 150.0, 100.0),
                    ],
                    "name": "curve3d",
                    "color": "blue",
                    "points_per_segment": 10,
                }
            )
        )

        self.add_shape(
            json.dumps(
                {
                    "type": "bspline3d",
                    "control_points": [
                        [(0.0, 0.0, 100.0), (50.0, 0.0, 125.0), (100.0, 0.0, 125.0), (150.0, 0.0, 100.0)],
                        [(0.0, 50.0, 125.0), (50.0, 50.0, 175.0), (100.0, 50.0, 175.0), (150.0, 50.0, 125.0)],
                        [(0.0, 100.0, 125.0), (50.0, 100.0, 175.0), (100.0, 100.0, 175.0), (150.0, 100.0, 125.0)],
                        [(0.0, 150.0, 100.0), (50.0, 150.0, 125.0), (100.0, 150.0, 125.0), (150.0, 150.0, 100.0)],
                    ],
                    "name": "bspline3d",
                    "color": "red",
                    "points_per_segment": 10,
                }
            )
        )

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
