from abc import ABC, abstractmethod
from math import cos, radians, sin, sqrt
from typing import Literal, Optional, Self

import numpy as np
import numpy.typing as npt

from vector3 import Vector3


class Transformer(ABC):
    transformation_matrix: npt.NDArray
    points: list[Vector3]

    @abstractmethod
    def rotate(self, degree: float, point: Vector3) -> Self: ...

    @abstractmethod
    def translation(self, d: Vector3, inverse: bool = False) -> Self: ...

    @abstractmethod
    def scale(self, factor: float) -> Self: ...

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

    def rotate(self, degree: float, point: Vector3) -> Self:
        self.translation(-point)

        matrix = np.array([[cos(degree), -sin(degree), 0], [sin(degree), cos(degree), 0], [0, 0, 1]])

        self.transformation_matrix = np.matmul(self.transformation_matrix, matrix)

        self.translation(point)

        return self

    def translation(self, d: Vector3, inverse: bool = False) -> Self:
        matrix = np.array([[1, 0, 0], [0, 1, 0], [d.x, d.y, 1]])

        if inverse:
            matrix = np.linalg.inv(matrix)

        self.transformation_matrix = np.matmul(self.transformation_matrix, matrix)
        return self

    def scale(self, factor: float) -> Self:
        c = self.center(self.points)

        self.translation(-c)
        matrix = np.array([[factor, 0, 0], [0, factor, 0], [0, 0, 1]])
        self.transformation_matrix = np.matmul(self.transformation_matrix, matrix)
        self.translation(c)
        return self

    def apply(self):
        for i, point in enumerate(self.points):
            arr = [round(x, 6) for x in point]

            #print(f"BEFORE: {self.points[i]=}")
            vec = Vector3.from_array(np.matmul(arr, self.transformation_matrix))

            self.points[i].x = vec.x
            self.points[i].y = vec.y
            self.points[i].z = vec.z
            #print(f"AFTER: {self.points[i]=}")


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
    ) -> Self:
        """
        Roda o mundo em torno de um eixo arbitrário.
        """

        magnitude = sqrt(sum([a**2 for a in axis]))
        cx = axis.x / magnitude
        cy = axis.y / magnitude
        cz = axis.z / magnitude

        q0 = cos(degree / 2)
        q1 = sin(degree / 2) * cx
        q2 = sin(degree / 2) * cy
        q3 = sin(degree / 2) * cz

        matrix = [
            [q0**2 + q1**2 - q2**2 - q3**2, 2 * (q1 * q2 - q0 * q3), 2 * (q1 * q3 + q0 * q2), 0],
            [2 * (q1 * q2 + q0 * q3), q0**2 - q1**2 + q2**2 - q3**2, 2 * (q2 * q3 - q0 * q1), 0],
            [2 * (q1 * q3 - q0 * q2), 2 * (q2 * q3 + q0 * q1), q0**2 - q1**2 - q2**2 + q3**2, 0],
            [0, 0, 0, 1],
        ]
        print(matrix)
        self.transformation_matrix = np.matmul(self.transformation_matrix, matrix)
        return self

    def rotate_x_y_z(self, rad: float, axis: Literal["X", "Y", "Z"]) -> Self:
        """
        Roda o mundo em torno do eixo X, Y ou Z
        """

        matrix = self.rotation_matrix(axis, rad)
        self.transformation_matrix = np.matmul(self.transformation_matrix, matrix)
        return self

    def translation(self, d: Vector3, inverse: bool = False) -> Self:
        matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [d.x, d.y, d.z, 1]])

        if inverse:
            matrix = np.linalg.inv(matrix)

        self.transformation_matrix = np.matmul(self.transformation_matrix, matrix)
        return self

    def scale(self, factor: float) -> Self:
        c = self.center(self.points)

        self.translation(-c)

        matrix = np.array([[factor, 0, 0, 0], [0, factor, 0, 0], [0, 0, factor, 0], [0, 0, 0, 1]])

        self.transformation_matrix = np.matmul(self.transformation_matrix, matrix)
        self.translation(c)
        return self

    def apply(self) -> None:
        for i, p in enumerate(self.points):
            arr = [round(x, 6) for x in list(p) + [1]]
            vec = Vector3.from_array(np.matmul(np.array(arr), self.transformation_matrix))

            self.points[i].x = vec.x
            self.points[i].y = vec.y
            self.points[i].z = vec.z

        self.transformation_matrix = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
