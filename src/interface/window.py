from tkinter import StringVar
import traceback

from vector3 import Vector3


class Window:
    step: float
    step_var: StringVar
    min: Vector3
    max: Vector3

    def __init__(self, vector1: Vector3, vector3: Vector3):
        self.min = vector1
        self.max = vector3
        self.step = 10.0
        self.step_var = StringVar(value=str(10.0))

        self.step_var.trace_add("write", self.set_step)

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
        self.min += step
        self.max -= step

    def move(self, direction: str):
        print(f"Movendo Window para {direction}")
        print(f"window max original: {self.max}\nwindow min original: {self.min}")
        if direction == "R":
            self.max.x += self.step
            self.min.x += self.step
        elif direction == "L":
            self.max.x -= self.step
            self.min.x -= self.step
        elif direction == "U":
            self.max.y += self.step
            self.min.y += self.step
        else:
            self.min.y -= self.step
            self.max.y -= self.step

        print(f"window max final: {self.max}\nwindow min final: {self.min}")

