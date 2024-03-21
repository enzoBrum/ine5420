from tkinter import Canvas, Misc

from line import Line
from point import Point
from shape import Shape
from vector2 import Vector2
from wireframe import Wireframe


class Viewport:
    _canvas: Canvas

    def __init__(
        self,
        vector1: Vector2,
        vector2: Vector2,
        parent: Misc,
        background_color: str = "gray75",
    ):
        self._min = vector1
        self._max = vector2

        canvas_size = vector2 - vector1
        self._canvas = Canvas(
            parent,
            width=canvas_size.x,
            height=canvas_size.y,
            background=background_color,
            highlightthickness=3,
            highlightbackground="gray"

        )

    @property
    def canvas(self) -> Canvas:
        return self._canvas

    def _viewport_transform(
        self, window_min: Vector2, window_max: Vector2, points: list[Vector2]
    ) -> list[Vector2]:
        for point in points:
            point.x = ((point.x - window_min.x) / (window_max.x - window_min.x)) * (
                self._max.x - self._min.x
            )
            point.y = (1 - (point.y - window_min.y) / (window_max.y - window_min.y)) * (
                self._max.y - self._min.y
            )

        return points

    def draw(self, window_min: Vector2, window_max: Vector2, display_file: list[Shape]):
        self.canvas.delete("all")

        # points = self._viewport_transform(window_min, window_max, [Vector2(window_min.x, window_min.y),
        # Vector2(window_max.x, window_max.y)])
        # self.canvas.create_rectangle(points[0].x, points[0].y, points[1].x, points[1].y, fill="red", width=10)
        for shape in display_file:
            if isinstance(shape, Point):
                point = self._viewport_transform(
                    window_min, window_max, [Vector2(shape.x, shape.y)]
                )[0]
                self.canvas.create_oval(
                    point.x - 3, point.y - 3, point.x + 3, point.y + 3, fill="red"
                )
            elif isinstance(shape, Line):
                points = self._viewport_transform(
                    window_min,
                    window_max,
                    [
                        Vector2(shape.point1.x, shape.point1.y),
                        Vector2(shape.point2.x, shape.point2.y),
                    ],
                )
                self.canvas.create_line(
                    points[0].x,
                    points[0].y,
                    points[1].x,
                    points[1].y,
                    fill="red",
                    width=10,
                )
            elif isinstance(shape, Wireframe):
                points = self._viewport_transform(
                    window_min,
                    window_max,
                    [Vector2(point.x, point.y) for point in shape.points],
                )
                for i in range(len(points) - 1):
                    self.canvas.create_line(
                        points[i].x,
                        points[i].y,
                        points[i + 1].x,
                        points[i + 1].y,
                        fill="red",
                        width=5,
                    )

                self.canvas.create_line(
                    points[-1].x,
                    points[-1].y,
                    points[0].x,
                    points[0].y,
                    fill="red",
                    width=5,
                )
