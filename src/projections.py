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

    window_min = window.min
    window_max = window.max

    transformer = Transformer3D()
    window.ppc_points = deepcopy(window.points)
    transformer.points = window.ppc_points

    for shape in display_file:
        transformer.points += shape.ppc_points

    vrp = Vector3((window_max.x + window_min.x) / 2, (window_max.y + window_min.y) / 2, (window_max.z + window_min.z) / 2)
    transformer.translation(-vrp)

    v1 = window_max + vrp
    v2 = window_min - vrp

    vpn = Vector3.from_array(np.cross(np.array(list(v1)), np.array(list(v2))))
    vup = Vector3(0, 1, 0)  # TODO: vup deve ser arbitrário

    r_z = vpn / sqrt(sum(x**2 for x in vpn))
    r_x = Vector3.from_array(np.cross(list(vup), list(r_z))) / sqrt(sum([x**2 for x in np.cross(list(vup), list(r_z))]))
    r_y = Vector3.from_array(np.cross(list(r_z), list(r_x)))

    print(f"{r_z=}, {r_x=}, {r_y=}, {vpn=}, {v1=}, {v2=}")

    rotation_matrix = [[r_x[0], r_x[1], r_x[2], 0], [r_y[0], r_y[1], r_y[2], 0], [r_z[0], r_z[1], r_z[2], 0], [0, 0, 0, 1]]
    transformer.transformation_matrix = np.matmul(transformer.transformation_matrix, rotation_matrix)

    # https://www.youtube.com/watch?v=vH-DagcgJvE --> simplesmente perfeito pra achar o ângulo entre vetor e eixo <3

    length = sqrt(sum([x**2 for x in vpn]))

    x_angle = acos(vpn.x / length)
    y_angle = acos(vpn.y / length)

    print(f"{vpn=}, {x_angle=}, {y_angle=}, {length=}, {v1=}, {v2=}, {vrp=}, {window_max=}, {window_min=}")

    # transformer.rotate_x_y_z(-x_angle, "X")
    # transformer.rotate_x_y_z(-y_angle, "Y")

    transformer.apply()

    print(f"{transformer.points=}")
