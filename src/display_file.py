from shape import Shape
from tkinter import StringVar
from typing import Optional

class DisplayFile:
    _shapes: list[Shape]
    shapes_str_var: StringVar

    def __init__(self, shapes: Optional[list[Shape]] = None) -> None:
        if shapes is None:
            shapes = []

        self._shapes = shapes
        self.shapes_str_var = StringVar(value=self._shapes)

    def append(self, shape: Shape):
        self._shapes.append(shape)
        self.shapes_str_var.set(self._shapes)

    def __len__(self) -> int:
        return len(self._shapes)
    
    def __contains__(self, shape: Shape) -> bool:
        return shape in self._shapes
    
    def __iter__(self):
        return iter(self._shapes)