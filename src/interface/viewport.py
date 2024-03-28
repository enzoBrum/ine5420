from copy import deepcopy
from tkinter import Canvas, Misc

from shape import Shape
from vector3 import Vector3


class Viewport:
    _canvas: Canvas

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
        for point in converted_points:
            point.x = ((point.x - window_min.x) / (window_max.x - window_min.x)) * (
                self._max.x - self._min.x
            )
            point.y = (1 - (point.y - window_min.y) / (window_max.y - window_min.y)) * (
                self._max.y - self._min.y
            )

        return converted_points

    def _inside_window(
        self, points: list[Vector3], window_min: Vector3, window_max: Vector3
    ) -> bool:
        for point in points:
            inside = window_min.x <= point.x <= window_max.x and window_min.y <= point.y
            if not inside:
                return False
        return True

    def draw(self, window_min: Vector3, window_max: Vector3, display_file: list[Shape]):
        self.canvas.delete("all")

        for shape in display_file:
            # if not self._inside_window(shape.points, window_min, window_max):
            #     continue
            points = shape.points
            points = self._viewport_transform(window_min, window_max, points)
            # print(f"{shape.points} --> {points}")
            if len(points) == 1:
                point = points[0]
                self.canvas.create_oval(
                    point.x - 3, point.y - 3, point.x + 3, point.y + 3, fill=shape.color
                )
            else:
                for i in range(len(points) - 1):
                    self.canvas.create_line(
                        points[i].x,
                        points[i].y,
                        points[i + 1].x,
                        points[i + 1].y,
                        fill=shape.color,
                        width=3,
                    )

                self.canvas.create_line(
                    points[-1].x,
                    points[-1].y,
                    points[0].x,
                    points[0].y,
                    fill=shape.color,
                    width=3,
                )
