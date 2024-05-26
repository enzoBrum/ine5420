from tkinter import Canvas

from numpy import array, matmul

from clipping import BezierClipper
from vector3 import Vector3

from .shape import Shape
from .utils import ignore_lines_in_window_border


class BSpline(Shape):
    shape_name: str = "BSpline"
    clipper = BezierClipper

    def __init__(
        self,
        points: list[Vector3],
        name: str | None = None,
        color: str = "red",
        points_per_segment: int = 10,
    ) -> None:
        super().__init__(points, name, color)

        self.points_per_segment = min(max(points_per_segment, 100), 1000)

        self._calculate_delta_matrix()
        self._bsplines()

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

    def _bsplines(self) -> None:
        new_points = []
        coeficients = self.__calculate_coefficients()

        for i in range(len(coeficients["X"])):
            D_x = matmul(self.delta_matrix, coeficients["X"][i])
            D_y = matmul(self.delta_matrix, coeficients["Y"][i])
            D_z = matmul(self.delta_matrix, coeficients["Z"][i])

            points = self.__calculate_segment_points(D_x, D_y, D_z)
            new_points.extend(points)

        self.points = new_points

    def _calculate_delta_matrix(self) -> None:
        delta = 1 / self.points_per_segment
        delta2 = delta * delta
        delta3 = delta2 * delta

        self.delta_matrix = [
            [0, 0, 0, 1],
            [delta3, delta2, delta, 0],
            [6 * delta3, 2 * delta2, 0, 0],
            [6 * delta3, 0, 0, 0],
        ]

    def __calculate_coefficients(self) -> None:
        Mbs = [
            [-1 / 6, 3 / 6, -3 / 6, 1 / 6],
            [3 / 6, -6 / 6, 3 / 6, 0],
            [-3 / 6, 0, 3 / 6, 0],
            [1 / 6, 4 / 6, 1 / 6, 0],
        ]

        coeficients = {"X": [], "Y": [], "Z": []}

        for i in range(3, len(self.points), 1):
            Gbs_x = [
                self.points[i - 3].x,
                self.points[i - 2].x,
                self.points[i - 1].x,
                self.points[i].x,
            ]

            Gbs_y = [
                self.points[i - 3].y,
                self.points[i - 2].y,
                self.points[i - 1].y,
                self.points[i].y,
            ]

            Gbs_z = [
                self.points[i - 3].z,
                self.points[i - 2].z,
                self.points[i - 1].z,
                self.points[i].z,
            ]

            coeficients["X"].append(matmul(Mbs, Gbs_x))
            coeficients["Y"].append(matmul(Mbs, Gbs_y))
            coeficients["Z"].append(matmul(Mbs, Gbs_z))

        return coeficients

    def __calculate_segment_points(self, x_delta: array, y_delta: array, z_delta: array) -> list[Vector3]:
        new_points = []

        x, d_x, d2_x, d3_x = x_delta
        y, d_y, d2_y, d3_y = y_delta
        z, d_z, d2_z, d3_z = z_delta

        new_points.append(Vector3(x, y, z))

        for _ in range(self.points_per_segment - 1):
            x = x + d_x
            y = y + d_y
            z = z + d_z

            d_x = d_x + d2_x
            d_y = d_y + d2_y
            d_z = d_z + d2_z

            d2_x = d2_x + d3_x
            d2_y = d2_y + d3_y
            d2_z = d2_z + d3_z

            new_points.append(Vector3(x, y, z))

        return new_points

    def draw(self, canvas: Canvas, points: list[Vector3]) -> None:
        new_points = []
        for i in range(0, len(points), 2):
            new_points.append((points[i], points[i + 1]))
        for p1, p2 in new_points:
            canvas.create_line(p1.x, p1.y, p2.x, p2.y, width=3, fill=self.color, tags=self.id)
