from math import e
from tokenize import Pointfloat
from display_file import DisplayFile
from shape import Point, Line, Wireframe
from vector3 import Vector3


class DescritorOBJ:
    """
    Assume duas coisas:
        1. os índices dos vértices são relativos
        2. cada shape segue o seguinte formato:
            o [nome do objeto]
            usemtl [cor do objeto] # red, green, blue, etc
            v x y z --> coordenadas do objeto. Várias
            [f/l/p] [índices] --> índices relativos indicando a ordem das coordenadas

            Exemplo:
                o quadrado
                usemtl green
                v 0 0 0
                v 10 0 0
                v 10 10 0
                v 0 10 0
                f -4 -3 -2 -1
    """

    @classmethod
    def load(cls, path: str) -> DisplayFile:
        with open(path, "r") as file:
            lines = [line.strip() for line in file.readlines()]

            shapes = []
            i = 0

            while i < len(lines):
                while not len(lines[i]) or lines[i][0] == "#" and i < len(lines):
                    i += 1

                if i >= len(lines):
                    break

                name = color = points = indices = None
                points = []
                while not name or not color or not points or not indices:
                    if lines[i].startswith("o"):
                        name = lines[i][1:].strip()
                    elif lines[i].startswith("usemtl"):
                        color = lines[i][len("usemtl") :].strip()
                    elif lines[i].startswith("v"):
                        point = [float(p) for p in lines[i].split()[1:]]
                        points.append(Vector3.from_array(point))
                    else:
                        indices = [int(x) for x in lines[i].split()[1:]]

                    i += 1

                points = [points[i] for i in indices]
                match len(indices):
                    case 1:
                        shapes.append(Point(points, name, color))
                    case 2:
                        shapes.append(Line(points, name, color))
                    case _:
                        shapes.append(Wireframe(points, name, color))
                i += 1

        return DisplayFile(shapes)

    @classmethod
    def save(cls, display_file: DisplayFile, path: str):
        with open(path, "w") as file:
            for shape in display_file:
                file.write(f"o {shape.name}\n")
                file.write(f"usemtl {shape.color}\n")

                for point in shape.points:
                    file.write(f"v {point.x} {point.y} {point.z}\n")

                indices = " ".join([str(-i) for i in range(len(shape.points), 0, -1)])

                match shape.shape_name:
                    case "Point":
                        file.write(f"p {indices}\n")
                    case "Line":
                        file.write(f"l {indices}\n")
                    case "Wireframe":
                        file.write(f"f {indices}\n")

                file.write("\n")
