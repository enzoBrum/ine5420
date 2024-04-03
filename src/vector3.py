from typing import Union

import numpy as np
import numpy.typing as npt


class Vector3:
    x: float
    y: float
    z: float

    def __init__(self, x: float, y: float, z: float = 1):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other: Union["Vector3", int]) -> "Vector3":
        if not isinstance(other, Vector3) and isinstance(other, (int, float)):
            other = Vector3(other, other)

        return Vector3(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: Union["Vector3", int]) -> "Vector3":
        if not isinstance(other, Vector3) and isinstance(other, (int, float)):
            other = Vector3(other, other)

        self.x += other.x
        self.y += other.y

        return self

    def __sub__(self, other: Union["Vector3", int]) -> "Vector3":
        if not isinstance(other, Vector3) and isinstance(other, (int, float)):
            other = Vector3(other, other)

        return Vector3(self.x - other.x, self.y - other.y)

    def __isub__(self, other: Union["Vector3", int]) -> "Vector3":
        if not isinstance(other, Vector3) and isinstance(other, (int, float)):
            other = Vector3(other, other)

        self.x -= other.x
        self.y -= other.y

        return self

    def __repr__(self) -> str:
        return f"Vector3(x={self.x}, y={self.y})"

    def __str__(self) -> str:
        return self.__repr__()

    @classmethod
    def from_array(
        cls, arr: npt.NDArray[np.float32] | tuple[float, float, float]
    ) -> "Vector3":
        return Vector3(arr[0], arr[1], arr[2])
