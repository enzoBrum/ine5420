from copy import deepcopy
from math import acos, pi
from typing import TYPE_CHECKING

import numpy as np

from transformations import Transformer3D
from vector3 import Vector3

if TYPE_CHECKING:
    from interface import Window

def parallel_projection(window: "Window", transformer: Transformer3D):
    vrp = deepcopy(window.vrp)
    vpn = deepcopy(window.vpn) - vrp

    # https://stackoverflow.com/a/10801900
    # Alinha VPN com o eixo Z
    angle = 2*pi - acos(np.dot(vpn, (0, 0, 1)))
    axis = np.cross(vpn, (0, 0, 1))
    transformer.translation(-vrp).rotate(angle, Vector3.from_array(axis))
