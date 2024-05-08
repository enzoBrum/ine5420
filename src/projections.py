from copy import deepcopy
from math import acos, pi
from typing import TYPE_CHECKING

import numpy as np

from display_file import DisplayFile
from transformations import Transformer3D
from vector3 import Vector3

if TYPE_CHECKING:
    from interface import Window

def parallel_projection(window: "Window", display_file: DisplayFile):
    window.ppc_points = deepcopy(window.points)
    points = window.ppc_points[:]

    for shape in display_file:
        if shape.dirty:
            points += shape.ppc_points

    vrp = deepcopy(window.vrp)
    vpn = deepcopy(window.vpn) - vrp

    # https://stackoverflow.com/a/10801900
    # Alinha VPN com o eixo Z
    angle = 2*pi - acos(np.dot(vpn, (0, 0, 1)))
    axis = np.cross(vpn, (0, 0, 1))
    Transformer3D(points).translation(-vrp).rotate(angle, Vector3.from_array(axis)).apply()
