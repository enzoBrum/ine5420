from point import Point
from shape import Shape

class Line(Shape):
    def __init__(self, point1: Point, point2: Point):
        self._point1 = point1
        self._point2 = point2

    @property
    def point1(self):
        return self._point1

    @property
    def point2(self):
        return self._point2