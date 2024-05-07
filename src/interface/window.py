from copy import deepcopy
from hmac import new
from math import atan2, degrees, pi
from tkinter import StringVar
import traceback

import numpy as np

from shape import Shape
from transformations import Transformer2D, Transformer3D
from vector3 import Vector3


class Window:
    points: list[Vector3]
    ppc_points: list[Vector3]
    __og_points: list[Vector3]
    vrp: Vector3
    vpn: Vector3
    """
    (x3, y3) ------------------------- (x2, y2)
        |                                 |
        |                                 |
        |                                 |
        |                                 |
        |                                 |
        |                                 |
    (x0, y0) ------------------------- (x1, y1)
    """

    def __init__(self, min: Vector3, max: Vector3):
        self.points = [
            min,  # (x0, y0)
            Vector3(max.x, min.y, max.z),  # (x1, y1)
            max,  # (x2, y2)
            Vector3(min.x, max.y, min.z),  # (x3, y3)
        ]

        print(f"WINDOW POINTSSS: {self.points}")

        self.__og_points = deepcopy(self.points)
        self.ppc_points = deepcopy(self.points)
        self.vrp = Transformer3D().center(self.points)
        self.vpn = Vector3.from_array(np.cross(self.points[2] - self.vrp, self.points[1] - self.vrp))
        self.n_zoom = 0

        if self.vpn.z < 0:
            self.vpn = -self.vpn
        self.vpn = self.vpn / np.linalg.norm(self.vpn) + self.vrp

    def reset(self):
        self.points = deepcopy(self.__og_points)
        self.vrp = Transformer3D().center(self.points)
        self.vpn = Vector3.from_array(np.cross(self.points[2] - self.vrp, self.points[1] - self.vrp))
        self.n_zoom = 0

        if self.vpn.z < 0:
            self.vpn = -self.vpn
        self.vpn = self.vpn / np.linalg.norm(self.vpn) + self.vrp

    def ppc_transformation(self, shapes: list[Shape]):
        print(f"{self.ppc_points=}, {len(self.ppc_points)=}")

        transformer = Transformer2D()
        wcx, wcy, _ = transformer.center(self.ppc_points)

        transformer.points = self.ppc_points[:]
        for shape in shapes:
            if shape.dirty:
                transformer.points += shape.ppc_points

        print(f"{wcx=}, {wcy=}")

        transformer.translation(Vector3(-wcx, -wcy))

        # print(f"{transformer.points=}")

        x = transformer.points[3].x - transformer.points[0].x
        y = transformer.points[3].y - transformer.points[0].y
        degree = atan2(y, x) - pi / 2

        if abs(degree) > 1e-6:
            transformer.rotate(degree, Vector3(wcx, wcy))

        transformer.apply()

        print(f"{self.ppc_points=}")
        # print(transformer.points)

    @property
    def v_up(self) -> tuple[Vector3, Vector3]:
        return self.points[0], self.points[3]

    @property
    def max(self) -> Vector3:
        return self.points[2]

    @property
    def min(self) -> Vector3:
        return self.points[0]

    @property
    def max_ppc(self) -> Vector3:
        return self.ppc_points[2]

    @property
    def min_ppc(self) -> Vector3:
        return self.ppc_points[0]

    def zoom(self, mult: float, step: float):
        step = step * mult

        final_max = self.max - step
        final_min = self.min + step

        if abs(final_max.x - final_min.x) < 10 or abs(final_max.y - final_min.y) < 10:
            print("Window muito pequena!")
            return

        print(f"ZOOM:\n\twindow max: {self.max} --> {final_max}\n\twindow min: {self.min} --> {final_min}")

        self.points[0].x += step
        self.points[0].y += step

        self.points[1].x -= step
        self.points[1].y += step

        self.points[2].x -= step
        self.points[2].y -= step

        self.points[3].x += step
        self.points[3].y -= step

        self.n_zoom += step

    def move(self, direction: str, step: float):
        print(f"Movendo Window para {direction}")
        print(f"window max original: {self.max}\nwindow min original: {self.min}")

        vup = [self.points[3].x - self.points[0].x, self.points[3].y - self.points[0].y, self.points[3].z - self.points[0].z]

        # Normalize vup to reduce the numerical error
        vup_normalized = np.array(vup) / np.linalg.norm(vup)

        # np.cross returns a vector perpendicular to the normalized vup and [0, 0, 1]
        # the vector [0, 0, 1] is penpendicular to axes x and y, so np.cross return
        # a vector thats is pendicular to vup, x, y and is multiply by the scalar step
        # to give a sensation to a unique direction
        if direction == "R":
            displacement_vector = np.cross(vup_normalized, [0, 0, 1]) * step
        elif direction == "L":
            displacement_vector = -np.cross(vup_normalized, [0, 0, 1]) * step
        # Up and Down dont need np.cross
        elif direction == "U":
            displacement_vector = vup_normalized * step
        elif direction == "D":
            
            displacement_vector = -vup_normalized * step
        elif direction == "F":
            displacement_vector = [0, 0, step]
        else:
            displacement_vector = [0, 0, -step]

        print(f"Displacement vector: {displacement_vector}")
        # Apply the displacement_vector for window points
        for i in range(len(self.points)):
            self.points[i] += Vector3.from_array(displacement_vector)

        self.vpn += Vector3.from_array(displacement_vector)
        self.vrp += Vector3.from_array(displacement_vector)

        print(f"window max final: {self.max}\nwindow min final: {self.min}")

    def rotate(self, degree: float, type: str):
        print(f"Rotacionando Window {degree} graus {type}")

        transformer = Transformer3D()
        c = transformer.center(self.points)
        transformer.points = self.points[:] + [self.vpn, self.vrp]
        transformer.translation(-c).apply()
        if type == "X":
            v = (self.points[3] + self.points[2]) / 2
        elif type == "Y":
            v = (self.points[3] + self.points[0]) / 2
        elif type == "Z":
            v = self.vpn

        print(f"ROTAÇÃO ANTES: {self.points=}, {self.vpn=}, {self.vrp=}")
        transformer.rotate(degree, v).translation(c).apply()
        print(f"ROTAÇÃO DEPOIS: {self.points=}, {self.vpn=}, {self.vrp=}")
        print(f"window max final: {self.max}\nwindow min final: {self.min}")
