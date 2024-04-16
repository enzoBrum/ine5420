from abc import ABC, abstractmethod, abstractproperty
from tkinter import Canvas
from typing import Callable, Optional, TypeVar
from uuid import uuid4

from vector3 import Vector3


class Shape(ABC):
    color: str
    name: str
    shape_name: str

    def __init__(self, name: Optional[str] = None, color: str = "red") -> None:
        self.color = color
        self.name = name if name else uuid4().hex

    def __str__(self) -> str:
        return f"{self.shape_name}[{self.name}]"

    @abstractmethod
    def serialize(
        self, vertices: dict[Vector3, int], hex_to_color: dict[str, str]
    ) -> str: ...

    @abstractproperty
    def points(self) -> list[Vector3]: ...

    @abstractproperty
    def ppc_points(self) -> list[Vector3]: ...

    @ppc_points.setter
    def ppc_points(self, points: list[Vector3]): ...

    @abstractmethod
    def draw(
        self,
        canvas: Canvas,
        viewport_transform: Callable[[list[Vector3]], list[Vector3]],
        window_min: Vector3,
        window_max: Vector3,
    ): ...
