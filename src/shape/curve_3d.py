from copy import deepcopy
from .curve import Curve2D
from transformations import Transformer3D
from clipping import Bezier3DClipper
from shape import Shape
from vector3 import Vector3

import numpy as np              

class Curve3D(Curve2D):
    shape_name = "Bezier3D"
    transformer = Transformer3D
    clipper = Bezier3DClipper
    control_points: list[Vector3]
    
    def __init__(self, control_points: list[Vector3], name: str, color: str, points_per_segment: int = 10):
        self.control_points = control_points

        points_per_segment = min(points_per_segment, 10)
        print(f"CONTROL POINTS: {control_points} ({len(control_points)})")
        super().__init__([], name, color, points_per_segment)
        

    def _bezier(self):
        M = np.array([
            [-1, 3, -3, 1],
            [3, -6, 3, 0],
            [-3, 3, 0, 0],
            [1, 0, 0, 0]
        ])
        MT = np.transpose(M)

        for i in range(0, len(self.control_points) - 15, 16):
            Gx = np.array([
                [self.control_points[i].x, self.control_points[i+1].x, self.control_points[i+2].x, self.control_points[i+3].x],
                [self.control_points[i+4].x, self.control_points[i+5].x, self.control_points[i+6].x, self.control_points[i+7].x],
                [self.control_points[i+8].x, self.control_points[i+9].x, self.control_points[i+10].x, self.control_points[i+11].x],
                [self.control_points[i+12].x, self.control_points[i+13].x, self.control_points[i+14].x, self.control_points[i+15].x]
            ])
            Gy = np.array([
                [self.control_points[i].y, self.control_points[i+1].y, self.control_points[i+2].y, self.control_points[i+3].y],
                [self.control_points[i+4].y, self.control_points[i+5].y, self.control_points[i+6].y, self.control_points[i+7].y],
                [self.control_points[i+8].y, self.control_points[i+9].y, self.control_points[i+10].y, self.control_points[i+11].y],
                [self.control_points[i+12].y, self.control_points[i+13].y, self.control_points[i+14].y, self.control_points[i+15].y]
            ])
            Gz = np.array([
                [self.control_points[i].z, self.control_points[i+1].z, self.control_points[i+2].z, self.control_points[i+3].z],
                [self.control_points[i+4].z, self.control_points[i+5].z, self.control_points[i+6].z, self.control_points[i+7].z],
                [self.control_points[i+8].z, self.control_points[i+9].z, self.control_points[i+10].z, self.control_points[i+11].z],
                [self.control_points[i+12].z, self.control_points[i+13].z, self.control_points[i+14].z, self.control_points[i+15].z]
            ])
            
            # s --> coluna
            # t --> linha
            #
            # iteração i 
            # - Calcual point_matrix[s, t]
            #
            #
            # Depois de calcular tudo.
            # 1. Linhas verticais --> cada coluna da matriz é uma linha da nossa superfície
            # 2. linhas horizontais --> cada linha da matriz é uma linha da nossa superfície
            range_s = list(np.linspace(0, 1, self.points_per_segment))
            range_t = list(np.linspace(0, 1, self.points_per_segment))
            
            print(f"RANGE S: {len(range_s)}")
            print(f"RANGE T: {len(range_t)}")
            
            points_matrix = [[None for _i in range(len(range_s))] for _j in range(len(range_t))]

            for j, s in enumerate(range_s):
                S = np.array([s**3, s**2, s, 1])

                for i, t in enumerate(range_t):
                    T = np.transpose(np.array([t**3, t**2, t, 1]))
                    
                    x = y = z = S
                    for matrix in (M, Gx, MT, T):
                        x = np.matmul(x, matrix)
                    for matrix in (M, Gy, MT, T):
                        y = np.matmul(y, matrix)
                    for matrix in (M, Gz, MT, T):
                        z = np.matmul(z, matrix)

                    points_matrix[i][j] = Vector3(x, y, z)
            
            # Linhas horizontais
            for i in range(len(points_matrix)):
               for j in range(len(points_matrix[i]) - 1):
                   self.points.append(deepcopy(points_matrix[i][j]))
                   self.points.append(deepcopy(points_matrix[i][j+1]))
                    
            #Linhas verticais
            for j in range(len(points_matrix[0])):
                for i in range(len(points_matrix) - 1):
                    self.points.append(deepcopy(points_matrix[i][j]))
                    self.points.append(deepcopy(points_matrix[i+1][j]))

        self.ppc_points = deepcopy(self.points)
        self.transformer.points = self.points
        
        # print(f"LEN: {len(self.points)}")
        print(f"BEZIER: {self.points}")
        
    def process_clipped_points(self, points: list[Vector3], transformed_points: list[Vector3], window_min: Vector3, window_max: Vector3) -> list[Vector3]:
        return transformed_points