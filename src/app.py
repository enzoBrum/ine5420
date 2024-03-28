from functools import wraps
from tkinter import Canvas, E, Event, Listbox, N, NS, NW, S, StringVar, Tk, Toplevel, W, ttk

import sv_ttk

from display_file import DisplayFile
from interface import Viewport, Window
from shape import Line, Point, Wireframe, Shape
from widgets import ShapeListbox, WindowControls
from vector3 import Vector3
from transformations import rotate, translation, scale, center

VIEWPORT_DIMENSION = (600, 600)
GEOMETRY = "1000x1000"
PROGRAM_NAME = "sistema básico de CG 2D"

"""
TODO:
    - mudar  código do App para outras classes em widgets/
"""

class App:
    window: Window
    viewport: Viewport
    display_file: DisplayFile
    display_file_str_var: StringVar
    root: Tk
    frame: ttk.Frame
    selected_shape: Shape | None
    selected_shape_old_color: str
    shape_listbox: ShapeListbox
    window_controls: WindowControls

    def redraw_viewport(func):
        @wraps(func)
        def wrapper(self: "App", *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.viewport.draw(self.window, self.display_file)
            return result

        return wrapper

    @redraw_viewport
    def add_point(self, x, y, name, color):
        self.display_file.append(Point([Vector3(x, y)], name=name, color=color))

    @redraw_viewport
    def add_line(self, x1, y1, x2, y2, name, color):
        self.display_file.append(Line([Vector3(x1, y1), Vector3(x2, y2)], name=name, color=color))

    @redraw_viewport
    def add_wireframe(self, points, name, color):
        self.display_file.append(
            Wireframe([Vector3(x, y) for x, y in points], name=name, color=color)
        )

    @redraw_viewport
    def rotate_window(self):
        rotate(45, Vector3(*center(self.window.points)), self.window.points)

    @redraw_viewport
    def zoom_out(self):
        self.window.zoom(-1)

    @redraw_viewport
    def zoom_in(self):
        self.window.zoom(1)

    @redraw_viewport
    def move_left(self):
        self.window.move("L")

    @redraw_viewport
    def move_right(self):
        self.window.move("R")

    @redraw_viewport
    def move_up(self):
        self.window.move("U")

    @redraw_viewport
    def move_down(self):
        self.window.move("D")

    @redraw_viewport
    def translation_up(self):
        translation(0, 10, self.selected_shape.points)
    
    @redraw_viewport
    def translation_down(self):
        translation(0, -10, self.selected_shape.points)

    @redraw_viewport
    def translation_right(self):
        translation(10, 0, self.selected_shape.points)

    @redraw_viewport
    def translation_left(self):
        translation(-10, 0, self.selected_shape.points)

    @redraw_viewport
    def scale_zoom(self):
        scale(1.2, self.selected_shape.points)
    
    @redraw_viewport
    def scale_out(self):
        scale(0.8, self.selected_shape.points)

    @redraw_viewport
    def rotate(self, degree, x, y):
        rotate(degree, Vector3(x, y, 1), self.selected_shape.points)

    @redraw_viewport
    def __update_selected_shape(self, event: Event, clear_selection: bool = False):
        if clear_selection:
            if self.selected_shape:
                self.selected_shape.color = self.selected_shape_old_color
                self.selected_shape = None
                self.xvar.set(0)
                self.yvar.set(0)
            return
        

        index = event.widget.curselection()
        if index:
            if self.selected_shape:
                self.selected_shape.color = self.selected_shape_old_color
            self.selected_shape = self.display_file.get_shape_by_id(event.widget.get(index[0]))
            self.selected_shape_old_color = self.selected_shape.color
            print("Color: %s" % self.selected_shape_old_color)
            self.selected_shape.color = "gold"
            
            cx, cy = center(self.selected_shape.points)
            self.xvar.set(cx)
            self.yvar.set(cy)

        print(f"Selected shape: {self.selected_shape}")

    def __create_object_listbox(self, menu_frame: ttk.Frame):
        ttk.Label(menu_frame, text="Objetos").grid(column=0, row=1, sticky="w")

        listbox = Listbox(
            menu_frame,
            height=12,
            width=24,
            borderwidth=3,
            listvariable=self.display_file.shapes_str_var,
            highlightbackground="black",
            highlightthickness=1,
        )
        listbox.grid(column=0, row=2, sticky=(N, S, E, W))
        scrollbar = ttk.Scrollbar(menu_frame, orient="vertical", command=listbox.yview)
        scrollbar.grid(column=1, row=2, sticky=(N, S, W))
        listbox.configure(yscrollcommand=scrollbar.set)
        listbox.bind("<<ListboxSelect>>", self.__update_selected_shape)
        
        button_frame = ttk.Frame(menu_frame)
        button_frame.grid(column=0, row=3)
        ttk.Button(button_frame, text="Add Object", command=self.__add_object).grid(
            column=0, row=0
        )
        ttk.Button(button_frame, text="Clear Selection", command=lambda: self.__update_selected_shape(None, clear_selection=True)).grid(
            column=1, row=0, sticky="w"
        )

    def __add_object(self):
        frame = Toplevel(self.root)
        frame.title("Add Object")

        shape_frame = ttk.Frame(frame)
        shape_frame.grid(row=4, columnspan=2, padx=10, pady=5)

        ttk.Label(frame, text="Object Name:").grid(row=0, column=0, padx=10, pady=5)
        entry_name = ttk.Entry(frame)
        entry_name.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(frame, text="Color:").grid(row=1, column=0, padx=10, pady=5)
        entry_color = ttk.Entry(frame)
        entry_color.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(frame, text="Shape:").grid(row=2, column=0, padx=10, pady=5)
        type_var = StringVar(frame)
        options = ["Select a shape", "Point", "Line", "Wireframe"]
        ttk.OptionMenu(
            frame,
            type_var,
            *options,
            command=lambda selection: self.__update_shape_frame(
                shape_frame, type_var.get()
            ),
        ).grid(row=2, column=1, padx=10, pady=5)

        ttk.Button(
            frame,
            text="Add",
            command=lambda: self.__add_selected_object(
                type_var.get(), entry_name.get(), entry_color.get(), shape_frame
            ),
        ).grid(row=6, columnspan=2, padx=10, pady=5)

    def __add_selected_object(self, type_obj: str, name: str, color: str, shape_frame: ttk.Frame):
        row = 4 if type_obj == 'Line' else 2
        column = 0 if type_obj == 'Wireframe' else 1
        if name == '':
            ttk.Label(shape_frame, text="Digit a name.").grid(row=row, column=column)
            return
        
        colors = ['black', 'yellow', 'blue', 'green', 'red', 'orange', 'purple', 'gray']
        if color not in colors:
            ttk.Label(shape_frame, text=f'Digit an available color: {", ".join(colors)}').grid(row=row, column=column)
            return

        try:
            if type_obj == "Point":
                x = float(shape_frame.winfo_children()[1].get())
                y = float(shape_frame.winfo_children()[3].get())
                self.add_point(x, y, name, color)
            elif type_obj == "Line":
                x1 = float(shape_frame.winfo_children()[1].get())
                y1 = float(shape_frame.winfo_children()[3].get())
                x2 = float(shape_frame.winfo_children()[5].get())
                y2 = float(shape_frame.winfo_children()[7].get())
                self.add_line(x1, y1, x2, y2, name, color)
            elif type_obj == "Wireframe":
                points = str(shape_frame.winfo_children()[1].get())
                self.add_wireframe(eval(f"[{points}]"), name, color)
        except:
            error_message = "X's and Y's must be a number." if type_obj in ['Line', 'Point'] else \
                            "Format is incorrect or X's and Y's are not a number."
            ttk.Label(shape_frame, text=error_message).grid(row=row, column=column)
        
        self.__update_shape_frame(shape_frame, type_obj)
            
    def __update_shape_frame(self, shape_frame: ttk.Frame, type_obj: str):
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
            ttk.Label(
                shape_frame,
                text="Give the points in exactly format: (x1, y1), (x2, y2), (x3,y3) ...",
            ).grid(row=0, column=0, padx=5, pady=5)
            entry_points = ttk.Entry(shape_frame)
            entry_points.grid(row=1, column=0, padx=5, pady=5)

    
    def __create_window_controls(self, menu_frame: ttk.Frame):
        window_control_frame = ttk.Frame(
            menu_frame, padding="12 -3 12 12", border=3, borderwidth=3, relief="groove"
        )

        window_control_frame.grid(column=0, row=4, sticky="nswe", pady=12)
        window_control_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(window_control_frame, text="Window").grid(
            column=0, row=4, sticky="nw"
        )

        ttk.Label(window_control_frame, text="Passo:").grid(column=0, row=5, sticky="w")

        ttk.Entry(window_control_frame, textvariable=self.window.step_var).grid(
            column=1, row=5, sticky="w"
        )

        move_controls_frame = ttk.Frame(window_control_frame, padding="3 30 3 3")
        move_controls_frame.grid(column=0, row=6, columnspan=2, rowspan=2)
        ttk.Button(move_controls_frame, text="Up", command=self.move_up).grid(
            column=1, row=0, sticky="ns"
        )
        ttk.Button(move_controls_frame, text="Left", command=self.move_left).grid(
            column=0,
            row=1,
            sticky="w",
        )
        ttk.Button(move_controls_frame, text="Right", command=self.move_right).grid(
            column=2, row=1, sticky="e"
        )
        ttk.Button(move_controls_frame, text="Down", command=self.move_down).grid(
            column=1, row=1
        )

        zoom_controls = ttk.Frame(window_control_frame, padding="3 30 3 3")
        zoom_controls.grid(column=0, row=8, columnspan=2)
        ttk.Button(zoom_controls, text="In", command=self.zoom_in).grid(column=0, row=3)
        ttk.Button(zoom_controls, text="Out", command=self.zoom_out).grid(
            column=1, row=3
        )
        ttk.Button(zoom_controls, text="Rotate", command=self.rotate_window).grid(column=2, row=3)

        move_object_frame = ttk.Frame(window_control_frame, padding="3 30 3 3")
        move_object_frame.grid(column=0, row=9, columnspan=1)
        ttk.Label(move_object_frame, text="Object Translation:").grid(row=0, column=0, padx=5)
        ttk.Button(move_object_frame, text="Up", command=self.translation_up).grid(row=1, column=2, sticky="ns")
        ttk.Button(move_object_frame, text="Left", command=self.translation_left).grid(row=2, column=1, sticky="w",)
        ttk.Button(move_object_frame, text="Right", command=self.translation_right).grid(row=2, column=3, sticky="e")
        ttk.Button(move_object_frame, text="Down", command=self.translation_down).grid(row=2, column=2)

        scale_frame = ttk.Frame(window_control_frame, padding="3 30 3 3")
        scale_frame.grid(column=0, row=11, columnspan=1)
        ttk.Label(scale_frame, text="Object Scale:").grid(row=0, column=0, padx=7)
        ttk.Button(scale_frame, text="+", command=self.scale_zoom).grid(row=0, column=1)
        ttk.Button(scale_frame, text="-", command=self.scale_out).grid(row=0, column=2)

        object_rotation_frame = ttk.Frame(window_control_frame, padding="10 -3 10 10", 
                                         border=3, borderwidth=3, relief="groove")
        object_rotation_frame.grid(column=0, row=13, pady=12)
        ttk.Label(object_rotation_frame, text="Rotation").grid(row=0, column=0, sticky="n")
        ttk.Label(object_rotation_frame, text="Degree:").grid(row=1, column=0)
        degree = ttk.Entry(object_rotation_frame, width=10)
        degree.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(object_rotation_frame, text="Rotation point:").grid(row=2, column=0)

        ttk.Label(object_rotation_frame, text="X:").grid(row=3, column=0)
        self.xvar = StringVar(object_rotation_frame)
        self.xvar.set(0)
        entry_x = ttk.Entry(object_rotation_frame, textvariable=self.xvar, width=10)
        entry_x.grid(row=3, column=1)

        ttk.Label(object_rotation_frame, text="Y:").grid(row=4, column=0)
        self.yvar = StringVar(object_rotation_frame)
        self.yvar.set(0)
        entry_y = ttk.Entry(object_rotation_frame, textvariable=self.yvar, width=10)
        entry_y.grid(row=4, column=1)

        ttk.Button(object_rotation_frame, text='Rotate', command=lambda: self.rotate(float(degree.get()), float(entry_x.get()), float(entry_y.get()))).grid(row=5, column=0)




    def __create_left_menu(self):
        menu_frame = ttk.Frame(
            self.frame, padding="12 -3 12 12", border=3, borderwidth=3, relief="groove"
        )
        menu_frame.grid(column=0, row=0)

        ttk.Label(menu_frame, text="Menu de Funções").grid(column=0, row=0, sticky="n")

        self.__create_object_listbox(menu_frame)
        self.__create_window_controls(menu_frame)

    def __create_viewport_and_log(self):
        viewport_frame = ttk.Frame(self.frame, padding="12 -3 12 12")
        viewport_frame.grid(column=1, row=0)

        ttk.Label(viewport_frame, text="Viewport").grid(column=0, row=0, sticky="w")

        self.viewport = Viewport(
            Vector3(0, 0),
            Vector3(VIEWPORT_DIMENSION[0], VIEWPORT_DIMENSION[1]),
            viewport_frame,
            "#ffffff",
        )

        self.viewport.canvas.grid(column=0, row=1)

    def __test(self):
        menu_frame = ttk.Frame(
            self.frame, padding="12 -3 12 12", border=3, borderwidth=3, relief="groove"
        )
        menu_frame.grid(column=0, row=0)

        ttk.Label(menu_frame, text="Menu de Funções").grid(column=0, row=0, sticky="n")

        self.shape_listbox = ShapeListbox(
            menu_frame, 
            self.display_file, 
            lambda: self.viewport.draw(self.window.min, self.window.max, self.display_file), 
            0, 
            2
        )

        self.window_controls = WindowControls(
            menu_frame,
            self.window,
            lambda: self.viewport.draw(self.window.min, self.window.max, self.display_file),
            0,
            4
        )


    def __init__(self):
        self.root = Tk()
        self.root.title(PROGRAM_NAME)
        self.root.geometry(GEOMETRY)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.selected_shape = None
        self.window = Window(
            Vector3(0, 0), Vector3(VIEWPORT_DIMENSION[0], VIEWPORT_DIMENSION[1])
        )
        self.frame = ttk.Frame(self.root, padding="3 3 12 12")
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.display_file = DisplayFile()

        self.__create_left_menu()
        # self.__test()
        self.__create_viewport_and_log()

        self.add_line(100,100,500,500, "Foo", "blue")
        self.add_line(300,400,500,500, "Bar", "red")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
