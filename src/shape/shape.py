from abc import ABC, abstractproperty
from typing import Optional
from uuid import uuid4
from math import sin, cos, radians

import numpy as np
import numpy.typing as npt

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

    def rotate(self, degree: float, point: Vector3) -> None:
        degree = radians(degree)
        matrix_t = self.__create_translation_matrix((point.x, point.y), Vector3(0,0,1), 1)
        matrix_r = np.array(
            [
                 [cos(degree), -sin(degree), 0],
                 [sin(degree), cos(degree), 0],
                 [0, 0, 1]
            ]
        )
        matrix_t2 = self.__create_translation_matrix((point.x, point.y), Vector3(0,0,1), -1)

        matrix = np.matmul(matrix_t, matrix_r)
        matrix = np.matmul(matrix, matrix_t2)
        
        for i in range(len(self.points)):
            point = np.array([self.points[i].x, self.points[i].y, self.points[i].z])
            self.points[i] = Vector3.from_array(np.matmul(point, matrix)) 


    def translation(self, dx: float, dy: float) -> None:
        matrix = np.array(
            [
                 [1, 0, 0],
                 [0, 1, 0],
                 [dx, dy, 1]
            ]
        )
        for i in range(len(self.points)):
            point = np.array([self.points[i].x, self.points[i].y, self.points[i].z])
            self.points[i] = Vector3.from_array(np.matmul(point, matrix)) 
    
    def scale(self, factor: float) -> None:
        center = self.center
        
        matrix_t = self.__create_translation_matrix(center, Vector3(0, 0, 1), 1)
        matrix_s = np.array(
            [
                [factor, 0, 0],
                [0, factor, 0],
                [0,0,1]
            ]
        )
        matrix_t2 = self.__create_translation_matrix(center, Vector3(0, 0, 1), -1)

        matrix = np.matmul(matrix_t, matrix_s)
        matrix = np.matmul(matrix, matrix_t2)

        for i in range(len(self.points)):
            og_point = self.points[i]
            point = np.array([self.points[i].x, self.points[i].y, self.points[i].z])
            self.points[i] = Vector3.from_array(np.matmul(point, matrix))

    def __create_translation_matrix(self, center: tuple[float, float], point: Vector3, center_mult: float) -> npt.NDArray[np.float32]:
        cx, cy = center
        return np.array(
            [
                 [1, 0, 0],
                 [0, 1, 0],
                 [point.x - cx*center_mult, point.y - cy*center_mult, 1]
            ]
        )
    
    @property
    def center(self) -> tuple[float, float]:
        n = len(self.points)
        cx = sum(point.x for point in self.points) / n
        cy = sum(point.y for point in self.points) / n

        return cx, cy
