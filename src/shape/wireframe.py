from itertools import batched, chain
from tkinter import Canvas, PhotoImage
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

    def sutherland_hodgman(
        self, window_max: Vector3, window_min: Vector3
    ) -> list[Line]:
        lines: list[Line] = []
        for line in self.lines:
            p, q = line.ppc_points
            print(f"P: {p}, Q: {q}")

            p_inside = (window_min.x <= p.x <= window_max.x) and (
                window_min.y <= p.y <= window_max.y
            )
            q_inside = (window_min.x <= q.x <= window_max.x) and (
                window_min.y <= q.y <= window_max.y
            )

            if p_inside and q_inside:
                print("P e Q dentro")
                lines.append(Line(p, q))
            elif p_inside and not q_inside:
                print("P dentro e Q fora")
                p, q = Line(p, q).liang_barsky(window_max, window_min)
                lines.append(Line(p, q))
            elif not p_inside and q_inside:
                print("P fora e Q dentro")
                p, q = Line(p, q).liang_barsky(window_max, window_min)
                lines.append(Line(p, q))
            elif not p_inside and not q_inside:
                print("P e Q fora")
                if len(p_q := Line(p, q).liang_barsky(window_max, window_min)) > 0:
                    lines.append(Line(p_q[0], p_q[1]))
                else:
                    lines.append(None)

            # print(f"OUTPUT: {[(l.p1.ppc_points, l.p2.ppc_points) for l in lines]}")
        return lines

    def draw(
        self,
        canvas: Canvas,
        viewport_transform: Callable[[list[Vector3]], list[Vector3]],
        window_min: Vector3,
        window_max: Vector3,
    ):
        if len(lines := self.sutherland_hodgman(window_max, window_min)) > 0:
            if self.fill:
                for i, line in enumerate(lines):
                    if line is not None:
                        continue

                    og_line = self.lines[i]
                    line_p = [l for l in lines if l.p1 == og_line.p1]

                points = list(chain(*[l.ppc_points for l in lines]))
                transformed_points = [(p.x, p.y) for p in viewport_transform(points)]
                canvas.create_polygon(*transformed_points, fill=self.color)
                return

            for line in lines:
                if line is None:
                    continue
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
