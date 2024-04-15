from itertools import batched, chain
from tkinter import Canvas
from typing import Callable, Optional

from shape.line import Line
from vector3 import Vector3

from .shape import Shape


class Wireframe(Shape):
    shape_name: str = "Wireframe"
    fill: bool
    lines: list[Line]

    def __init__(
        self,
        lines: list[Line],
        fill: bool,
        name: Optional[str] = None,
        color: str = "red",
    ) -> None:
        self.lines = lines
        self.fill = fill
        super().__init__(name, color)

    @classmethod
    def from_vector3(
        cls: type["Wireframe"], points: list[Vector3], *args, **kwargs
    ) -> "Wireframe":
        lines = []
        for i in range(len(points)):
            lines.append(Line.from_vector3(points[i], points[(i + 1) % len(points)]))
        return cls(lines, *args, **kwargs)

    def draw(
        self,
        canvas: Canvas,
        viewport_transform: Callable[[list[Vector3]], list[Vector3]],
        clipping_func: Callable[[list[Line]], list[Line]],
    ):
        if len(lines := clipping_func(self.lines)) > 0:
            if self.fill:
                canvas.create_polygon(*[l.ppc_points for l in lines], fill=self.color)
                return

            for line in lines:
                p1, p2 = viewport_transform(line.ppc_points)
                canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill=self.color, width=3)

    def serialize(
        self, vertices: dict[Vector3, int], hex_to_color: dict[str, str]
    ) -> str:
        return (
            f"o {self.name}\n"
            f"usemtl {hex_to_color[self.color]}\n"
            f"f {' '.join([vertices[p] for p in self.points])}"
        )

    @property
    def points(self) -> list[Vector3]:
        points = []
        for line in self.lines:
            points += line.points
        return points

    @property
    def ppc_points(self) -> list[Vector3]:
        points = []
        for line in self.lines:
            points += line.ppc_points
        return points

    @ppc_points.setter
    def ppc_points(self, points: list[Vector3]):
        points = list(batched(points, 2))
        for i, line in enumerate(self.lines):
            line.ppc_points = points[i]
