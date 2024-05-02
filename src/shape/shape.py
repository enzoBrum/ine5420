from abc import ABC, abstractmethod
from copy import deepcopy
from tkinter import Canvas
from typing import Optional
from uuid import uuid4

from clipping import Clipper
from transformations import Transformer
from vector3 import Vector3


class Shape(ABC):
    color: str
    name: str
    shape_name: str
    points: list[Vector3]
    ppc_points: list[Vector3]
    clipper: Clipper
    transformer: Transformer

    def __init__(self, points: list[Vector3], name: Optional[str] = None, color: str = "red") -> None:
        self.color = color
        self.name = name if name else uuid4().hex
        self.points = points
        self.ppc_points = deepcopy(points)

    def __str__(self) -> str:
        return f"{self.shape_name}[{self.name}]"

    @abstractmethod
    def serialize(self, vertices: dict[Vector3, int], hex_to_color: dict[str, str]) -> str: ...

    @abstractmethod
    def draw(self, canvas: Canvas, points: list[Vector3]): ...

    def process_clipped_points(
        self,
        points: list[Vector3],
        transformed_points: list[Vector3],
        window_min: Vector3,
        window_max: Vector3,
    ) -> list[Vector3]:
        return transformed_points
