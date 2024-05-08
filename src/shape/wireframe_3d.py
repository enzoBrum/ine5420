from itertools import batched
from tkinter import Canvas
from typing import Optional

from transformations import Transformer3D
from vector3 import Vector3

from .shape import Shape
from .wireframe import Wireframe


class Wireframe3D(Wireframe):
    shape_name = "Object3D"
    transformer = Transformer3D

    lines: list[tuple[Vector3, Vector3]]

    def __init__(self, lines: list[tuple[Vector3, Vector3]], name: Optional[str] = None, color: str = "red") -> None:
        self.lines = lines
        points = [p for line in lines for p in line]
        print(f"{points=}")
        super().__init__(points, False, name, color)

    def serialize(self, vertices: dict[Vector3, int], hex_to_color: dict[str, str]) -> str: ...

    def process_clipped_points(
        self, points: list[Vector3], transformed_points: list[Vector3], window_min: Vector3, window_max: Vector3
    ) -> list[Vector3]:
        return transformed_points

    def draw(self, canvas: Canvas, points: list[Vector3]):
        for i in range(0, len(points), 2):
            p1, p2 = points[i], points[i + 1]
            x1, y1, _ = p1
            x2, y2, _ = p2
            canvas.create_line(x1, y1, x2, y2, fill=self.color, tags=self.id)
