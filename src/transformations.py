from math import sin, cos, radians

import numpy as np
import numpy.typing as npt

from vector3 import Vector3


def rotate(degree: float, point: Vector3, points: list[Vector3]) -> None:
    degree = radians(degree)
    matrix_t = create_translation_matrix((point.x, point.y), Vector3(0, 0, 1), 1)
    matrix_r = np.array(
        [[cos(degree), -sin(degree), 0], [sin(degree), cos(degree), 0], [0, 0, 1]]
    )
    matrix_t2 = create_translation_matrix((point.x, point.y), Vector3(0, 0, 1), -1)

    matrix = np.matmul(matrix_t, matrix_r)
    matrix = np.matmul(matrix, matrix_t2)

    for i in range(len(points)):
        point = [points[i].x, points[i].y, points[i].z]
        point = [round(x, 6) for x in point]
        point = np.array(point)
        points[i] = Vector3.from_array(np.matmul(point, matrix))


def translation(dx: float, dy: float, points: list[Vector3]) -> None:
    matrix = np.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])
    for i in range(len(points)):
        point = np.array([points[i].x, points[i].y, points[i].z])
        points[i] = Vector3.from_array(np.matmul(point, matrix))


def scale(factor: float, points: list[Vector3]) -> None:
    c = center(points)

    matrix_t = create_translation_matrix(c, Vector3(0, 0, 1), 1)
    matrix_s = np.array([[factor, 0, 0], [0, factor, 0], [0, 0, 1]])
    matrix_t2 = create_translation_matrix(c, Vector3(0, 0, 1), -1)

    matrix = np.matmul(matrix_t, matrix_s)
    matrix = np.matmul(matrix, matrix_t2)

    for i in range(len(points)):
        point = np.array([points[i].x, points[i].y, points[i].z])
        points[i] = Vector3.from_array(np.matmul(point, matrix))


def create_translation_matrix(
    center: tuple[float, float], point: Vector3, center_mult: float
) -> npt.NDArray[np.float32]:
    cx, cy = center
    return np.array(
        [
            [1, 0, 0],
            [0, 1, 0],
            [point.x - cx * center_mult, point.y - cy * center_mult, 1],
        ]
    )


def center(points: list[Vector3]) -> tuple[float, float]:
    n = len(points)
    cx = sum(point.x for point in points) / n
    cy = sum(point.y for point in points) / n

    return cx, cy
