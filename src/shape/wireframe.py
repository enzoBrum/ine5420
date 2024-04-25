from tkinter import Canvas

from clipping import SutherlandHodgman
from vector3 import Vector3

from .shape import Shape
from .utils import ignore_lines_in_window_border


class Wireframe(Shape):
    shape_name: str = "Wireframe"
    fill: bool
    clipper = SutherlandHodgman

    def __init__(
        self,
        points: list[Vector3],
        fill: bool,
        name: str | None = None,
        color: str = "red",
    ) -> None:
        self.fill = fill
        super().__init__(points, name, color)

    def serialize(
        self, vertices: dict[Vector3, int], hex_to_color: dict[str, str]
    ) -> str:
        return (
            f"o {self.name}\n"
            f"usemtl {hex_to_color[self.color]}\n"
            f"f {' '.join([vertices[p] for p in self.points])}"
        )

    def process_clipped_points(
        self,
        points: list[Vector3],
        transformed_points: list[Vector3],
        window_min: Vector3,
        window_max: Vector3,
    ) -> list[Vector3]:
        if self.fill or not len(transformed_points):
            return transformed_points

        points.append(points[0])
        transformed_points.append(transformed_points[0])
        return ignore_lines_in_window_border(
            points, transformed_points, window_min, window_max
        )

    def draw(self, canvas: Canvas, points: list[Vector3]):
        if self.fill:
            canvas.create_polygon(
                *[(p.x, p.y) for p in points],
                fill=self.color,
            )
        else:
            new_points = []
            for i in range(0, len(points), 2):
                new_points.append((points[i], pointts[i + 1]))
            for p1, p2 in new_points:
                canvas.create_line(p1.x, p1.y, p2.x, p2.y, width=3, fill=self.color)
