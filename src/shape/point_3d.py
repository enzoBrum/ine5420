from .point import Point
from transformations import Transformer3D


class Point3D(Point):
    shape_name: str = "Point3D"
    transformer = Transformer3D
