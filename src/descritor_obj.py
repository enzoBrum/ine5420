from itertools import chain
from math import e
import os
from pathlib import Path

from display_file import DisplayFile
from shape import Line, Point, Wireframe
from shape import Shape
from vector3 import Vector3


class DescritorOBJ:

    # Linhas que começam com palavras que não estão nos sets abaixo são ignoradas.
    obj_keywords: set[str] = {
        "v",
        "o",
        "g",  # Por enquanto, tratamos `g` e o `o` como a mesma coisa.
        "f",
        "p",
        "mtllib",
        "usemtl",
    }

    mtl_keywords: set[str] = {
        "newmtl",
        "Kd",
        "Ka",
    }  # Por enquanto, Ka e Kd são tratadas da mesma forma

    @classmethod
    def hex_to_rgb(cls, hex_color: str) -> tuple[float, float, float]:
        """
        Convert uma cor em hexadecimal para uma em rgb usando valores entre 0 e 1.
        E.g: #ffffff --> (1.000000, 1.000000, 1.000000)
        """

        color_value = int(hex_color[1:], 16)
        mask = 0x0000FF

        blue = (color_value & mask) / 255
        green = ((color_value >> 8) & mask) / 255
        red = ((color_value >> 16) & mask) / 255

        return red, green, blue

    @classmethod
    def rgb_to_hex(cls, rgb_color: tuple[float, float, float]) -> str:
        """
        Converte uma cor em RGB (com valores entre 0 e 1) para hexadecimal
        E.g: (1.000000, 1.000000, 1.000000) --> #ffffff
        """

        red, green, blue = [int(255 * col) for col in rgb_color]
        return f"#{red:02x}{green:02x}{blue:02x}"

    @classmethod
    def __parse_mtllib(cls, obj_path: Path, line: str) -> dict[str, str]:
        mtl_filenames = [Path(filename) for filename in line.split()[1:]]
        print(f"MTL files found: {mtl_filenames}")
        hex_color_names = {}
        for filename in mtl_filenames:
            if not filename.exists():
                filename = obj_path.parent / filename

            with filename.open("r") as file:
                lines = [l.strip() for l in file.readlines()]

                i = 0
                while i < len(lines):
                    curr_line = lines[i]
                    if not curr_line or curr_line[0] == "#":
                        i += 1
                        continue

                    first_word = curr_line[0 : curr_line.find(" ")]
                    if first_word not in cls.mtl_keywords:
                        i += 1
                        continue
                    if first_word == "newmtl":
                        color_name = curr_line.split()[1]

                        while not curr_line.startswith(
                            "Ka"
                        ) and not curr_line.startswith("Kd"):
                            i += 1
                            curr_line = lines[i]

                        color_hex = cls.rgb_to_hex(
                            [float(val) for val in curr_line.split()[1:]]
                        )

                        hex_color_names[color_hex] = color_name

                    i += 1

        print(f"Colors found: {hex_color_names}")
        return hex_color_names

    @classmethod
    def __parse_shape(
        cls,
        lines: list[str],
        i: int,
        hex_color_name: dict[str, str],
        vertices: list[Vector3],
    ) -> tuple[int, Shape]:
        name: str = None
        color: str = None
        indices: list[int] = None

        name_color_hex = {name: color_hex for color_hex, name in hex_color_name.items()}
        while name is None or color is None or indices is None:
            line = lines[i]
            if line.startswith("o"):
                name = " ".join(line.split()[1:])
            elif line.startswith("v"):
                x, y, z = [float(val) for val in line.split()[1:]]
                vertices.append(Vector3(x, y, z))
            elif line.startswith("usemtl"):
                color = name_color_hex[" ".join(line.split()[1:])]
            elif line[0 : line.find(" ")] in ("p", "l", "f"):
                indices = [int(x) for x in line.split()[1:]]
            i += 1

        points = [vertices[idx - 1] for idx in indices]
        match len(points):
            case 1:
                return i, Point(points, name, color)
            case 2:
                return i, Line(points, name, color)
            case _:
                return i, Wireframe(points, name, color)

    @classmethod
    def load(cls, obj_path: str) -> tuple[DisplayFile, dict[str, str]]:
        """
        Retorna o display_file e um dicionário que mapeia o valor hexadecimal de uma cor ao seu nome.
        """

        obj_path: Path = Path(obj_path).absolute()
        print(f"Loading file: {obj_path}")
        with obj_path.open("r") as file:
            lines = [line.strip() for line in file.readlines()]

            vertices: list[Vector3] = []
            shapes: list[Shape] = []
            hex_color_name: dict[str, str] = {}
            i = 0

            while i < len(lines):
                line = lines[i]
                if not line or line[0] == "#":
                    i += 1
                    continue

                first_word = line[0 : line.find(" ")]
                match first_word:
                    case "mtllib":
                        hex_color_name |= cls.__parse_mtllib(obj_path, line)
                        i += 1
                    case "v":
                        x, y, z = [float(x) for x in line.split()[1:]]
                        vertices.append(Vector3(x, y, z))
                        i += 1
                    case "o" | "g":
                        i, shape = cls.__parse_shape(lines, i, hex_color_name, vertices)
                        shapes.append(shape)
                        print(f"Created shape {shape} with vertices: {shape.points}")
                        # O __parse_shape já retorna o i incrementado
                    case _:
                        print(f"Ignoring wrong word: {first_word}")

        return DisplayFile(shapes), hex_color_name

    @classmethod
    def save(cls, display_file: DisplayFile, name_color_hex: dict[str, str], path: str):
        """
        name_color_hex: mapeia o nome de uma cor à sua representação em hexadecimal
        E.x: {"white": "#ffffff", "black": "#000000"}
        """
        if not len(display_file):
            return

        hex_color_name = {
            color_hex: color_name for color_name, color_hex in name_color_hex.items()
        }

        mtl_path = (
            path + ".mtl" if not path.endswith(".obj") else path.replace(".obj", ".mtl")
        )
        with open(mtl_path, "w") as file:
            for color_hex, name in hex_color_name.items():
                file.write(f"newmtl {name}\n")

                rgb_color = [str(color) for color in cls.hex_to_rgb(color_hex)]
                file.write(f"Kd {' '.join(rgb_color)}\n\n")

        with open(path, "w") as file:
            all_points = [shape.points for shape in display_file]
            all_points: list[Vector3] = sorted(chain.from_iterable(all_points))

            points_idx: dict[Vector3, int] = {}
            for p in all_points:
                if p in points_idx:
                    continue
                points_idx[p] = len(points_idx) + 1

            file.write(f"mtllib {os.path.basename(mtl_path)}\n\n")
            file.writelines(
                [f"v {point.x} {point.y} {point.z}\n" for point in points_idx]
            )
            file.write("\n")

            for shape in display_file:
                file.write(f"o {shape.name}\n")
                file.write(f"usemtl {hex_color_name[shape.color]}\n")

                indices = [points_idx[point] for point in shape.points]
                indices = " ".join([str(idx) for idx in indices])
                match shape.shape_name:
                    case "Point":
                        file.write(f"p {indices}\n")
                    case "Line":
                        file.write(f"l {indices}\n")
                    case "Wireframe":
                        file.write(f"f {indices}\n")

                file.write("\n")


if __name__ == "__main__":
    from sys import argv

    print(DescritorOBJ.load(argv[1]))
