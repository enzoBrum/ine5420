from vector3 import Vector3
from .shape import Shape


class Wireframe(Shape):
    shape_name: str = "Wireframe"
    fill: bool

    def __init__(
        self,
        points: list[Vector3],
        fill: bool,
        name: str | None = None,
        color: str = "red",
    ) -> None:
        self.fill = fill
        super().__init__(points, name, color)
