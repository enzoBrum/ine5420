from copy import deepcopy
from functools import partial
from tkinter import Canvas, Misc
from typing import Callable

from interface.window import Window
from shape import Shape
from shape.line import Line
from shape.point import Point
from shape.wireframe import Wireframe
from vector3 import Vector3


class Viewport:
    _canvas: Canvas
    _min: Vector3
    _max: Vector3

    def __init__(
        self,
        min_vec: Vector3,
        max_vec: Vector3,
        parent: Misc,
        background_color: str = "gray75",
    ):
        self._min = min_vec
        self._max = max_vec

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

    def _viewport_transform(
        self, window_min: Vector3, window_max: Vector3, points: list[Vector3]
    ) -> list[Vector3]:
        converted_points = deepcopy(points)
        window_max += 10
        window_min -= 10
        for point in converted_points:
            point.x = ((point.x - window_min.x) / (window_max.x - window_min.x)) * (
                self._max.x - self._min.y
            )
            point.y = (1 - (point.y - window_min.y) / (window_max.y - window_min.y)) * (
                self._max.y - self._min.y
            )
        window_min += 10
        window_max -= 10

        return converted_points

    def draw(self, window: Window, display_file: list[Shape]):
        self.canvas.delete("all")
        self.canvas.create_rectangle(
            10,
            10,
            self._max.x - self._min.x - 10,
            self._max.y - self._min.y - 10,
            outline="red",
        )

        window.ppc_transformation(display_file)

        window_max = window.max_ppc
        window_min = window.min_ppc

        viewport_transform = partial(self._viewport_transform, window_min, window_max)
        for shape in display_file:
            shape.draw(self.canvas, viewport_transform, window_min, window_max)
