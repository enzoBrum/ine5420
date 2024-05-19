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

def perspective_projection(window: "Window", display_file: DisplayFile):
    # print(f"AAAAAAAAAAAAA: {window.cop}")
    window.ppc_points = deepcopy(window.points)
    points = []

    for shape in display_file:
        if shape.dirty:
            points += shape.ppc_points

    vrp = deepcopy(window.vrp)
    cop = deepcopy(window.cop)
    vpn = deepcopy(window.vpn) - vrp

    #vpn = vpn / np.linalg.norm(vpn)

    vpn2 = deepcopy(window.vpn)

    # https://stackoverflow.com/a/10801900
    # Alinha VPN com o eixo Z

    # print(f"{window.cop=}")
    # print(f"{vpn=}, {np.dot(vpn, (0, 0, 1))=}")
    angle = 2*pi - acos(np.dot(vpn, (0, 0, 1)))
    axis = np.cross(vpn, (0, 0, 1))

    cop = Vector3(0, 0, -150)
    Transformer3D(window.ppc_points[:] + [vpn2]).translation(-window.vrp).rotate(angle, Vector3.from_array(axis)).translation(-cop).apply()
    Transformer3D(points).translation(-window.vrp).rotate(angle, Vector3.from_array(axis)).translation(-cop).apply()

    # print(f"{vpn2=}, {window.ppc_points=}, {Transformer3D().center(window.ppc_points)=}")

    d = window.min_ppc.z
    # print(f"{points=}")
    for point in points:
        if point.z < d:
            point.z = d
        
        point.x = point.x/(point.z/d)
        point.y = point.y/(point.z/d)
