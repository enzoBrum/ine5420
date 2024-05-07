from tkinter import StringVar
from typing import Optional

from shape import Shape


class DisplayFile:
    _shapes: list[Shape]
    _shapes_dict: dict[str, Shape]

    def __init__(self, shapes: Optional[list[Shape]] = None) -> None:
        if shapes is None:
            shapes = []
            shapes_dict = {}
        else:
            shapes_dict = {str(shape): shape for shape in shapes}

        self._shapes = shapes
        self._shapes_dict = shapes_dict

    def append(self, shape: Shape):
        self._shapes.append(shape)
        self._shapes_dict[str(shape)] = shape

    def get_shape_by_id(self, shape_id: str) -> Optional[Shape]:
        return self._shapes_dict.get(shape_id)

    def all_dirty(self):
        for shape in self._shapes:
            shape.dirty = True

    def __len__(self) -> int:
        return len(self._shapes)

    def __contains__(self, shape: Shape) -> bool:
        return shape in self._shapes

    def __iter__(self):
        return iter(self._shapes)
