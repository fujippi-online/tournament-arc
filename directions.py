"""
Create directions on the world map.
"""
import math
import geometry

from collections import namedtuple

Location = namedtuple("Location", ["name", "x", "y"])

# from SO
# http://stackoverflow.com/questions/28260962/calculating-angles-between-line-segments-python-with-math-atan2
def dot(vA, vB):
    return vA[0]*vB[0]+vA[1]*vB[1]
def angle_between_lines(lineA, lineB):
    # Get nicer vector form
    vA = [(lineA[0][0]-lineA[1][0]), (lineA[0][1]-lineA[1][1])]
    vB = [(lineB[0][0]-lineB[1][0]), (lineB[0][1]-lineB[1][1])]
    # Get dot prod
    dot_prod = dot(vA, vB)
    # Get magnitudes
    magA = dot(vA, vA)**0.5
    magB = dot(vB, vB)**0.5
    # Get cosine value
    cos_ = dot_prod/magA/magB
    # Get angle in radians and then convert to degrees
    angle = math.acos(dot_prod/magB/magA)
    # Basically doing angle <- angle mod 360
    ang_deg = math.degrees(angle)%360
    return ang_deg
# end from SO

def compass_direction(origin, destination):
    ox, oy = origin
    dstx, dsty = destination
    north_line = ((ox, oy),(ox, oy - 1))
    angle = angle_between_lines(north_line, (origin, destination))
    if angle < 180 and ox - dstx > 0:
        angle += 180
    print angle
    direction = "north"
    if angle > 45: direction = "east"
    if angle > 135: direction = "south"
    if angle > 225: direction = "west"
    if angle > 315: direction = "north"
    return direction

def describe_distance(p1, p2):
    distance = geometry.distance(p1, p2)
    if distance > 1000: return "a long way"
    if distance > 500: return "quite a way"
    if distance > 250: return "a little way"
    if distance > 125: return "not far"
    if distance > 60: return "a short walk"
    if distance > 30: return "a little bit"
    else: return "a few paces"

## TESTS

def test_distance_description():
    assert describe_distance((0,0), (1,1)) == "a few paces"
    assert describe_distance((0,0), (1,1000)) == "a long way"

def test_compass_directions():
    origin = (0,0)
    north = (0,-1)
    south = (0,1)
    east = (1,0)
    west = (-1, 0)
    assert compass_direction(origin, north) == "north"
    assert compass_direction(origin, south) == "south"
    assert compass_direction(origin, east) == "east"
    assert compass_direction(origin, west) == "west"

