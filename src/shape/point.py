from copy import deepcopy
from tkinter import Canvas
from typing import Callable, Optional

from vector3 import Vector3

from .shape import Shape


class Point(Shape):
    shape_name: str = "Point"
    __point: Vector3
    __ppc_point: Vector3
    radius: float = 1.5

    def __init__(
        self, point: Vector3, name: Optional[str] = None, color: str = "red"
    ) -> None:
        self.__point = point
        self.__ppc_point = deepcopy(self.__point)
        super().__init__(name, color)

    def serialize(
        self, vertices: dict[Vector3, int], hex_to_color: dict[str, str]
    ) -> str:
        return (
            f"o {self.name}\n"
            f"usemtl {hex_to_color[self.color]}\n"
            f"p {vertices[self.__point]}"
        )

    def point_clipping(self, window_max: Vector3, window_min: Vector3) -> bool:
        return (
            window_min.x <= self.ppc_points[0].x <= window_max.x
            and window_min.y <= self.ppc_points[0].y <= window_max.y
        )

    def draw(
        self,
        canvas: Canvas,
        viewport_transform: Callable[[list[Vector3]], list[Vector3]],
        window_min: Vector3,
        window_max: Vector3,
    ):
        if self.point_clipping(window_max, window_min, self.__ppc_point):
            x, y = viewport_transform([self.__ppc_point])
            canvas.create_oval(
                x - self.radius,
                y - self.radius,
                x + self.radius,
                y + self.radius,
            )

    @property
    def points(self) -> list[Vector3]:
        return [self.__point]

    @property
    def ppc_points(self) -> list[Vector3]:
        return [self.__ppc_point]

    @ppc_points.setter
    def ppc_points(self, points: list[Vector3]):
        self.__ppc_point = points[0]

    @property
    def x(self) -> float:
        return self.__point.x

    @property
    def y(self) -> float:
        return self.__point.y

    @property
    def z(self) -> float:
        return self.__point.z
