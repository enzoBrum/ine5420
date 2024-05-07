from tkinter import Canvas
from typing import Callable

from clipping import PointClipper
from vector3 import Vector3

from .shape import Shape


class Point(Shape):
    shape_name: str = "Point"
    clipper = PointClipper
    radius: float = 3.0

    def serialize(self, vertices: dict[Vector3, int], hex_to_color: dict[str, str]) -> str:
        return f"o {self.name}\nusemtl {hex_to_color[self.color]}\np {vertices[self.__point]}"

    def draw(self, canvas: Canvas, point: list[Vector3]):
        x, y, _ = point[0]
        canvas.create_oval(
            x - self.radius,
            y - self.radius,
            x + self.radius,
            y + self.radius,
            tags=self.id
        )
