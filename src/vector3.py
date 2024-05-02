from typing import Union

import numpy as np
import numpy.typing as npt


class Vector3:
    x: float
    y: float
    z: float

    def __init__(self, x: float, y: float, z: float = 1):
        self.x = round(x, 6)
        self.y = round(y, 6)
        self.z = round(z, 6)

    def __add__(self, other: Union["Vector3", int]) -> "Vector3":
        if not isinstance(other, Vector3) and isinstance(other, (int, float)):
            other = Vector3(other, other, other)

        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __iadd__(self, other: Union["Vector3", int]) -> "Vector3":
        if not isinstance(other, Vector3) and isinstance(other, (int, float)):
            other = Vector3(other, other)

        self.x += other.x
        self.y += other.y
        self.z += other.z

        return self

    def __sub__(self, other: Union["Vector3", int]) -> "Vector3":
        if not isinstance(other, Vector3) and isinstance(other, (int, float)):
            other = Vector3(other, other, other)

        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self) -> "Vector3":
        return Vector3(-self.x, -self.y, -self.z)

    def __isub__(self, other: Union["Vector3", int]) -> "Vector3":
        if not isinstance(other, Vector3) and isinstance(other, (int, float)):
            other = Vector3(other, other, other)

        self.x -= other.x
        self.y -= other.y
        self.z -= other.z

        return self

    def __mul__(self, other: Union["Vector3", int, float]) -> "Vector3":
        if isinstance(other, (int, float)):
            other = Vector3(other, other, other)
        return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)

    def __truediv__(self, other: Union["Vector3", int, float, tuple[int | float, int | float, int | float]]) -> "Vector3":
        if isinstance(other, (int, float)):
            other = Vector3(other, other, other)

        return Vector3(self.x / other[0], self.y / other[1], self.z / other[2])

    def __rtruediv__(self, other: Union["Vector3", int, float, tuple[int | float, int | float, int | float]]) -> "Vector3":
        if isinstance(other, (int, float)):
            other = Vector3(other, other, other)

        return Vector3(other[0] / self.x, other[1] / self.y, other[2] / self.z)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __repr__(self) -> str:
        return f"Vector3(x={self.x}, y={self.y}, z={self.z})"

    def __str__(self) -> str:
        return self.__repr__()

    def __getitem__(self, idx: int) -> float:
        match idx:
            case 0:
                return self.x
            case 1:
                return self.y
            case 2:
                return self.z
            case _:
                raise IndexError(f"{idx} é muito alto.")

    @classmethod
    def from_array(cls, arr: npt.NDArray[np.float32] | tuple[float, float, float]) -> "Vector3":
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
        return (self.x, self.y, self.z) < other

    def __gt__(self, other: object) -> bool:
        if isinstance(other, Vector3):
            return (self.x, self.y, self.z) > (other.x, other.y, other.z)
        return (self.x, self.y, self.z) > other

    def __ge__(self, other: object) -> bool:
        if isinstance(other, Vector3):
            return (self.x, self.y, self.z) >= (other.x, other.y, other.z)
        return (self.x, self.y, self.z) >= other
