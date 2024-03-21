from functools import wraps
from tkinter import Canvas, E, Listbox, N, NS, NW, S, StringVar, Tk, W, ttk

import sv_ttk

from display_file import DisplayFile
from line import Line
from point import Point
from shape import Shape
from vector2 import Vector2
from viewport import Viewport
from window import Window
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
    display_file: DisplayFile
    display_file_str_var: StringVar
    root: Tk
    frame: ttk.Frame

    def redraw_viewport(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.viewport.draw(self.window.min, self.window.max, self.display_file)
            return result
        return wrapper

    @redraw_viewport
    def add_point(self, x, y, name):
        self.display_file.append(Point(x, y, name=name))

    @redraw_viewport
    def add_line(self, x1, y1, x2, y2, name):
        self.display_file.append(Line(Point(x1,y1), Point(x2,y2), name=name))

    @redraw_viewport
    def add_wireframe(self, points, name):
        self.display_file.append(Wireframe([Point(x, y) for x, y in points], name=name))

    @redraw_viewport
    def zoom_out(self):
        print("AAAA")
        self.window.zoom(-10)
        self.viewport.draw(self.window.min, self.window.max, self.display_file)

    @redraw_viewport
    def zoom_in(self):
        print("BBBB")
        self.window.zoom(10)

    @redraw_viewport
    def move_left(self):
        self.window.move('L', 10)

    @redraw_viewport
    def move_right(self):
        self.window.move('R', 10)

    @redraw_viewport
    def move_up(self):
        self.window.move('U', 10)

    @redraw_viewport
    def move_down(self):
        self.window.move('D', 10)

    
    def __create_left_menu(self):
        ttk.Label(self.frame, text="Menu de Funções").grid(column=0, row=0)
        ttk.Label(self.frame, text="Objetos").grid(column=0, row=1)
        
        listbox = Listbox(self.frame, height=12, width=24, borderwidth=3, listvariable=self.display_file.shapes_str_var)
        listbox.grid(column=0, row=2, sticky=(N,S,E,W))
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=listbox.yview)
        scrollbar.grid(column=1, row=2, sticky=(N,S,W))
        listbox.configure(yscrollcommand=scrollbar.set)

    def add_object(self):
        frame = Tk()
        frame.title("Add Object")

        shape_frame = ttk.Frame(frame)
        shape_frame.grid(row=2, columnspan=2, padx=10, pady=5)

        ttk.Label(frame, text="Object Name:").grid(row=0, column=0, padx=10, pady=5)
        entry_name = ttk.Entry(frame)
        entry_name.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(frame, text="Shape:").grid(row=1, column=0, padx=10, pady=5)
        type_var = StringVar(frame)
        options = ['Select a shape', "Point", "Line", "Wireframe"]
        ttk.OptionMenu(frame, type_var, *options, command=lambda selection: self.update_shape_frame
                                     (shape_frame, type_var.get())).grid(row=1, column=1, padx=10, pady=5)


        ttk.Button(frame, text="Add", command=lambda: self.add_selected_object
                                (type_var.get(), entry_name.get(), shape_frame)).grid(row=3, columnspan=2, padx=10, pady=5)

    def add_selected_object(self, type_obj, name, shape_frame):
        if type_obj == "Point":
            x = float(shape_frame.winfo_children()[1].get())
            y = float(shape_frame.winfo_children()[3].get())
            self.add_point(x, y, name)
        elif type_obj == "Line":
            x1 = float(shape_frame.winfo_children()[1].get())
            y1 = float(shape_frame.winfo_children()[3].get())
            x2 = float(shape_frame.winfo_children()[5].get())
            y2 = float(shape_frame.winfo_children()[7].get())
            self.add_line(x1, y1, x2, y2, name)
        elif type_obj == "Wireframe":
            points = str(shape_frame.winfo_children()[1].get())
            print(type(points))
            poit = eval(f"[{points}]") 
            print(poit)
            self.add_wireframe(poit, name)

    def update_shape_frame(self, shape_frame, type_obj):
        for widget in shape_frame.winfo_children():
            widget.destroy()

        if type_obj == "Point":
            ttk.Label(shape_frame, text="X:").grid(row=0, column=0, padx=5, pady=5)
            entry_x = ttk.Entry(shape_frame)
            entry_x.grid(row=0, column=1, padx=5, pady=5)

            ttk.Label(shape_frame, text="Y:").grid(row=1, column=0, padx=5, pady=5)
            entry_y = ttk.Entry(shape_frame)
            entry_y.grid(row=1, column=1, padx=5, pady=5)
        elif type_obj == "Line":
            ttk.Label(shape_frame, text="X1:").grid(row=0, column=0, padx=5, pady=5)
            entry_x1 = ttk.Entry(shape_frame)
            entry_x1.grid(row=0, column=1, padx=5, pady=5)

            ttk.Label(shape_frame, text="Y1:").grid(row=1, column=0, padx=5, pady=5)
            entry_y1 = ttk.Entry(shape_frame)
            entry_y1.grid(row=1, column=1, padx=5, pady=5)

            ttk.Label(shape_frame, text="X2:").grid(row=2, column=0, padx=5, pady=5)
            entry_x2 = ttk.Entry(shape_frame)
            entry_x2.grid(row=2, column=1, padx=5, pady=5)

            ttk.Label(shape_frame, text="Y2:").grid(row=3, column=0, padx=5, pady=5)
            entry_y2 = ttk.Entry(shape_frame)
            entry_y2.grid(row=3, column=1, padx=5, pady=5)
        elif type_obj == "Wireframe":
            ttk.Label(shape_frame, text="Give the points in exactly format: (x1, y1), (x2, y2), (x3,y3) ...").grid(row=0, column=0, padx=5, pady=5)
            entry_points = ttk.Entry(shape_frame)
            entry_points.grid(row=1, column=0, padx=5, pady=5)
        
    def __init__(self):
        self.root = Tk()
        self.root.title(PROGRAM_NAME)
        self.root.geometry(f"{VIEWPORT_DIMENSION.x*2}x{VIEWPORT_DIMENSION.y*2}")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        self.window = Window(Vector2(0,0), VIEWPORT_DIMENSION)
        self.frame = ttk.Frame(self.root, padding="3 3 12 12")
        # self.frame.place(relx=0.5, rely=0.5, anchor="center")
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.viewport = Viewport(Vector2(0,0), VIEWPORT_DIMENSION, self.frame, column=7, row=7)
        self.display_file = DisplayFile()

        self.__create_left_menu()

        #ttk.Button(self.frame, text="Add line", command=self.add_line).grid(column=0, row=7)
        #ttk.Button(self.frame, text="Add point", command=self.add_point).grid(column=1, row=7)
        #ttk.Button(self.frame, text="Add wireframe", command=self.add_wireframe).grid(column=7, row=5)
        ttk.Button(self.frame, text="zoom in", command=self.zoom_in).grid(column=0, row=4)
        ttk.Button(self.frame, text="zoom out", command=self.zoom_out).grid(column=1, row=4)
        ttk.Button(self.frame, text="move left", command=self.move_left).grid(column=2, row=4)
        ttk.Button(self.frame, text="move right", command=self.move_right).grid(column=0, row=5)
        ttk.Button(self.frame, text="move up", command=self.move_up).grid(column=1, row=5)
        ttk.Button(self.frame, text="move down", command=self.move_down).grid(column=2, row=5)
        ttk.Button(self.frame, text="Add Object", command=self.add_object).grid(column=0, row=6)



        sv_ttk.set_theme("dark")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
