from numpy import poly
from shape import Point, Line, Wireframe
from shape.curve import Curve2D
from vector3 import Vector3


def point_clipping(
    points: list[Point], window_max: Vector3, window_min: Vector3
) -> list[Point]:
    return [
        p
        for p in points
        if window_min.x <= p.ppc_points[0].x <= window_max.x
        and window_min.y <= p.ppc_points[0].y <= window_max.y
    ]


def liang_barsky(
    lines: list[Line], window_max: Vector3, window_min: Vector3
) -> list[Line]:
    return_lines = []
    for line in lines:
        p_a = line.ppc_points[1]
        p_b = line.ppc_points[0]

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
            continue

        pk_up = [i for i in range(len(pk)) if pk[i] > 0]
        pk_down = [i for i in range(len(pk)) if pk[i] < 0]

        c1 = max([rk[i] for i in pk_down] + [0])
        c2 = min([rk[i] for i in pk_up] + [1])

        if c1 > c2:
            continue

        x1 = p_b.x + c1 * p2
        y1 = p_b.y + c1 * p4
        x2 = p_b.x + c2 * p2
        y2 = p_b.y + c2 * p4

        line.ppc_points[0] = Vector3(x1, y1, 0)
        line.ppc_points[1] = Vector3(x2, y2, 0)

        return_lines.append(line)

    return return_lines


def __cohen_sutherland_get_rc(
    x: float, y: float, xw_min: float, xw_max: float, yw_min: float, yw_max: float
) -> int:
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


def cohen_sutherland(
    lines: list[Line], window_max: Vector3, window_min: Vector3
) -> list[Line]:
    returned_lines = []
    xw_min = window_min.x
    xw_max = window_max.x

    yw_min = window_min.y
    yw_max = window_max.y
    for line in lines:
        x1, y1 = line.ppc_points[0].x, line.ppc_points[0].y
        x2, y2 = line.ppc_points[1].x, line.ppc_points[1].y

        if x1 > x2:
            line.ppc_points[0], line.ppc_points[1] = (
                line.ppc_points[1],
                line.ppc_points[0],
            )
            x1, y1, x2, y2 = x2, y2, x1, y1

        rc1 = __cohen_sutherland_get_rc(x1, y1, xw_min, xw_max, yw_min, yw_max)
        rc2 = __cohen_sutherland_get_rc(x2, y2, xw_min, xw_max, yw_min, yw_max)

        # print(f"RC1: {bin(rc1)}, RC2: {bin(rc2)}")
        # print(f"XW_MIN: {xw_min}, X1: {x1}, X2: {x2}")

        # dentro
        if rc1 == rc2 == 0:
            returned_lines.append(line)
            continue

        # totalmente fora
        if (rc1 & rc2) != 0:
            continue

        # parcialmente dentro
        if abs(x2 - x1) < 1e-6:
            if not (xw_min <= x1 <= xw_max):
                continue

            if y1 <= y2:
                y1 = max(y1, yw_min)
                y2 = min(y2, yw_max)
            else:
                y2 = max(y2, yw_min)
                y1 = min(y1, yw_max)

            line.ppc_points[0].y = y1
            line.ppc_points[1].y = y2
            returned_lines.append(line)
            continue

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
                continue

            line.ppc_points[0].x = x1 if x_inside else xw_min
            line.ppc_points[0].y = y1 if y_inside else yw_max
        # p1 na esquerda
        elif rc1 == 0b0001:
            y1 = m * (xw_min - x1) + y1

            if not (yw_min <= y1 <= yw_max):
                continue

            line.ppc_points[0].x = xw_min
            line.ppc_points[0].y = y1
        # p1 no canto inferior esquerdo
        elif rc1 == 0b0101:
            old_y1 = y1
            y1 = m * (xw_min - x1) + y1
            x1 = x1 + 1 / m * (yw_min - old_y1)

            x_inside = xw_min <= x1 <= xw_max
            y_inside = yw_min <= y1 <= yw_max
            if not (x_inside or y_inside):
                continue

            line.ppc_points[0].x = x1 if x_inside else xw_min
            line.ppc_points[0].y = y1 if y_inside else yw_min
        # p1 no topo
        elif rc1 == 0b1000:
            x1 = x1 + 1 / m * (yw_max - y1)

            if not (xw_min <= x1 <= xw_max):
                continue

            line.ppc_points[0].x = x1
            line.ppc_points[0].y = yw_max
        # p1 no fundo
        elif rc1 == 0b0100:
            x1 = x1 + 1 / m * (yw_min - y1)

            if not (xw_min <= x1 <= xw_max):
                continue

            line.ppc_points[0].x = x1
            line.ppc_points[0].y = yw_min
        # p2 no topo
        if rc2 == 0b1000:
            x2 = x2 + 1 / m * (yw_max - y2)

            if not (xw_min <= x2 <= xw_max):
                continue

            line.ppc_points[1].x = x2
            line.ppc_points[1].y = yw_max
        # p2 no fundo
        elif rc2 == 0b0100:
            x2 = x2 + 1 / m * (yw_min - y2)

            if not (xw_min <= x2 <= xw_max):
                continue

            line.ppc_points[1].x = x2
            line.ppc_points[1].y = yw_min
        # p2 no canto superior direito
        elif rc2 == 0b1010:
            old_y2 = y2
            y2 = m * (xw_max - x2) + y2
            x2 = x2 + 1 / m * (yw_max - old_y2)
            x_inside = xw_min <= x2 <= xw_max
            y_inside = yw_min <= y2 <= yw_max
            if not (x_inside or y_inside):
                continue

            line.ppc_points[1].x = x2 if x_inside else xw_max
            line.ppc_points[1].y = y2 if y_inside else yw_max
        # p2 na direita
        elif rc2 == 0b0010:
            y2 = m * (xw_max - x2) + y2

            if not (yw_min <= y2 <= yw_max):
                continue

            line.ppc_points[1].x = xw_max
            line.ppc_points[1].y = y2
        # p2 no canto inferior esquerdo
        elif rc2 == 0b0110:
            old_y2 = y2
            y2 = m * (xw_max - x2) + y2
            x2 = x2 + 1 / m * (yw_min - old_y2)
            x_inside = xw_min <= x2 <= xw_max
            y_inside = yw_min <= y2 <= yw_max
            if not (x_inside or y_inside):
                continue

            line.ppc_points[1].x = x2 if x_inside else xw_max
            line.ppc_points[1].y = y2 if y_inside else yw_min

        # print(f"X1: {x1}, X2: {x2}, Y1: {y1}, Y2: {y2}, XW_MAX: {xw_max}")
        returned_lines.append(line)
    return returned_lines


def sutherland_hodgman(
    polygons: list[Wireframe], window_max: Vector3, window_min: Vector3
) -> list[Wireframe]:
    retuned_polygons = []

    for polygon in polygons:
        points_list = []

        for i in range(len(polygon.ppc_points)):
            p = polygon.ppc_points[i]
            q = polygon.ppc_points[(i + 1) % len(polygon.ppc_points)]
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
                intersect = liang_barsky(
                    [Line([p, q], "", "")], window_max, window_min
                )[0].ppc_points
                points_list.append(intersect[1])
            elif not p_inside and q_inside:
                print("P fora e Q dentro")
                intersect = liang_barsky(
                    [Line([p, q], "", "")], window_max, window_min
                )[0].ppc_points
                if intersect[0] == q:
                    points_list.append(intersect[1])
                else:
                    points_list.append(intersect[0])
                points_list.append(q)
            elif not p_inside and not q_inside:
                print("P e Q fora")
                intersect = liang_barsky([Line([p, q], "", "")], window_max, window_min)
                if len(intersect) > 0:
                    points_list.append(intersect[0].ppc_points[0])
                    points_list.append(intersect[0].ppc_points[1])
                else:
                    # q não foi inserido, logo não há seguimento entre q e o póximo ponto.
                    # polygon.ppc_inexistent_lines.add(
                    #     (i % len(polygon.ppc_points), (i + 1) % len(polygon.ppc_points))
                    # )
                    if (p.x < window_min.x and q.y < window_min.y) or (
                        q.x < window_min.x and p.y < window_min.y
                    ):
                        points_list.append(Vector3(window_min.x, window_min.y, 0))
                    if (p.x < window_min.x and q.y > window_max.y) or (
                        q.x < window_min.x and p.y > window_max.y
                    ):
                        points_list.append(Vector3(window_min.x, window_max.y, 0))
                    if (p.x > window_max.x and q.y > window_max.y) or (
                        q.x > window_max.x and p.y > window_max.y
                    ):
                        points_list.append(Vector3(window_max.x, window_max.y, 0))
                    if (p.x > window_max.x and q.y < window_min.y) or (
                        q.x > window_max.x and p.y < window_min.y
                    ):
                        points_list.append(Vector3(window_max.x, window_min.y, 0))

            print(f"OUTPUT: {points_list}")

        polygon.ppc_points = points_list
        retuned_polygons.append(polygon)

    return retuned_polygons


def bezier_clipping(
    curves: list[Curve2D], window_min: Vector3, window_max: Vector3
) -> list[Curve2D]:
    returned_curves = []
    for curve in curves:
        points = []
        for i in range(len(curve.ppc_points) - 1):
            p1, p2 = curve.ppc_points[i], curve.ppc_points[i + 1]

            line = liang_barsky([Line([p1, p2])], window_max, window_min)
            if len(line):
                points.append(line[0].ppc_points[0])

        line = liang_barsky([Line([points[-2], points[-1]])], window_max, window_min)
        if len(line):
            points.append(line[0].ppc_points[1])

        curve.ppc_points = points
        returned_curves.append(curve)
    return returned_curves
