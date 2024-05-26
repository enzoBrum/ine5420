from .bspline import BSpline
from vector3 import Vector3
from transformations import Transformer3D
from clipping import Bezier3DClipper

from copy import deepcopy
import numpy as np

class BSpline3D(BSpline):
    control_points: list[Vector3]
    shape_name: str = "bspline3D"
    transformer = Transformer3D
    clipper = Bezier3DClipper

    def __init__(
        self,
        control_points: list[list[Vector3]],
        name: str | None = None,
        color: str = "red",
        points_per_segment: int = 10,
    ) -> None:
        
        self.control_points = control_points
        points_per_segment = min(points_per_segment, 10)
        super().__init__([], name, color, points_per_segment)
        
    def _bsplines(self) -> None:
        new_points = []
        coeficients = self._calculate_coefficients()
        
        NST = 5
        Delta = 1 / (NST - 1)


        EDelta = [
            [0, 0, 0, 1],
            [Delta**3, Delta**2, Delta, 0],
            [6*Delta**3, 2*Delta**2, 0, 0],
            [6*Delta**3, 0, 0, 0]
        ]

        EDeltaT = np.transpose(EDelta)

        for i in range(len(coeficients["X"])):
            DX = np.matmul(np.matmul(EDelta, coeficients["X"][i]), EDeltaT)
            DY = np.matmul(np.matmul(EDelta, coeficients["Y"][i]), EDeltaT)
            DZ = np.matmul(np.matmul(EDelta, coeficients["Z"][i]), EDeltaT)

            DXT = np.transpose(DX)
            DYT = np.transpose(DY)
            DZT = np.transpose(DZ)

            # s
            for _ in range(NST):
                points = self._calculate_segment_points(DX[0], DY[0], DZ[0])
                for j in range(len(points) - 1):
                    new_points.append(deepcopy(points[j]))
                    new_points.append(deepcopy(points[j+1]))
                
                for j in range(3):
                    for k in range(4):
                        DX[j][k] += DX[j+1][k]
            
            # t
            for _ in range(NST):
                points = self._calculate_segment_points(DXT[0], DYT[0], DZT[0])

                for j in range(len(points) - 1):
                    new_points.append(deepcopy(points[j]))
                    new_points.append(deepcopy(points[j+1]))
                
                for j in range(3):
                    for k in range(4):
                        DXT[j][k] += DXT[j+1][k]
        
        self.points = new_points
        
    def _calculate_coefficients(self) -> None: 
        M = np.array([
            [-1, 3, -3, 1],
            [3, -6, 3, 0],
            [-3, 3, 0, 0],
            [1, 0, 0, 0]
        ])

        MT = np.transpose(M)
        
        coeficients = {"X": [], "Y": [], "Z": []}

        for i in range(len(self.control_points) - 3):
            for j in range(len(self.control_points) - 3):
                Gx = np.array([
                    [self.control_points[i][j].x, self.control_points[i][j+1].x, self.control_points[i][j+2].x, self.control_points[i][j+3].x],
                    [self.control_points[i+1][j].x, self.control_points[i+1][j+1].x, self.control_points[i+1][j+2].x, self.control_points[i+1][j+3].x],
                    [self.control_points[i+2][j].x, self.control_points[i+2][j+1].x, self.control_points[i+2][j+2].x, self.control_points[i+2][j+3].x],
                    [self.control_points[i+3][j].x, self.control_points[i+3][j+1].x, self.control_points[i+3][j+2].x, self.control_points[i+3][j+3].x]
                ])
                
                Gy = np.array([
                    [self.control_points[i][j].y, self.control_points[i][j+1].y, self.control_points[i][j+2].y, self.control_points[i][j+3].y],
                    [self.control_points[i+1][j].y, self.control_points[i+1][j+1].y, self.control_points[i+1][j+2].y, self.control_points[i+1][j+3].y],
                    [self.control_points[i+2][j].y, self.control_points[i+2][j+1].y, self.control_points[i+2][j+2].y, self.control_points[i+2][j+3].y],
                    [self.control_points[i+3][j].y, self.control_points[i+3][j+1].y, self.control_points[i+3][j+2].y, self.control_points[i+3][j+3].y]
                ])
                Gz = np.array([
                    [self.control_points[i][j].z, self.control_points[i][j+1].z, self.control_points[i][j+2].z, self.control_points[i][j+3].z],
                    [self.control_points[i+1][j].z, self.control_points[i+1][j+1].z, self.control_points[i+1][j+2].z, self.control_points[i+1][j+3].z],
                    [self.control_points[i+2][j].z, self.control_points[i+2][j+1].z, self.control_points[i+2][j+2].z, self.control_points[i+2][j+3].z],
                    [self.control_points[i+3][j].z, self.control_points[i+3][j+1].z, self.control_points[i+3][j+2].z, self.control_points[i+3][j+3].z]
                ])
                

                coeficients["X"].append(np.matmul(np.matmul(M, Gx), MT))
                coeficients["Y"].append(np.matmul(np.matmul(M, Gy), MT))
                coeficients["Z"].append(np.matmul(np.matmul(M, Gz), MT))
        
        return coeficients

    def process_clipped_points(self, points: list[Vector3], transformed_points: list[Vector3], window_min: Vector3, window_max: Vector3) -> list[Vector3]:
        return transformed_points