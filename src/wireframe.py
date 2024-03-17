from point import Point 
from shape import Shape

class Wireframe(Shape):
    shape_name: str = "Wireframe"

    def __init__(self, points: Point, color: str = "red", name: str = ""):
        self._points = points
        super().__init__(color, name)
    
    @property
    def points(self):
        return self._points
