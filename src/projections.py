from copy import deepcopy
from math import acos, sqrt
from typing import TYPE_CHECKING

import numpy as np

from display_file import DisplayFile
from transformations import Transformer3D
from vector3 import Vector3

if TYPE_CHECKING:
    from interface import Window

PI = 1.5683580323815514


def parallel_projection(window: "Window", display_file: DisplayFile):

    # FIXME: Lidar com os sinais dos ângulos da forma correta.
    # FIXME: Por enquanto, ta hard coded pra usar y negativado.
    window_min = window.min
    window_max = window.max

    window.ppc_points = deepcopy(window.points)
    points = window.ppc_points[:]

    for shape in display_file:
        points += shape.ppc_points

    vrp = deepcopy(window.vrp)
    vpn = deepcopy(window.vpn)

    vpn_transformer = Transformer3D([vpn])
    Transformer3D([vpn]).translation(-vrp).apply()

    length = lambda vec: sqrt(vec.x**2 + vec.y**2 + vec.z**2)
    
    x_angle = acos(sqrt(vpn.y**2 + vpn.z**2) / length(vpn))

    # Zera a componente X
    vpn_transformer.rotate_x_y_z(x_angle, "Y").apply()

    y_angle = acos(sqrt(vpn.x**2 + vpn.z**2) / length(vpn))

    # Zera a componente Y
    vpn_transformer.rotate_x_y_z(-y_angle, "Z").apply()

    print(f"{vrp=}")
    print(f"{window.vpn=}")
    print(f"{vpn=}")

    vpn2 = deepcopy(window.vpn)
    points.append(vpn2)
    points.append(vrp)

    print(f"{x_angle=}")
    print(f"{y_angle=}")

    # z_angle = PI - z_angle
    # x_angle = np.pi/2 - x_angle
    # y_angle = np.pi/2 - y_angle

    Transformer3D(points).translation(-vrp).rotate_x_y_z(x_angle, "Y").rotate_x_y_z(-y_angle, "X").apply()

    print(f"{vpn2=}")
    print(f"{vrp=}")

    for shape in display_file:
        if len(shape.points) > 1:
            print(f"WIREFRAME3D: {shape.ppc_points}")
