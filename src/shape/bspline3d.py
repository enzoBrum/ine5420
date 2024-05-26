from bspline import BSpline
from vector3 import Vector3

import numpy as np
from numpy import matmul

class BSpline3D(BSpline):
    control_points: list[Vector3]


    def __init__(
        self,
        control_points: list[Vector3],
        name: str | None = None,
        color: str = "red",
        points_per_segment: int = 10,
    ) -> None:
        
        self.control_points = control_points
        super().__init__([], name, color, points_per_segment)


    def _bsplines(self) -> None:
        new_points = []
        coeficients = self.__calculate_coefficients()
        
        self.points.clear()

        NST = 10
        Delta = 1 / (NST - 1)

        EDelta = [
            [0, 0, 0, 1],
            [Delta**3, Delta**2, Delta, 0],
            [6*Delta**3, 2*Delta**2, 0, 0],
            [6*Delta**3, 0, 0, 0]
        ]

        EDeltaT = np.transpose(EDelta)

        DX = np.matmul(np.matmul(EDelta, coeficients["X"]))
        DY = np.matmul(np.matmul(EDelta, coeficients["X"]))
        DZ = np.matmul(np.matmul(EDelta, coeficients["X"]))
        

        # for i in range()
    
    def __calculate_coefficients(self) -> None: 
        M = np.array([
            [-1, 3, -3, 1],
            [3, -6, 3, 0],
            [-3, 3, 0, 0],
            [1, 0, 0, 0]
        ])

        MT = np.transpose(M)
        
        coeficients = {"X": [], "Y": [], "Z": []}

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
            

            coeficients["X"].append(matmul(matmul(M, Gx), MT))
            coeficients["Y"].append(matmul(matmul(M, Gy), MT))
            coeficients["Z"].append(matmul(matmul(M, Gz), MT))
        
        return coeficients