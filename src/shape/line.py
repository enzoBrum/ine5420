from tkinter import Canvas

from clipping import CohenSutherland
from vector3 import Vector3

from .shape import Shape


class Line(Shape):
    shape_name: str = "Line"
    clipper = CohenSutherland

    def draw(
        self,
        canvas: Canvas,
        points: list[Vector3],
    ):
        p1, p2 = points
        canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill=self.color, width=3, tags=self.id)

    def serialize(self, vertices: dict[Vector3, int], hex_to_color: dict[str, str]) -> str:
        return f"o {self.name}\nusemtl {hex_to_color[self.color]}\nl {vertices[self.p1]} {vertices[self.p2]}\n"
