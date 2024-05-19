from copy import deepcopy
from tkinter import Canvas, Misc
from typing import Callable

from display_file import DisplayFile
from interface.window import Window
from projections import parallel_projection, perspective_projection
from shape import Shape
from vector3 import Vector3


class Viewport:
    _canvas: Canvas
    _min: Vector3
    _max: Vector3
    projection: Callable[[Window, DisplayFile], None]

    def __init__(
        self,
        min_vec: Vector3,
        max_vec: Vector3,
        parent: Misc,
        background_color: str = "gray75",
    ):
        self._min = min_vec
        self._max = max_vec
        self.projection = perspective_projection

        canvas_size = self._max - self._min
        self._canvas = Canvas(
            parent,
            width=canvas_size.x,
            height=canvas_size.y,
            background=background_color,
            highlightthickness=3,
            highlightbackground="gray",
        )

    @property
    def canvas(self) -> Canvas:
        return self._canvas

    def _viewport_transform(self, window_min: Vector3, window_max: Vector3, points: list[Vector3], zoom: int) -> list[Vector3]:
        converted_points = deepcopy(points)
        const = 0.01 if zoom < 40 else 0.05 if zoom < 70 else 0.025 if zoom < 180 else 0.03 if zoom < 250 else 0.032
        window_max += 10 - zoom * const
        window_min -= 10 - zoom * const

        for point in converted_points:
            point.x = ((point.x - window_min.x) / (window_max.x - window_min.x)) * (self._max.x - self._min.y)
            point.y = (1 - (point.y - window_min.y) / (window_max.y - window_min.y)) * (self._max.y - self._min.y)
        window_min += 10 - zoom * const
        window_max -= 10 - zoom * const

        return converted_points

    def clean(self, display_file: DisplayFile):
        for shape in display_file:
            if shape.dirty:
                self.canvas.delete(shape.id)

    def draw(self, window: Window, display_file: DisplayFile):
        self.clean(display_file)
        self.canvas.create_rectangle(
            10,
            10,
            self._max.x - self._min.x - 10,
            self._max.y - self._min.y - 10,
            outline="red",
        )
        
        for shape in display_file:
            if shape.dirty:
                shape.ppc_points = deepcopy(shape.points)

        self.projection(window, display_file)
        window.ppc_transformation(display_file)

        window_max = window.max_ppc
        window_min = window.min_ppc
        for shape in display_file:
            if not shape.dirty:
                continue
            points = shape.clipper.clip(shape.ppc_points, window_max, window_min)
            transformed_points = self._viewport_transform(window_min, window_max, points, window.n_zoom)
            final_points = shape.process_clipped_points(points, transformed_points, window_min, window_max)

            if not len(final_points):
                continue

            shape.draw(self.canvas, final_points)
            shape.dirty = False
