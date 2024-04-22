from itertools import batched
from tkinter import Canvas

from clipping import SutherlandHodgman
from vector3 import Vector3

from .shape import Shape

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

    def process_clipped_points(self, points: list[Vector3], transformed_points: list[Vector3], window_min: Vector3, window_max: Vector3) -> list[Vector3]:
        if self.fill:
            return transformed_points

        returned_points = []
        for i in range(len(points)):
            p1_in_window_border = False
            p2_in_window_border = False
            same_border = False

            p1x, p1y = points[i].x, points[i].y
            p2x, p2y = points[(i+1) % len(points)].x, points[(i+1) % len(points)].y

            for limit in (window_max, window_min):
                wx, wy = limit.x, limit.y

                p1_in_window_border = (
                    abs(p1x - wx) < 1e-6 or abs(p1y - wy) < 1e-6
                ) or p1_in_window_border

                p2_in_window_border = (
                    abs(p2x - wx) < 1e-6 or abs(p2y - wy) < 1e-6
                ) or p2_in_window_border

                if (abs(p1x - wx) < 1e-6 and abs(p2x - wx) < 1e-6) or (
                    abs(p1y - wy) < 1e-6 and abs(p2y - wy) < 1e-6
                ):
                    same_border = True

            if (
                p1_in_window_border and p2_in_window_border and same_border
            ): 
                continue

            returned_points.append(transformed_points[i])
            returned_points.append(transformed_points[(i+1) % len(transformed_points)])

        return returned_points

    def draw(self, canvas: Canvas, points: list[Vector3]):
        if self.fill:
            canvas.create_polygon(
                *[(p.x, p.y) for p in points],
                fill=self.color,
            )
        else:
            points: list[tuple[Vector3, Vector3]] = batched(points, 2)
            for p1, p2 in points:
                canvas.create_line(p1.x, p1.y, p2.x, p2.y, width=3, fill=self.color)
