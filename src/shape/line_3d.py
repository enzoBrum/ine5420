from .line import Line
from transformations import Transformer3D


class Line3D(Line):
    shape_name = "Line3D"
    transformer = Transformer3D
