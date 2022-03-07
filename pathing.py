from collections import deque

class Mask:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Node:
    def __init__(self, point, parent):
        self.point = point
        self.parent = parent
def extract_path(node):
    current = node
    reverse_path = []
    while current.parent:
        reverse_path.append(current.point)
        current = current.parent
    return list(reversed(reverse_path))
def point_blocked(things, point):
    x, y = point
    for thing in things:
        if thing.x == x and thing.y == y and thing.blocks:
            return True
    return False
def _path(background, p1_node, p2, frontier, visited, seen, things = None):
    if things == None: things = []
    frontier.append(p1_node)
    while len(frontier) > 0:
        node = frontier.pop()
        free = lambda p: not point_blocked(things, p)
        adjacent = list(filter(free, background.adjacent(node.point)))
        if p2 in adjacent:
            p2_node = Node(p2, node)
            return extract_path(p2_node)
        for point in adjacent:
            if point not in visited and point not in seen:
                seen.add(point)
                frontier.appendleft(Node(point, node))
        visited.add(node.point)
    return None
def path(background, p1, p2, things = None):
    return _path(background, Node(p1, None), p2, deque(), set(), set(), things = None)

