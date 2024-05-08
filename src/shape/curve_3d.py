from .curve import Curve
from transformations import Transformer3D


class Curve3D(Curve):
    shape_name = "Curve3D"
    transformer = Transformer3D
