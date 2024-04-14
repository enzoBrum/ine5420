from copy import deepcopy
from tkinter import Canvas, Misc
from typing import Callable

from clipping import cohen_sutherland, liang_barsky, point_clipping, sutherland_hodgman
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
    line_clipping_function: Callable[[list[Line]], list[Line]]

    def __init__(
        self,
        min_vec: Vector3,
        max_vec: Vector3,
        parent: Misc,
        background_color: str = "gray75",
        line_clipping: Callable[[list[Line]], list[Line]] = cohen_sutherland,
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

        self.line_clipping_function = line_clipping

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

    def _inside_window(
        self, points: list[Vector3], window_min: Vector3, window_max: Vector3
    ) -> bool:
        for point in points:
            inside = window_min.x <= point.x <= window_max.x and window_min.y <= point.y
            if not inside:
                return False
        return True

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

        points = []
        lines = []
        wireframes = []
        for shape in display_file:
            if isinstance(shape, Point):
                points.append(shape)
            elif isinstance(shape, Line):
                lines.append(shape)
            else:
                wireframes.append(shape)

        points = point_clipping(points, window_max, window_min)
        lines = self.line_clipping_function(lines, window_max, window_min)
        wireframes = sutherland_hodgman(wireframes, window_max, window_min)

        # TODO: OOP
        for shape in points + lines + wireframes:
            points = shape.ppc_points
            points = self._viewport_transform(window_min, window_max, points)
            if isinstance(shape, Point):
                point = points[0]
                self.canvas.create_oval(
                    point.x - 3, point.y - 3, point.x + 3, point.y + 3, fill=shape.color
                )
            elif isinstance(shape, Line):
                self.canvas.create_line(
                    points[0].x,
                    points[0].y,
                    points[1].x,
                    points[1].y,
                    fill=shape.color,
                    width=3,
                )
            elif shape.fill:
                self.canvas.create_polygon(
                    *[(p.x, p.y) for p in points],
                    fill=shape.color,
                )
            else:
                for i in range(len(points)):
                    p1_in_window_border = False
                    p2_in_window_border = False
                    same_border = False

                    p1x, p1y = shape.ppc_points[i].x, shape.ppc_points[i].y
                    p2x, p2y = (
                        shape.ppc_points[(i + 1) % len(points)].x,
                        shape.ppc_points[(i + 1) % len(points)].y,
                    )

                    for limit in (window_max, window_min):
                        wx, wy = limit.x, limit.y

                        p1_in_window_border = (
                            abs(p1x - wx) < 1e-6 or abs(p1y - wy) < 1e-6
                        ) or p1_in_window_border

                        p2_in_window_border = (
                            abs(p2x - wx) < 1e-6 or abs(p2y - wy) < 1e-6
                        ) or p2_in_window_border

                        if (abs(p1x - wx) < 1e-6 and abs(p2x - wx) < 1e-6) or (
                            abs(p1y - wy) < 1e-6 and abs(p2y - wy) < 1e-6
                        ):
                            same_border = True

                    if (
                        p1_in_window_border and p2_in_window_border and same_border
                    ):  # TODO: Usar OOP
                        continue

                    self.canvas.create_line(
                        points[i].x,
                        points[i].y,
                        points[(i + 1) % len(points)].x,
                        points[(i + 1) % len(points)].y,
                        fill=shape.color,
                        width=3,
                    )
