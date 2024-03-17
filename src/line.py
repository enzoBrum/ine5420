from point import Point
from shape import Shape

class Line(Shape):
    shape_name: str = "Line"

    def __init__(self, point1: Point, point2: Point, color: str = "red", name: str = ""):
        self._point1 = point1
        self._point2 = point2
        
        super().__init__(color, name)

    @property
    def point1(self):
        return self._point1

    @property
    def point2(self):
        return self._point2