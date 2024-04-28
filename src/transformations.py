from abc import ABC, abstractmethod
from enum import _EnumNames
from math import sin, cos, radians, sqrt
from typing import Literal

import numpy as np
import numpy.typing as npt

from vector3 import Vector3


class Transformer(ABC):
    @abstractmethod
    @classmethod
    def rotate(cls, degree: float, point: Vector3, points: list[Vector3]) -> None: ...

    @abstractmethod
    @classmethod
    def translation(cls, d: Vector3, points: list[Vector3]) -> None: ...

    @abstractmethod
    @classmethod
    def scale(cls, factor: float, points: list[Vector3]) -> None: ...

    @abstractmethod
    @classmethod
    def center(cls, points: list[Vector3]) -> Vector3:
        n = len(points)
        cx = sum(point.x for point in points) / n
        cy = sum(point.y for point in points) / n
        cz = sum(point.z for point in points) / n

        return Vector3(cx, cy, cz)


class Transformer2D(Transformer):
    @classmethod
    def rotate(cls, degree: float, point: Vector3, points: list[Vector3]) -> None:
        degree = radians(degree)
        matrix_t = cls.create_translation_matrix(
            (point.x, point.y), Vector3(0, 0, 1), 1
        )
        matrix_r = np.array(
            [[cos(degree), -sin(degree), 0], [sin(degree), cos(degree), 0], [0, 0, 1]]
        )
        matrix_t2 = cls.create_translation_matrix(
            (point.x, point.y), Vector3(0, 0, 1), -1
        )

        matrix = np.matmul(matrix_t, matrix_r)
        matrix = np.matmul(matrix, matrix_t2)

        for i in range(len(points)):
            point = [points[i].x, points[i].y, points[i].z]
            point = [round(x, 6) for x in point]
            point = np.array(point)
            points[i] = Vector3.from_array(np.matmul(point, matrix))

    @classmethod
    def translation(cls, d: Vector3, points: list[Vector3]) -> None:
        matrix = np.array([[1, 0, 0], [0, 1, 0], [d.x, d.y, 1]])
        for i in range(len(points)):
            point = np.array([points[i].x, points[i].y, points[i].z])
            points[i] = Vector3.from_array(np.matmul(point, matrix))

    @classmethod
    def scale(cls, factor: float, points: list[Vector3]) -> None:
        c = cls.center(points)

        matrix_t = cls.create_translation_matrix(c, Vector3(0, 0, 1), 1)
        matrix_s = np.array([[factor, 0, 0], [0, factor, 0], [0, 0, 1]])
        matrix_t2 = cls.create_translation_matrix(c, Vector3(0, 0, 1), -1)

        matrix = np.matmul(matrix_t, matrix_s)
        matrix = np.matmul(matrix, matrix_t2)

        for i in range(len(points)):
            point = np.array([points[i].x, points[i].y, points[i].z])
            points[i] = Vector3.from_array(np.matmul(point, matrix))

    @classmethod
    def create_translation_matrix(
        cls, center: tuple[float, float], point: Vector3, center_mult: float
    ) -> npt.NDArray[np.float32]:
        cx, cy = center
        return np.array(
            [
                [1, 0, 0],
                [0, 1, 0],
                [point.x - cx * center_mult, point.y - cy * center_mult, 1],
            ]
        )


class Transformer3D(Transformer):

    # @classmethod
    # def rotation_matrix(axis: Literal["X", "Y", "Z"], degree: float):
    #     match axis:
    #         case "X":
    #             matrix_r = np.array(
    #                 [
    #                     [1, 0, 0, 0],
    #                     [0, cos(degree), sin(degree), 0],
    #                     [0, -sin(degree), cos(degree), 0],
    #                     [0, 0, 0, 1],
    #                 ]
    #             )
    #         case "Y":
    #             matrix_r = np.array(
    #                 [
    #                     [cos(degree), 0, -sin(degree), 0],
    #                     [0, 1, 0, 0],
    #                     [sin(degree), 0, cos(degree), 0],
    #                     [0, 0, 0, 1],
    #                 ]
    #             )
    #         case "Z":
    #             matrix_r = np.array(
    #                 [
    #                     [cos(degree), sin(degree), 0, 0],
    #                     [-sin(degree), cos(degree), 0, 0],
    #                     [0, 0, 1, 0],
    #                     [0, 0, 0, 1],
    #                 ]
    #             )
    #     return matrix_r

    @classmethod
    def rotate(
        cls,
        degree: float,
        axis: Vector3,
        points: list[Vector3]
    ) -> None:

        degree = radians(degree)

        """# passo 1
        matrix_t = cls.create_translation_matrix(point, Vector3(0, 0, 0), 1)

        # passo 2
        center = cls.center(points)
        xy_angle = np.arccos(center.z / sqrt(center.x**2 + center.y**2 + center.z**2))
        matrix = np.matmul(matrix_t, cls.rotation_matrix("X", xy_angle))

        # passo 3
        z_angle = np.arccos(center.y / sqrt(center.x**2 + center.y**2 + center.z**2))
        matrix = np.matmul(matrix, cls.rotation_matrix("Z", z_angle))

        # passo 4
        matrix = np.matmul(matrix, cls.rotation_matrix("Y", degree))

        # passo 5
        matrix = np.matmul(matrix, np.linalg.inv(cls.rotation_matrix("Z", -z_angle)))

        # passo 6
        matrix = np.matmul(matrix, np.linalg.inv(cls.rotation_matrix("X", -xy_angle)))

        # passo 7
        matrix_t2 = cls.create_translation_matrix(point, Vector3(0, 0, 0), -1)
        matrix = np.matmul(matrix, matrix_t2)"""

        magnitude = sqrt(sum([a**2 for a in axis]))
        cx = axis.x / magnitude
        cy = axis.y / magnitude
        cz = axis.z / magnitude

        q0 = cos(degree / 2)
        q1 = sin(degree / 2) * cx
        q2 = sin(degree / 2) * cy
        q3 = sin(degree / 2) * cz

        matrix = [
            [q0**2 + q1**2 - q2**2 - q3**2, 2 * (q1 * q2 - q0 * q3), 2 * (q1 * q3 + q0 * q2)],
            [2 * (q1 * q2 + q0 * q3), q0**2 - q1**2 + q2**2 - q3**2, 2 * (q2 * q3 - q0 * q1)],
            [2 * (q1 * q3 - q0 * q2), 2 * (q2 * q3 + q0 * q1), q0**2 - q1**2 - q2**2 + q3**2]
        ]

        for i, p in enumerate(points):
            arr = np.array([p.x, p.y, p.z])
            points[i] = Vector3.from_array(np.matmul(arr, matrix))

    @classmethod
    def translation(
        cls, dx: float, dy: float, dz: float, points: list[Vector3]
    ) -> None:
        matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [dx, dy, dz, 1]])
        for i in range(len(points)):
            point = np.array([points[i].x, points[i].y, points[i].z, 1])
            points[i] = Vector3.from_array(np.matmul(point, matrix))

    @classmethod
    def scale(cls, factor: float, points: list[Vector3]) -> None:
        c = cls.center(points)

        matrix_t = cls.create_translation_matrix(c, Vector3(0, 0, 1), 1)
        matrix_s = np.array(
            [[factor, 0, 0, 0], [0, factor, 0, 0], [0, 0, factor, 1], [0, 0, 0, 1]]
        )
        matrix_t2 = cls.create_translation_matrix(c, Vector3(0, 0, 1), -1)

        matrix = np.matmul(matrix_t, matrix_s)
        matrix = np.matmul(matrix, matrix_t2)

        for i in range(len(points)):
            point = np.array([points[i].x, points[i].y, points[i].z, 1])
            points[i] = Vector3.from_array(np.matmul(point, matrix))

    @classmethod
    def create_translation_matrix(
        cls,
        center: Vector3 | tuple[float, float, float],
        point: Vector3,
        center_mult: float,
    ) -> npt.NDArray[np.float32]:
        cx, cy, cz = center
        return np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [
                    point.x - cx * center_mult,
                    point.y - cy * center_mult,
                    point.z - cz * center_mult,
                ],
            ],
        )
