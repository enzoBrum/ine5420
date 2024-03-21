from typing import Union

import numpy as np

class Vector2:
    x: float
    y: float
    z: float

    def __init__(self, x: float, y: float, z: float = 1):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other: Union["Vector2", int]) -> "Vector2":
        if not isinstance(other, Vector2) and isinstance(other, (int, float)):
            other = Vector2(other, other)
        
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __iadd__(self, other: Union["Vector2", int]) -> "Vector2":
        if not isinstance(other, Vector2) and isinstance(other, (int, float)):
            other = Vector2(other, other)

        self.x += other.x
        self.y += other.y

        return self

    def __sub__(self, other: Union["Vector2", int]) -> "Vector2":
        if not isinstance(other, Vector2) and isinstance(other, (int, float)):
            other = Vector2(other, other)

        return Vector2(self.x - other.x, self.y - other.y)
    
    def __isub__(self, other: Union["Vector2", int]) -> "Vector2":
        if not isinstance(other, Vector2) and isinstance(other, (int, float)):
            other = Vector2(other, other)

        self.x -= other.x
        self.y -= other.y

        return self


    def __repr__(self) -> str:
        return f"Vector2(x={self.x}, y={self.y})"

    def __str__(self) -> str:
        return self.__repr__()
    
    @classmethod
    def from_array(arr: np.array) -> "Vector2":
        return Vector2(arr[0], arr[1], arr[2])