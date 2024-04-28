from .wireframe import Wireframe
from transformations import Transformer3D


class Wireframe3D(Wireframe):
    shape_name = "Object3D"
    transformer = Transformer3D
