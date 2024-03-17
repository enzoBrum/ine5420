from tkinter import Tk, Canvas, ttk, N, E, W, S

from vector2 import Vector2
from window import Window
from viewport import Viewport
from shape import Shape
from line import Line
from point import Point
from wireframe import Wireframe

VIEWPORT_DIMENSION = Vector2(400, 400)
PROGRAM_NAME = "sistema básico de CG 2D"

"""
Vector2:
    x: float
    y: float

    (xw_min + xw_max, yw_min + yw_max)
    w_min + w_max
    
    soma ...
    
Window:
    min: Vector2
    max: Vector2
    
    zoom(zoom_factor)
    move(direction, value)
    
Viewport:
    min: Vector2
    max: Vector2

    _viewport_transform(window_min, window_max, *points)
    draw(display_file)


window: Window --> representa a parte do nosso 
viewport: Viewport --> canvas onde os objetos são desenhados.
display_file: list[Point] --> estrutura com as formas geométricas

add_object()
"""
class App:
    window: Window
    viewport: Viewport
    display_file: list[Shape]
    root: Tk
    frame: ttk.Frame

    def add_point(self):
        self.display_file.append(Point(100, 100))
        self.viewport.draw(self.window.min, self.window.max, self.display_file)

    def add_line(self):
        self.display_file.append(Line(Point(100,100), Point(200,200)))
        
        print(self.display_file)
        self.viewport.draw(self.window.min, self.window.max, self.display_file)

    def add_wireframe(self):
        self.display_file.append(Wireframe([Point(100,100), Point(200,200), Point(100, 300)]))
        self.viewport.draw(self.window.min, self.window.max, self.display_file)

    def zoom_out(self):
        print("AAAA")
        self.window.zoom(-10)
        self.viewport.draw(self.window.min, self.window.max, self.display_file)

    def zoom_in(self):
        print("BBBB")
        self.window.zoom(10)
        self.viewport.draw(self.window.min, self.window.max, self.display_file)

    def move_left(self):
        self.window.move('L', 2)
        self.viewport.draw(self.window.min, self.window.max, self.display_file)

    def move_right(self):
        self.window.move('R', 2)
        self.viewport.draw(self.window.min, self.window.max, self.display_file)

    def move_up(self):
        self.window.move('U', 2)
        self.viewport.draw(self.window.min, self.window.max, self.display_file)

    def move_down(self):
        self.window.move('D', 2)
        self.viewport.draw(self.window.min, self.window.max, self.display_file)

    def __init__(self):
        self.root = Tk()
        self.root.title(PROGRAM_NAME)
        self.root.geometry(f"{VIEWPORT_DIMENSION.x*2}x{VIEWPORT_DIMENSION.y*2}")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.window = Window(Vector2(0,0), VIEWPORT_DIMENSION)
        self.frame = ttk.Frame(self.root, padding="3 3 12 12")
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.viewport = Viewport(Vector2(0,0), VIEWPORT_DIMENSION, self.frame, column=4, row=3)
        self.display_file = []


        ttk.Button(self.frame, text="Add line", command=self.add_line).grid(column=0, row=0)
        ttk.Button(self.frame, text="Add point", command=self.add_point).grid(column=1, row=0)
        ttk.Button(self.frame, text="Add wireframe", command=self.add_wireframe).grid(column=2, row=0)
        ttk.Button(self.frame, text="zoom in", command=self.zoom_in).grid(column=0, row=1)
        ttk.Button(self.frame, text="zoom out", command=self.zoom_out).grid(column=1, row=1)
        ttk.Button(self.frame, text="move left", command=self.move_left).grid(column=2, row=1)
        ttk.Button(self.frame, text="move right", command=self.move_right).grid(column=0, row=2)
        ttk.Button(self.frame, text="move up", command=self.move_up).grid(column=1, row=2)
        ttk.Button(self.frame, text="move down", command=self.move_down).grid(column=2, row=2)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()