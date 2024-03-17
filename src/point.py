from shape import Shape

class Point(Shape):
    shape_name: str = "Point"

    def __init__(self, x: int, y: int, color: str = "red", name: str = ""):
        self._x = x
        self._y = y
        
        super().__init__(color, name)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value