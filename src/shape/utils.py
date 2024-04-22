from vector3 import Vector3

def ignore_lines_in_window_border(points: list[Vector3], transformed_points: list[Vector3], window_min: Vector3, window_max: Vector3) -> list[Vector3]:
    returned_points = []
    for i in range(len(points) - 1):
        p1_in_window_border = False
        p2_in_window_border = False
        same_border = False

        p1x, p1y = points[i].x, points[i].y
        p2x, p2y = points[i+1].x, points[i+1].y

        for limit in (window_max, window_min):
            wx, wy = limit.x, limit.y

            p1_in_window_border = (
                abs(p1x - wx) < 4 or abs(p1y - wy) < 4
            ) or p1_in_window_border

            p2_in_window_border = (
                abs(p2x - wx) < 4 or abs(p2y - wy) < 4
            ) or p2_in_window_border

            if (abs(p1x - wx) < 4 and abs(p2x - wx) < 4) or (
                abs(p1y - wy) < 4 and abs(p2y - wy) < 4
            ):
                same_border = True

        if (
            p1_in_window_border and p2_in_window_border and same_border
        ): 
            continue

        returned_points.append(transformed_points[i])
        returned_points.append(transformed_points[i+1])

    return returned_points
