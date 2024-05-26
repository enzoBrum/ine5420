from copy import deepcopy
from itertools import batched
from tkinter import Canvas

from numpy import arange

from clipping import BezierClipper
from shape import Shape
from vector3 import Vector3

from .utils import ignore_lines_in_window_border


class Curve2D(Shape):
    shape_name: str = "Curve2D"
    points_per_segment: int
    clipper = BezierClipper

    def __init__(
        self,
        points: list[Vector3],
        name: str | None = None,
        color: str = "red",
        points_per_segment: int = 10,
    ) -> None:
        super().__init__(points, name, color)
        self.points_per_segment = min(max(points_per_segment, 10), 100)
        self._bezier()

    def _bezier(self) -> None:
        new_points = []

        print(self.points, self.points_per_segment)

        for i in range(0, len(self.points) - 3, 3):
            p1 = self.points[i]
            p2 = self.points[i + 1]
            p3 = self.points[i + 2]
            p4 = self.points[i + 3]

            print(f"p1: {p1}, p2: {p2}, p3: {p3}, p4: {p4}")

            r1 = p2
            r4 = p3

            print(f"r1: {r1}, r4: {r4}")

            for t in arange(0, 1, 1 / self.points_per_segment):
                # t2 = t * t
                # t3 = t2 * t

                # h1 = 2 * t3 - 3 * t2 + 1
                # h2 = -2 * t3 + 3 * t2
                # h3 = t3 - 2 * t2 + t
                # h4 = t3 - t2

                texp = 1 - t
                texp2 = texp * texp
                texp3 = texp2 * texp

                h1 = texp3
                h2 = 3 * texp2 * t
                h3 = 3 * texp * t * t
                h4 = t * t * t

                px = h1 * p1.x + h2 * p2.x + h3 * p3.x + h4 * p4.x
                py = h1 * p1.y + h2 * p2.y + h3 * p3.y + h4 * p4.y
                pz = h1 * p1.z + h2 * p2.z + h3 * p3.z + h4 * p4.z

                new_points.append(Vector3(px, py, pz))

        self.points = new_points
        self.ppc_points = deepcopy(self.points)
        print(f"BEZIER 2D: {self.points}")

    def serialize(self, vertices: dict[Vector3, int], hex_to_color: dict[str, str]) -> str:
        raise NotImplementedError

    def process_clipped_points(
        self,
        points: list[Vector3],
        transformed_points: list[Vector3],
        window_min: Vector3,
        window_max: Vector3,
    ) -> list[Vector3]:
        return ignore_lines_in_window_border(points, transformed_points, window_min, window_max)

    def draw(self, canvas: Canvas, points: list[Vector3]):
        for p1, p2 in batched(points, 2):
            canvas.create_line(p1.x, p1.y, p2.x, p2.y, width=3, fill=self.color, tags=self.id)
