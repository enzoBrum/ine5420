from point import Point 
from shape import Shape

class Wireframe(Shape):
    def __init__(self, points: Point):
        self._points = points
    
    @property
    def points(self):
        return self._points
