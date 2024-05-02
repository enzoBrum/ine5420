from abc import ABC, abstractmethod
from math import cos, radians, sin, sqrt
from typing import Literal, Optional

import numpy as np
import numpy.typing as npt

from vector3 import Vector3


class Transformer(ABC):
    transformation_matrix: npt.NDArray
    points: list[Vector3]

    @abstractmethod
    def rotate(self, degree: float, point: Vector3) -> None: ...

    @abstractmethod
    def translation(self, d: Vector3, inverse: bool = False) -> None: ...

    @abstractmethod
    def scale(self, factor: float) -> None: ...

    def center(self, points: list[Vector3]) -> Vector3:
        n = len(points)
        cx = sum(point.x for point in points) / n
        cy = sum(point.y for point in points) / n
        cz = sum(point.z for point in points) / n

        return Vector3(cx, cy, cz)

    @abstractmethod
    def apply(self): ...


class Transformer2D(Transformer):
    def __init__(self, points: Optional[list[Vector3]] = None) -> None:
        self.points = points or []

        # matriz identidade. A x I = A
        self.transformation_matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    def rotate(self, degree: float, point: Vector3) -> None:
        self.translation(-point)

        matrix = np.array([[cos(degree), -sin(degree), 0], [sin(degree), cos(degree), 0], [0, 0, 1]])

        self.transformation_matrix = np.matmul(self.transformation_matrix, matrix)

        self.translation(point)

    def translation(self, d: Vector3, inverse: bool = False) -> None:
        matrix = np.array([[1, 0, 0], [0, 1, 0], [d.x, d.y, 1]])

        if inverse:
            matrix = np.linalg.inv(matrix)

        self.transformation_matrix = np.matmul(self.transformation_matrix, matrix)

    def scale(self, factor: float) -> None:
        c = self.center(self.points)

        self.translation(-c)
        matrix = np.array([[factor, 0, 0], [0, factor, 0], [0, 0, 1]])
        self.transformation_matrix = np.matmul(self.transformation_matrix, matrix)
        self.translation(c)

    def apply(self):
        for i, point in enumerate(self.points):
            point = [point.x, point.y, point.z]
            arr = [round(x, 6) for x in point]

            vec = Vector3.from_array(np.matmul(arr, self.transformation_matrix))

            self.points[i].x = vec.x
            self.points[i].y = vec.y
            self.points[i].z = vec.z


class Transformer3D(Transformer):

    def rotation_matrix(self, axis: Literal["X", "Y", "Z"], degree: float):
        match axis:
            case "X":
                matrix_r = np.array(
                    [
                        [1, 0, 0, 0],
                        [0, cos(degree), sin(degree), 0],
                        [0, -sin(degree), cos(degree), 0],
                        [0, 0, 0, 1],
                    ]
                )
            case "Y":
                matrix_r = np.array(
                    [
                        [cos(degree), 0, -sin(degree), 0],
                        [0, 1, 0, 0],
                        [sin(degree), 0, cos(degree), 0],
                        [0, 0, 0, 1],
                    ]
                )
            case "Z":
                matrix_r = np.array(
                    [
                        [cos(degree), sin(degree), 0, 0],
                        [-sin(degree), cos(degree), 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1],
                    ]
                )
        return matrix_r

    def __init__(self, points: Optional[list[Vector3]] = None) -> None:
        self.points = points or []

        # matriz identidade. A x I = A
        self.transformation_matrix = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

    def rotate(
        self,
        degree: float,
        axis: Vector3,
    ) -> None:
        """
        Roda o mundo em torno de um eixo arbitrário.
        """

        degree = radians(degree)

        # passo 1
        self.translation(-axis)

        # passo 2
        xy_angle = np.arccos(axis.z / sqrt(axis.x**2 + axis.y**2 + axis.z**2))
        matrix = self.rotation_matrix("X", xy_angle)

        # passo 3
        z_angle = np.arccos(axis.y / sqrt(axis.x**2 + axis.y**2 + axis.z**2))
        matrix = np.matmul(matrix, self.rotation_matrix("Z", z_angle))

        # passo 4
        matrix = np.matmul(matrix, self.rotation_matrix("Y", degree))

        # passo 5
        matrix = np.matmul(matrix, np.linalg.inv(self.rotation_matrix("Z", -z_angle)))

        # passo 6
        matrix = np.matmul(matrix, np.linalg.inv(self.rotation_matrix("X", -xy_angle)))

        # passo 7
        self.transformation_matrix = np.matmul(self.transformation_matrix, matrix)
        self.translation(axis, inverse=True)

    def rotate_x_y_z(self, rad: float, axis: Literal["X", "Y", "Z"]) -> None:
        """
        Roda o mundo em torno do eixo X, Y ou Z
        """

        matrix = self.rotation_matrix(axis, rad)
        self.transformation_matrix = np.matmul(self.transformation_matrix, matrix)

    def translation(self, d: Vector3, inverse: bool = False) -> None:
        matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [d.x, d.y, d.z, 1]])

        if inverse:
            matrix = np.linalg.inv(matrix)

        self.transformation_matrix = np.matmul(self.transformation_matrix, matrix)

    def scale(self, factor: float) -> None:
        c = self.center(self.points)

        self.translation(-c)

        matrix = np.array([[factor, 0, 0, 0], [0, factor, 0, 0], [0, 0, factor, 1], [0, 0, 0, 1]])

        self.transformation_matrix = np.matmul(self.transformation_matrix, matrix)
        self.translation(c)

    def apply(self):
        for i, p in enumerate(self.points):
            arr = np.array([p.x, p.y, p.z, 1])
            vec = Vector3.from_array(np.matmul(arr, self.transformation_matrix))

            self.points[i].x = vec.x
            self.points[i].y = vec.y
            self.points[i].z = vec.z
