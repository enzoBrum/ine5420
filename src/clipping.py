from abc import ABC, abstractmethod

from numpy import poly

from shape import Line, Point, Wireframe
from shape.curve import Curve2D
from vector3 import Vector3

class Clipper(ABC):
    @classmethod
    @abstractmethod
    def clip(cls, points: list[Vector3], window_max: Vector3, window_min: Vector3) -> list[Vector3]:
        ...

class PointClipper(Clipper):
    @classmethod
    def clip(cls, points: list[Vector3], window_max: Vector3, window_min: Vector3) -> list[Vector3]:
        x, y = points[0]
        return points if window_min.x <= x <= window_max.x and window_min.y <= y <= window_max.y else []

class LiangBarsky(Clipper):
    @classmethod
    def clip(cls, points: list[Vector3], window_max: Vector3, window_min: Vector3) -> list[Vector3]:
        print("Clipando com Liang")
        p_b, p_a = points

        p1 = -(p_a.x - p_b.x)
        p2 = p_a.x - p_b.x
        p3 = -(p_a.y - p_b.y)
        p4 = p_a.y - p_b.y
        pk = [p1, p2, p3, p4]

        q1 = p_b.x - window_min.x
        q2 = window_max.x - p_b.x
        q3 = p_b.y - window_min.y
        q4 = window_max.y - p_b.y
        qk = [q1, q2, q3, q4]

        r1 = q1 / p1
        r2 = q2 / p2
        r3 = q3 / p3
        r4 = q4 / p4
        rk = [r1, r2, r3, r4]

        if any(p == 0 and q < 0 for p, q in zip(pk, qk)):
            return []

        pk_up = [i for i in range(len(pk)) if pk[i] > 0]
        pk_down = [i for i in range(len(pk)) if pk[i] < 0]

        c1 = max([rk[i] for i in pk_down] + [0])
        c2 = min([rk[i] for i in pk_up] + [1])

        if c1 > c2:
            return []

        x1 = p_b.x + c1 * p2
        y1 = p_b.y + c1 * p4
        x2 = p_b.x + c2 * p2
        y2 = p_b.y + c2 * p4

        return [Vector3(x1, y1), Vector3(x2, y2)]

class CohenSutherland(Clipper):
    @classmethod
    def __get_rc(cls, x: float, y: float, xw_min: float, xw_max: float, yw_min: float, yw_max: float) -> int:
        rc = 0
        if x < xw_min:
            rc |= 1 << 0
        elif x > xw_max:
            rc |= 1 << 1

        if y < yw_min:
            rc |= 1 << 2
        elif y > yw_max:
            rc |= 1 << 3

        return rc

    @classmethod
    def clip(cls, points: list[Vector3], window_max: Vector3, window_min: Vector3) -> list[Vector3]:
        print("Clipando com cohen")
        xw_min = window_min.x
        xw_max = window_max.x

        yw_min = window_min.y
        yw_max = window_max.y

        p1, p2 = points
        x1, y1 = p1
        x2, y2 = p2

        if x1 > x2:
            x1, y1, x2, y2 = x2, y2, x1, y1

        rc1 = cls.__get_rc(x1, y1, xw_min, xw_max, yw_min, yw_max)
        rc2 = cls.__get_rc(x2, y2, xw_min, xw_max, yw_min, yw_max)

        # print(f"RC1: {bin(rc1)}, RC2: {bin(rc2)}")
        # print(f"XW_MIN: {xw_min}, X1: {x1}, X2: {x2}")

        # dentro
        if rc1 == rc2 == 0:
            return [Vector3(x1, y1), Vector3(x2, y2)]

        # totalmente fora
        if (rc1 & rc2) != 0:
            return []

        # parcialmente dentro
        if abs(x2 - x1) < 1e-6:
            if not (xw_min <= x1 <= xw_max):
                return []

            if y1 <= y2:
                y1 = max(y1, yw_min)
                y2 = min(y2, yw_max)
            else:
                y2 = max(y2, yw_min)
                y1 = min(y1, yw_max)
            return [Vector3(x1, y1), Vector3(x2, y2)]

        m = (y2 - y1) / (x2 - x1)

        # p1 sempre possui x maior que p2.
        # o y é desconhecido.

        # p1 no canto superior esquerdo
        if rc1 == 0b1001:
            old_y1 = y1
            y1 = m * (xw_min - x1) + y1
            x1 = x1 + 1 / m * (yw_max - old_y1)

            x_inside = xw_min <= x1 <= xw_max
            y_inside = yw_min <= y1 <= yw_max
            if not (x_inside or y_inside):
                return []

            if not x_inside:
                x1 = xw_min
            if not y_inside:
                y1 = yw_max
        # p1 na esquerda
        elif rc1 == 0b0001:
            y1 = m * (xw_min - x1) + y1

            if not (yw_min <= y1 <= yw_max):
                return []
            x1 = xw_min
        # p1 no canto inferior esquerdo
        elif rc1 == 0b0101:
            old_y1 = y1
            y1 = m * (xw_min - x1) + y1
            x1 = x1 + 1 / m * (yw_min - old_y1)

            x_inside = xw_min <= x1 <= xw_max
            y_inside = yw_min <= y1 <= yw_max
            if not (x_inside or y_inside):
                return []

            if not x_inside:
                x1 = xw_min
            if not y_inside:
                y1 = yw_min
        # p1 no topo
        elif rc1 == 0b1000:
            x1 = x1 + 1 / m * (yw_max - y1)

            if not (xw_min <= x1 <= xw_max):
                return []

            y1 = yw_max
        # p1 no fundo
        elif rc1 == 0b0100:
            x1 = x1 + 1 / m * (yw_min - y1)

            if not (xw_min <= x1 <= xw_max):
                return []
            y1 = yw_min
        # p2 no topo
        if rc2 == 0b1000:
            x2 = x2 + 1 / m * (yw_max - y2)

            if not (xw_min <= x2 <= xw_max):
                return []
            y2 = yw_max
        # p2 no fundo
        elif rc2 == 0b0100:
            x2 = x2 + 1 / m * (yw_min - y2)

            if not (xw_min <= x2 <= xw_max):
                return []
            y2 = yw_min
        # p2 no canto superior direito
        elif rc2 == 0b1010:
            old_y2 = y2
            y2 = m * (xw_max - x2) + y2
            x2 = x2 + 1 / m * (yw_max - old_y2)
            x_inside = xw_min <= x2 <= xw_max
            y_inside = yw_min <= y2 <= yw_max
            if not (x_inside or y_inside):
                return []

            if not x_inside:
                x2 = xw_max
            if not y_inside:
                y2 = yw_max
        # p2 na direita
        elif rc2 == 0b0010:
            y2 = m * (xw_max - x2) + y2

            if not (yw_min <= y2 <= yw_max):
                return []

            x2 = xw_max
        # p2 no canto inferior esquerdo
        elif rc2 == 0b0110:
            old_y2 = y2
            y2 = m * (xw_max - x2) + y2
            x2 = x2 + 1 / m * (yw_min - old_y2)
            x_inside = xw_min <= x2 <= xw_max
            y_inside = yw_min <= y2 <= yw_max
            if not (x_inside or y_inside):
                return []

            if not x_inside:
                x2 = xw_max
            if not y_inside:
                y2 = yw_min
        # print(f"X1: {x1}, X2: {x2}, Y1: {y1}, Y2: {y2}, XW_MAX: {xw_max}")
        return [Vector3(x1, y1), Vector3(x2, y2)]

class SutherlandHodgman(Clipper):
    @classmethod
    def clip(cls, points: list[Vector3], window_max: Vector3, window_min: Vector3) -> list[Vector3]:
        points_list = []
        extra_points = 0
        for i in range(len(points)):
            p = points[i]
            q = points[(i + 1) % len(points)]
            print(f"P: {p}, Q: {q}")

            p_inside = (window_min.x <= p.x <= window_max.x) and (
                window_min.y <= p.y <= window_max.y
            )
            q_inside = (window_min.x <= q.x <= window_max.x) and (
                window_min.y <= q.y <= window_max.y
            )

            if p_inside and q_inside:
                print("P e Q dentro")
                points_list.append(q)
            elif p_inside and not q_inside:
                print("P dentro e Q fora")
                intersect = LiangBarsky.clip([p,q], window_max, window_min)
                points_list.append(intersect[1])
            elif not p_inside and q_inside:
                print("P fora e Q dentro")
                intersect = LiangBarsky.clip([p,q], window_max, window_min)
                if intersect[0] == q:
                    points_list.append(intersect[1])
                else:
                    points_list.append(intersect[0])
                points_list.append(q)
            elif not p_inside and not q_inside:
                print("P e Q fora")
                intersect = LiangBarsky.clip([p,q], window_max, window_min)
                if len(intersect) > 0:
                    points_list.append(intersect[0])
                    points_list.append(intersect[1])
                else:
                    # q não foi inserido, logo não há seguimento entre q e o póximo ponto.
                    # polygon.ppc_inexistent_lines.add(
                    #     (i % len(polygon.ppc_points), (i + 1) % len(polygon.ppc_points))
                    # )
                    if (p.x < window_min.x and q.y < window_min.y) or (
                        q.x < window_min.x and p.y < window_min.y
                    ):
                        points_list.append(Vector3(window_min.x, window_min.y, 1))
                        extra_points += 1
                    if (p.x < window_min.x and q.y > window_max.y) or (
                        q.x < window_min.x and p.y > window_max.y
                    ):
                        points_list.append(Vector3(window_min.x, window_max.y, 1))
                        extra_points += 1
                    if (p.x > window_max.x and q.y > window_max.y) or (
                        q.x > window_max.x and p.y > window_max.y
                    ):
                        points_list.append(Vector3(window_max.x, window_max.y, 1))
                        extra_points += 1
                    if (p.x > window_max.x and q.y < window_min.y) or (
                        q.x > window_max.x and p.y < window_min.y
                    ):
                        points_list.append(Vector3(window_max.x, window_min.y, 1))
                        extra_points += 1

        if extra_points == len(points_list):
            points_list = []
        print(f"OUTPUT: {points_list}")

        return points_list

class BezierClipper(Clipper):
    @classmethod
    def clip(cls, points: list[Vector3], window_max: Vector3, window_min: Vector3) -> list[Vector3]:
        returned_points = []
        for i in range(len(points) - 1):
            p1, p2 = points[i], points[i + 1]

            line = LiangBarsky.clip([p1,p2], window_max, window_min)
            if len(line):
                points.append(line[0])

        line = LiangBarsky.clip([points[-2], points[-1]], window_max, window_min)
        if len(line):
            points.append(points[1])

        return returned_points
