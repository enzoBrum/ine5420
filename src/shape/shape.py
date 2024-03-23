from abc import ABC, abstractproperty
from typing import Optional
from uuid import uuid4

import numpy as np

from vector3 import Vector3


class Shape(ABC):
    color: str
    name: str
    shape_name: str
    points: list[Vector3]

    def __init__(
        self, points: list[Vector3], name: Optional[str] = None, color: str = "red"
    ) -> None:
        self.color = color
        self.name = name if name else uuid4().hex
        self.points = points

    def __str__(self) -> str:
        return f"{self.shape_name}[{self.name}]"

    # def rotate(self, degree: float, axis: str) -> None:
    #     for i in range(len(self.points)):
    #         point = self.points[i]
    #         array = np.matmul(np.array([point.x, point.y, point.z]), np.array([[np.cos(degree), -np.sin(degree), 0],
    #                                                                           [np.sin(degree), np.cos(degree), 0],
    #         self.points[i] = Vector3.from_array(array)                         [0, 0, 1]]))
    #
    # def translation(self, offset: float) -> None:
    #     for i in range(len(self.points)):
    #         point = self.point[i]
    #         array = np.matmul(np.array([point.x, point.y, point.z]), np.array([[1, 0, 0],
    #                                                                           [0, 1, 0],
    #         self.points[i] = Vector3.from_array(array)                        [0, 0, 1]]))
    #
    # def scale(self, factor: float) -> None:
    #     matrix = np.array(
    #         [
    #             [factor, 0, 0],
    #             [0, factor, 0],
    #             [0,0,1]
    #         ]
    #     )
    #     for i in range(len(self.points)):
    #         point = np.array([self.points[i].x, self.points[i].y, self.points[i].z])
    #         self.points[i] = np.matmul(point, matrix)
    #
