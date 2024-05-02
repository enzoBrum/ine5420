from copy import deepcopy
from math import acos, sqrt
from typing import TYPE_CHECKING

import numpy as np

from display_file import DisplayFile
from transformations import Transformer3D
from vector3 import Vector3

if TYPE_CHECKING:
    from interface import Window


def parallel_projection(window: "Window", display_file: DisplayFile):

    # FIXME: Isso tá errado. O vpn tem que terminar sendo (0, 0, 1) :(
    window_min = window.min
    window_max = window.max

    transformer = Transformer3D()
    window.ppc_points = deepcopy(window.points)
    transformer.points = window.ppc_points[:]

    for shape in display_file:
        transformer.points += shape.ppc_points

    vrp = Vector3((window_max.x + window_min.x) / 2, (window_max.y + window_min.y) / 2, (window_max.z + window_min.z) / 2)

    v1 = window_max + vrp
    v2 = window_min - vrp

    vpn = Vector3.from_array(np.cross(np.array(list(v1)), np.array(list(v2))))
    vpn.z = 2
    print(f"{vpn=}")

    # https://www.youtube.com/watch?v=vH-DagcgJvE --> simplesmente perfeito pra achar o ângulo entre vetor e eixo <3
    length = sqrt(sum([x**2 for x in vpn]))

    x_angle = acos(vpn.x / length)
    y_angle = acos(vpn.y / length)

    transformer.translation(-vrp)
    transformer.rotate_x_y_z(-x_angle, "X")
    transformer.rotate_x_y_z(-y_angle, "Y")

    transformer.apply()

    window_max = window.max_ppc
    window_min = window.min_ppc
    vrp = Vector3((window_max.x + window_min.x) / 2, (window_max.y + window_min.y) / 2, (window_max.z + window_min.z) / 2)

    v1 = window_max + vrp
    v2 = window_min - vrp

    vpn = Vector3.from_array(np.cross(np.array(list(v1)), np.array(list(v2))))
    print(f"{vpn=}")
