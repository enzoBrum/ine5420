from abc import ABC, abstractproperty
from typing import Optional
from uuid import uuid4
from math import sin, cos, radians

import numpy as np
import numpy.typing as npt

from vector3 import Vector3
from copy import deepcopy


class Shape(ABC):
    color: str
    name: str
    shape_name: str
    points: list[Vector3]
    ppc_points: list[Vector3]

    def __init__(
        self, points: list[Vector3], name: Optional[str] = None, color: str = "red"
    ) -> None:
        self.color = color
        self.name = name if name else uuid4().hex
        self.points = points
        self.ppc_points = deepcopy(points)

    def __str__(self) -> str:
        return f"{self.shape_name}[{self.name}]"
