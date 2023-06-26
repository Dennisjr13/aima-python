def bresenham_line(x1, y1, x2, y2):
    """Bresenham's Line Algorithm
    Produces a list of tuples from start and end (x, y) points
    """
    points = []
    is_steep = abs(y2 - y1) > abs(x2 - x1)
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    is_reversed = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        is_reversed = True
    deltax = x2 - x1
    deltay = abs(y2 - y1)
    extray = int(deltax / 2)
    currenty = y2 if is_reversed else y1
    points_range = range(x2, x1 - 1, -1) if is_reversed else range(x1, x2 + 1)
    for currentx in points_range:
        point = (currenty, currentx) if is_steep else (currentx, currenty)
        points.append(point)
        extray -= deltay
        if extray < 0:
            currenty = currenty - 1 if is_reversed else currenty + 1
            extray += deltax
    return points
