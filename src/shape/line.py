from tkinter import Canvas
from typing import Callable, Optional

from vector3 import Vector3

from .point import Point
from .shape import Shape


class Line(Shape):
    shape_name: str = "Line"
    __points: list[Point]

    def __init__(
        self, p1: Point, p2: Point, name: Optional[str] = None, color: str = "red"
    ) -> None:
        self.__points = [p1, p2]
        super().__init__(name, color)

    @classmethod
    def from_vector3(
        cls: type["Line"], v1: Vector3, v2: Vector3, *args, **kwargs
    ) -> "Line":
        return cls(Point(v1), Point(v2), *args, **kwargs)

    def draw(
        self,
        canvas: Canvas,
        viewport_transform: Callable[[list[Vector3]], list[Vector3]],
        clipping_func: Callable[["Line"], tuple[Vector3, Vector3] | None],
    ):
        if len(line := clipping_func(self)) > 0:
            p1, p2 = line
            tp1, tp2 = viewport_transform([p1, p2])
            canvas.create_line(tp1.x, tp1.y, tp2.x, tp2.y, fill=self.color, width=3)

    def serialize(
        self, vertices: dict[Vector3, int], hex_to_color: dict[str, str]
    ) -> str:
        return (
            f"o {self.name}\n"
            f"usemtl {hex_to_color[self.color]}\n"
            f"l {vertices[self.p1]} {vertices[self.p2]}\n"
        )

    @property
    def p1(self) -> Point:
        return self.__points[0]

    @property
    def p2(self) -> Point:
        return self.__points[1]

    @property
    def ppc_points(self) -> list[Vector3]:
        return self.p1.ppc_points + self.p2.ppc_points

    @ppc_points.setter
    def ppc_points(self, points: list[Vector3]):
        self.p1.ppc_points = [points[0]]
        self.p2.ppc_points = [points[1]]

    @property
    def points(self) -> list[Vector3]:
        return self.p1.points + self.p2.points
