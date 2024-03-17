from vector2 import Vector2


class Window:
    def __init__(self, vector1: Vector2, vector2: Vector2):
        self._min = vector1
        self._max = vector2

    def zoom(self, zoom_factor: float):
        print(f"ZOOM: {zoom_factor}")
        print(self._min, self._max)
        
        final_size = self._max - zoom_factor
        final_size = final_size + self._min + zoom_factor

        if final_size.x < 10 or final_size.y < 10:
            return

        self._min += zoom_factor
        self._max -= zoom_factor

        print(self._min, self._max)

    def move(self, direction: str, value: float):
        if direction == 'R':
            self._max.x += value
            self._min.x += value
        elif direction == 'L':
            self._max.x -= value
            self._min.x -= value
        elif direction == 'U':
            self._max.y += value
            self._min.y += value
        else:
            self._min.y -= value
            self._max.y -= value

    @property
    def max(self) -> Vector2:
        return self._max
    
    @property
    def min(self) -> Vector2:
        return self._min