from copy import deepcopy
from tkinter import StringVar
import traceback

from vector3 import Vector3
from shape import Shape
from transformations import translation, rotate, center

from math import degrees, atan2
import numpy as np

class Window:
    step: float
    step_var: StringVar
    points: list[Vector3]
    ppc_points: list[Vector3]
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
            min, # (x0, y0)
            Vector3(max.x, min.y), # (x1, y1)
            max, # (x2, y2)
            Vector3(min.x, max.y) # (x3, y3)
        ]

        self.ppc_points = deepcopy(self.points)
        
        self.step = 10.0
        self.step_var = StringVar(value=str(10.0))

        self.step_var.trace_add("write", self.set_step)

    def ppc_transformation(self, shapes: list[Shape]):
        wcx, wcy = center(self.points)

        points = deepcopy(self.points)
        for shape in shapes:
            points += deepcopy(shape.points)
                    
        translation(-wcx, -wcy, points)

        x = self.points[3].x - self.points[0].x
        y = self.points[3].y - self.points[0].y
        degree = degrees(atan2(y, x)) - 90

        print(degree)
        rotate(degree, Vector3(wcx, wcy), points)


        i = 0
        for j in range(len(self.ppc_points)):
            self.ppc_points[j] = points[i]
            i += 1

        for shape in shapes:
            for j in range(len(shape.ppc_points)):
                shape.ppc_points[j] = points[i]
                i += 1

    
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

    def set_step(self, *args):
        print(f"Alterando step da window para {self.step_var.get()}")

        try:
            self.step = float(self.step_var.get())
        except ValueError:
            print(
                f"Erro ao setar step para {self.step_var.get()}!\nMantendo o valor {self.step}"
            )

    def zoom(self, mult: int):
        step = self.step * mult

        final_max = self.max - step
        final_min = self.min + step

        if abs(final_max.x - final_min.x) < 10 or abs(final_max.y - final_min.y) < 10:
            print("Window muito pequena!")
            return

        print(
            f"ZOOM:\n\twindow max: {self.max} --> {final_max}\n\twindow min: {self.min} --> {final_min}"
        )

        self.points[0] += step
        
        self.points[1].x -= step
        self.points[1].y += step
        
        self.points[2] -= step
        
        self.points[3].x += step
        self.points[3].y -= step

        

    def move(self, direction: str):
        print(f"Movendo Window para {direction}")
        print(f"window max original: {self.max}\nwindow min original: {self.min}")
        
        vup = [self.points[3].x - self.points[0].x, self.points[3].y - self.points[0].y, 1]

        # Normalize vup to reduce the numerical error
        vup_normalized = np.array(vup) / np.linalg.norm(vup)
        
        # np.cross returns a vector perpendicular to the normalized vup and [0, 0, 1]
        # the vector [0, 0, 1] is penpendicular to axes x and y, so np.cross return
        # a vector thats is pendicular to vup, x, y and is multiply by the scalar step
        # to give a sensation to a unique direction
        if direction == "R":
            displacement_vector = np.cross(vup_normalized, [0, 0, 1]) * self.step
        elif direction == "L":
            displacement_vector = -np.cross(vup_normalized, [0, 0, 1]) * self.step
        # Up and Down dont need np.cross
        elif direction == "U":
            displacement_vector = vup_normalized * self.step
        else:
            displacement_vector = -vup_normalized * self.step

        print(displacement_vector)
        # Apply the displacement_vector for window points
        for i in range(len(self.points)):
            self.points[i] += Vector3.from_array(displacement_vector)

        print(f"window max final: {self.max}\nwindow min final: {self.min}")
