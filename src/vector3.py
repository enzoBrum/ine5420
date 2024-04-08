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

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Vector3):
            return self.x == __value.x and self.y == __value.y and self.z == __value.z
        else:
            self.x == __value[0] and self.y == __value[1] and self.z == __value[2]

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Vector3):
            return (self.x, self.y, self.z) < (other.x, other.y, other.z)
        return (self.x, self.y, self.z) < other

    def __le__(self, other: object) -> bool:
        if isinstance(other, Vector3):
            return (self.x, self.y, self.z) <= (other.x, other.y, other.z)
        return (self.x, self.y, self.z) < -other

    def __gt__(self, other: object) -> bool:
        if isinstance(other, Vector3):
            return (self.x, self.y, self.z) > (other.x, other.y, other.z)
        return (self.x, self.y, self.z) > other

    def __ge__(self, other: object) -> bool:
        if isinstance(other, Vector3):
            return (self.x, self.y, self.z) >= (other.x, other.y, other.z)
        return (self.x, self.y, self.z) >= other
