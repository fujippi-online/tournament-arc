import math

def point_in_rect(rect, point):
    rx, ry, w, h = rect
    x, y = point
    if x >= rx and x <= rx+w and y >= ry and y <= ry+h:
        return True
    else:
        return False

def point_in_rects(rects, point):
    for rect in rects:
        if point_in_rect(rect, point):
            return True
    return False

def corners(rect):
    x, y, w, h = rect
    return [(x,y), (x+w, y), (x+w, y+h), (x, y+h)]

def side_middles(rect):
    """
    top, left, right, bottom
    """
    x, y, w, h = rect
    return [(x+w//2,y), (x, y+h//2), (x+w, y+h//2), (x+w//2, y+h)]

def intersects(r1, r2):
    for point in corners(r1):
        if point_in_rect(r2, point):
            return True
    for point in corners(r2):
        if point_in_rect(r1, point):
            return True
    return False

def contains(r1, r2):
    """
    Does r1 contain r2?
    """
    for point in corners(r2):
        if not point_in_rect(r1, point):
            return False
    return True

def iter_line(p1, p2):
    """
    Iterate through a line.
    """
    x1, y1 = p1
    x2, y2 = p2
    dy = abs(x2 - x1)
    dx = abs(y2 - y1)
    if x1 < x2:
        sx = 1 
    else:
        sx = -1
    if y1 < y2:
        sy = 1
    else:
        sy = -1
    err = dx - dy
    while x1 != x2 or y1 != y2:
        yield (x1, y1)
        e2 = err*2
        if e2 > -dy:
            err -= dy
            y1 += sy
        if e2 < dx:
            err += dx
            x1 += sx

def normalize(v):
    x, y = v
    length = math.sqrt(pow(x,2) + pow(y,2))
    if length == 0:
        return 0,0
    return (x/length, y/length)

def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    dx = x1 -x2
    dy = y1 -y2
    return math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))

def vec_add(u, v):
    u1, u2 = u
    v1, v2 = v
    return (u1+v1, u2+v2)

def grow(rect, amt):
    """
    grow rect by amt in all directions
    amt 1 means 2 wider and 2 higher. same centre.
    """
    x,y,w,h = rect
    shift = amt*2
    return (x-amt, y-amt, w+shift, h+shift)

def grow_x(rect, amt):
    """
    grow rect by amt in +/- x direction
    amt 1 means 2 wider and 2 higher. same centre.
    """
    x,y,w,h = rect
    shift = amt*2
    return (x-amt, y, w+shift, h)

def grow_y(rect, amt):
    """
    grow rect by amt in +/- x direction
    amt 1 means 2 wider and 2 higher. same centre.
    """
    x,y,w,h = rect
    shift = amt*2
    return (x, y-amt, w, h+shift)

def interval_closest_points(i, j):
    a, b = i
    c, d = j
    if (a <= c) and (c <= b):
        return c,c
    elif (c <= a) and (a <= d):
        return a,a
    elif (a < c) and (b <= c):
        return b,c
    elif c < a and d <= a:
        return a,d


def rect_closest_points(rect1, rect2):
    """
    plan: find closest in x, y using intervals
    """
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    cx1, cx2 = interval_closest_points((x1, x1+w1), (x2, x2+w2))
    cy1, cy2 = interval_closest_points((y1, y1+h1), (y2, y2+h2))
    return (cx1, cy1), (cx2, cy2)

def rect_distance(rect1, rect2):
    return distance(*rect_closest_points(rect1, rect2))

def closest_rect(r1, rects):
    closest = None
    dist = None
    for r2 in rects:
        d = rect_distance(r1, r2)
        if dist == None or d < dist:
            dist = d
            closest = r2
    return closest

def rect_center(rect):
    x,y,w,h = rect
    return (x+w//2, y+h//2)

def rect_centered_on(point, w, h):
    x,y = point
    rx = x - w//2
    ry = y - h//2
    return (rx, ry, w, h)

def rect_grid_translate(rect, xxx_todo_changeme):
    """
    Presuming that the rect is part of a grid of cells of the same size of
    itself that do not overlap, move it [dx, dy] in grid space.
    """
    (dx, dy) = xxx_todo_changeme
    rx, ry, w, h = rect
    return (rx+(w*dx), ry +(h*dy), w, h)

def regular_polygon(origin, radius, points, phase):
    tau = 2*math.pi
    step = tau/points
    ox, oy = origin
    sin = math.sin
    cos = math.cos
    return [(ox + radius*cos(phase + (step * n)), oy + radius*sin(phase + (step * n))) for n in range(points)]

def iter_rect(rect):
    x, y, w, h = rect
    for px in range(x, x + w):
        for py in range(y, y + h):
            yield (px, py)

def iter_circle(center, radius):
    x, y = center
    left = x - radius
    top = y - radius
    diameter = radius * 2
    for point in iter_rect((left, top, diameter, diameter)):
        if distance(point, center) < radius:
            yield point

def iter_circle_border(center, radius):
    x0, y0 = center
    f = 1 - radius
    ddf_x = 1
    ddf_y = -2 * radius
    x = 0
    y = radius
    yield x0, y0 + radius
    yield x0, y0 - radius
    yield x0 + radius, y0
    yield x0 - radius, y0
    while x < y:
        if f >= 0: 
            y -= 1
            ddf_y += 2
            f += ddf_y
        x += 1
        ddf_x += 2
        f += ddf_x    
        yield x0 + x, y0 + y
        yield x0 - x, y0 + y
        yield x0 + x, y0 - y
        yield x0 - x, y0 - y
        yield x0 + y, y0 + x
        yield x0 - y, y0 + x
        yield x0 + y, y0 - x
        yield x0 - y, y0 - x
