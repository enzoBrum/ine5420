from abc import ABC, abstractmethod
from tkinter import Canvas

class Shape(ABC):
    color: str
    name: str
    shape_name: str = "Shape"

    def __init__(self, color: str, name: str) -> None:
        self.color = color
        self.name = name

    def __str__(self) -> str:
        return f"{self.shape_name}[{self.name}]"